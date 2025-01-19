import json
import os
from pathlib import Path
from test import SESSION_FILE, SESSIONS_FOLDER

class SessionManager:
    def __init__(self):
        # Path to store sessions in a JSON file
        self.session_file = SESSION_FILE
        # Ensure the directory exists
        if not os.path.exists(os.path.dirname(self.session_file)):
            os.makedirs(os.path.dirname(self.session_file))

        # Load the sessions from the JSON file on initialization
        self.session = self.load_sessions()

    def load_sessions(self) -> list:
        """Loads the session data from the JSON file."""
        if os.path.exists(self.session_file):
            with open(self.session_file, "r") as file:
                return json.load(file)
        return []

    def save_sessions(self):
        """Saves the session data to the JSON file."""
        with open(self.session_file, "w") as file:
            json.dump(self.session, file)

    def append_session(self, session_id):
        """Appends a session_id to the session list."""
        self.session.append(session_id)
        self.save_sessions()

    def get_sessions(self) -> list:
        """Returns the list of sessions."""
        return self.session

    def clear_sessions(self):
        """Clears the session data by deleting the session file."""
        if os.path.exists(self.session_file):
            os.remove(self.session_file)
        self.session = []  # Clear the in-memory session list

    def clear_session_files(self):
        sessions_path = Path(SESSIONS_FOLDER)
        for session_file in sessions_path.glob("*.json"):
            session_file.unlink()


# Singleton instance to access session manager
session_manager = SessionManager()
