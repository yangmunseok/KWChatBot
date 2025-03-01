from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.prompt_route import router as promptRoutes
from backend.routes.student_route import router as studentRoutes
from backend.routes.auth_route import router as authRoutes

app = FastAPI()
app.include_router(promptRoutes, prefix="/api/prompts")
app.include_router(studentRoutes, prefix="/api/student")
app.include_router(authRoutes, prefix="/api/auth")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
