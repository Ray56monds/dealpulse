import streamlit as st
import sys
import os

# Add the agent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agent'))

try:
    from mongodb_agent import DealPulseAgentMongoDB
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False

st.set_page_config(page_title="DealPulse Agent Demo", page_icon="💼")

st.title("💼 DealPulse - AI Relationship Manager")
st.markdown("*Autonomous agent for financial services relationship management*")
st.markdown("**Specialized for Investment Banking, Wealth Management & Asset Management**")

# Initialize agent
if MONGODB_AVAILABLE:
    try:
        if 'agent' not in st.session_state:
            st.session_state.agent = DealPulseAgentMongoDB()
        st.success("✅ Connected to MongoDB Atlas - Live Data Active")
    except Exception as e:
        st.error(f"❌ MongoDB connection failed: {str(e)}")
        MONGODB_AVAILABLE = False

# Sidebar for agent actions
st.sidebar.header("Agent Actions")

if st.sidebar.button("🎯 Get Daily Priorities"):
    st.header("Today's Priority Clients")
    
    if MONGODB_AVAILABLE:
        with st.spinner("Agent analyzing live MongoDB data..."):
            response = st.session_state.agent.query_agent("Show me today's priority clients")
            st.text(response)
    else:
        st.info("Demo mode - MongoDB not available")
        # Fallback demo data
        priorities = [
            {"name": "TechFlow Ventures", "aum": "$500M", "deal_value": 1200000, "days_since_contact": 35, "risk": "CRITICAL", "performance": "-2.3%"},
            {"name": "Global Pension Fund", "aum": "$15B", "deal_value": 2500000, "days_since_contact": 1, "risk": "LOW", "performance": "5.4%"},
            {"name": "Sterling Insurance Group", "aum": "$3.2B", "deal_value": 680000, "days_since_contact": 28, "risk": "MEDIUM", "performance": "3.1%"}
        ]
        
        for i, client in enumerate(priorities, 1):
            col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
            with col1:
                st.write(f"**#{i}**")
            with col2:
                st.write(client["name"])
                st.caption(f"AUM: {client['aum']}")
            with col3:
                st.write(f"${client['deal_value']:,}")
            with col4:
                st.write(f"{client['performance']} YTD")
            with col5:
                color = {"CRITICAL": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}[client["risk"]]
                st.write(f"{color} {client['risk']}")

if st.sidebar.button("⚠️ At-Risk Deals"):
    st.header("At-Risk Deals Alert")
    
    if MONGODB_AVAILABLE:
        with st.spinner("Agent analyzing portfolio risks..."):
            response = st.session_state.agent.query_agent("Which deals are at risk?")
            st.text(response)
    else:
        st.warning("Agent detected deals requiring immediate attention:")
        
        at_risk = [
            {
                "client": "TechFlow Ventures",
                "aum": "$500M",
                "deal": "$1.2M Investment Banking",
                "issue": "Deal stalled, negative portfolio performance (-2.3%)",
                "action": "Partner escalation + performance turnaround plan"
            }
        ]
        
        for deal in at_risk:
            with st.expander(f"🚨 {deal['client']} - {deal['aum']} AUM"):
                st.write(f"**Deal:** {deal['deal']}")
                st.write(f"**Issue:** {deal['issue']}")
                st.write(f"**Recommended Action:** {deal['action']}")
                if st.button(f"Execute Action for {deal['client']}", key=deal['client']):
                    st.success(f"✅ Action executed for {deal['client']}")

if st.sidebar.button("📊 Portfolio Analysis"):
    st.header("Portfolio Performance Analysis")
    
    if MONGODB_AVAILABLE:
        with st.spinner("Agent analyzing portfolio performance by client type..."):
            response = st.session_state.agent.query_agent("Analyze portfolio performance by client type")
            st.text(response)
    else:
        st.info("Demo mode - showing sample analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Pension Funds", "5.4% YTD", "↗️ +1.2%")
            st.metric("Family Offices", "11.2% YTD", "↗️ +3.1%")
        with col2:
            st.metric("Insurance", "3.1% YTD", "↗️ +0.8%")
            st.metric("Venture Capital", "-2.3% YTD", "↘️ -4.1%")

# Main content area
st.header("Agent Insights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Active Deals", "5", "+1")
    
with col2:
    st.metric("Total Pipeline", "$5.83M", "+$1.2M")
    
with col3:
    st.metric("Total AUM", "$22.0B", "+$2.5B")

with col4:
    st.metric("At-Risk Deals", "1", "0")

# Recent activity
st.header("Recent Agent Activity")

activities = [
    {"time": "2 minutes ago", "action": "Identified critical risk: TechFlow Ventures (-2.3% performance)"},
    {"time": "15 minutes ago", "action": "Updated priority scores based on AUM and portfolio performance"},
    {"time": "1 hour ago", "action": "Analyzed client segmentation by type"},
    {"time": "3 hours ago", "action": "Connected to MongoDB Atlas for real-time data"}
]

for activity in activities:
    st.write(f"**{activity['time']}** - {activity['action']}")

# Chat interface
st.header("Chat with DealPulse Agent")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your DealPulse agent specialized in financial services relationship management. I can help you prioritize clients based on AUM, identify at-risk deals, analyze portfolio performance, and automate follow-ups. What would you like to know about your client relationships?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask about your clients or deals..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get agent response
    if MONGODB_AVAILABLE:
        with st.chat_message("assistant"):
            with st.spinner("Analyzing MongoDB data..."):
                response = st.session_state.agent.query_agent(prompt)
                st.text(response)
    else:
        # Simulate agent response for financial services
        if "high value" in prompt.lower() or "aum" in prompt.lower() or "billion" in prompt.lower():
            response = "I found 3 clients with AUM over $1B: Global Pension Fund ($15B), Sterling Insurance Group ($3.2B), and Apex Family Office ($800M). TechFlow Ventures needs urgent attention - negative performance affecting $1.2M deal!"
        elif "risk" in prompt.lower():
            response = "Currently tracking 1 critical at-risk deal: TechFlow Ventures ($1.2M - performance issues). AUM exposure: $500M. Recommend immediate partner-level intervention."
        elif "performance" in prompt.lower():
            response = "Portfolio performance analysis: Family Offices leading at 11.2% YTD, Pension Funds at 5.4%. TechFlow Ventures concerning at -2.3%. Sterling Insurance steady at 3.1%."
        else:
            response = "I can help you with client prioritization, AUM analysis, portfolio performance tracking, and renewal management. Try asking about 'high AUM clients', 'at-risk deals', or 'portfolio performance'."
        
        with st.chat_message("assistant"):
            st.write(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("**DealPulse** - Built for Google Cloud Rapid Agent Hackathon (MongoDB Track)")
if MONGODB_AVAILABLE:
    st.markdown("🟢 **Live MongoDB Atlas Integration Active**")
else:
    st.markdown("🟡 **Demo Mode** - Connect MongoDB for live data")