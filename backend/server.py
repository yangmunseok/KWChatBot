from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.prompt_route import router as promptRoutes
from backend.routes.user_route import router as userRoutes

app = FastAPI()
app.include_router(promptRoutes,prefix="/api/prompts")
app.include_router(userRoutes,prefix="/api/users")

origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

