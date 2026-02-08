# added a bloilerpalte fastapi server as a starting point created with gemini ai

import os
from fastapi import FastAPI
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
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    username: str


class UserSetInfoRequest(BaseModel):
    classes: list[dict[str, str | int]]
    skills: dict[str, int]
    specialization: str


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Backend!"}


@app.get("/api")
async def api_root():
    return {"message": "Welcome to the API!"}


@app.get("/api/classInfo")
async def api_class_info(userid: str = None):
    print(f"api_class_info called with userid: {userid}")
    if userid == "nathan":
        return {
            "data": [
                {
                    "className": "CS 161",
                    "description": "Design and Analysis of Algorithms",
                },
            ],
            "status": "ok",
            "message": "User Class Info",
        }
    elif userid == "alyssia":
        return {
            "data": [
                {"className": "CS 162", "description": "Formal Languages and Automata"},
            ],
            "status": "ok",
            "message": "User Class Info",
        }
    elif userid == "peter":
        return {
            "data": [
                {
                    "className": "CS 125",
                    "description": "Next Generation Search Systems",
                },
            ],
            "status": "ok",
            "message": "User Class Info",
        }
    print("User not found: loading default classes")

    return {
        "data": [
            {"className": "CS 125", "description": "Next Generation Search Systems"},
            {"className": "CS 161", "description": "Design and Analysis of Algorithms"},
            {"className": "CS 162", "description": "Formal Languages and Automata"},
        ],
        "status": "ok",
        "message": "Class info",
    }


@app.get("/api/allClasses")
async def all_classes():
    return {
        "data": [
            {"className": "CS 125", "description": "Next Generation Search Systems"},
            {"className": "CS 161", "description": "Design and Analysis of Algorithms"},
            {"className": "CS 162", "description": "Formal Languages and Automata"},
        ],
        "status": "ok",
        "message": "Class info",
    }


@app.get("/api/specializationInfo")
async def api_specialization_info():
    return {
        "data": [
            {"specialization": "AI", "description": "Artificial Intelligence"},
            {"specialization": "Algorithms", "description": "Algorithms"},
            {
                "specialization": "Formal Languages and Automata",
                "description": "Formal Languages and Automata",
            },
        ],
        "status": "ok",
        "message": "Specialization info",
    }


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
        print("User not found")
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/api/setUserInfo")
async def api_set_user_info(request: UserSetInfoRequest):
    print(request)
    return {
        "status": "ok",
        "message": "User info set successfully",
    }

@app.get("/api/getUserInfo")
async def api_get_user_info(userid: str = None):
    print(f"api_get_user_info called with userid: {userid}")
    if userid == "nathan":
        print("User Nathan: loading user info")
        return {
            "data": {
                "classes": [
                    {"className": "CS 161", "grade": "A-", "difficulty": 3},
                ],
                "skills": {"Math": 1, "Algorithms": 5, "Data Structures": 2, "Programming": 4, "Recursion": 3},
                "specialization": "Algorithms",
            },
            "status": "ok",
            "message": "User info",
        }
    return None

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 5001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
