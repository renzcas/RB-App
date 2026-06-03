import streamlit as st
from red_team import fuzzing
from blue_team import anomaly, defense_rules
from panels import attention, drift, introspection, mutation_timeline, replay_playback, dual_timeline
from data import logger

st.set_page_config(page_title="Red/Blue Hacking Cockpit", layout="wide")
st.title("🧠 Red/Blue Hacking Cockpit")

# Tabs for cockpit sections
tab1, tab2, tab3 = st.tabs(["Red Team", "Blue Team", "Panels"])

# --- Red Team ---
with tab1:
    st.header("Red Team: Offensive Modules")
    token = fuzzing.fuzz_tokens()
    result = fuzzing.send_request(token)
    st.write("Single Fuzzing Result:", result)

    st.subheader("Batch Fuzzing")
    logs = [fuzzing.send_request(fuzzing.fuzz_tokens()) for _ in range(5)]
    st.write(logs)

# --- Blue Team ---
with tab2:
    st.header("Blue Team: Defensive Modules")
    logs = [fuzzing.send_request(fuzzing.fuzz_tokens()) for _ in range(10)]
    st.write("Incoming Events:", logs)

    st.subheader("Defense Decisions")
    for event in logs:
        decisions = defense_rules.apply_rules(event)
        st.write(event, "→", decisions)
        # Log each fuzzing event
        logger.log_fuzz_event(event)

    st.subheader("Anomaly Detection")
    df = anomaly.detect_anomalies(logs)
    st.write(df)

    st.subheader("Rule Mutations")
    mutations = defense_rules.evolve_rules()
    st.write(mutations)
    for m in mutations:
        logger.log_mutation(m)

# --- Panels ---
with tab3:
    st.header("Cockpit Panels")

    st.subheader("Attention Overlay")
    attention.show_attention(df)

    st.subheader("Drift Tracker")
    drift.show_drift([{"rule": "entropy>4", "mutation": "lowered to 3.5"}])

    st.subheader("Multi-Agent Introspection")
    introspection.compare_agents(["Allowed", "Blocked"], ["Suspicious", "Allowed"])

    st.subheader("Mutation Timeline")
    mutation_timeline.show_mutation_timeline(mutations)

    st.subheader("Replay & Playback")
    replay_playback.show_replay_playback()

    st.subheader("Dual Timeline: Red vs Blue")
    dual_timeline.show_dual_timeline()                                           speed=playback_speed)