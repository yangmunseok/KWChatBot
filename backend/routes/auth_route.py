from fastapi import APIRouter, Response, Cookie, status, Depends
from backend.utils.db_utils import db
from passlib.context import CryptContext
from backend.helpers.auth_helper import get_password_hash, verify_password
import re
from pydantic import BaseModel
from typing import Annotated
from backend.helpers.auth_helper import (
    generate_token,
    get_user_from_token,
    authenticate_user,
)
from datetime import timedelta
import json

router = APIRouter(tags=["auth"])
users = db["users"]
students = db["students"]

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class SignUpForm(BaseModel):
    username: str
    password: str
    email: str


class LoginForm(BaseModel):
    username: str
    password: str


@router.post("/signup", status_code=201)
async def signup(userform: SignUpForm, response: Response):
    emailRegex = "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if re.match(emailRegex, userform.email) == None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Invalid email format"}

    existingUser = await users.find_one({"username": userform.username})

    if existingUser != None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "username is already taken"}

    existingEmail = await users.find_one({"email": userform.email})

    if existingEmail != None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "email is already taken"}

    if len(userform.password) < 6:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "password must be at least 6 characters long"}

    hashed_password = get_password_hash(userform.password)

    new_user = {
        "password": hashed_password,
        "username": userform.username,
        "email": userform.email,
        "student": None,
    }
    user = await users.insert_one(new_user)
    new_user["_id"] = user.inserted_id

    student = await students.insert_one(
        {
            "학부/학과": None,
            "입학 년도": None,
            "학번": None,
            "이름": None,
            "학적상황": None,
            "학위 과정": None,
            "전공 학점": None,
            "교양 학점": None,
            "기타 학점": None,
            "총 학점": None,
            "수강한 과목": None,
            "전공 타입": None,
            "크롤링": False,
            "userid": user.inserted_id,
            "topcit": False,
            "api_key": None,
        }
    )
    user = await users.find_one_and_update(
        {"_id": new_user["_id"]}, {"$set": {"student": student.inserted_id}}
    )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = generate_token(
        {
            "sub": json.dumps(
                {"username": new_user["username"], "_id": str(new_user["_id"])}
            )
        },
        expires_delta=access_token_expires,
    )
    response.set_cookie(
        key="jwt_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=3600,
    )

    new_user["_id"] = str(new_user["_id"])
    new_user["student"] = str(student.inserted_id)
    new_user.pop("password")
    print("new user:", new_user)

    return new_user


@router.post("/login", status_code=201)
def login(user: Annotated[dict, Depends(authenticate_user)], response: Response):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = generate_token(
        {"sub": json.dumps({"username": user["username"], "_id": user["_id"]})},
        expires_delta=access_token_expires,
    )
    response.set_cookie(
        key="jwt_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=3600,
    )

    return user


@router.get("/getme")
async def getMe(user: Annotated[dict, Depends(get_user_from_token)]):
    return user


@router.post("/logout", status_code=200)
async def logout(response: Response):
    response.delete_cookie("jwt_token")
    return
