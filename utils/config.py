from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configuration variables
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1")
APP_NAME = os.getenv("APP_NAME", "SmartCampusAI")
SESSION_TIMEOUT_SEC = int(os.getenv("SESSION_TIMEOUT_SEC", "1800"))

# Verify required configuration items
if not API_KEY:
    print("Warning: API_KEY is not set in the environment variables.")
