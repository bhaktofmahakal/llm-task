import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
CHROMA_DB_PATH = "chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.1-8b-instant"
TOP_K_FACTS = 3
CONFIDENCE_THRESHOLD = 0.3

FACT_BASE_PATH = "fact_base.csv"
