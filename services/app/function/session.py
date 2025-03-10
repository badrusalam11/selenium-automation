
import json
import os
from pathlib import Path
import time
from app import RUNNING_ID_FILE, SESSION_FILE, SESSIONS_FOLDER

def clear_sessions():
        session_file=SESSION_FILE
        """Clears the session data by deleting the session file."""
        if os.path.exists(session_file):
            os.remove(session_file)
        session = []  # Clear the in-memory session list

def clear_session_files():
    sessions_path = Path(SESSIONS_FOLDER)
    for session_file in sessions_path.glob("*.json"):
        session_file.unlink()