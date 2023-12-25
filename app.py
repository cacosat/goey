import streamlit
import openai
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    streamlit.error("OAI key not found")
    streamlit.stop()