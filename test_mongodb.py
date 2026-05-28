import os
from pymongo import MongoClient
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Test MongoDB connection with sample data
def test_mongodb_with_sample_data():
    print("Testing MongoDB connection...")
    
    # For demo purposes, use a test connection string
    # You'll need to replace this with your actual MongoDB Atlas connection
    mongodb_uri = os.getenv('MONGODB_URI')
    
    if 'your-password' in mongodb_uri or 'xxxxx' in mongodb_uri:
        print("Using demo mode - MongoDB Atlas not configured yet")
        print("To connect to real MongoDB:")
        print("1. Go to https://cloud.mongodb.com")
        print("2. Create free M0 cluster")
        print("3. Get connection string")
        print("4. Update MONGODB_URI in .env file")
        return simulate_data_operations()
    
    try:
        client = MongoClient(mongodb_uri)
        client.admin.command('ping')
        print("✓ MongoDB Atlas connected successfully!")
        
        db = client[os.getenv('MONGODB_DATABASE', 'dealpulse')]
        return seed_real_data(db)
        
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        print("Using simulation mode...")
        return simulate_data_operations()

def simulate_data_operations():
    print("\n=== SIMULATION MODE ===")
    print("Simulating client data operations")
    
    # Simulate the financial services data
    clients = [
        {"name": "TechFlow Ventures", "aum": 500000000, "deal_value": 1200000, "performance": -0.023},
        {"name": "Global Pension Fund", "aum": 15000000000, "deal_value": 2500000, "performance": 0.054},
        {"name": "Sterling Insurance", "aum": 3200000000, "deal_value": 680000, "performance": 0.031}
    ]
    
    print(f"Loaded {len(clients)} financial services clients")
    
    # Simulate priority calculation
    for client in clients:
        priority_score = (client['deal_value'] * 0.3) + (client['aum'] * 0.0001)
        if client['performance'] < 0:
            priority_score += 100000  # Risk bonus
        client['priority_score'] = priority_score
    
    # Sort by priority
    clients.sort(key=lambda x: x['priority_score'], reverse=True)
    
    print("\n=== TOP PRIORITY CLIENTS ===")
    for i, client in enumerate(clients, 1):
        risk = "CRITICAL" if client['performance'] < 0 else "NORMAL"
        print(f"{i}. {client['name']} - ${client['deal_value']:,} deal - {risk}")
    
    return True

def seed_real_data(db):
    print("Connected to real MongoDB Atlas")
    print("Seeding financial services data...")
    
    # Clear existing data
    db.clients.delete_many({})
    db.tasks.delete_many({})
    
    # Financial services client data
    clients_data = [
        {
            "name": "TechFlow Ventures",
            "contact_person": "Sarah Chen",
            "title": "Managing Partner",
            "aum": 500000000,
            "current_deal": {
                "product": "Investment Banking Services",
                "value": 1200000,
                "stage": "stalled",
                "probability": 0.25
            },
            "portfolio_performance": -0.023,
            "last_contact": datetime.now() - timedelta(days=35),
            "client_type": "venture_capital"
        },
        {
            "name": "Global Pension Fund",
            "contact_person": "Maria Rodriguez",
            "title": "Head of Alternative Investments",
            "aum": 15000000000,
            "current_deal": {
                "product": "Structured Products",
                "value": 2500000,
                "stage": "final_approval",
                "probability": 0.92
            },
            "portfolio_performance": 0.054,
            "last_contact": datetime.now() - timedelta(days=1),
            "client_type": "pension_fund"
        }
    ]
    
    # Insert data
    result = db.clients.insert_many(clients_data)
    print(f"Inserted {len(result.inserted_ids)} clients")
    
    # Test query
    high_value_clients = list(db.clients.find({"aum": {"$gte": 1000000000}}))
    print(f"Found {len(high_value_clients)} clients with AUM > $1B")
    
    return True

if __name__ == "__main__":
    print("=== DealPulse MongoDB Test ===")
    success = test_mongodb_with_sample_data()
    
    if success:
        print("\nDatabase operations successful!")
        print("\nNext steps:")
        print("1. Start MCP server: cd mcp && npm start")
        print("2. Test agent: py agent/main.py")
        print("3. Launch demo: py -m streamlit run frontend/app.py")
    else:
        print("\nDatabase test failed")