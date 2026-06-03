import streamlit as st
import pandas as pd
import os
import time

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FUZZ_LOG = os.path.join(DATA_DIR, "fuzz_logs.csv")
MUTATION_LOG = os.path.join(DATA_DIR, "mutation_logs.csv")

def show_battle_playback():
    st.subheader("🎬 Battle Playback Mode")

    # Load fuzzing events
    if os.path.isfile(FUZZ_LOG):
        fuzz_df = pd.read_csv(FUZZ_LOG)
        fuzz_df["timestamp"] = pd.to_datetime(fuzz_df["timestamp"])

        # Slider to step through events
        st.markdown("### Fuzzing Event Playback")
        idx = st.slider("Select event index", 0, len(fuzz_df)-1, 0)
        event = fuzz_df.iloc[idx]
        st.json(event.to_dict())
    else:
        st.info("No fuzzing logs found yet.")

    # Load mutations
    if os.path.isfile(MUTATION_LOG):
        mutation_df = pd.read_csv(MUTATION_LOG)
        mutation_df["timestamp"] = pd.to_datetime(mutation_df["timestamp"])

        st.markdown("### Mutation Playback")
        idx = st.slider("Select mutation index", 0, len(mutation_df)-1, 0, key="mutation_slider")
        mutation = mutation_df.iloc[idx]
        st.json(mutation.to_dict())
    else:
        st.info("No mutation logs found yet.")

    # Optional autoplay
    if st.button("▶ Auto‑play Battle"):
        for i in range(len(fuzz_df)):
            st.write(f"Event {i}: ", fuzz_df.iloc[i].to_dict())
            time.sleep(0.5)