import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv('MONGODB_URI').replace('&tls=true&tlsAllowInvalidCertificates=true', '')

print("Testing MongoDB with explicit CA certificate...")
print(f"CA Bundle: {certifi.where()}")

try:
    client = MongoClient(uri, tlsCAFile=certifi.where())
    client.admin.command('ping')
    print("SUCCESS! MongoDB connected with new password!")
    
    db = client['dealpulse']
    collections = db.list_collection_names()
    print(f"Collections: {collections}")
    
    count = db.clients.count_documents({})
    print(f"Clients in database: {count}")
    
except Exception as e:
    print(f"Failed: {e}")