# config.py
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env in working dir

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")  # change if needed
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
