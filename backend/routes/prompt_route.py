from fastapi import APIRouter, Response, Depends, status
from backend.utils.db_utils import db
from backend.rag.kw_chat_bot import (
    MdManager,
    LlmManager,
    VectorStoreManager,
    ConversationMemory,
    format_docs,
)
from backend.helpers.auth_helper import get_user_from_token, decode_api_key
from pydantic import BaseModel
from bson import ObjectId
from typing import Annotated
from datetime import datetime
from zoneinfo import ZoneInfo
import openai
import json
import os
import faiss
import pickle
from langchain_community.vectorstores import FAISS
import io
from bson.binary import Binary
from backend.rag.crawling import academic_info_kw

router = APIRouter(tags=["prompts"])
prompts = db["prompts"]
students = db["students"]
faissStores = db["faiss_stores"]

vec_manager = VectorStoreManager()
#llm_manager = LlmManager()
md_manager = MdManager()
kor_time_zone = ZoneInfo("Asia/Seoul")


class Query(BaseModel):
    query: str


class AddPromptForm(BaseModel):
    question: str


@router.get("/")
async def getPrompt(user: Annotated[dict, Depends(get_user_from_token)]):
    try:
        items = await prompts.find({"userid": ObjectId(user["_id"])}).to_list(100)
        for item in items:
            item["_id"] = str(item["_id"])
            item["userid"] = str(item["userid"])
        return {"success": True, "data": items}
    except Exception as e:
        return {"success": False, "message": str(e)}


async def LoadMemory(userid):
    faissStore = await faissStores.find_one({"userid": userid})
    memory = ConversationMemory()

    if faissStore is None:
        return memory

    data = bytes(faissStore["vector_store"])
    vector_store = FAISS.deserialize_from_bytes(
        data, embeddings=memory.getEmbedding(), allow_dangerous_deserialization=True
    )
    memory.setVectorStore(vector_store)
    return memory


