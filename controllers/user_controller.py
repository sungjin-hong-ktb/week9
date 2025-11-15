import re
from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException

users = [
    {"id": 1, "nickname": "Alice", "email": "alice@example.com", "password": "alicepwd"},
    {"id": 2, "nickname": "Bob", "email": "bob@example.com", "password": "bobpwd"},
    {"id": 3, "nickname": "Ned", "email": "ned@ktb.com", "password": "nedpwd"}
]

def create_user(data: dict):
    nickname = data.get("nickname")
    email = data.get("email")
    password = data.get("password")
    
    if not nickname or not email or not password:
        raise HTTPException(status_code=400, detail="닉네임, 이메일, 비밀번호를 모두 입력해주세요.")

    validation_nickname(nickname)
    validation_email(email)
    validation_password(password)
    
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


def update_user(user_id: int, data: dict):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다.")

    nickname = data.get("nickname")
    email = data.get("email")
    password = data.get("password")

    if not any([nickname, email, password]):
        raise HTTPException(status_code=400, detail="수정할 정보를 입력해주세요.")

    if nickname:
        validation_nickname(nickname)
        user["nickname"] = nickname

    if email:
        validation_email(email)
        user["email"] = email

    if password:
        validation_password(password)
        user["password"] = password

    return {"message": "회원 정보가 수정되었습니다.", "data": user}

def delete_user(user_id: int):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다.")

    users.remove(user)
    return {"message": "회원 정보가 삭제되었습니다."}

def validation_email(email: str):
    try:
        validate_email(email)
    except EmailNotValidError:
        raise HTTPException(
            status_code=400,
            detail="올바른 이메일 주소 형식을 입력해주세요. (예: example@example.com)"
        )

    if any(user["email"] == email for user in users):
        raise HTTPException(status_code=409, detail="중복된 이메일 입니다.")

def validation_password(password: str):
    PASSWORD_PATTERN = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]).{8,20}$"
    )
    
    if not password or not PASSWORD_PATTERN.match(password):
        raise HTTPException(
            status_code=400,
            detail="비밀번호는 8~20자이며 대문자, 소문자, 숫자, 특수문자를 각각 최소 1개 포함해야 합니다."
        )

def validation_nickname(nickname: str):
    if not nickname:
        raise HTTPException(status_code=400, detail="닉네임을 입력해주세요.")

    if len(nickname) >= 11:
        raise HTTPException(status_code=400, detail="닉네임은 최대 10자 까지 작성 가능합니다.")
    
    if " " in nickname:
        raise HTTPException(status_code=400, detail="띄어쓰기를 없애주세요.")
    
    if any(u["nickname"] == nickname for u in users):
        raise HTTPException(status_code=409, detail="중복된 닉네임 입니다.")
