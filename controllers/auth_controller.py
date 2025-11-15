from fastapi import HTTPException

users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Ned", "email": "ned@ktb.com"}
]

def login(data: dict):
    email = data.get("email")
    
    if not email:
        raise HTTPException(status_code=400, detail="Missing email field")

    user = next((user for user in users if user["email"] == email), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Login successful", "data": user}

def logout(user_id: int):
    user = next((user for user in users if user["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Logout successful"}