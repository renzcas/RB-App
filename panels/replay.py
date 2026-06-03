import streamlit as st
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FUZZ_LOG = os.path.join(DATA_DIR, "fuzz_logs.csv")
MUTATION_LOG = os.path.join(DATA_DIR, "mutation_logs.csv")

def show_replay_panel():
    st.subheader("📜 Replay Panel: Historical Battles")

    # --- Replay fuzzing events ---
    if os.path.isfile(FUZZ_LOG):
        st.markdown("### Past Fuzzing Events")
        fuzz_df = pd.read_csv(FUZZ_LOG)

        # Ensure timestamp is parsed
        if "timestamp" in fuzz_df.columns:
            fuzz_df["timestamp"] = pd.to_datetime(fuzz_df["timestamp"])

            # Session filter by date
            dates = fuzz_df["timestamp"].dt.date.unique()
            selected_date = st.selectbox("Select fuzzing session date", options=dates)
            filtered_fuzz = fuzz_df[fuzz_df["timestamp"].dt.date == selected_date]

            st.dataframe(filtered_fuzz)

            # Plot only if columns exist
            cols_to_plot = [c for c in ["entropy", "length"] if c in filtered_fuzz.columns]
            if cols_to_plot:
                st.line_chart(filtered_fuzz[cols_to_plot])
            else:
                st.warning("No entropy/length columns found in fuzz logs yet.")
        else:
            st.info("No timestamp column found in fuzz logs.")
    else:
        st.info("No fuzzing logs found yet.")

    # --- Replay mutations ---
    if os.path.isfile(MUTATION_LOG):
        st.markdown("### Past Rule Mutations")
        mutation_df = pd.read_csv(MUTATION_LOG)

        if "timestamp" in mutation_df.columns:
            mutation_df["timestamp"] = pd.to_datetime(mutation_df["timestamp"])

            dates = mutation_df["timestamp"].dt.date.unique()
            selected_date = st.selectbox("Select mutation session date", options=dates)

            filtered_mutations = mutation_df[mutation_df["timestamp"].dt.date == selected_date]
            st.dataframe(filtered_mutations)

            cols_to_plot = [c for c in ["OldThreshold", "NewThreshold"] if c in filtered_mutations.columns]
            if cols_to_plot:
                st.line_chart(filtered_mutations[cols_to_plot])
            else:
                st.warning("No threshold columns found in mutation logs yet.")
        else:
            st.info("No timestamp column found in mutation logs.")
    else:
        st.info("No mutation logs found yet.")