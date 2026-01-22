import os
import dotenv
import google.generativeai as genai

dotenv.load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
LLM_MODEL = os.getenv("LLM_MODEL")

genai.configure(api_key=GOOGLE_API_KEY)
MODEL = genai.GenerativeModel(LLM_MODEL)