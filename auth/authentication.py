from typing import Dict, Any
from database.database import add_user, authenticate_user
from utils.validators import validate_email, validate_password
from auth.session import login as session_login

def register_user(name: str, username: str, email: str, password: str, confirm_password: str) -> Dict[str, Any]:
    """
    Validate field values, verify email formatting and password rules, check for duplicates,
    and register the user in the JSON database.
    """
    # Verify all fields are present
    name = name.strip()
    username = username.strip()
    email = email.strip()
    
    if not name or not username or not email or not password or not confirm_password:
        return {"success": False, "message": "All fields are required."}
        
    # Verify username doesn't have spaces or special characters
    if not username.isalnum():
        return {"success": False, "message": "Username must be alphanumeric (letters and numbers only)."}
        
    # Validate passwords match
    if password != confirm_password:
        return {"success": False, "message": "Passwords do not match."}
        
    # Validate email formatting
    if not validate_email(email):
        return {"success": False, "message": "Invalid email address."}
        
    # Validate password complexity
    pw_validation = validate_password(password)
    if not pw_validation["valid"]:
        return {"success": False, "message": pw_validation["message"]}
        
    # Save user to database
    return add_user(name, username, email, password)

def login_user(username_or_email: str, password: str) -> Dict[str, Any]:
    """
    Authenticate the user against the database and log them in, creating a Streamlit session.
    """
    username_or_email = username_or_email.strip()
    
    if not username_or_email or not password:
        return {"success": False, "message": "Username/Email and password are required."}
        
    user = authenticate_user(username_or_email, password)
    if user:
        session_login(user)
        return {"success": True, "message": "Login successful!", "user": user}
    else:
        return {"success": False, "message": "Incorrect username/email or password."}
