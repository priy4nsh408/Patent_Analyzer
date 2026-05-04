from dotenv import load_dotenv
import os

load_dotenv()

LENS_API_URL = os.getenv("LENS_API_URL")
LENS_API_KEY = os.getenv("LENS_API_KEY")

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

TOP_K = int(os.getenv("TOP_K_PATENTS", 3))
HIGH_THRESHOLD = int(os.getenv("SIMILARITY_THRESHOLD_HIGH", 75))
MEDIUM_THRESHOLD = int(os.getenv("SIMILARITY_THRESHOLD_MEDIUM", 40))