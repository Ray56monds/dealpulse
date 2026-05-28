import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(page_title="DealPulse Agent Demo", page_icon="💼")

st.title("💼 DealPulse - AI Relationship Manager")
st.markdown("*Autonomous agent for financial services relationship management*")
st.markdown("**Specialized for Investment Banking, Wealth Management & Asset Management**")

# Sidebar for agent actions
st.sidebar.header("Agent Actions")

if st.sidebar.button("🎯 Get Daily Priorities"):
    st.header("Today's Priority Clients")
    st.info("Agent is analyzing client data and calculating priority scores...")
    
    # Simulate agent response
    st.success("✅ Analysis complete! Here are your top priorities:")
    
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
    st.warning("Agent detected deals requiring immediate attention:")
    
    at_risk = [
        {
            "client": "TechFlow Ventures",
            "aum": "$500M",
            "deal": "$1.2M Investment Banking",
            "issue": "Deal stalled, negative portfolio performance (-2.3%)",
            "action": "Partner escalation + performance turnaround plan"
        },
        {
            "client": "Sterling Insurance Group", 
            "aum": "$3.2B",
            "deal": "$680K Risk Management",
            "issue": "28 days no contact, needs assessment incomplete",
            "action": "Executive meeting + tailored proposal"
        }
    ]
    
    for deal in at_risk:
        with st.expander(f"🚨 {deal['client']} - {deal['aum']} AUM"):
            st.write(f"**Deal:** {deal['deal']}")
            st.write(f"**Issue:** {deal['issue']}")
            st.write(f"**Recommended Action:** {deal['action']}")
            if st.button(f"Execute Action for {deal['client']}", key=deal['client']):
                st.success(f"✅ Action executed for {deal['client']}")

if st.sidebar.button("📞 Create Follow-up"):
    st.header("Create Follow-up Task")
    
    with st.form("follow_up_form"):
        client = st.selectbox("Select Client", [
            "Meridian Capital Partners",
            "TechFlow Ventures", 
            "Global Pension Fund",
            "Apex Family Office",
            "Sterling Insurance Group"
        ])
        
        message = st.text_area("Follow-up Message", 
                              "Hi [Client], following up on our recent discussion regarding your portfolio performance and investment strategy...")
        
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        
        if st.form_submit_button("Create Task"):
            st.success(f"✅ Follow-up task created for {client}")
            st.info(f"**Message:** {message}")
            st.info(f"**Priority:** {priority}")

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
    st.metric("At-Risk Deals", "2", "+1")

# Recent activity
st.header("Recent Agent Activity")

activities = [
    {"time": "2 minutes ago", "action": "Identified critical risk: TechFlow Ventures (-2.3% performance)"},
    {"time": "15 minutes ago", "action": "Created follow-up task for Sterling Insurance Group"},
    {"time": "1 hour ago", "action": "Updated priority scores based on AUM and portfolio performance"},
    {"time": "3 hours ago", "action": "Automated renewal reminder for Apex Family Office"}
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
    
    # Simulate agent response for financial services
    if "high value" in prompt.lower() or "aum" in prompt.lower() or "billion" in prompt.lower():
        response = "I found 3 clients with AUM over $1B: Global Pension Fund ($15B), Sterling Insurance Group ($3.2B), and Apex Family Office ($800M). TechFlow Ventures needs urgent attention - negative performance affecting $1.2M deal!"
    elif "risk" in prompt.lower():
        response = "Currently tracking 2 critical at-risk deals: TechFlow Ventures ($1.2M - performance issues) and Sterling Insurance Group ($680K - 28 days no contact). Combined AUM exposure: $3.7B. Recommend immediate partner-level intervention."
    elif "performance" in prompt.lower():
        response = "Portfolio performance analysis: Global Pension Fund leading at 5.4% YTD, while TechFlow Ventures is concerning at -2.3%. Sterling Insurance and Apex Family Office showing steady 3.1% and 11.2% respectively."
    else:
        response = "I can help you with client prioritization, AUM analysis, portfolio performance tracking, and renewal management. Try asking about 'high AUM clients', 'at-risk deals', or 'portfolio performance'."
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    with st.chat_message("assistant"):
        st.write(response)