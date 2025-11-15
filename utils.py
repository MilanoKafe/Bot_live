import json
import os
from config import USERS_FILE, QUESTIONS_FILE, DATA_DIR
from datetime import datetime, timedelta
from config import OWNER_ID
import re

# Ensure data directories
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

USERS_DIR = os.path.join(DATA_DIR, "users")
QUESTIONS_DIR = os.path.join(DATA_DIR, "questions")
HISTORY_DIR = os.path.join(DATA_DIR, "history")
USERS_INDEX = USERS_FILE  # keep existing index path for compatibility

if not os.path.exists(USERS_DIR):
    os.makedirs(USERS_DIR)
if not os.path.exists(QUESTIONS_DIR):
    os.makedirs(QUESTIONS_DIR)
if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

ADMINS_FILE = os.path.join(DATA_DIR, "admins.json")


def load_admins():
    """Return list of admin dicts from admins file.

    Format: [{"id": 7613..., "level": "owner|full|user_admin|question_admin"}, ...]
    If file is missing, return owner with level 'owner'. If file contains list of ints (old format), convert.
    """
    if os.path.exists(ADMINS_FILE):
        try:
            with open(ADMINS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # If file contains list of ints, convert to dicts with default level 'user_admin' (except owner)
                if isinstance(data, list) and data and all(isinstance(x, int) or (isinstance(x, str) and x.isdigit()) for x in data):
                    out = []
                    for x in data:
                        uid = int(x)
                        lvl = 'owner' if uid == OWNER_ID else 'user_admin'
                        out.append({'id': uid, 'level': lvl})
                    return out
                # If it's already a list of dicts, validate
                if isinstance(data, list) and data and isinstance(data[0], dict):
                    return [{'id': int(d.get('id')), 'level': d.get('level', 'user_admin')} for d in data]
                return [{'id': OWNER_ID, 'level': 'owner'}]
        except Exception:
            return [{'id': OWNER_ID, 'level': 'owner'}]
    # default admin list contains owner
    return [{'id': OWNER_ID, 'level': 'owner'}]


def save_admins(admins):
    try:
        with open(ADMINS_FILE, 'w', encoding='utf-8') as f:
            json.dump(list(admins), f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def add_admin(user_id, level='user_admin'):
    admins = load_admins()
    if any(a['id'] == int(user_id) for a in admins):
        return False
    admins.append({'id': int(user_id), 'level': level})
    save_admins(admins)
    return True


def remove_admin(user_id):
    admins = load_admins()
    if not any(a['id'] == int(user_id) for a in admins):
        return False
    admins = [a for a in admins if a['id'] != int(user_id)]
    save_admins(admins)
    return True


def is_admin(user_id):
    admins = load_admins()
    try:
        return any(a['id'] == int(user_id) for a in admins)
    except Exception:
        return False


def get_admin_level(user_id):
    admins = load_admins()
    for a in admins:
        if a['id'] == int(user_id):
            return a.get('level')
    return None


def admins_ids_list():
    return [a['id'] for a in load_admins()]


def _user_file_path(user_id):
    return os.path.join(USERS_DIR, f"{user_id}.json")


def load_users():
    """Return list of users by reading per-user JSON files in `data/users/`.

    This intentionally does NOT maintain or write an index file; all user data
    lives in per-user files named by id.
    """
    users = []
    if not os.path.exists(USERS_DIR):
        return users
    for fname in os.listdir(USERS_DIR):
        if fname.endswith('.json'):
            try:
                with open(os.path.join(USERS_DIR, fname), 'r', encoding='utf-8') as f:
                    users.append(json.load(f))
            except Exception:
                continue
    return users


def save_users(users):
    """Deprecated: keep for compatibility but do not write a global users index."""
    try:
        # intentionally no-op to avoid creating redundant users.json
        return True
    except Exception:
        return False


def get_user(user_id):
    """Return a single user's full data from per-user file if exists, otherwise from index."""
    path = _user_file_path(user_id)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass

    # fallback to index
    users = load_users()
    for user in users:
        if user.get('id') == user_id:
            return user
    return None


def create_user(user_id, username=None, referral_code=None):
    """Create per-user JSON file and update index."""
    now = str(datetime.now())
    new_user = {
        'id': user_id,
        'username': username,
        'qbc': 0.0,
        'total_questions': 0,
        'correct_answers': 0,
        'referrals': [],
        'referred_by': referral_code,
        'created_at': now,
        'is_premium': False,
        'premium_until': None,
        'is_banned': False,
        # attempted_questions is now a dict: {"backend": [ids], "frontend": [ids], ...}
        'attempted_questions': {},
        # completed_tests: list of categories the user finished and should not retake
        'completed_tests': [],
        # chat history: list of {'ts': iso, 'direction': 'in'|'out', 'text': '...'}
        'chat_history': []
    }
    # write per-user file
    try:
        with open(_user_file_path(user_id), 'w', encoding='utf-8') as f:
            json.dump(new_user, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

    # do not touch a global users index; per-user file is the source of truth
    return new_user


def update_user(user_id, **kwargs):
    """Update per-user file and index.

    Accepts keyword args to update stored user data.
    """
    user = get_user(user_id)
    if not user:
        return None

    user.update(kwargs)
    # write back per-user file
    try:
        with open(_user_file_path(user_id), 'w', encoding='utf-8') as f:
            json.dump(user, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

    # per-user file was already written above; do not write a global users index
    return user


def append_chat_entry(user_id, text, direction='in'):
    """Append a chat entry to the user's `chat_history` list (keeps latest entries)."""
    try:
        user = get_user(user_id)
        if not user:
            # create a minimal user record if missing
            user = create_user(user_id, username=None)

        entry = {'ts': str(__import__('datetime').datetime.now()), 'direction': direction, 'text': text}
        hist = user.get('chat_history', [])
        hist.append(entry)
        # keep last 1000 entries to avoid unbounded growth
        if len(hist) > 1000:
            hist = hist[-1000:]
        user['chat_history'] = hist
        # persist
        try:
            with open(_user_file_path(user_id), 'w', encoding='utf-8') as f:
                json.dump(user, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

        # do not maintain an external users index file; per-user file is authoritative
        # also append to separate history file and prune older entries
        try:
            append_history(user_id, text, direction=direction)
        except Exception:
            pass
        return True
    except Exception:
        return False


def _history_file_path(user_id: int) -> str:
    return os.path.join(HISTORY_DIR, f"{user_id}.json")


def load_history(user_id: int):
    path = _history_file_path(user_id)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # ensure list
                if isinstance(data, list):
                    return data
        except Exception:
            return []
    return []


def save_history(user_id: int, history_list):
    path = _history_file_path(user_id)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(history_list, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def append_history(user_id: int, text: str, direction: str = 'in'):
    """Append to a per-user history file and prune entries older than 30 days."""
    try:
        hist = load_history(user_id)
        entry = {'ts': str(datetime.now()), 'direction': direction, 'text': text}
        hist.append(entry)
        # prune older than 30 days
        cutoff = datetime.now() - timedelta(days=30)
        new_hist = []
        for h in hist:
            try:
                hts = datetime.fromisoformat(h.get('ts'))
            except Exception:
                # keep entries with unparsable ts as they may be recent
                new_hist.append(h)
                continue
            if hts >= cutoff:
                new_hist.append(h)
        # keep last 2000 entries as absolute cap
        if len(new_hist) > 2000:
            new_hist = new_hist[-2000:]
        save_history(user_id, new_hist)
        return True
    except Exception:
        return False


def add_referral(user_id, referral_user_id):
    """Add referral to a user (referrer user_id gets credit)"""
    ref_user = get_user(user_id)
    if ref_user:
        if referral_user_id not in ref_user.get('referrals', []):
            ref_user.setdefault('referrals', []).append(referral_user_id)
            ref_user['qbc'] = ref_user.get('qbc', 0) + 0.2
            update_user(user_id, **ref_user)
            return True
    return False


def load_questions():
    """Load all questions by reading per-category files in QUESTIONS_DIR"""
    data = {}
    for fname in os.listdir(QUESTIONS_DIR):
        if fname.endswith('.json'):
            cat = fname[:-5]
            try:
                with open(os.path.join(QUESTIONS_DIR, fname), 'r', encoding='utf-8') as f:
                    data[cat] = json.load(f)
            except Exception:
                data[cat] = []
    return data


def _normalize_category(category: str) -> str:
    """Return a filesystem-safe normalized category name (lowercase, underscore)."""
    if not category:
        return ''
    s = str(category).strip().lower()
    # replace spaces and slashes with underscore
    s = re.sub(r'[\s/\\]+', '_', s)
    # remove any chars that are not alnum or underscore
    s = re.sub(r'[^0-9a-zA-Z_]+', '', s)
    # collapse multiple underscores
    s = re.sub(r'_+', '_', s)
    return s


def save_questions(questions):
    """Save questions dict into per-category files (overwrites categories present in dict)."""
    for cat, qlist in questions.items():
        ncat = _normalize_category(cat)
        path = os.path.join(QUESTIONS_DIR, f"{ncat}.json")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(qlist, f, indent=2, ensure_ascii=False)
        except Exception:
            pass


def add_question(category, question_text, answers):
    """Add a question into category file."""
    ncat = _normalize_category(category)
    path = os.path.join(QUESTIONS_DIR, f"{ncat}.json")
    qlist = []
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                qlist = json.load(f)
        except Exception:
            qlist = []

    question_id = len(qlist) + 1
    new_question = {
        'id': question_id,
        'question': question_text,
        'answers': answers
    }
    qlist.append(new_question)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(qlist, f, indent=2, ensure_ascii=False)
    except Exception:
        pass
    return new_question


def get_questions_by_category(category):
    """Return list of questions for a category (reads category file)."""
    ncat = _normalize_category(category)
    path = os.path.join(QUESTIONS_DIR, f"{ncat}.json")
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []


def get_user_statistics():
    """Barcha foydalanuvchilarning statistikasini olish"""
    users = load_users()
    stats = {
        'total_users': len(users),
        'premium_users': len([u for u in users if u.get('is_premium') or (u.get('premium_until') and datetime.fromisoformat(u.get('premium_until')) > datetime.now())]),
        'total_qbc': sum(u.get('qbc', 0) for u in users),
        'users': users
    }
    return stats


def load_help_requests():
    """Load help requests list"""
    help_file = os.path.join(DATA_DIR, "help_requests.json")
    if os.path.exists(help_file):
        with open(help_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_help_requests(requests):
    help_file = os.path.join(DATA_DIR, "help_requests.json")
    with open(help_file, 'w', encoding='utf-8') as f:
        json.dump(requests, f, indent=2, ensure_ascii=False)


def add_help_request(user_id, username, text):
    reqs = load_help_requests()
    new_req = {
        'id': len(reqs) + 1,
        'user_id': user_id,
        'username': username,
        'text': text,
        'created_at': str(__import__('datetime').datetime.now()),
        'status': 'new',
        'admin_reply': None
    }
    reqs.append(new_req)
    save_help_requests(reqs)
    return new_req


def update_help_request(req_id, **kwargs):
    reqs = load_help_requests()
    for req in reqs:
        if req.get('id') == req_id:
            req.update(kwargs)
            save_help_requests(reqs)
            return req
    return None
