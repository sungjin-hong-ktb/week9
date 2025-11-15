from fastapi import APIRouter

from controllers import auth_controller
from schemas import LoginRequest

router = APIRouter()

@router.post("/login")
def login(data: LoginRequest):
    return auth_controller.login(data)

@router.post("/logout")
def logout(user_id: int):
    return auth_controller.logout(user_id)