@router.post("/addPrompt")
async def AddPrompt(
    user: Annotated[dict, Depends(get_user_from_token)],
    data: AddPromptForm,
    response: Response,
):
    stu_info = await students.find_one({"_id": ObjectId(user["student"])})

    userid = ObjectId(user["_id"])

    if stu_info is None or not stu_info["크롤링"]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "success": False,
            "error": "No Student Info Provided, Crawl Your Student Info Via User Setting.",
        }

    memory = await LoadMemory(userid)
    llm_manager = LlmManager(api_key=decode_api_key(stu_info["api_key"]))
    query = data.question
    answer = {"question": query}
    now_kst = datetime.now(kor_time_zone)
    # 카테고리 gpt ------------------------------------------------------------
    llm_manager.set_llm_type("category")
    chain = llm_manager.get_chain()
    response = chain.invoke({"question": query})
    print("gpt가 선택한 카테고리: ----------------------------------")
    print(response)
    answer["category"] = response

    prev_prompt = await prompts.find_one({"userid": userid, "category": response})
    if prev_prompt and not response == "Academic Info":
        answer["reference_data"] = prev_prompt["reference_data"]
    else:
        reference_data = None
        match response:
            case "Graduation":
                print("졸업 카테고리----------------------------")
                if not vec_manager.visited("Graduation"):
                    # 초기화
                    credit_gpt_response = str(None)
                    liberalArts_gpt_response = str(None)
                    major_gpt_response = str(None)
                    engineer_msi_response = str(None)
                    engineer_subj_response = str(None)

                    grad_vecs = vec_manager.get_vectorstores(
                        "Graduation"
                    )  # 졸업 vectorstore 로드
                    for idx, vecs in enumerate(grad_vecs, start=1):
                        # 1. 학점
                        if idx == 1:
                            retriever = vecs[0].as_retriever(
                                search_type="mmr",
                                search_kwargs={"k": 1, "lambda_mult": 0.5},
                            )
                            chosen_doc = retriever.invoke(stu_info["입학 년도"])
                            # print("chosen doc: ", chosen_doc)
                            chosen_text = format_docs(chosen_doc)
                            llm_manager.set_llm_type(
                                "grad_credits_table"
                            )  # 학점 표 이해 gpt ---------------------------------------
                            chain = llm_manager.get_chain()
                            table_dict = chain.invoke(
                                {
                                    "major": stu_info["학부/학과"],
                                    "stu_id": f"{stu_info['학번'][:4]}학번",
                                    "credits_table": chosen_text,
                                }
                            )
                            llm_manager.set_llm_type(
                                "grad_credits"
                            )  # 학점 gpt ------------------------------------------
                            chain = llm_manager.get_chain()
                            credit_gpt_response = chain.invoke(
                                {
                                    "major_type": stu_info["전공 타입"],
                                    "major_credits": stu_info["전공 학점"],
                                    "liberal_credits": stu_info["교양 학점"],
                                    "extra_credits": stu_info["기타 학점"],
                                    "tot_credits": stu_info["총 학점"],
                                    "credits_dictionary": table_dict,
                                }
                            )
                            print("1. 학점에 대한 평가-------------------------")
                            print(credit_gpt_response)
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
                                or (
                                    int(credit) >= 3
                                    and course_name not in excluded_subj
                                )
                            }
                            intersection_summary = {
                                "필수영역": (
                                    "광운인되기"
                                    if "광운인되기" in filtered_courses
                                    else None
                                ),
                                **{
                                    f"균형영역: {section}": list(
                                        courses & filtered_courses
                                    )
                                    or None
                                    for section, courses in curriculum_summary.items()
                                },
                            }
                            retriever = vecs[0].as_retriever(
                                search_type="mmr",
                                search_kwargs={"k": 1, "lambda_mult": 0.5},
                            )
                            chosen_doc = retriever.invoke(stu_info["입학 년도"])
                            chosen_text = format_docs(chosen_doc)
                            llm_manager.set_llm_type(
                                "grad_liberalArts_table"
                            )  # 교양이수체계 표 이해 gpt-----------------------
                            chain = llm_manager.get_chain()
                            table_dict = chain.invoke(
                                {"liberalArts_table": chosen_text}
                            )
                            llm_manager.set_llm_type(
                                "grad_liberalArts"
                            )  # 교양 gpt --------------------------------
                            chain = llm_manager.get_chain()
                            liberalArts_gpt_response = chain.invoke(
                                {
                                    "table_info": table_dict,
                                    "stu_id": f"{stu_info['학번'][:4]}",
                                    "intersection_summary": intersection_summary,
                                }
                            )
                            print("2. 교양에 대한 평가------------------------")
                            print(liberalArts_gpt_response)
                        # 3. 전공 gpt
                        elif idx == 3:
                            retriever = vecs[0].as_retriever(
                                search_type="mmr",
                                search_kwargs={"k": 1, "lambda_mult": 0.5},
                            )
                            chosen_doc = retriever.invoke(stu_info["학부/학과"])
                            chosen_text = format_docs(chosen_doc)
                            llm_manager.set_llm_type(
                                "grad_majors"
                            )  # 전공 gpt -----------------------------
                            chain = llm_manager.get_chain()
                            major_gpt_response = chain.invoke(
                                {
                                    "stu_major": stu_info["학부/학과"],
                                    "stu_year": stu_info["입학 년도"],
                                    "stu_sbj": {
                                        course[0] for course in stu_info["수강한 과목"]
                                    },
                                    "major_requirement": chosen_text,
                                }
                            )
                            print("3. 전공에 대한 평가 -----------------------")
                            print(major_gpt_response)
                        # 4. 공학 인증 gpt (기초교양)
                        elif idx == 4:
                            if stu_info["학위 과정"] == "공학 프로그램":
                                # 1. MSI 학점 확인
                                retriever = vecs[0].as_retriever(
                                    search_type="mmr",
                                    search_kwargs={"k": 1, "lambda_mult": 0.5},
                                )
                                chosen_doc = retriever.invoke(f'# {stu_info["학부/학과"].split()[0]}_{stu_info["입학 년도"][:4]}')
                                chosen_text = format_docs(chosen_doc)
                                llm_manager.set_llm_type(
                                    "grad_engineer_msi_table"
                                )  # 표 이해 gpt ----------------------------------
                                chain = llm_manager.get_chain()
                                table_info = chain.invoke({"msi_table": chosen_text})
                                llm_manager.set_llm_type(
                                    "grad_engineer_msi"
                                )  # msi gpt ------------------------
                                chain = llm_manager.get_chain()
                                engineer_msi_response = chain.invoke({'msi_info': table_info, 'attended_sbj': stu_info['수강한 과목']})
                                print("4. 공학인증 MSI에 대한 평가-----------------------------\n", engineer_msi_response)
                                # 2. 공학필수 과목
                                retriever = vecs[1].as_retriever(
                                    search_type="mmr",
                                    search_kwargs={"k": 1, "lambda_mult": 0.5},
                                )
                                chosen_doc = retriever.invoke(stu_info["입학 년도"])
                                chosen_text = format_docs(chosen_doc)
                                llm_manager.set_llm_type(
                                    "grad_engineer_subj_table"
                                )  # 표 이해 gpt --------------------
                                chain = llm_manager.get_chain()
                                table_info = chain.invoke(
                                    {
                                        "major": stu_info["학부/학과"],
                                        "engineer_table": chosen_text,
                                    }
                                )
                                llm_manager.set_llm_type(
                                    "grad_engineer_subj"
                                )  # 공학 필수 과목 gpt --------------------
                                chain = llm_manager.get_chain()
                                engineer_subj_response = chain.invoke(
                                    {
                                        "attended_sbj": {
                                            course[0]
                                            for course in stu_info["수강한 과목"]
                                        },
                                        "required_sbj": table_info,
                                    }
                                )
                                print("table_info: ",table_info)
                                print(
                                    "5. 공학필수과목에 대한 평가 --------------------"
                                )
                                print(engineer_subj_response)
                    grad_reference_data = "\n\n\n".join(
                        [
                            credit_gpt_response,
                            liberalArts_gpt_response,
                            major_gpt_response,
                            engineer_msi_response,
                            engineer_subj_response,
                        ]
                    )
                # 최종 참고 정보
                reference_data = [{"role": "user", "content": grad_reference_data}]
                answer["reference_data"] = reference_data
            case "Food":
                print("음식 평가 카테고리")
                md_manager.set_path("./backend/rag/upload/Food/food/kw_restaurants.md")
                content = md_manager.get_content()
                reference_data = [{"role": "user", "content": content}]
                answer["reference_data"] = reference_data
            case "Course":
                print("강의 카테고리")
                if not vec_manager.visited("Course"):  # 강의 카테고리 처음 방문시
                    course_vecs = vec_manager.get_vectorstores(
                        "Course"
                    )  # 강의평가 vectorstore 로드
                retriever = course_vecs[0][0].as_retriever(
                    search_type="mmr", search_kwargs={"k": 3, "lambda_mult": 0.5}
                )
                chosen_doc = retriever.invoke(query)
                print("chosen doc: ", chosen_doc)
                course_reference_data = format_docs(chosen_doc)
                reference_data = [{"role": "user", "content": course_reference_data}]
                answer["reference_data"] = reference_data
            case "Academic Info":
                print("공지사항 카테고리")
                notices = academic_info_kw()  # 공지사항 - 광운대 사이트 크롤링
                reference_data = [{"role": "user", "content": notices}]
                answer["reference_data"] = reference_data
            case "None":
                print("카테고리 없음")
                reference_data = [{"role": "user", "content": None}]
                answer["reference_data"] = None

    # 해당 category vs 질문  -----------------------------------------------------------------

    final_chain = llm_manager.get_chat_history_chain()
    final_response = final_chain.invoke(
        {
            "input": query,
            "reference_data": answer["reference_data"],
            "chat_history": memory.search(query),
        }
    )
    print("final response: ", final_response)
    answer["final_response"] = final_response
    memory.add_conversation(query, final_response)
    print("대화기록 중 질문과 가장 유사한 5개는?: ")
    for i in memory.search(query):
        print(i)

    faissStore = await faissStores.find_one({"userid": userid})
    vector_store = memory._vector_store.serialize_to_bytes()
    if faissStore is None:
        await faissStores.insert_one({"userid": userid, "vector_store":Binary(vector_store)})
    else:
        await faissStores.find_one_and_replace(
            {"userid": userid},
            {"userid": userid, "vector_store": Binary(vector_store)},
        )

    result = await prompts.insert_one(answer)
    result = await prompts.find_one_and_update(
        {"_id": result.inserted_id}, {"$set": {"userid": userid}}
    )

    return {
        "success": True,
        "data": {
            "question": answer["question"],
            "final_response": answer["final_response"],
        },
    }
