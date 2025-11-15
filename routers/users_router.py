from fastapi import APIRouter
from controllers import user_controller

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_users():
    return user_controller.get_all_users()

@router.get("/{user_id}")
def get_user(user_id: int):
    return user_controller.get_user_by_id(user_id)

@router.post("/", status_code=201)
def create_user(data: dict):
    return user_controller.create_user(data)

@router.put("/{user_id}")
def update_user(user_id: int, data: dict):
    return user_controller.update_user(user_id, data)

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int):
    return user_controller.delete_user(user_id)
