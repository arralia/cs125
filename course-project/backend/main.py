# added a bloilerpalte fastapi server as a starting point created with gemini ai

import os
from fastapi import FastAPI, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.exceptions import HTTPException

# Load environment variables from .env
load_dotenv()

app = FastAPI(title="FastAPI Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],  # Specified origin is required for credentials
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Backend!"}


@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Server is running smoothly"}


@app.get("/api")
async def api_root():
    return {"message": "Welcome to the API!"}


@app.get("/api/classInfo")
async def api_class_info():
    print("api_class_info called")
    return {
        "data": [
            {"className": "CS 125", "description": "Next Generation Search Systems"},
            {"className": "CS 161", "description": "Design and Analysis of Algorithms"},
            {"className": "CS 162", "description": "Formal Languages and Automata"},
        ],
        "status": "ok",
        "message": "Class info is running smoothly",
    }


class LoginRequest(BaseModel):
    username: str


@app.post("/api/login")
async def api_login(request: LoginRequest):
    usernames = ["nathan", "alyssia", "peter"]
    if request.username in usernames:
        return {
            "status": "ok",
            "message": f"Login is running smoothly, user: {request.username} has been seen",
            "userid": request.username,
        }
    else:
        # This sends a 404 status code to the frontend
        raise HTTPException(status_code=404, detail="User not found")


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 5001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
