import os
from pathlib import Path
from dotenv import load_dotenv

CURRENT_DIR = Path(__file__).parent
ENV_FILE = CURRENT_DIR.parent / ".env"

if os.path.exists(ENV_FILE):
    load_dotenv(dotenv_path=ENV_FILE)
else:
    print(f"Warning: .env file not found at {ENV_FILE}. Using environment variables directly.")
    
# Database
DATABASE_URL = os.getenv("DATABASE_URL")