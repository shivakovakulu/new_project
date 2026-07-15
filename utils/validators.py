import re
from typing import Dict, Any

def validate_email(email: str) -> bool:
    """Validate email address format. Uses email-validator package with a regex fallback."""
    if not email:
        return False
    try:
        from email_validator import validate_email as check_email
        check_email(email, check_deliverability=False)
        return True
    except (ImportError, Exception):
        # Fallback regex email validation in case package load fails or raises error
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(email_regex, email))

def validate_password(password: str) -> Dict[str, Any]:
    """
    Validate password strength according to instructions:
    - Minimum 8 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 number
    """
    if not password:
        return {"valid": False, "message": "Password cannot be empty."}
    
    if len(password) < 8:
        return {"valid": False, "message": "Password must be at least 8 characters long."}
        
    if not any(c.isupper() for c in password):
        return {"valid": False, "message": "Password must contain at least one uppercase letter."}
        
    if not any(c.islower() for c in password):
        return {"valid": False, "message": "Password must contain at least one lowercase letter."}
        
    if not any(c.isdigit() for c in password):
        return {"valid": False, "message": "Password must contain at least one number."}
        
    return {"valid": True, "message": "Password meets all requirements."}
