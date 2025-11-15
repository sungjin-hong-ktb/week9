from fastapi import HTTPException

from schemas import LoginRequest

users = [
    {"id": 1, "nickname": "Alice", "email": "alice@example.com", "password": "alicepwd"},
    {"id": 2, "nickname": "Bob", "email": "bob@example.com", "password": "bobpwd"},
    {"id": 3, "nickname": "Ned", "email": "ned@ktb.com", "password": "nedpwd"}
]

def login(data: LoginRequest):
    email = data.email
    password = data.password

    user = next(
        (user for user in users if user["email"] == email and user["password"] == password),
        None
    )

    if not user:
        raise HTTPException(status_code=400, detail="아이디 또는 비밀번호를 확인해주세요.")
    
    return {"message": "로그인에 성공했습니다.", "data": user}

def logout(user_id: int):
    user = next((user for user in users if user["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다.")

    return {"message": "로그아웃에 성공했습니다."}
