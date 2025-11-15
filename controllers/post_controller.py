from fastapi import HTTPException
from datetime import datetime
import zoneinfo

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

def create_post(data: dict):
    if not data:
        raise HTTPException(status_code=400, detail="요청 본문이 비어 있습니다.")

    title = data.get("title")
    content = data.get("content")
    author_id = data.get("author_id")
    author_name = data.get("author_name")

    if not title or not title.strip():
        raise HTTPException(status_code=400, detail="제목을 입력해주세요.")

    if len(title.strip()) > 26:
        raise HTTPException(status_code=400, detail="제목은 26자 이내로 작성해주세요.")

    if not content or not content.strip():
        raise HTTPException(status_code=400, detail="내용을 입력해주세요.")

    if author_id is None:
        raise HTTPException(status_code=400, detail="작성자 ID를 입력해주세요.")

    if not author_name or not author_name.strip():
        raise HTTPException(status_code=400, detail="작성자 이름을 입력해주세요.")

    new_id = max(post["id"] for post in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "title": title.strip(),
        "content": content.strip(),
        "author_id": author_id,
        "author_name": author_name.strip(),
        "created_at": datetime.now(KST).isoformat(),
        "updated_at": datetime.now(KST).isoformat(),
        "views": 0,
        "likes": 0,
    }
    posts.append(new_post)
    return {"data": new_post}


def update_post(post_id: int, data: dict):
    post = next((post for post in posts if post["id"] == post_id), None)

    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    
    title = data.get("title")
    content = data.get("content")
    author_name = data.get("author_name")

    new_title = post["title"]
    if title is not None:
        stripped_title = title.strip()
        if not stripped_title:
            raise HTTPException(status_code=400, detail="제목을 입력해주세요.")
        if len(stripped_title) > 26:
            raise HTTPException(status_code=400, detail="제목은 26자 이내로 작성해주세요.")
        new_title = stripped_title

    new_content = post["content"]
    if content is not None:
        stripped_content = content.strip()
        if not stripped_content:
            raise HTTPException(status_code=400, detail="내용을 입력해주세요.")
        new_content = stripped_content

    new_author_name = post["author_name"]
    if author_name is not None:
        stripped_author_name = author_name.strip()
        if not stripped_author_name:
            raise HTTPException(status_code=400, detail="작성자 이름을 입력해주세요.")
        new_author_name = stripped_author_name

    updated_post = {
        "title": new_title,
        "content": new_content,
        "author_id": data.get("author_id", post["author_id"]),
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
