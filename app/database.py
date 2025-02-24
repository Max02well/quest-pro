import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "questpro"

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI is not set in .env file")

try:
    client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
    db = client[DB_NAME]
    job_collection = db["jobs"]
    application_collection = db["applications"]  
    # Test connection
    db.command("ping")
    print("✅ MongoDB connected successfully!")

except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    client = None
    db = None
    job_collection = None  


