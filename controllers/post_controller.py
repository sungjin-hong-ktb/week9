from datetime import datetime
import zoneinfo

from fastapi import HTTPException

from schemas import PostCreate, PostUpdate

KST = zoneinfo.ZoneInfo("Asia/Seoul")
posts = [
    {
        "id": 1,
        "title": "피곤한데 집에 갈까요?",
        "content": "오늘 하루 너무 피곤했어요. 집에 가고 싶어요.",
        "author_id": 123,
        "author_name": "ned",
        "created_at": "2025-11-13T10:30:00",
        "updated_at": "2025-11-13T10:30:00",
        "views": 42,
        "likes": 5,
    },
    {
        "id": 2,
        "title": "저녁 뭐 먹을까요?",
        "content": "저녁 메뉴 추천해주세요",
        "author_id": 124,
        "author_name": "ned",
        "created_at": "2025-11-14T17:00:00",
        "updated_at": "2025-11-14T17:00:00",
        "views": 30,
        "likes": 3,
    }
]

def get_all_posts():
    return {"data": posts}

def get_post_by_id(post_id: int):
    if not post_id:
        raise HTTPException(status_code=400, detail="게시글 ID를 입력해주세요.")
    
    if post_id <= 0:
        raise HTTPException(status_code=400, detail="유효하지 않은 게시글 ID입니다.")

    post = next(
        (post for post in posts if post["id"] == post_id), None
    )

    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    return {"data": post}

def create_post(data: PostCreate):
    new_id = max(post["id"] for post in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "title": data.title,
        "content": data.content,
        "author_id": data.author_id,
        "author_name": data.author_name,
        "created_at": datetime.now(KST).isoformat(),
        "updated_at": datetime.now(KST).isoformat(),
        "views": 0,
        "likes": 0,
    }
    posts.append(new_post)
    return {"data": new_post}


def update_post(post_id: int, data: PostUpdate):
    post = next((post for post in posts if post["id"] == post_id), None)

    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    
    update_data = {
        key: value
        for key, value in data.model_dump(exclude_unset=True).items()
        if value is not None
    }

    title = update_data.get("title")
    content = update_data.get("content")
    author_name = update_data.get("author_name")

    new_title = post["title"]
    if title is not None:
        new_title = title

    new_content = post["content"]
    if content is not None:
        new_content = content

    new_author_name = post["author_name"]
    if author_name is not None:
        new_author_name = author_name

    updated_post = {
        "title": new_title,
        "content": new_content,
        "author_id": update_data.get("author_id", post["author_id"]),
        "author_name": new_author_name,
        "updated_at": datetime.now(KST).isoformat(),
    }

    post.update(updated_post)

    return {"data": post}

def delete_post(post_id: int):
    post = next((post for post in posts if post["id"] == post_id), None)

    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    posts.remove(post)
    return {"message": "게시글이 삭제되었습니다."}
