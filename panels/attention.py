import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def show_attention(df):
    st.subheader("Attention Tensor Overlay")
    fig, ax = plt.subplots()
    sns.heatmap(df[["length", "status"]].corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)