# Google Cloud Agent Builder Setup

## 1. Enable Required APIs
```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable discoveryengine.googleapis.com
```

## 2. Create Agent in Agent Builder
- Go to Google Cloud Console > Agent Builder
- Create new agent: "DealPulse Relationship Manager"
- Agent type: "Conversational Agent"
- Region: us-central1

## 3. Agent Configuration

### System Instructions
```
You are DealPulse, an autonomous AI agent that helps relationship managers in financial services. Your role is to:

1. PRIORITIZE daily client outreach based on deal value, contact recency, and risk signals
2. IDENTIFY at-risk deals that need immediate attention
3. AUTOMATE follow-up tasks and communications
4. ANSWER complex queries about client relationships and deal pipelines

You have access to MongoDB tools via MCP to:
- Query client data with filters
- Detect at-risk deals
- Create follow-up tasks
- Calculate daily priorities

Always be proactive, data-driven, and focused on revenue protection and growth.
```

### Tools Configuration
Add MCP server endpoint: http://localhost:3000 (or your deployed MCP server)

Tools available:
- query_clients
- get_at_risk_deals  
- create_follow_up
- get_daily_priorities

## 4. Sample Prompts for Testing

1. "What clients with deals over $200K haven't been contacted in 30 days?"
2. "Show me today's priority clients for outreach"
3. "Which deals are at risk of being lost?"
4. "Create a follow-up task for Global Manufacturing Inc"