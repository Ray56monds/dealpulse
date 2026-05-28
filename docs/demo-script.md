# DealPulse Demo Video Script (3 minutes)

## Opening (30 seconds)
**[Screen: DealPulse logo/title]**
"Hi, I'm presenting DealPulse - an autonomous AI agent that acts as a co-pilot for relationship managers in financial services."

**[Screen: Problem slide]**
"Relationship managers juggle hundreds of clients and deals. Critical opportunities slip through the cracks - not from lack of effort, but lack of intelligent prioritization."

## Architecture Overview (45 seconds)
**[Screen: Architecture diagram]**
"DealPulse uses Google Cloud Agent Builder with Gemini 3 for reasoning, connected to MongoDB via Model Context Protocol. This gives our agent real-time access to client data, deal pipelines, and interaction history."

**[Screen: MCP server code]**
"The MCP server provides four key tools: query clients, detect at-risk deals, create follow-ups, and calculate daily priorities."

## Live Demo (90 seconds)
**[Screen: Streamlit demo UI]**
"Let me show you DealPulse in action. Here's our relationship manager dashboard."

**[Click "Get Daily Priorities"]**
"The agent analyzes all client data and surfaces today's priorities. Global Manufacturing Inc is flagged as urgent - $500K deal, 45 days no contact, past close date."

**[Click "At-Risk Deals"]**
"DealPulse proactively identifies at-risk deals. It's detected two deals totaling $575K that need immediate attention."

**[Demo chat interface]**
"I can ask complex questions: 'Which clients with deals over $200K haven't been contacted in 30 days?' The agent queries MongoDB and provides actionable insights."

**[Show follow-up creation]**
"DealPulse doesn't just identify problems - it takes action. It creates follow-up tasks, drafts communications, and updates our CRM automatically."

## Multi-Step Reasoning (30 seconds)
**[Screen: Agent reasoning flow]**
"This demonstrates true agent behavior - DealPulse reasons about the data, plans multi-step actions, and executes tasks autonomously while keeping the human in control."

## Closing (15 seconds)
**[Screen: Impact metrics]**
"DealPulse transforms relationship management from reactive to proactive, helping teams protect revenue and never miss critical opportunities again."

**[Screen: GitHub/submission links]**
"Built for the Google Cloud Rapid Agent Hackathon, MongoDB track. Code available on GitHub."

---

## Demo Checklist
- [ ] MongoDB Atlas cluster running
- [ ] Sample data seeded
- [ ] MCP server started
- [ ] Streamlit UI running
- [ ] Screen recording software ready
- [ ] Audio quality tested