from typing import Optional

from fastapi import HTTPException

from schemas import UserCreate, UserUpdate

users = [
    {"id": 1, "nickname": "Alice", "email": "alice@example.com", "password": "alicepwd"},
    {"id": 2, "nickname": "Bob", "email": "bob@example.com", "password": "bobpwd"},
    {"id": 3, "nickname": "Ned", "email": "ned@ktb.com", "password": "nedpwd"}
]

def create_user(data: UserCreate):
    nickname = data.nickname
    email = data.email
    password = data.password

    ensure_unique_nickname(nickname)
    ensure_unique_email(email)
    
    new_user = {
        "id": max((user["id"] for user in users), default=0) + 1,
        "nickname": nickname,
        "email": email,
        "password": password
    }
    
    users.append(new_user)
    return {"message": "회원 가입이 완료되었습니다.", "data": new_user}

def get_all_users():
    return {"data": users}

def get_user_by_id(user_id: int):
    user = next((user for user in users if user["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다.")
    return user


def update_user(user_id: int, data: UserUpdate):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다.")

    update_data = {
        key: value
        for key, value in data.model_dump(exclude_unset=True).items()
        if value is not None
    }

    if not update_data:
        raise HTTPException(status_code=400, detail="수정할 정보를 입력해주세요.")

    nickname = update_data.get("nickname")
    email = update_data.get("email")
    password = update_data.get("password")

    if nickname:
        ensure_unique_nickname(nickname, current_user_id=user_id)
        user["nickname"] = nickname

    if email:
        ensure_unique_email(email, current_user_id=user_id)
        user["email"] = email

    if password:
        user["password"] = password

    return {"message": "회원 정보가 수정되었습니다.", "data": user}

def delete_user(user_id: int):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다.")

    users.remove(user)
    return {"message": "회원 정보가 삭제되었습니다."}

def ensure_unique_email(email: str, current_user_id: Optional[int] = None):
    if any(user["email"] == email and user["id"] != current_user_id for user in users):
        raise HTTPException(status_code=409, detail="중복된 이메일 입니다.")


def ensure_unique_nickname(nickname: str, current_user_id: Optional[int] = None):
    if any(u["nickname"] == nickname and u["id"] != current_user_id for u in users):
        raise HTTPException(status_code=409, detail="중복된 닉네임 입니다.")
