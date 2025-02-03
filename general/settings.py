import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load env variables from file
dotenv_file = BASE_DIR / ".env"
if os.path.isfile(dotenv_file):
    load_dotenv(dotenv_file, override=True)

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
BOT_NICKNAME = os.getenv("TG_BOT_NICKNAME")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")

DEBUG = os.getenv("DEBUG")