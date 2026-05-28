import os
from pymongo import MongoClient
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_DATABASE', 'dealpulse')]

# Financial Services Client Data
clients_data = [
    {
        "name": "Meridian Capital Partners",
        "contact_person": "James Morrison",
        "title": "Chief Investment Officer",
        "email": "j.morrison@meridiancap.com",
        "phone": "+1-212-555-0123",
        "aum": 2500000000,  # Assets Under Management
        "current_deal": {
            "product": "Private Wealth Management",
            "value": 850000,  # Annual fee
            "stage": "contract_review",
            "close_date": datetime.now() + timedelta(days=12),
            "probability": 0.85
        },
        "last_contact": datetime.now() - timedelta(days=2),
        "relationship_strength": "strong",
        "client_type": "institutional",
        "risk_profile": "moderate",
        "portfolio_performance": 0.087,  # 8.7% YTD return
        "renewal_date": datetime.now() + timedelta(days=180)
    },
    {
        "name": "TechFlow Ventures",
        "contact_person": "Sarah Chen",
        "title": "Managing Partner",
        "email": "s.chen@techflow.vc",
        "phone": "+1-415-555-0456",
        "aum": 500000000,
        "current_deal": {
            "product": "Investment Banking Services",
            "value": 1200000,  # Deal fee
            "stage": "stalled",
            "close_date": datetime.now() - timedelta(days=8),
            "probability": 0.25
        },
        "last_contact": datetime.now() - timedelta(days=35),
        "relationship_strength": "weak",
        "client_type": "venture_capital",
        "risk_profile": "aggressive",
        "portfolio_performance": -0.023,  # -2.3% YTD
        "renewal_date": datetime.now() + timedelta(days=45)
    },
    {
        "name": "Global Pension Fund",
        "contact_person": "Maria Rodriguez",
        "title": "Head of Alternative Investments",
        "email": "m.rodriguez@globalpension.org",
        "phone": "+1-312-555-0789",
        "aum": 15000000000,
        "current_deal": {
            "product": "Structured Products",
            "value": 2500000,
            "stage": "final_approval",
            "close_date": datetime.now() + timedelta(days=5),
            "probability": 0.92
        },
        "last_contact": datetime.now() - timedelta(days=1),
        "relationship_strength": "strong",
        "client_type": "pension_fund",
        "risk_profile": "conservative",
        "portfolio_performance": 0.054,  # 5.4% YTD
        "renewal_date": datetime.now() + timedelta(days=365)
    },
    {
        "name": "Apex Family Office",
        "contact_person": "Robert Kim",
        "title": "Family Office Director",
        "email": "r.kim@apexfamily.com",
        "phone": "+1-203-555-0321",
        "aum": 800000000,
        "current_deal": {
            "product": "Tax Optimization Strategy",
            "value": 450000,
            "stage": "proposal_review",
            "close_date": datetime.now() + timedelta(days=25),
            "probability": 0.65
        },
        "last_contact": datetime.now() - timedelta(days=18),
        "relationship_strength": "medium",
        "client_type": "family_office",
        "risk_profile": "moderate_aggressive",
        "portfolio_performance": 0.112,  # 11.2% YTD
        "renewal_date": datetime.now() + timedelta(days=120)
    },
    {
        "name": "Sterling Insurance Group",
        "contact_person": "Dr. Amanda Foster",
        "title": "Chief Financial Officer",
        "email": "a.foster@sterlinginsurance.com",
        "phone": "+1-617-555-0654",
        "aum": 3200000000,
        "current_deal": {
            "product": "Risk Management Solutions",
            "value": 680000,
            "stage": "needs_assessment",
            "close_date": datetime.now() + timedelta(days=45),
            "probability": 0.45
        },
        "last_contact": datetime.now() - timedelta(days=28),
        "relationship_strength": "medium",
        "client_type": "insurance",
        "risk_profile": "conservative",
        "portfolio_performance": 0.031,  # 3.1% YTD
        "renewal_date": datetime.now() + timedelta(days=90)
    }
]

def seed_database():
    # Clear existing data
    db.clients.delete_many({})
    db.tasks.delete_many({})
    
    # Insert clients
    db.clients.insert_many(clients_data)
    
    # Insert some sample tasks for relationship managers
    tasks_data = [
        {
            "client_id": "Meridian Capital Partners",
            "type": "contract_review",
            "message": "Follow up on wealth management contract terms - fee structure discussion",
            "priority": "high",
            "created_at": datetime.now() - timedelta(days=1),
            "completed": False,
            "deal_value": 850000
        },
        {
            "client_id": "TechFlow Ventures",
            "type": "urgent_call",
            "message": "Investment banking deal stalled - portfolio performance concerns",
            "priority": "critical",
            "created_at": datetime.now(),
            "completed": False,
            "deal_value": 1200000
        },
        {
            "client_id": "Global Pension Fund",
            "type": "final_approval",
            "message": "Structured products deal - board approval meeting scheduled",
            "priority": "high",
            "created_at": datetime.now() - timedelta(hours=6),
            "completed": False,
            "deal_value": 2500000
        },
        {
            "client_id": "Sterling Insurance Group",
            "type": "needs_assessment",
            "message": "Risk management solutions - schedule comprehensive review",
            "priority": "medium",
            "created_at": datetime.now() - timedelta(days=2),
            "completed": False,
            "deal_value": 680000
        }
    ]
    
    db.tasks.insert_many(tasks_data)
    
    print(f"Seeded {len(clients_data)} clients and {len(tasks_data)} tasks")

if __name__ == "__main__":
    seed_database()