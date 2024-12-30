from fastapi import FastAPI
from .rags import load_data, text_split, indexing, get_chain
from pydantic import BaseModel
import openai

app = FastAPI()

vectorstore = indexing(text_split(load_data()))
retriever = vectorstore.as_retriever(search_kwargs={'k': 5})
chain = get_chain()

class Query(BaseModel):
    query: str

@app.get("/api")
def work(data: Query):
    docs = retriever.invoke(data.query)
    try:
        response = chain.invoke({'context': docs, 'question': data.query})
        return {"success": True, "data": response}
    except openai.RateLimitError:
        return {"success": False, "message": "요청 한도가 초과되었습니다. 잠시 후 다시 시도해 주세요."}
    except Exception as e:
        return {"success": False, "message":str(e)}

# query = '2021학년도 소프트웨어학부 신입학자가 졸업하기 위해 들어야 하는 교양 이수 체계를 알려줘줘.'