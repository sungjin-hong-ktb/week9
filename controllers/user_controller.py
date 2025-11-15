from fastapi import HTTPException

users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Ned", "email": "ned@ktb.com"}
]

def create_user(data: dict):
    name = data.get("name")
    email = data.get("email")
    
    if not name or not email:
        raise HTTPException(status_code=400, detail="Missing required fields")

    if "@" not in email:
        raise HTTPException(status_code=400, detail="Invalid email format")

    if any(user["email"] == email for user in users):
        raise HTTPException(status_code=409, detail="Email already exists")

    new_user = {
        "id": max((user["id"] for user in users), default=0) + 1,
        "name": name,
        "email": email
    }
    users.append(new_user)
    return {"message": "User created successfully", "data": new_user}

def get_all_users():
    return {"data": users}

def get_user_by_id(user_id: int):
    user = next((user for user in users if user["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_user(user_id: int, data: dict):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        raise HTTPException(status_code=400, detail="Missing required fields")

    if "@" not in email:
        raise HTTPException(status_code=400, detail="Invalid email format")

    user["name"] = name
    user["email"] = email
    return user

def delete_user(user_id: int):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    users.remove(user)
