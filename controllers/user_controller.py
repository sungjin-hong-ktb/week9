import re
from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException

from models import user_model


def create_user(data: dict):
    nickname = data.get("nickname")
    email = data.get("email")
    password = data.get("password")
    
    if not nickname or not email or not password:
        raise HTTPException(status_code=400, detail="닉네임, 이메일, 비밀번호를 모두 입력해주세요.")

    validation_nickname(nickname)
    validation_email(email)
    validation_password(password)
    
    new_user = user_model.create_user(nickname=nickname, email=email, password=password)
    
    return {"message": "회원 가입이 완료되었습니다.", "data": new_user}


def get_all_users():
    return {"data": user_model.list_users()}


def get_user_by_id(user_id: int):
    user = user_model.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다.")
    return user


def update_user(user_id: int, data: dict):
    user = user_model.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다.")

    nickname = data.get("nickname")
    email = data.get("email")
    password = data.get("password")

    if not any([nickname, email, password]):
        raise HTTPException(status_code=400, detail="수정할 정보를 입력해주세요.")

    if nickname:
        validation_nickname(nickname, current_user_id=user_id)

    if email:
        validation_email(email, current_user_id=user_id)

    if password:
        validation_password(password)

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
    try:
        validate_email(email)
    except EmailNotValidError:
        raise HTTPException(
            status_code=400,
            detail="올바른 이메일 주소 형식을 입력해주세요. (예: example@example.com)",
        )

    if user_model.email_exists(email, exclude_id=current_user_id):
        raise HTTPException(status_code=409, detail="중복된 이메일 입니다.")


def validation_password(password: str):
    password_pattern = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]).{8,20}$"
    )
    
    if not password or not password_pattern.match(password):
        raise HTTPException(
            status_code=400,
            detail="비밀번호는 8~20자이며 대문자, 소문자, 숫자, 특수문자를 각각 최소 1개 포함해야 합니다.",
        )


def validation_nickname(nickname: str, current_user_id: int | None = None):
    if not nickname:
        raise HTTPException(status_code=400, detail="닉네임을 입력해주세요.")

    if len(nickname) >= 11:
        raise HTTPException(status_code=400, detail="닉네임은 최대 10자 까지 작성 가능합니다.")
    
    if " " in nickname:
        raise HTTPException(status_code=400, detail="띄어쓰기를 없애주세요.")
    
    if user_model.nickname_exists(nickname, exclude_id=current_user_id):
        raise HTTPException(status_code=409, detail="중복된 닉네임 입니다.")
