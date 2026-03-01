import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(page_title="AI Quote Generator", page_icon="✨")

st.title("✨ AI Quote Generator")
st.caption("Powered by google/gemma-3-27b-it via OpenRouter")

category = st.selectbox(
    "Choose a vibe",
    ["Motivation", "Discipline", "Coding", "Success", "Gym", "Life"]
)

def generate_quote(category):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "Streamlit Quote App"
    }

    prompt = f"""
    Generate ONE short, original, powerful {category.lower()} quote.
    No explanation.
    No quotation marks.
    Only the quote.
    """

    payload = {
        "model": "google/gemma-3-27b-it:free",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9,
        "max_tokens": 60
    }

    response = requests.post(url, headers=headers, json=payload)

    # Proper error inspection
    if response.status_code != 200:
        return f"API Error {response.status_code}: {response.text}"

    data = response.json()

    if "choices" not in data:
        return f"Unexpected response format: {data}"

    return data["choices"][0]["message"]["content"].strip()


if st.button("🎲 Generate Quote"):
    if not API_KEY:
        st.error("API key not found in .env file.")
    else:
        with st.spinner("Generating..."):
            quote = generate_quote(category)
            st.success(quote)