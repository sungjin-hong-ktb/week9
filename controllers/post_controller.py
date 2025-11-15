from fastapi import HTTPException
from datetime import datetime, timedelta

posts = [
    {
        "id": 1,
        "title": "피곤한데 집에 갈까요?",
        "content": "오늘 하루 너무 피곤했어요. 집에 가고 싶어요.",
        "author_id": 123,
        "author_name": "홍길동",
        "created_at": "2025-11-13T10:30:00",
        "updated_at": "2025-11-13T10:30:00",
        "views": 42,
        "likes": 5
    },
    {
        "id": 2,
        "title": "저녁 뭐 먹을까요?",
        "content": "저녁 메뉴 추천해주세요",
        "author_id": 124,
        "author_name": "김철수",
        "created_at": "2025-11-14T17:00:00",
        "updated_at": "2025-11-14T17:00:00",
        "views": 30,
        "likes": 3
    }
]

def get_all_posts():
    return {"data": posts}

def get_post_by_id(post_id: int):
    if not post_id:
        raise HTTPException(status_code=400, detail="Post ID is required")
    
    if post_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid Post ID")

    post = next((post for post in posts if post["id"] == post_id), None)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"data": post}

def create_post(data: dict):
    if not data:
        raise HTTPException(status_code=400, detail="Request body is empty")

    new_id = max(post["id"] for post in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "title": data.get("title", ""),
        "content": data.get("content", ""),
        "author_id": data.get("author_id", 0),
        "author_name": data.get("author_name", ""),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "views": 0,
        "likes": 0
    }
    posts.append(new_post)
    return {"data": new_post}


def update_post(post_id: int, data: dict):
    post = next((post for post in posts if post["id"] == post_id), None)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.update({
        "title": data.get("title", post["title"]),
        "content": data.get("content", post["content"]),
        "author_id": data.get("author_id", post["author_id"]),
        "author_name": data.get("author_name", post["author_name"]),
        "updated_at": datetime.utcnow().isoformat(),
    })

    return {"data": post}

def delete_post(post_id: int):
    post = next((post for post in posts if post["id"] == post_id), None)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    posts.remove(post)
    return {"message": "Post deleted successfully"}