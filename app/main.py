from fastapi import FastAPI
from app.routers import post, user, auth, vote
from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine) # not required once alembic is used for database migration

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def home():
    return {"message": "Hello World"}
