# DealPulse

> AI-powered relationship manager co-pilot that prioritizes clients, surfaces at-risk deals, and automates follow-ups — powered by Gemini and MongoDB.

## 🎯 Problem

Relationship managers in financial services juggle hundreds of client relationships, deal pipelines, and follow-up tasks. Critical deals slip through the cracks, clients go cold, and revenue is lost — not from lack of effort, but from lack of intelligent prioritization.

## 💡 Solution

DealPulse is an **autonomous agent** that acts as a co-pilot for relationship managers. It doesn't just answer questions — it **reasons, plans, and executes multi-step tasks**:

1. **Prioritizes daily outreach** — scores clients by deal value, recency of contact, and risk signals
2. **Surfaces at-risk deals** — identifies stalled pipelines, upcoming renewals, clients going cold
3. **Automates follow-ups** — drafts communications, creates tasks, logs interactions
4. **Answers complex queries** — "Which clients with deals over $100K haven't been contacted in 30 days?"

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│           Google Cloud Agent Builder            │
│         (Orchestration + Gemini 3)              │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌───────────┐    ┌──────────────────────────┐  │
│  │  Gemini   │───▶│   Agent Tools (MCP)      │  │
│  │  Reasoning│    │                          │  │
│  └───────────┘    │  • query_clients         │  │
│                   │  • get_at_risk_deals      │  │
│                   │  • create_follow_up       │  │
│                   │  • log_interaction        │  │
│                   │  • get_daily_priorities   │  │
│                   └──────────┬───────────────┘  │
│                              │                  │
└──────────────────────────────┼──────────────────┘
                               │ MCP Protocol
                               ▼
                 ┌─────────────────────────┐
                 │   MongoDB MCP Server    │
                 │                         │
                 │  Collections:           │
                 │  • clients              │
                 │  • deals                │
                 │  • interactions         │
                 │  • tasks                │
                 └─────────────────────────┘
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Brain | Gemini 3 (Google Cloud) |
| Orchestration | Google Cloud Agent Builder |
| Data Layer | MongoDB Atlas (via MCP) |
| MCP Server | MongoDB MCP Server |
| Frontend | Streamlit (demo UI) |
| Language | Python 3.11+ |

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Google Cloud account with Agent Builder enabled
- MongoDB Atlas cluster
- Node.js 18+ (for MongoDB MCP server)

### Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/dealpulse.git
cd dealpulse

# Install Python dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your credentials

# Seed MongoDB with sample data
python seed/seed_data.py

# Start the MongoDB MCP server
cd mcp && npm install && npm start

# Run the agent
python agent/main.py

# (Optional) Launch demo UI
streamlit run frontend/app.py
```

### Environment Variables

```
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
MONGODB_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/dealpulse
MONGODB_DATABASE=dealpulse
```

## 📂 Project Structure

```
dealpulse/
├── agent/          # Agent definition, tools, and orchestration
├── mcp/            # MongoDB MCP server configuration
├── seed/           # Sample data for demo
├── frontend/       # Streamlit demo UI
├── docs/           # Architecture diagrams
├── LICENSE         # MIT License
└── README.md
```

## 🎬 Demo

[Watch the 3-minute demo video →](https://youtu.be/placeholder)

## 🏆 Hackathon

**Google Cloud Rapid Agent Hackathon**
- **Track:** MongoDB
- **Domain:** Financial Services — Relationship Manager Co-pilot

## License

MIT — see [LICENSE](./LICENSE)
