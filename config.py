"""Configuration settings for Pret Pour Support Bot"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================
# REDDIT API CREDENTIALS (from environment variables)
# ============================================================
# Get these from https://www.reddit.com/prefs/apps
# Create a "script" type app

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "pret-pour-support-bot/1.0")

# ============================================================
# MONITORING SETTINGS
# ============================================================

# Subreddits to monitor (add more as needed)
SUBREDDITS = [
    "webdev",
    "startups",
    "smallbusiness",
    "entrepreneur",
    "sideproject",
]

# Keywords to search for (case-insensitive)
KEYWORDS = [
    "pret-pour",
    "pret pour",
    "pret pour.com",
    "pretpour",
]

# Search settings
CHECK_INTERVAL_HOURS = 1  # How often to check (in hours)
MAX_POSTS_PER_SEARCH = 25  # Maximum posts to fetch per keyword
TIME_FILTER = "day"  # Options: hour, day, week, month, year, all

# ============================================================
# OUTPUT SETTINGS
# ============================================================

# Database file path
DATABASE_PATH = "seen_posts.db"

# Export file path (CSV)
EXPORT_FILE = "results.csv"

# Console output
SHOW_SCORE = True
SHOW_COMMENTS = True
SHOW_URL = True

# ============================================================
# SAFETY SETTINGS
# ============================================================

# READ-ONLY MODE: Never change this to True
# This bot ONLY monitors and logs - it does NOT auto-post
READ_ONLY = True

# Rate limiting (seconds between API calls)
RATE_LIMIT_DELAY = 2

# Maximum posts to track in database (oldest gets deleted)
MAX_DATABASE_RECORDS = 10000
