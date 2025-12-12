# app/database/mongo.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MASTER_DB = os.getenv("MASTER_DB", "master_db")

client = MongoClient(MONGO_URL)
master_db = client[MASTER_DB]


