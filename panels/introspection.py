import streamlit as st

def compare_agents(agent1, agent2):
    st.subheader("Multi-Agent Introspection")
    st.write("Agent 1 Decisions:", agent1)
    st.write("Agent 2 Decisions:", agent2)