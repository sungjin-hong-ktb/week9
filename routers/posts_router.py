from fastapi import APIRouter

from controllers import post_controller
from schemas import PostCreate, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/")
def get_posts():
    return post_controller.get_all_posts()

@router.get("/{post_id}")
def get_post_by_id(post_id: int):
    return post_controller.get_post_by_id(post_id)

@router.post("/", status_code=201)
def create_post(data: PostCreate):
    return post_controller.create_post(data)

@router.put("/{post_id}")
def update_post(post_id: int, data: PostUpdate):
    return post_controller.update_post(post_id, data)

@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int):
    return post_controller.delete_post(post_id)
