from fastapi import APIRouter, Depends
from backend.utils.db_utils import db
from backend.utils.rag import retriever, chain
from backend.rag.kw_chat_bot import (
    MdManager,
    LlmManager,
    VectorStoreManager,
    format_docs,
)
from backend.helpers.auth_helper import get_user_from_token
from pydantic import BaseModel
from bson import ObjectId
from typing import Annotated
from datetime import datetime
from zoneinfo import ZoneInfo
import openai
import json

router = APIRouter(tags=["prompts"])
prompts = db["prompts"]

vec_manager = VectorStoreManager()
llm_manager = LlmManager()
md_manager = MdManager()
kor_time_zone = ZoneInfo("Asia/Seoul")


class Query(BaseModel):
    query: str


class AddPromptForm(BaseModel):
    personal_info: dict
    question: str


@router.get("/")
async def getPrompt(user: Annotated[dict, Depends(get_user_from_token)]):
    try:
        items = await prompts.find({"userid": ObjectId(user["_id"])}).to_list(1000)
        for item in items:
            item["_id"] = str(item["_id"])
        return {"success": True, "data": items}
    except Exception as e:
        return {"success": False, "message": str(e)}


@router.post("/addPrompt")
async def AddPrompt(
    user: Annotated[dict, Depends(get_user_from_token)], data: AddPromptForm
):
    stu_info = data.personal_info
    query = data.question
    now_kst = datetime.now(kor_time_zone)
    # 카테고리 gpt ------------------------------------------------------------
    llm_manager.set_llm_type("category")
    chain = llm_manager.get_chain()
    response = chain.invoke({"question": query})
    print("gpt가 선택한 카테고리: ----------------------------------")
    print(response)
    answer = dict()
    # response = 'Graduation'

    # 해당 category vs 질문  -----------------------------------------------------------------
    match response:
        case "Graduation":
            print("졸업 카테고리----------------------------")

            grad_vecs = vec_manager.get_vectorstores(
                "Graduation"
            )  # 졸업 처음 방문할 때, 졸업 vectorstore 로드 및 학생 전공 타입 물어봄,
            # 참고: grad_vecs = [[학점], [교양], [전공], [공학]]      (현재: [[학점],[교양],[공학] )

            for idx, vecs in enumerate(grad_vecs, start=1):
                # 1. 학점
                if idx == 1:
                    retriever = vecs[0].as_retriever(
                        search_type="mmr",
                        search_kwargs={"k": 1, "lambda_mult": 0.5},  # 하나만
                    )
                    chosen_doc = retriever.invoke(
                        stu_info["입학 년도"]
                    )  # 사용자 신입학 연도 가져오기    2020
                    # chosen_doc = retriever.invoke('2025년도 신입학자')  # 2025

                    chosen_text = format_docs(chosen_doc)

                    llm_manager.set_llm_type("grad_credits_table")  # 학점 표 이해 gpt
                    chain = llm_manager.get_chain()
                    table_dict = chain.invoke(
                        {
                            "major": stu_info["학부/학과"],
                            # 'major': '공과대학 건축학과',
                            "stu_id": f"{stu_info['학번'][:4]}학번",
                            # 'stu_id': f"2025학번",
                            "credits_table": chosen_text,
                        }
                    )

                    llm_manager.set_llm_type("grad_credits")  # 학점 gpt
                    chain = llm_manager.get_chain()
                    credit_gpt_response = chain.invoke(
                        {
                            "major_type": stu_info[
                                "전공 타입"
                            ],  # stu_info 에 존재하지 않음 (klas어디에 있는지 모르겠음)
                            "major_credits": stu_info["전공 학점"],
                            "liberal_credits": stu_info["교양 학점"],
                            "extra_credits": stu_info["기타 학점"],
                            "tot_credits": stu_info["총 학점"],
                            "credits_dictionary": table_dict,
                        }
                    )

                    print(
                        "학점 gpt 답변:-------------------------------------------------------------------"
                    )
                    print(credit_gpt_response)
                    answer["credit_gpt_response"] = credit_gpt_response

                # 2. 교양 gpt
                elif idx == 2:
                    # 교양 균형 영역
                    md_manager.set_path(
                        "./backend/rag/upload/Graduation/LiberalArts/curriculum_summary.md"
                    )
                    curriculum_summary = md_manager.get_dictionary()

                    excluded_subj = {"체육실기", "음악실기", "미술실기"}
                    filtered_courses = {
                        course_name
                        for course_name, credit in stu_info["수강한 과목"]
                        if course_name == "광운인되기"
                        or (int(credit) >= 3 and course_name not in excluded_subj)
                    }

                    intersection_summary = {
                        "필수영역": (
                            "광운인되기" if "광운인되기" in filtered_courses else None
                        ),
                        **{
                            f"균형영역: {section}": list(courses & filtered_courses)
                            or None
                            for section, courses in curriculum_summary.items()
                        },
                    }

                    print("겹치는 영역: -----")
                    for key, value in intersection_summary.items():
                        print(key, value)

                    retriever = vecs[0].as_retriever(
                        search_type="mmr",
                        search_kwargs={"k": 1, "lambda_mult": 0.5},  # 하나만
                    )
                    chosen_doc = retriever.invoke(
                        stu_info["입학 년도"]
                    )  # 사용자 신입학 연도 가져오기

                    chosen_text = format_docs(chosen_doc)

                    llm_manager.set_llm_type(
                        "grad_liberalArts_table"
                    )  # 교양이수체계 표 이해 gpt-----------------------
                    chain = llm_manager.get_chain()
                    table_dict = chain.invoke({"liberalArts_table": chosen_text})

                    llm_manager.set_llm_type("grad_liberalArts")  # 교양 gpt
                    chain = llm_manager.get_chain()
                    liberalArts_gpt_response = chain.invoke(
                        {
                            "table_info": table_dict,
                            "stu_id": f"{stu_info['학번'][:4]}",
                            #'stu_id': f"2025",
                            "intersection_summary": intersection_summary,
                        }
                    )

                    print(
                        "교양 gpt 답변:-------------------------------------------------------------------"
                    )
                    print(liberalArts_gpt_response)
                    answer["liberalArts_gpt_response"] = liberalArts_gpt_response

                # 3. 전공 gpt

                # 4. 공학 인증 gpt (기초교양)
                elif idx == 3:  # idx == 4
                    if stu_info["학위 과정"] == "공학 프로그램":
                        # 1. MSI 학점 확인
                        retriever = vecs[0].as_retriever(
                            search_type="mmr",
                            search_kwargs={"k": 1, "lambda_mult": 0.5},  # 하나만
                        )
                        chosen_doc = retriever.invoke(
                            f'# {stu_info["학부/학과"]}_{stu_info["입학 년도"][:4]}'
                        )
                        chosen_text = format_docs(chosen_doc)

                        llm_manager.set_llm_type(
                            "grad_engineer_msi_table"
                        )  # 표 이해 gpt
                        chain = llm_manager.get_chain()
                        table_info = chain.invoke({"msi_table": chosen_text})

                        llm_manager.set_llm_type("grad_engineer_msi")  # 표 이해 gpt
                        chain = llm_manager.get_chain()
                        engineer_msi_response = chain.invoke(
                            {
                                "msi_info": table_info,
                                "attended_sbj": stu_info["수강한 과목"],
                            }
                        )

                        print("\n공학 msi gpt: -------------------------------")
                        print(engineer_msi_response)

                        # 2. 공학필수 과목
                        retriever = vecs[1].as_retriever(
                            search_type="mmr",
                            search_kwargs={"k": 1, "lambda_mult": 0.5},
                        )
                        chosen_doc = retriever.invoke(stu_info["입학 년도"])
                        print("chosen doc: ", chosen_doc)
                        chosen_text = format_docs(chosen_doc)

                        llm_manager.set_llm_type(
                            "grad_engineer_subj_table"
                        )  # 표 이해 gpt
                        chain = llm_manager.get_chain()
                        table_info = chain.invoke(
                            {
                                "major": stu_info["학부/학과"],
                                #'major': '공과대학 환경공학과',
                                "engineer_table": chosen_text,
                            }
                        )

                        llm_manager.set_llm_type(
                            "grad_engineer_subj"
                        )  # 공학 필수 과목 gpt
                        chain = llm_manager.get_chain()
                        engineer_subj_response = chain.invoke(
                            {
                                "attended_sbj": {
                                    course[0] for course in stu_info["수강한 과목"]
                                },
                                "required_sbj": table_info,
                            }
                        )
                        print("\n공학 필수 과목 gpt: -------------------------------")
                        print(engineer_subj_response)

                        """ 
                        words = '\n\n'.join([engineer_msi_response, engineer_subj_response])
                        llm_manager.set_llm_type('summarize')  # 요약 gpt
                        chain = llm_manager.get_chain()

                        summary = chain.invoke({
                            'words': words})
                        print("\n요약 gpt: -----------------------------------------")
                        print(summary)
                        """
                        answer["engineer_msi_response"] = engineer_msi_response
                        answer["engineer_subj_response"] = engineer_subj_response
        case "Food":
            print("음식 평가 카테고리")

        case "Course":
            print("강의 카테고리")

        case "Academic Info":
            print("정보 카테고리")

        case "None":
            print("카테고리 없음")
    return answer
