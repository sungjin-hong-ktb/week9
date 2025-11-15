from fastapi import HTTPException

from models import user_model
from schemas import UserCreate, UserUpdate

def create_user(data: UserCreate):
    payload = data.model_dump()
    nickname = payload["nickname"]
    email = payload["email"]
    password = payload["password"]
    
    validation_nickname(nickname)
    validation_email(email)
    
    new_user = user_model.create_user(nickname=nickname, email=email, password=password)
    
    return {"message": "회원 가입이 완료되었습니다.", "data": new_user}

def get_all_users():
    return {"data": user_model.list_users()}

def get_user_by_id(user_id: int):
    user = user_model.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다.")
    return user

def update_user(user_id: int, data: UserUpdate):
    user = user_model.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다.")

    payload = data.model_dump(exclude_unset=True)
    nickname = payload.get("nickname")
    email = payload.get("email")
    password = payload.get("password")

    if not any([nickname, email, password]):
        raise HTTPException(status_code=400, detail="수정할 정보를 입력해주세요.")

    if nickname:
        validation_nickname(nickname, current_user_id=user_id)

    if email:
        validation_email(email, current_user_id=user_id)

    updated_user = user_model.update_user(
        user_id,
        nickname=nickname,
        email=email,
        password=password,
    )

    return {"message": "회원 정보가 수정되었습니다.", "data": updated_user}

def delete_user(user_id: int):
    deleted = user_model.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다.")

    return {"message": "회원 정보가 삭제되었습니다."}

def validation_email(email: str, current_user_id: int | None = None):
    if user_model.email_exists(email, exclude_id=current_user_id):
        raise HTTPException(status_code=409, detail="중복된 이메일 입니다.")

def validation_nickname(nickname: str, current_user_id: int | None = None):
    if user_model.nickname_exists(nickname, exclude_id=current_user_id):
        raise HTTPException(status_code=409, detail="중복된 닉네임 입니다.")
