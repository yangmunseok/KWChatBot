from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .rags import load_data, text_split, indexing, get_chain
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from .config.db import connectDB
from .models.prompt_model import Prompt


app = FastAPI()

origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    global retriever, chain, database
    load_dotenv()
    vectorstore = indexing(text_split(load_data()))
    retriever = vectorstore.as_retriever(search_kwargs={'k': 5})
    chain = get_chain()
    MongoDB = await connectDB()
    database = MongoDB.Cluster0


class Query(BaseModel):
    query: str

@app.post("/api/prompts")
async def AddPrompt(data: Query):
    try:    
        global retriever, chain, database
        docs = retriever.invoke(data.query)

        response = chain.invoke({'context': docs, 'question': data.query})
        item = {"question": data.query, "answer": response}
        result = await database["prompts"].insert_one(item)
        item["_id"] = str(result.inserted_id)
        return {"success": True, "data": item}
    except openai.RateLimitError:
        return {"success": False, "message": "요청 한도가 초과되었습니다. 잠시 후 다시 시도해 주세요."}
    except Exception as e:
        return {"success": False, "message":str(e)}

@app.get("/api/prompts")
async def GetPrompt():
    try:
        global database
        items = await database["prompts"].find().to_list(1000)
        for item in items:
            item["_id"] = str(item["_id"])
        return {"success": True, "data": items}
    except Exception as e:
        return {"success": False, "message":str(e)}