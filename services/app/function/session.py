
import json
import os
from pathlib import Path
import time
from app import RUNNING_ID_FILE, SESSION_FILE, SESSIONS_FOLDER, REFERENCE_NUMBER_FILE

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

def generate_reference_number(refnumber=None) -> str:
    try:
        if refnumber is None:
            refnumber = str(int(time.time()))
        
        # Convert to Path object for better path handling
        ref_file = Path(REFERENCE_NUMBER_FILE).resolve()
        sessions_dir = ref_file.parent
        
        # Debug prints
        print(f"Absolute path: {ref_file}")
        print(f"Parent directory: {sessions_dir}")
        
        # Create directory if it doesn't exist
        sessions_dir.mkdir(parents=True, exist_ok=True)
        
        reference_data = {
            'reference_number': refnumber
        }
        
        # Write using Path object
        ref_file.write_text(json.dumps(reference_data, indent=4), encoding='utf-8')
        
        # Verify file exists and is readable
        if ref_file.exists():
            print(f"File created successfully. Content:\n{ref_file.read_text()}")
            return refnumber
        else:
            print("File creation failed!")
            return None
            
    except Exception as e:
        print(f"Error generating reference number: {str(e)}")
        print(f"Exception type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return None
    
def clear_reference_number():
    if os.path.exists(REFERENCE_NUMBER_FILE):
        os.remove(REFERENCE_NUMBER_FILE)