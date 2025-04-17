# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    REFRESH_INTERVAL = 60  # seconds
    EMBEDDING_MODEL = "embed-english-v3.0"
    CHAT_MODEL = "command"
    CHAT_TEMPERATURE = 0.3