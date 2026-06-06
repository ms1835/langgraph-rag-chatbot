from langchain_groq import ChatGroq
from config.settings import GROQ_API_KEY

def get_llm():
    return ChatGroq(
        model_name="llama-3.1-8b-instant",
        api_key=GROQ_API_KEY
    )