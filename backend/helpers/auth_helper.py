from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import jwt
import os
from pydantic import BaseModel
from backend.utils.db_utils import db
from fastapi import Cookie, status, HTTPException
from fastapi.responses import ORJSONResponse
from typing import Annotated
import pytz
import json
from jwt.exceptions import ExpiredSignatureError

seoul_tz = pytz.timezone("Asia/Seoul")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
users = db["users"]

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


class UserForm(BaseModel):
    username: str
    password: str


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def generate_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(seoul_tz) + expires_delta
    else:
        expire = datetime.now(seoul_tz) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user_from_token(jwt_token: Annotated[str, Cookie()] = None):
    if jwt_token is None:
        raise HTTPException(
            status_code=401, detail={"error": "Unauthorized: No Token Provided"}
        )
    try:
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_data: dict = json.loads(payload.get("sub"))
        if "username" in user_data and "_id" in user_data:
            current_user = await users.find_one({"username": user_data["username"]})
            if current_user is None:
                raise HTTPException(status_code=404, detail={"error": "User not found"})
        else:
            raise HTTPException(
                status_code=401, detail={"error": "Unauthorized: Invalid Token"}
            )
        current_user["_id"] = str(current_user["_id"])
        current_user["student"] = str(current_user["student"])
        current_user.pop("password")
        return current_user
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail={"error": "Signature has expired"})


async def authenticate_user(userform: UserForm):
    current_user = await users.find_one({"username": userform.username})

    if current_user == None or not verify_password(
        userform.password, current_user["password"]
    ):
        raise HTTPException(
            status_code=400, detail={"error": "Invalid username or password"}
        )

    current_user["_id"] = str(current_user["_id"])
    current_user["student"] = str(current_user["student"])
    current_user.pop("password")
    print(current_user)
    return current_user
