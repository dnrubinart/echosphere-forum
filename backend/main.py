from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.auth import auth_router
from routers.categories import category_router
from routers.messages import message_router
from routers.replies import reply_router
from routers.topics import topics_router
from routers.users import users_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(topics_router)
app.include_router(category_router)
app.include_router(reply_router)
app.include_router(message_router)
app.include_router(users_router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
