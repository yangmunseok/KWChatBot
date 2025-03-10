import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI")

try:
    client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client.Cluster0
except Exception as e:
    print("MongoDB 연결 실패:", e)
    os._exit(1)
