import streamlit as st
import pandas as pd
import os
import time

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FUZZ_LOG = os.path.join(DATA_DIR, "fuzz_logs.csv")
MUTATION_LOG = os.path.join(DATA_DIR, "mutation_logs.csv")

def outcome_color(decision: str) -> str:
    """Return a color-coded emoji for decision outcomes."""
    if "Allowed" in decision:
        return "🟢 Allowed"
    elif "Blocked" in decision:
        return "🔴 Blocked"
    elif "Mutated" in decision or "Threshold" in decision:
        return "🟡 Mutated"
    else:
        return f"⚪ {decision}"

def show_animated_timeline(events, label="Battle Timeline", speed=0.5):
    st.subheader(f"⏱ {label}")
    placeholder = st.empty()
    progress = st.progress(0)

    total = len(events)
    for i, ev in enumerate(events):
        decision = ev.get("decision", "Unknown")
        colored = outcome_color(decision)
        placeholder.write(f"Step {i+1}/{total}: {colored} → {ev}")
        progress.progress((i+1)/total)
        time.sleep(speed)

def show_replay_playback():
    st.subheader("📜 Replay & 🎬 Playback Panel")

    # Speed control
    speed_option = st.radio("Playback speed", ["Slow", "Normal", "Fast"], index=1)
    speed_map = {"Slow": 1.0, "Normal": 0.5, "Fast": 0.2}
    playback_speed = speed_map[speed_option]

    # --- Fuzzing Events ---
    if os.path.isfile(FUZZ_LOG):
        fuzz_df = pd.read_csv(FUZZ_LOG)
        if "timestamp" in fuzz_df.columns:
            fuzz_df["timestamp"] = pd.to_datetime(fuzz_df["timestamp"])
            dates = fuzz_df["timestamp"].dt.date.unique()
            selected_date = st.selectbox("Select fuzzing session date", options=dates)

            filtered_fuzz = fuzz_df[fuzz_df["timestamp"].dt.date == selected_date]
            st.dataframe(filtered_fuzz)

            if not filtered_fuzz.empty:
                idx = st.slider("Step through fuzzing events", 0, len(filtered_fuzz)-1, 0)
                event = filtered_fuzz.iloc[idx].to_dict()
                st.json(event)

                if st.button("▶ Auto-play fuzzing events"):
                    show_animated_timeline(filtered_fuzz.to_dict(orient="records"),
                                           label="Fuzzing Battle",
                                           speed=playback_speed)

            cols_to_plot = [c for c in ["entropy", "length"] if c in filtered_fuzz.columns]
            if cols_to_plot:
                st.line_chart(filtered_fuzz[cols_to_plot])
        else:
            st.info("No timestamp column found in fuzz logs.")
    else:
        st.info("No fuzzing logs found yet.")

    # --- Mutations ---
    if os.path.isfile(MUTATION_LOG):
        mutation_df = pd.read_csv(MUTATION_LOG)
        if "timestamp" in mutation_df.columns:
            mutation_df["timestamp"] = pd.to_datetime(mutation_df["timestamp"])
            dates = mutation_df["timestamp"].dt.date.unique()
            selected_date = st.selectbox("Select mutation session date", options=dates)

            filtered_mutations = mutation_df[mutation_df["timestamp"].dt.date == selected_date]
            st.dataframe(filtered_mutations)

            if not filtered_mutations.empty:
                idx = st.slider("Step through mutations", 0, len(filtered_mutations)-1, 0, key="mutation_slider")
                mutation = filtered_mutations.iloc[idx].to_dict()
                st.json(mutation)

                if st.button("▶ Auto-play mutations"):
                    show_animated_timeline(filtered_mutations.to_dict(orient="records"),
                                           label="Mutation Drift",
                                           speed=playback_speed)

            cols_to_plot = [c for c in ["OldThreshold", "NewThreshold"] if c in filtered_mutations.columns]
            if cols_to_plot:
                st.line_chart(filtered_mutations[cols_to_plot])
        else:
            st.info("No timestamp column found in mutation logs.")
    else:
        st.info("No mutation logs found yet.")