import os
import json
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ADMIN_ID can be a single integer, a comma-separated list, or a JSON list like [1,2]
_admin_raw = os.getenv("ADMIN_ID", "")
ADMIN_IDS = []
if _admin_raw:
	try:
		# Try JSON first (handles [1,2])
		parsed = json.loads(_admin_raw)
		if isinstance(parsed, list):
			ADMIN_IDS = [int(x) for x in parsed]
		else:
			ADMIN_IDS = [int(parsed)]
	except Exception:
		# Fallback: comma-separated or single number
		try:
			parts = [p.strip() for p in _admin_raw.split(',') if p.strip()]
			ADMIN_IDS = [int(p) for p in parts]
		except Exception:
			ADMIN_IDS = []

# For backwards compatibility, expose first admin as ADMIN_ID (or 0)
ADMIN_ID = ADMIN_IDS[0] if ADMIN_IDS else 0

CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))
CHANNEL_URL = os.getenv("CHANNEL_URL")

# Owner ID: can be set via env OWNER_ID, otherwise default to a sensible value
# Default owner set to the deployer (change if needed)
try:
	OWNER_ID = int(os.getenv("OWNER_ID", "7613242496"))
except Exception:
	OWNER_ID = ADMIN_ID

# Web admin token for accessing the admin web app. Keep this secret in .env.
ADMIN_WEB_TOKEN = os.getenv("ADMIN_WEB_TOKEN", str(OWNER_ID))

QBC_PER_CORRECT = 0.5
QBC_PER_REFERRAL = 0.2
QUESTION_TIME_LIMIT = 15

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
QUESTIONS_FILE = os.path.join(DATA_DIR, "questions.json")
