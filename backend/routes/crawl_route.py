from fastapi import APIRouter
import requests
from backend.config.crawl import personalInfo
from pydantic import BaseModel

router = APIRouter(tags=["crawl"])

class Form(BaseModel):
    id: str
    password: str   

@router.get("/userInfo")
async def getPersonalInfo(data:Form):
    personalInfo(data.id,data.password)


