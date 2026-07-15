import json
import os
import threading
from datetime import datetime
from typing import Dict, Any, Optional

DB_FILE = os.path.join(os.path.dirname(__file__), "users.json")
db_lock = threading.Lock()

def init_db() -> None:
    """Initialize the database file with default empty users structure if it does not exist."""
    try:
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
        if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
            with open(DB_FILE, "w") as f:
                json.dump({"users": []}, f, indent=4)
    except Exception as e:
        print(f"Error initializing database: {e}")

def load_users() -> Dict[str, Any]:
    """Load users from the JSON file. Safe from missing files and invalid JSON."""
    init_db()
    with db_lock:
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            # Re-initialize on corrupted/missing database
            print(f"Error loading database ({e}). Re-initializing database file...")
            try:
                with open(DB_FILE, "w") as f:
                    json.dump({"users": []}, f, indent=4)
            except Exception:
                pass
            return {"users": []}

def save_users(users_data: Dict[str, Any]) -> None:
    """Save user structure to the JSON file safely."""
    init_db()
    with db_lock:
        try:
            # Write to a temporary backup first
            backup_file = DB_FILE + ".backup"
            with open(backup_file, "w") as f:
                json.dump(users_data, f, indent=4)
            
            # Atomic rename / overwrite
            if os.path.exists(backup_file):
                os.replace(backup_file, DB_FILE)
        except Exception as e:
            print(f"Error saving database: {e}")

def add_user(name: str, username: str, email: str, password: str) -> Dict[str, Any]:
    """Add a new user to the JSON database. Encrypts password using bcrypt via password_utils."""
    # Importing dynamically to avoid circular references
    from auth.password_utils import hash_password

    data = load_users()
    users = data.get("users", [])

    # Check for duplicate username
    if any(u["username"].lower() == username.lower() for u in users):
        return {"success": False, "message": "Username is already registered."}

    # Check for duplicate email
    if any(u["email"].lower() == email.lower() for u in users):
        return {"success": False, "message": "Email is already registered."}

    # Hash the password
    hashed_pw = hash_password(password)
    user_id = max([u["id"] for u in users], default=0) + 1

    new_user = {
        "id": user_id,
        "name": name,
        "username": username,
        "email": email,
        "password": hashed_pw,
        "created_at": datetime.now().isoformat(),
        "last_login": None
    }

    users.append(new_user)
    data["users"] = users
    save_users(data)

    return {"success": True, "message": "Registration successful!", "user": new_user}

def authenticate_user(username_or_email: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate a user using username/email and password."""
    from auth.password_utils import verify_password

    data = load_users()
    users = data.get("users", [])

    for u in users:
        # Match against either email or username (case-insensitive)
        if u["username"].lower() == username_or_email.lower() or u["email"].lower() == username_or_email.lower():
            if verify_password(password, u["password"]):
                # Update last login time
                update_last_login(u["id"])
                user_copy = u.copy()
                # Clear password hash from copy for session safety
                user_copy.pop("password", None)
                return user_copy
    return None

def update_last_login(user_id: int) -> None:
    """Update the last login timestamp for a user by ID."""
    data = load_users()
    users = data.get("users", [])
    for u in users:
        if u["id"] == user_id:
            u["last_login"] = datetime.now().isoformat()
            break
    data["users"] = users
    save_users(data)
