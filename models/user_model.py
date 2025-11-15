from typing import Dict, List, Optional

users: List[Dict[str, str | int]] = [
    {"id": 1, "nickname": "Alice", "email": "alice@example.com", "password": "alicepwd"},
    {"id": 2, "nickname": "Bob", "email": "bob@example.com", "password": "bobpwd"},
    {"id": 3, "nickname": "Ned", "email": "ned@ktb.com", "password": "nedpwd"},
]

def list_users() -> List[Dict[str, str | int]]:
    return users

def get_user(user_id: int) -> Optional[Dict[str, str | int]]:
    return next((user for user in users if user["id"] == user_id), None)

def create_user(nickname: str, email: str, password: str) -> Dict[str, str | int]:
    new_user = {
        "id": max((user["id"] for user in users), default=0) + 1,
        "nickname": nickname,
        "email": email,
        "password": password,
    }
    users.append(new_user)
    return new_user

def update_user(
    user_id: int, *, nickname: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None
) -> Optional[Dict[str, str | int]]:
    user = get_user(user_id)
    if not user:
        return None

    if nickname is not None:
        user["nickname"] = nickname
    if email is not None:
        user["email"] = email
    if password is not None:
        user["password"] = password

    return user

def delete_user(user_id: int) -> bool:
    user = get_user(user_id)
    if not user:
        return False

    users.remove(user)
    return True

def email_exists(email: str, exclude_id: Optional[int] = None) -> bool:
    for user in users:
        if exclude_id is not None and user["id"] == exclude_id:
            continue
        if user["email"] == email:
            return True
    return False

def nickname_exists(nickname: str, exclude_id: Optional[int] = None) -> bool:
    for user in users:
        if exclude_id is not None and user["id"] == exclude_id:
            continue
        if user["nickname"] == nickname:
            return True
    return False
