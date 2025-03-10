from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import promptRoutes, authRoutes, studentRoutes
import os
from backend.utils.db_utils import db

faissStores = db["faiss_stores"]

app = FastAPI()
app.include_router(promptRoutes, prefix="/api/prompts")
app.include_router(studentRoutes, prefix="/api/student")
app.include_router(authRoutes, prefix="/api/auth")


@app.on_event("shutdown")
async def shutdown():
    print("Program shut down!", os.__file__)
    # os.remove("./chat_history")
    return


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
