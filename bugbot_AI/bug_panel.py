#  Streamlit Gen‑AI Bug Panel for RB‑AppThis is a light, visual, non‑Pygame panel that fits into RB‑App

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def bug_embedding_agent_state(hand_x, bug_x, hand_y, bug_y):
    threat = 1.0 - min(1.0, np.hypot(hand_x - bug_x, hand_y - bug_y))
    return np.array([threat, 0.5])

def bug_embedding_action(state_vec):
    embeddings = {
        "escape_left": np.array([-1.0, 1.0]),
        "escape_right": np.array([1.0, 1.0]),
        "hide": np.array([0.0, -1.0]),
        "wait": np.array([0.1, 0.0]),
    }
    best, best_score = "wait", -999
    for act, vec in embeddings.items():
        num = np.dot(state_vec, vec)
        den = np.linalg.norm(state_vec) * np.linalg.norm(vec) + 1e-8
        score = num / den
        if score > best_score:
            best, best_score = act, score
    return best, best_score

def show_bug_panel():
    st.header("Gen-AI Bug Agent – Embedding Phase Space")

    cols = st.columns(4)
    with cols[0]:
        hand_x = st.slider("Hand X", 0.0, 1.0, 0.3)
    with cols[1]:
        hand_y = st.slider("Hand Y", 0.0, 1.0, 0.2)
    with cols[2]:
        bug_x = st.slider("Bug X", 0.0, 1.0, 0.7)
    with cols[3]:
        bug_y = st.slider("Bug Y", 0.0, 1.0, 0.8)

    state = bug_embedding_agent_state(hand_x, bug_x, hand_y, bug_y)
    action, score = bug_embedding_action(state)

    st.write(f"**State vector:** {state}")
    st.write(f"**Chosen action:** `{action}`  (similarity: {score:.3f})")

    fig, ax = plt.subplots()
    ax.set_title("Bug vs Hand in 2D Arena")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    bridge_y = 0.5
    bridge_h = 0.1
    ax.axhspan(bridge_y - bridge_h / 2, bridge_y + bridge_h / 2, color="gray", alpha=0.3, label="Bridge zone")

    ax.scatter(hand_x, hand_y, c="blue", label="Hand")
    ax.scatter(bug_x, bug_y, c="red", label="Bug")
    ax.legend()
    st.pyplot(fig)