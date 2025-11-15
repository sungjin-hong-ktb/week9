from datetime import datetime
from typing import Dict, List, Optional
import zoneinfo

KST = zoneinfo.ZoneInfo("Asia/Seoul")

posts: List[Dict[str, str | int]] = [
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
    },
]

def list_posts() -> List[Dict[str, str | int]]:
    return posts

def get_post(post_id: int) -> Optional[Dict[str, str | int]]:
    return next((post for post in posts if post["id"] == post_id), None)

def create_post(title: str, content: str, author_id: int, author_name: str) -> Dict[str, str | int]:
    timestamp = datetime.now(KST).isoformat()
    new_post = {
        "id": max((post["id"] for post in posts), default=0) + 1,
        "title": title,
        "content": content,
        "author_id": author_id,
        "author_name": author_name,
        "created_at": timestamp,
        "updated_at": timestamp,
        "views": 0,
        "likes": 0,
    }
    posts.append(new_post)
    return new_post

def update_post(
    post_id: int,
    *,
    title: Optional[str] = None,
    content: Optional[str] = None,
    author_name: Optional[str] = None,
    author_id: Optional[int] = None,
) -> Optional[Dict[str, str | int]]:
    post = get_post(post_id)
    if not post:
        return None

    if title is not None:
        post["title"] = title
    if content is not None:
        post["content"] = content
    if author_name is not None:
        post["author_name"] = author_name
    if author_id is not None:
        post["author_id"] = author_id

    post["updated_at"] = datetime.now(KST).isoformat()
    return post

def delete_post(post_id: int) -> bool:
    post = get_post(post_id)
    if not post:
        return False

    posts.remove(post)
    return True
