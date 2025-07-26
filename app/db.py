import motor.motor_asyncio
import os
from dotenv import load_dotenv
import logging

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "parksense")

client = None
db = None

# async def connect_to_mongo():
#     global client, db
#     client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
#     db = client[MONGO_DB]

async def connect_to_mongo():
    global client, db
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
        db = client[MONGO_DB]
        # FastAPI app sends a "ping" command to MongoDB
        await db.command("ping")
        logging.info("Successfully connected to MongoDB Atlas")
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    global client
    if client:
        client.close()

def get_database():
    global db
    return db 