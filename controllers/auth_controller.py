from fastapi import HTTPException
from models import auth_model
from schemas import LoginRequest

def login(data: LoginRequest):
    email = data.email
    password = data.password

    user = auth_model.find_user_by_credentials(email, password)

    if not user:
        raise HTTPException(status_code=400, detail="아이디 또는 비밀번호를 확인해주세요.")
    return {"message": "로그인에 성공했습니다.", "data": user}

def logout(user_id: int):
    user = auth_model.find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다.")

    return {"message": "로그아웃에 성공했습니다."}
