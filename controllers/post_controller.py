from fastapi import HTTPException

from models import post_model
from schemas import PostCreate, PostUpdate

def get_all_posts():
    return {"data": post_model.list_posts()}

def get_post_by_id(post_id: int):
    if not post_id:
        raise HTTPException(status_code=400, detail="게시글 ID를 입력해주세요.")
    
    if post_id <= 0:
        raise HTTPException(status_code=400, detail="유효하지 않은 게시글 ID입니다.")

    post = post_model.get_post(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    return {"data": post}

def create_post(data: PostCreate):
    payload = data.model_dump()
    new_post = post_model.create_post(
        title=payload["title"],
        content=payload["content"],
        author_id=payload["author_id"],
        author_name=payload["author_name"],
    )
    return {"data": new_post}

def update_post(post_id: int, data: PostUpdate):
    post = post_model.get_post(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    
    payload = data.model_dump(exclude_unset=True)
    title = payload.get("title")
    content = payload.get("content")
    author_name = payload.get("author_name")

    new_title = title if title is not None else post["title"]
    new_content = content if content is not None else post["content"]
    new_author_name = author_name if author_name is not None else post["author_name"]

    updated_post = post_model.update_post(
        post_id,
        title=new_title,
        content=new_content,
        author_name=new_author_name,
        author_id=payload.get("author_id", post["author_id"]),
    )

    return {"data": updated_post}

def delete_post(post_id: int):
    deleted = post_model.delete_post(post_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    return {"message": "게시글이 삭제되었습니다."}
