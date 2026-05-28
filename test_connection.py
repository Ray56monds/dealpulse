import os
from dotenv import load_dotenv

load_dotenv()

def test_connection_string():
    """Quick test to validate MongoDB connection string format"""
    mongodb_uri = os.getenv('MONGODB_URI', '')
    
    print("=== MongoDB Connection Test ===")
    
    if not mongodb_uri or 'your-password' in mongodb_uri:
        print("MongoDB URI not configured")
        print("\nQuick Setup Steps:")
        print("1. Go to https://cloud.mongodb.com")
        print("2. Create free M0 cluster: 'dealpulse-cluster'")
        print("3. Create user: 'dealpulse-user' with password")
        print("4. Whitelist IP: 0.0.0.0/0 (allow all)")
        print("5. Get connection string")
        print("6. Update .env file")
        print("\nConnection string format:")
        print("mongodb+srv://dealpulse-user:PASSWORD@dealpulse-cluster.xxxxx.mongodb.net/dealpulse")
        return False
    
    # Basic validation
    if mongodb_uri.startswith('mongodb+srv://') and 'dealpulse' in mongodb_uri:
        print("Connection string format looks good")
        
        # Try actual connection
        try:
            from pymongo import MongoClient
            client = MongoClient(mongodb_uri)
            client.admin.command('ping')
            print("MongoDB connection successful!")
            
            # Test database operations
            db = client[os.getenv('MONGODB_DATABASE', 'dealpulse')]
            collections = db.list_collection_names()
            print(f"Database accessible, collections: {collections}")
            
            return True
            
        except Exception as e:
            print(f"Connection failed: {e}")
            print("Check: cluster running, IP whitelisted, credentials correct")
            return False
    else:
        print("Invalid connection string format")
        return False

if __name__ == "__main__":
    test_connection_string()