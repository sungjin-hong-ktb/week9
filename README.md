# ktb_assign_type2

## 개요
FastAPI로 Route, Controller 만 이용해서 구현 후 Postman 요청에 응답하는 커뮤니티 백엔드 구현  
커뮤니티에 맞는 백엔드로 변환

## 프로젝트 구조
```
type2/
├── main.py                # FastAPI 앱, 라우터 등록
├── routers/               # HTTP Layer: 요청/응답 스펙 정의
├── controllers/           # Service Layer: 검증 및 비즈니스 규칙
├── schemas/               # Pydantic 모델: 요청/응답 스키마 및 검증
```

## 실행 방법
1. 가상환경(리눅스)
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   
2. 의존성 설치
   ```bash
   pip install -r requirements.txt
   ```
3. 서버 실행
   ```bash
   uvicorn main:app --reload
   ```
4. `http://127.0.0.1:8000/docs`에서 Swagger UI, Postman에서는 `http://127.0.0.1:8000` 사용

## 기능 요약
### 인증
- `POST /login` : 이메일/비밀번호 필수 검사, 일치하지 않으면 400
- `POST /logout` : 존재하지 않는 사용자면 404

### 회원
- `GET /users`, `GET /users/{id}` : 목록 및 단건 조회
- `POST /users` : 닉네임(공백 금지, 10자 제한), 이메일, 비밀번호(8~20자/대소문자/숫자/특수문자) 검증
- `PUT /users/{id}` : 수정 대상이 하나도 없으면 400
- `DELETE /users/{id}` : 없는 회원 삭제 시 404

### 게시글
- `GET /posts`, `GET /posts/{id}` : ID 유효성 검사 포함
- `POST /posts` : 제목 26자 제한, 내용/작성자 필수, 생성·수정 시각(KST) 기록
- `PUT /posts/{id}` : 비어 있는 값으로 수정 불가, 수정 시각 갱신
- `DELETE /posts/{id}` : 없는 게시글이면 404
