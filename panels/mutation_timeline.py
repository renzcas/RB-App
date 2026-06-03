import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_mutation_timeline(mutations):
    """
    Display a timeline of rule mutations.
    mutations = list of dicts with keys:
        Rule, OldThreshold, NewThreshold, Timestamp
    """
    if not mutations:
        st.info("No mutations yet. Defense rules are stable.")
        return

    st.subheader("🌀 Mutation Timeline")

    # Convert to DataFrame for plotting
    df = pd.DataFrame(mutations)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s")

    st.write(df)

    # Plot threshold drift over time
    fig, ax = plt.subplots()
    for rule_name in df["Rule"].unique():
        subset = df[df["Rule"] == rule_name]
        ax.plot(subset["Timestamp"], subset["NewThreshold"], marker="o", label=rule_name)

    ax.set_title("Threshold Drift Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Threshold Value")
    ax.legend()
    st.pyplot(fig)