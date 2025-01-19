import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.server:app",port=5000, reload=True, log_level="info")