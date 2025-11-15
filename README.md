# ktb_assign_type2

## 개요
FastAPI로 작성한 간단한 커뮤니티 백엔드입니다. 라우터와 컨트롤러만을 사용해 로그인, 회원 CRUD, 게시글 CRUD 요청을 처리하도록 구성했습니다. 모든 데이터는 인메모리 리스트에 저장되며, Postman 같은 클라이언트로 요청을 보내 시나리오를 검증할 수 있습니다.

## 실행 방법
1. 의존성 설치
   ```bash
   pip install -r requirements.txt
   ```
2. 서버 실행
   ```bash
   uvicorn main:app --reload
   ```
3. 기본 주소는 `http://127.0.0.1:8000`이며, `/docs`에서 자동 생성된 Swagger 문서를 확인할 수 있습니다.

## 주요 라우트
- `POST /login`, `POST /logout` : 로그인/로그아웃 (컨트롤러에서 이메일 기반 검증)
- `/users` : 회원 목록 조회, 단일 조회, 생성, 수정, 삭제
- `/posts` : 게시글 목록 조회, 상세 조회, 생성, 수정, 삭제