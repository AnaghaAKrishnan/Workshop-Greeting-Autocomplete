"""Streamlit UI for greeting autocomplete."""

import streamlit as st
from matcher import match_greeting

st.set_page_config(page_title="Greeting Autocomplete", page_icon="👋", layout="centered")

st.title("👋 Greeting Autocomplete")
st.write(
    "Type a greeting below and the app will suggest an appropriate response using "
    "NLP-based matching."
)

user_input = st.text_input("Enter a greeting:", placeholder="e.g. good morning, hi, how are you")

if st.button("Get Response") or user_input:
    response = match_greeting(user_input)
    if not response:
        st.info("Please enter a greeting to get a response.")
    else:
        st.success(f"**Response:** {response}")

st.markdown("---")
st.caption("Powered by scikit-learn TF-IDF cosine similarity")
