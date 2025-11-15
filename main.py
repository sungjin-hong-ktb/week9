from fastapi import FastAPI
from routers.users_router import router as user_router
from routers.auth_router import router as auth_router
from routers.posts_router import router as post_router

app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(post_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
