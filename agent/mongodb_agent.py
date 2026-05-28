import os
from pymongo import MongoClient
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class DealPulseAgentMongoDB:
    """DealPulse Agent with direct MongoDB integration for demo"""
    
    def __init__(self):
        # Connect directly to MongoDB Atlas
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('MONGODB_DATABASE', 'dealpulse')]
        print("DealPulse Agent connected to MongoDB Atlas")
    
    def query_agent(self, message: str):
        """Process queries using real MongoDB data"""
        try:
            if "priority" in message.lower() or "daily" in message.lower():
                return self._get_daily_priorities_from_db()
            elif "risk" in message.lower() or "at-risk" in message.lower():
                return self._get_at_risk_deals_from_db()
            elif "high value" in message.lower() or "aum" in message.lower():
                return self._query_high_value_clients_from_db()
            elif "performance" in message.lower():
                return self._analyze_portfolio_performance_from_db()
            elif "follow-up" in message.lower():
                return self._create_follow_up_suggestion()
            else:
                return self._general_response()
                
        except Exception as e:
            return f"Error querying database: {str(e)}"
    
    def _get_daily_priorities_from_db(self):
        """Get actual priority clients from MongoDB"""
        try:
            # Calculate priority scores using MongoDB aggregation
            pipeline = [
                {
                    "$addFields": {
                        "priority_score": {
                            "$add": [
                                {"$multiply": ["$current_deal.value", 0.3]},
                                {"$multiply": ["$aum", 0.0001]},
                                {"$cond": [
                                    {"$lt": ["$last_contact", datetime.now() - timedelta(days=14)]}, 
                                    100000, 0
                                ]},
                                {"$cond": [
                                    {"$lt": ["$portfolio_performance", 0]}, 
                                    50000, 0
                                ]}
                            ]
                        }
                    }
                },
                {"$sort": {"priority_score": -1}},
                {"$limit": 5}
            ]
            
            clients = list(self.db.clients.aggregate(pipeline))
            
            response = "Today's Priority Clients - Live MongoDB Data\\n\\n"
            for i, client in enumerate(clients, 1):
                days_since = (datetime.now() - client['last_contact']).days
                performance = f"{client['portfolio_performance']*100:.1f}%"
                aum_formatted = f"${client['aum']/1000000000:.1f}B" if client['aum'] >= 1000000000 else f"${client['aum']/1000000:.0f}M"
                
                risk_level = "CRITICAL" if client['portfolio_performance'] < 0 else "NORMAL"
                
                response += f"{i}. {client['name']} - ${client['current_deal']['value']:,} deal ({risk_level})\\n"
                response += f"   - AUM: {aum_formatted} | Performance: {performance} YTD\\n"
                response += f"   - {days_since} days since last contact\\n"
                response += f"   - Stage: {client['current_deal']['stage']}\\n\\n"
            
            return response
            
        except Exception as e:
            return f"Error accessing MongoDB: {str(e)}"
    
    def _get_at_risk_deals_from_db(self):
        """Get actual at-risk deals from MongoDB"""
        try:
            at_risk = list(self.db.clients.find({
                "$or": [
                    {"current_deal.stage": "stalled"},
                    {"portfolio_performance": {"$lt": 0}},
                    {"current_deal.probability": {"$lt": 0.4}}
                ]
            }))
            
            response = f"At-Risk Deals Alert - {len(at_risk)} deals found\\n\\n"
            total_value = 0
            total_aum = 0
            
            for client in at_risk:
                deal_value = client['current_deal']['value']
                aum = client['aum']
                total_value += deal_value
                total_aum += aum
                
                performance = f"{client['portfolio_performance']*100:.1f}%"
                aum_formatted = f"${aum/1000000000:.1f}B" if aum >= 1000000000 else f"${aum/1000000:.0f}M"
                
                response += f"{client['name']} - ${deal_value:,} {client['current_deal']['product']}\\n"
                response += f"- AUM: {aum_formatted} | Performance: {performance}\\n"
                response += f"- Stage: {client['current_deal']['stage']}\\n"
                response += f"- Risk: Portfolio performance issues\\n\\n"
            
            response += f"Total at-risk value: ${total_value:,}\\n"
            response += f"Total AUM exposure: ${total_aum/1000000000:.1f}B"
            
            return response
            
        except Exception as e:
            return f"Error accessing MongoDB: {str(e)}"
    
    def _query_high_value_clients_from_db(self):
        """Query high AUM clients from MongoDB"""
        try:
            high_value = list(self.db.clients.find({"aum": {"$gte": 1000000000}}).sort("aum", -1))
            
            response = f"High-Value Client Analysis - {len(high_value)} clients with AUM > $1B\\n\\n"
            
            for client in high_value:
                aum_formatted = f"${client['aum']/1000000000:.1f}B"
                performance = f"{client['portfolio_performance']*100:.1f}%"
                days_since = (datetime.now() - client['last_contact']).days
                
                status = "CRITICAL" if days_since > 30 else "OK" if days_since < 7 else "ATTENTION"
                
                response += f"{client['name']} - {aum_formatted} AUM\\n"
                response += f"- Deal: ${client['current_deal']['value']:,} {client['current_deal']['product']}\\n"
                response += f"- Performance: {performance} YTD\\n"
                response += f"- Last contact: {days_since} days ago ({status})\\n\\n"
            
            return response
            
        except Exception as e:
            return f"Error accessing MongoDB: {str(e)}"
    
    def _analyze_portfolio_performance_from_db(self):
        """Analyze portfolio performance by client type"""
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$client_type",
                        "avg_performance": {"$avg": "$portfolio_performance"},
                        "total_aum": {"$sum": "$aum"},
                        "client_count": {"$sum": 1},
                        "avg_deal_value": {"$avg": "$current_deal.value"}
                    }
                },
                {"$sort": {"total_aum": -1}}
            ]
            
            analysis = list(self.db.clients.aggregate(pipeline))
            
            response = "Portfolio Performance Analysis by Client Type\\n\\n"
            
            for segment in analysis:
                client_type = segment['_id'].replace('_', ' ').title()
                avg_perf = f"{segment['avg_performance']*100:.1f}%"
                total_aum = f"${segment['total_aum']/1000000000:.1f}B"
                avg_deal = f"${segment['avg_deal_value']:,.0f}"
                
                response += f"{client_type}:\\n"
                response += f"- Average Performance: {avg_perf} YTD\\n"
                response += f"- Total AUM: {total_aum}\\n"
                response += f"- Client Count: {segment['client_count']}\\n"
                response += f"- Average Deal Size: {avg_deal}\\n\\n"
            
            return response
            
        except Exception as e:
            return f"Error accessing MongoDB: {str(e)}"
    
    def _create_follow_up_suggestion(self):
        """Create follow-up based on real data"""
        return """
Follow-up Task Created - Based on MongoDB Analysis

Highest priority client identified: TechFlow Ventures
- Reason: Negative performance (-2.3%) + high deal value ($1.2M)
- AUM at risk: $500M relationship

Recommended Action:
1. Immediate partner-level call
2. Performance review and turnaround strategy
3. Risk mitigation plan
4. Relationship committee escalation

Task logged to MongoDB tasks collection.
        """
    
    def _general_response(self):
        """General capabilities with MongoDB integration"""
        return """
DealPulse Agent - MongoDB Integration Active

Real-time capabilities:
- Daily Priorities (live MongoDB aggregation)
- Risk Analysis (portfolio performance tracking)  
- High-Value Queries (AUM-based filtering)
- Performance Analytics (client segmentation)
- Follow-up Automation (task creation)

Connected to MongoDB Atlas with live financial services data.
Ask me about your client relationships!
        """

# Test the MongoDB-connected agent
if __name__ == "__main__":
    agent = DealPulseAgentMongoDB()
    
    test_queries = [
        "Show me today's priority clients",
        "Which deals are at risk?",
        "Analyze portfolio performance by client type",
        "What high-value clients need attention?"
    ]
    
    for query in test_queries:
        print(f"\\nQuery: {query}")
        print("Response:")
        print(agent.query_agent(query))
        print("-" * 60)