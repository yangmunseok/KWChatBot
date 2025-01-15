import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def connectDB():
    try:
        MongoDB = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Get server status of admin database
        server_status = await MongoDB.admin.command("serverStatus")
        print("MongoDB connected: {}".format(server_status["host"]))

        # List databases
        databases = await MongoDB.list_database_names()
        print("Databases: {}".format(databases))

        return MongoDB
    except Exception as e:
        print("MongoDB 연결 실패:", e)
        os._exit(1)

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")