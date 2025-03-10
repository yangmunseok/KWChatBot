import uvicorn
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run("backend.server:app", port=5000, reload=True, log_level="info")
