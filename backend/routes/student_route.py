from fastapi import APIRouter, Depends, Response, status
import requests
from backend.rag.crawling import personalInfo
from pydantic import BaseModel
from backend.helpers.auth_helper import get_user_from_token
from backend.utils.db_utils import db
from typing import Annotated
import json
from bson import ObjectId
from dotenv import load_dotenv

router = APIRouter(tags=["student"])
students = db["students"]
users = db["users"]


class SetStudentInfoForm(BaseModel):
    id: str
    password: str


class StudentInfoForm(BaseModel):
    major_type: str
    topcit: bool


@router.post("/crawlStudentInfo")
async def setStudentInfo(
    user: Annotated[dict, Depends(get_user_from_token)],
    data: SetStudentInfoForm,
    response: Response,
):
    stu_info = personalInfo(data.id, data.password)
    if not stu_info:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error": "Crawling failed. Make sure whether you fill the right id and password."
        }
    stu_info["userid"] = ObjectId(user["_id"])
    student = await students.find_one({"userid": stu_info["userid"]})

    if student is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "No Student Found"}

    stu_info["전공 타입"] = student["전공 타입"]
    stu_info["크롤링"] = True
    student = await students.find_one_and_replace(
        {"userid": stu_info["userid"]}, replacement=stu_info, return_document=True
    )

    student["_id"] = str(student["_id"])
    student["userid"] = str(student["userid"])
    return student


@router.get("/getStudentInfo")
async def getStudentInfo(
    user: Annotated[dict, Depends(get_user_from_token)], response: Response
):
    student = await students.find_one({"userid": ObjectId(user["_id"])})

    if student is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "No Student Found"}

    student["_id"] = str(student["_id"])
    student["userid"] = str(student["userid"])
    return student


@router.post("/updateStudentInfo")
async def setStudentMajorType(
    user: Annotated[dict, Depends(get_user_from_token)],
    data: StudentInfoForm,
    response: Response,
):
    student = await students.find_one_and_update(
        {"userid": ObjectId(user["_id"])},
        {"$set": {"전공 타입": data.major_type, "topcit": data.topcit}},
        return_document=True,
    )

    if student is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "No Student Found"}

    student["_id"] = str(student["_id"])
    student["userid"] = str(student["userid"])
    return student
