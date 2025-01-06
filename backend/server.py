from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .rags import load_data, text_split, indexing, get_chain
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

app = FastAPI()

origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

global retriever, chain

load_dotenv()
vectorstore = indexing(text_split(load_data()))
retriever = vectorstore.as_retriever(search_kwargs={'k': 5})
chain = get_chain()


class Query(BaseModel):
    query: str

@app.post("/api/prompts")
def work(data: Query):
    global retriever, chain
    docs = retriever.invoke(data.query)
    try:
        response = chain.invoke({'context': docs, 'question': data.query})
        return {"success": True, "data": response}
    except openai.RateLimitError:
        return {"success": False, "message": "요청 한도가 초과되었습니다. 잠시 후 다시 시도해 주세요."}
    except Exception as e:
        return {"success": False, "message":str(e)}
