import debugpy
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import post, user, auth, vote
from app.config.database import Base, engine
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()

if os.getenv("RUN_MAIN") == "true":
    debugpy.listen(("0.0.0.0", 5680))
    print("✅ Debugger attached. Waiting for connection...")

origins = ["*"]

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
def root():
    return {"message": "Welcome to my FastAPI app"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
