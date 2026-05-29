import streamlit as st

st.title("DealPulse - Simple Test")
st.write("If you see this, Streamlit is working!")

if st.button("Test Button"):
    st.success("Button clicked successfully!")

st.write("MongoDB URI configured:", "Yes" if st.secrets.get("MONGODB_URI") else "Check .env file")