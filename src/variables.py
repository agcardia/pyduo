import os
import sys
import pyaudio

from dotenv import load_dotenv

load_dotenv(".env")

API_KEY = os.getenv("API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == "darwin" else 2
RATE = 44100
RECORD_SECONDS = 5
