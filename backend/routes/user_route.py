from fastapi import APIRouter
import requests
from backend.config.crawl import login_to_school
from pydantic import BaseModel

router = APIRouter(tags=["users"])

class Form(BaseModel):
    id: str
    password: str   

@router.post("/")
async def login(data:Form):
    return login_to_school(data.id,data.password)


