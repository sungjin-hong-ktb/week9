from fastapi import FastAPI
from routers.users import router as user_router
from routers.auth import router as auth_router
from routers.posts import router as post_router

app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(post_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
