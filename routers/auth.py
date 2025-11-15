from fastapi import APIRouter
from controllers import auth_controller

router = APIRouter()

@router.post("/login")
def login(data: dict):
    return auth_controller.login(data)

@router.post("/logout")
def logout(user_id: int):
    return auth_controller.logout(user_id)
