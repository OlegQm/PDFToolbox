from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import os

root_path = os.getenv("FASTAPI_ROOT_PATH", "")
app = FastAPI(root_path=root_path)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def pong():
    return {"message": "pong!"}
