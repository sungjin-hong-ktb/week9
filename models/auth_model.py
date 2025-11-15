from typing import Dict, Optional

from models import user_model

def find_user_by_credentials(email: str, password: str) -> Optional[Dict[str, str | int]]:
    return next(
        (user for user in user_model.list_users() if user["email"] == email and user["password"] == password),
        None,
    )

def find_user_by_id(user_id: int) -> Optional[Dict[str, str | int]]:
    return user_model.get_user(user_id)
