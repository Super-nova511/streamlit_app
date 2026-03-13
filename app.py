import streamlit as st
import random

st.set_page_config(
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

FAKE_ERRORS = [
    "openai.RateLimitError: You exceeded your current quota, please check your plan and billing details.",
    "openai.AuthenticationError: Incorrect API key provided. You can find your API key at https://platform.openai.com/account/api-keys.",
    "openai.APIConnectionError: Error communicating with OpenAI. Check your network settings, proxy configuration, SSL certificates, or firewall rules.",
    "openai.InternalServerError: The server had an error processing your request. Sorry about that! You can retry your request, or contact us through our help center.",
    "openai.RateLimitError: Rate limit reached for gpt-4o on tokens per minute (TPM). Current limit: 10,000, Used: 9,984, Requested: 512. Please retry after 3s.",
    "openai.APIStatusError: 503 Service Unavailable. The OpenAI API is temporarily overloaded. Please retry your request after a brief wait.",
]

st.title("RAG Application")
st.caption("Answers queries related to your context documents")


user_input = st.text_input("Your message", placeholder="Type something and hit Generate...")

if st.button("Generate Output"):
    if not user_input.strip():
        st.warning("Please enter a message first.")
    else:
        with st.spinner("Calling model..."):
            import time
            time.sleep(random.uniform(1.2, 2.8))
        st.error(random.choice(FAKE_ERRORS))

