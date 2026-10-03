import os

from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.environ["API_BASE_URL"]
API_USERNAME = os.environ["API_USERNAME"]
API_PASSWORD = os.environ["API_PASSWORD"]
PAGE_SIZE = int(os.getenv("PAGE_SIZE", "100"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "5"))
LOOKBACK_MIN = int(os.getenv("LOOKBACK_MIN", "30"))
LAKE = os.getenv("LAKE_ROOT", "lake")
PII_SALT = os.environ["PII_SALT"]
