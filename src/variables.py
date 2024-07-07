import os
from dotenv import load_dotenv

load_dotenv(".env")

API_KEY = os.getenv("API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
