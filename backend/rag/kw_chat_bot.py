from dotenv import load_dotenv
import os
import bs4  # 웹페이지 파싱
from langchain import hub  # 텍스트 분할, 문서 로딩, 벡터 저장, 출력 파싱
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # OpenAI의 챗봇과 임베딩
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain.prompts import ChatPromptTemplate
import backend.rag.crawling
from langchain_teddynote import logging
import ast

"""
1번 행 찾기를 내가 하자.
"""


def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


def get_personal_info(stu_id, stu_pw):
    stu_info_dict = crawling.personalInfo(stu_id, stu_pw)
    return stu_info_dict


class VectorStoreManager:
    def __init__(self):
        self._vectorstores = {
            "Graduation": [],
            "Course": [],
            "Food": [],
            "Academic Info": [],
        }
        self._embeddings_model = HuggingFaceEmbeddings(  # 768 차원
            model_name="jhgan/ko-sroberta-nli",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    def get_vectorstores(self, category):
        if not self._vectorstores[category]:
            print(f"{category} Vectorstore 로드중")
            try:
                category_path = os.path.join("./backend/rag/db", category)
                for topic_folder in os.listdir(category_path):
                    topic_folder_path = os.path.join(category_path, topic_folder)
                    topic_vectorstore = []

                    for detail_folder in os.listdir(topic_folder_path):
                        detail_folder_path = os.path.join(
                            topic_folder_path, detail_folder
                        )

                        vectorstore = FAISS.load_local(
                            detail_folder_path,
                            self._embeddings_model,
                            distance_strategy=DistanceStrategy.COSINE,
                            allow_dangerous_deserialization=True,
                        )
                        topic_vectorstore.append(vectorstore)

                    self._vectorstores[category].append(topic_vectorstore)

                print(f"{category} 모든 Vectorstore 로드 완료")

            except Exception as e:
                print(f"{category} Vectorstore 로드 실패: {e}")
        else:
            print(f"{category} Vectorstore 이미 로드됨.")

        return self._vectorstores[category]


class LlmManager:
    def __init__(self):
        self._llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self._llm_type = None
        self._template = None

    def set_llm_type(self, llm_type):
        self._llm_type = llm_type

    def get_template(self):
        if self._llm_type == "category":
            self._template = """
                Select the category that best matches the question below. 
                The categories are: "Graduation", "Food", "Course", "Academic Info", and "None".

                1. Graduation: Questions related to requirements or conditions needed for graduation.
                2. Food: Questions related to food, such as recommendations or information.
                3. Course: Questions about course evaluations or recommendations.
                4. Academic Info: Questions about school announcements or academic-related information.
                5. None: If the question does not fit any of the above categories.

                Question: {question}
                Category Name:
                """

        elif self._llm_type == "grad_credits_table":
            self._template = """
            당신은 표에 대한 정보를 dictionary 형태로 변환하는 전문 에이전트입니다.
            학생의 개인 정보와 학점 졸업 요건 표가 주어지면, 학생에게 해당하는 행을 정확히 추출하여 딕셔너리로 반환하세요.

            ### 학생 개인 정보:
            - **전공**: {major}
            - **학번**: {stu_id}

            ### 학점 졸업 요건 표:
            {credits_table}

            ___
            ### 해당 행(row) 찾기
            - `credits_table`에서 '단과대' 열들을 확인하여 **학생의 전공 '{major}'과 일치하는 행(row)**을 찾습니다.  
            - 특정 학번에 대한 기준이 존재하는 경우, 학생의 학번에 맞는 행을 선택합니다.  
                - **학생의 학번 '{stu_id}'이 정확히 "2020학번"이면, "2020학번" 행을 선택합니다.**  
                - **학생의 학번 '{stu_id}'이 "2021학번" 이상(2021, 2022, 2023)이면, "2021학번~" 행을 선택합니다.** 
            - 적절한 행을 찾았다면, 모든 열의 이름을 key로, 해당 행의 값을 value로 매핑하세요.
            
            ### 출력
            - 열의 이름을 최대한 자세하게 반드시 하위 항목이 명시되도록 작성해주세요.
            - 추출한 딕셔너리만 출력하세요.
            - 추출을 잘할시 팁 $100 와 당근 500개를 드리겠습니다.
            """
        elif self._llm_type == "grad_credits":
            self._template = """
            당신은 학생의 **학점 정보**가 졸업 요건을 충족하는지 판단하는 에이전트입니다.
            학생의 학점 정보와 졸업 요건이 담긴 딕셔너리가 주어지며, 이를 비교하여 졸업 가능 여부를 검토해야 합니다.

            ### 학생 정보:
            - **전공 유형**: {major_type} (ex: 단일 전공, 심화 전공, 복수 전공, 연계 전공 등)
            - **전공 취득 학점**: {major_credits}
            - **교양 취득 학점**: {liberal_credits}
            - **총 취득 학점**: {tot_credits}

            ### 졸업 요건 딕셔너리:
            {credits_dictionary}

            ___
            ### 학생의 정보와 dictionary를 비교
            - **총 학점:** 학생의 총 취득 학점 vs dictionary의 졸업이수학점  
            - **교양 학점:** 학생의 취득 교양 학점 vs dictionary의 교양 관련 학점 합 
            - **전공 학점:** 학생의 취득 전공 학점 vs dictionary의 학생 전공 유형에 해당하는 학점  
                _(참고: **학생 전공이 복수 전공일 경우, dictionary의 학생 전공 유형에 해당하는 학점은 복수전공 학점과 부전공 학점의 합입니다.**)_

            """

        elif self._llm_type == "grad_liberalArts_table":
            self._template = """
            당신은 표에 대한 정보를 dictionary 형태로 변환하는 전문 에이전트입니다.
            교양 이수 체계 표가 주어지면, 해당하는 행을 정확히 추출하여 딕셔너리로 반환하세요.

            ### 교양 이수 체계 표:
            {liberalArts_table}

            ___
            ### 교양 조건 딕셔너리 구성 지침
            -   **key: '필수교양'** 
                **value:** '필수교양'행에 기재된 조건을 요약합니다. _(참고: 학점에 대한 정보는 제외)_
            -   **key: '균형교양'**  
                **value:** '균형교양' 행의 마지막 열에 해당하는 조건을 요약합니다. _(참고: 학점 관련 정보는 제외)_
    
            ### 출력 요건
            - 추출한 딕셔너리만 출력하세요.
            - 추출을 잘할시 팁 $100 와 당근 500개를 드리겠습니다.
            """
        elif self._llm_type == "grad_liberalArts":
            self._template = """
            당신은 학생의 수강 정보가 교양 졸업 요건(필수교양과 균형교양)을 충족하는지 평가하는 에이전트입니다.
            아래 제공된 **학생 정보**와 **교양 이수 체계 딕셔너리**를 참고하여, 학생이 교양 졸업 요건을 만족하는지 판단하세요.
            
            ### [입력 데이터]
            
            **학생 정보**
            - **학번**: {stu_id}
            - **수강 정보**: {intersection_summary}
            
            **교양 이수 체계 딕셔너리**
            {table_info}
            
            ___
            ### [평가 항목]
            1. **필수교양 평가**
            - 딕셔너리의 '필수교양' 항목과 수강 정보의 '필수교양'을 비교합니다.
            - 해당 영역의 요건이 충족되었는지 여부를 출력하세요.
            
            2. **균형교양 평가**
            - 딕셔너리에서 제시된 '균형교양' 항목들을 출력합니다.
            - **특별 조건**: 학번{stu_id}이 2024, 2025가 아닐 경우, 수강 정보의 '균형영역: 수리와자연'은 평가 대상에서 제외합니다.
            - 각 균형교양 영역에 대해, 수강 정보에서 과목 이수 여부를 확인하고 이수한 과목의 수를 집계합니다.
            - 총 포함된 균형교양 영역의 수와 이수한 과목의 총 개수를 출력하세요.
       
            3. **최종 결론**  
            - 위의 평가 결과를 종합하여, 학생이 전체 교양 졸업 요건(필수교양 및 균형교양)을 충족하는지 최종 결론을 내려주세요.
            """
        return self._template

    def get_chain(self):
        template = self.get_template()
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self._llm | StrOutputParser()
        return chain


class MdManager:
    def __init__(self):
        self._file_path = None

    def set_path(self, file_path):
        self._file_path = file_path

    def get_dictionary(self):
        with open(self._file_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()
            result = dict()
            for line in markdown_content.splitlines():
                if line.startswith("#"):
                    current_section = line.lstrip("#").strip()  # '#' 제거 후 제목 추출
                    result[current_section] = None
                else:
                    result[current_section] = ast.literal_eval(line)
        return result
