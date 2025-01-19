from fastapi import APIRouter
from backend.config.db import db
from backend.config.rag import retriever, chain
from pydantic import BaseModel
import openai

router = APIRouter(tags=["prompts"])
prompts = db["prompts"]

class Query(BaseModel):
    query: str   

@router.get("/")
async def getPrompt():
    try:
        global prompts
        items = await prompts.find().to_list(1000)
        for item in items:
            item["_id"] = str(item["_id"])
        return {"success": True, "data": items}
    except Exception as e:
        return {"success": False, "message":str(e)} 

@router.post("/")
async def AddPrompt(data: Query):
    try:    
        global prompts
        docs = retriever.invoke(data.query)

        response = chain.invoke({'context': docs, 'question': data.query})
        item = {"question": data.query, "answer": response}
        result = await prompts.insert_one(item)
        item["_id"] = str(result.inserted_id)
        return {"success": True, "data": item}
    except openai.RateLimitError:
        return {"success": False, "message": "요청 한도가 초과되었습니다. 잠시 후 다시 시도해 주세요."}
    except Exception as e:
        return {"success": False, "message":str(e)}