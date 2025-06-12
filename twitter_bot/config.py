import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# X/Twitter API Keys
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET_KEY = os.getenv("X_API_SECRET_KEY")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

# Other potential configurations
BOT_LOG_LEVEL = os.getenv("BOT_LOG_LEVEL", "INFO")
# Add more configurations as needed
