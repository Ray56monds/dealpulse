import os
# from google.cloud import aiplatform  # Comment out for demo
# from google.oauth2 import service_account  # Comment out for demo
import json

class DealPulseAgent:
    def __init__(self):
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        self.location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
        
        # Initialize AI Platform client (commented for demo)
        # aiplatform.init(
        #     project=self.project_id,
        #     location=self.location
        # )
        print("DealPulse Agent initialized in demo mode")
    
    def query_agent(self, message: str, session_id: str = "default"):
        """Send query to DealPulse agent and get response"""
        try:
            # This would connect to your Agent Builder endpoint
            # For now, we'll simulate the agent logic
            
            if "priority" in message.lower() or "daily" in message.lower():
                return self._get_daily_priorities()
            elif "risk" in message.lower() or "at-risk" in message.lower():
                return self._get_at_risk_deals()
            elif "high value" in message.lower() or "$" in message:
                return self._query_high_value_clients(message)
            elif "follow-up" in message.lower() or "create task" in message.lower():
                return self._create_follow_up_suggestion(message)
            else:
                return self._general_response()
                
        except Exception as e:
            return f"Error querying agent: {str(e)}"
    
    def _get_daily_priorities(self):
        """Simulate agent getting daily priorities for financial services"""
        return """
Today's Priority Clients - Financial Services

Based on AUM, deal value, contact recency, and portfolio performance:

1. TechFlow Ventures - $1.2M Investment Banking Deal (CRITICAL)
   - AUM: $500M | Performance: -2.3% YTD
   - 35 days since last contact
   - Deal stalled, past close date
   - Action: Urgent partner call + performance review

2. Global Pension Fund - $2.5M Structured Products (HIGH)
   - AUM: $15B | Performance: 5.4% YTD
   - Final approval stage
   - Action: Board presentation prep

3. Sterling Insurance Group - $680K Risk Management (MEDIUM)
   - AUM: $3.2B | Performance: 3.1% YTD
   - 28 days since contact, needs assessment stage
   - Action: Schedule comprehensive review
        """
    
    def _get_at_risk_deals(self):
        """Simulate agent identifying at-risk deals in financial services"""
        return """
At-Risk Deals Alert - Financial Services

I've identified 3 deals requiring immediate attention:

TechFlow Ventures - $1.2M Investment Banking
- Issue: Deal stalled, negative portfolio performance (-2.3%)
- Risk Level: CRITICAL
- AUM Impact: $500M client relationship at risk
- Recommended Action: Partner escalation + performance turnaround plan

Sterling Insurance Group - $680K Risk Management  
- Issue: 28 days no contact, needs assessment incomplete
- Risk Level: MEDIUM
- AUM: $3.2B relationship
- Recommended Action: Executive meeting + tailored proposal

Apex Family Office - $450K Tax Optimization
- Issue: 18 days no contact, proposal under review
- Risk Level: MEDIUM
- AUM: $800M family office
- Recommended Action: Follow-up call + additional analysis

Total at-risk value: $2.33M | Total AUM exposure: $4.5B
        """
    
    def _query_high_value_clients(self, message):
        """Handle high-value client queries for financial services"""
        return """
High-Value Client Analysis - Financial Services

Clients with AUM over $1B or deals over $500K:

1. Global Pension Fund - $15B AUM, $2.5M deal
   - Last contact: 1 day ago (OK)
   - Performance: 5.4% YTD
   - Status: Final approval stage - ON TRACK

2. Sterling Insurance Group - $3.2B AUM, $680K deal
   - Last contact: 28 days ago (WARNING)
   - Performance: 3.1% YTD
   - Status: NEEDS ATTENTION

3. TechFlow Ventures - $500M AUM, $1.2M deal
   - Last contact: 35 days ago (CRITICAL)
   - Performance: -2.3% YTD
   - Status: CRITICAL - Deal stalled

Action Required: Prioritize TechFlow Ventures - performance issues affecting $1.2M deal.
        """
    
    def _create_follow_up_suggestion(self, message):
        """Suggest follow-up actions for financial services"""
        return """
Follow-up Task Created - Financial Services

I've analyzed the client situation and recommend:

Client: TechFlow Ventures (Managing Partner: Sarah Chen)
Priority: CRITICAL
Deal Value: $1.2M Investment Banking Services
AUM at Risk: $500M

Message Template:
"Hi Sarah, I wanted to personally follow up on our investment banking engagement. I understand market conditions have been challenging, and I see your portfolio performance has been impacted. I'd like to schedule a call with our senior team to discuss how we can adjust our strategy to better support TechFlow's current objectives and help turn around performance. Are you available for a strategic review this week?"

Next Steps:
1. Partner-level call within 24 hours
2. Prepare performance analysis and turnaround recommendations
3. Schedule in-person strategic review meeting
4. Escalate to relationship committee

Task added to CRM with CRITICAL priority flag.
        """
    
    def _general_response(self):
        """General agent capabilities for financial services"""
        return """
DealPulse Agent Ready - Financial Services

I can help you with:

Daily Priorities - "Show me today's priority clients"
Risk Analysis - "Which deals are at risk?"
High-Value Queries - "Clients with AUM over $1B"
Portfolio Analysis - "Analyze portfolio performance by client type"
Follow-ups - "Create follow-up for [client]"
Renewal Management - "Clients with renewals in next 90 days"
Performance Tracking - "Clients with negative performance"

Specialized for relationship managers in:
- Investment Banking - Wealth Management - Asset Management
- Family Offices - Pension Funds - Insurance

What would you like to know about your client relationships?
        """

# Example usage
if __name__ == "__main__":
    agent = DealPulseAgent()
    
    # Test queries for financial services
    test_queries = [
        "Show me today's priority clients",
        "Which deals are at risk?", 
        "What clients with AUM over $1B haven't been contacted recently?",
        "Create a follow-up task for TechFlow Ventures",
        "Analyze portfolio performance by client type",
        "Which clients have renewals coming up in the next 90 days?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("Response:")
        print(agent.query_agent(query))
        print("-" * 50)