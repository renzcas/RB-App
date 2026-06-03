import streamlit as st
import pandas as pd
import os
import time

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FUZZ_LOG = os.path.join(DATA_DIR, "fuzz_logs.csv")
MUTATION_LOG = os.path.join(DATA_DIR, "mutation_logs.csv")

def outcome_color(decision: str) -> str:
    if "Allowed" in decision:
        return "🟢 Allowed"
    elif "Blocked" in decision:
        return "🔴 Blocked"
    elif "Mutated" in decision or "Threshold" in decision:
        return "🟡 Mutated"
    else:
        return f"⚪ {decision}"

def show_dual_timeline():
    st.subheader("⚔️ Dual Timeline: Red vs Blue")

    # Load fuzzing events
    fuzz_df = pd.read_csv(FUZZ_LOG) if os.path.isfile(FUZZ_LOG) else pd.DataFrame()
    mut_df = pd.read_csv(MUTATION_LOG) if os.path.isfile(MUTATION_LOG) else pd.DataFrame()

    if not fuzz_df.empty and "timestamp" in fuzz_df.columns:
        fuzz_df["timestamp"] = pd.to_datetime(fuzz_df["timestamp"])
    if not mut_df.empty and "timestamp" in mut_df.columns:
        mut_df["timestamp"] = pd.to_datetime(mut_df["timestamp"])

    # Align by timestamp
    st.markdown("### Battle Playback")
    placeholder_attack = st.empty()
    placeholder_defense = st.empty()
    progress = st.progress(0)

    # Choose playback speed
    speed_option = st.radio("Playback speed", ["Slow", "Normal", "Fast"], index=1)
    speed_map = {"Slow": 1.0, "Normal": 0.5, "Fast": 0.2}
    playback_speed = speed_map[speed_option]

    # Merge timelines (simplified by timestamp sort)
    combined = pd.concat([fuzz_df, mut_df], ignore_index=True)
    if not combined.empty and "timestamp" in combined.columns:
        combined = combined.sort_values("timestamp")

        total = len(combined)
        for i, row in enumerate(combined.to_dict(orient="records")):
            ts = row.get("timestamp")
            if "token" in row:  # fuzzing event
                decision = row.get("decision", "Unknown")
                placeholder_attack.write(f"🟥 Red Team {ts}: {row['token']} → {outcome_color(decision)}")
            elif "Rule" in row:  # mutation event
                placeholder_defense.write(f"🟦 Blue Team {ts}: Rule {row['Rule']} drifted "
                                          f"{row.get('OldThreshold')} → {row.get('NewThreshold')}")
            progress.progress((i+1)/total)
            time.sleep(playback_speed)
    else:
        st.info("No logs available yet for dual timeline playback.")