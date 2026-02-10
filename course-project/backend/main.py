# added a bloilerpalte fastapi server as a starting point created with gemini ai

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
from database import Database

# Load environment variables from .env
load_dotenv()


db = Database()

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
    completedClasses: list[dict[str, str | int]]
    strengths: dict[str, int]
    specialization: str
    username: str | None = None
    quartersLeft: int | None = None


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
    print(f"Saving info for user: {request.username}")

    user_collection = db.get_collection("users")

    # Upsert: Update if exists, insert if not
    user_data = request.model_dump()
    user_collection.update_one(
        {"username": request.username}, {"$set": user_data}, upsert=True
    )

    return {
        "status": "ok",
        "message": "User info set successfully",
    }


@app.get("/api/getUserInfo")
async def api_get_user_info(userid: str = None):
    print(f"api_get_user_info called with userid: {userid}")

    if not userid:
        return None

    user_collection = db.get_collection("users")
    user = user_collection.find_one({"username": userid}, {"_id": 0})

    if user:
        print(f"User {userid}: loading user info from DB")
        return {
            "data": user,
            "status": "ok",
            "message": "User info",
        }

    # Fallback/Default for new users
    return {
        "data": {
            "username": userid,
            "completedClasses": [],
            "strengths": {
                "Math": 3,
                "Algorithms": 3,
                "Data Structures": 3,
                "Programming": 3,
                "Recursion": 3,
            },
            "specialization": "",
            "quartersLeft": 4,
        },
        "status": "ok",
        "message": "Default user info",
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 5001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
