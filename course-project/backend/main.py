import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
from database import Database
import gemini
import util

TESTING = False

# Load environment variables from .env
load_dotenv()

gemini = gemini.Gemini()

if not TESTING:
    db = Database()
else:
    db = None

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
    interests: list[dict[str, str]] | None = None
    specialization: str
    username: str | None = None
    quartersLeft: int | None = None


class Username(BaseModel):
    username: str


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Backend!"}


"""

This section is for the class information

"""


@app.get("/api/allClassesData")
async def all_classes():
    """
    Returns all the classes in the database
    """

    try:
        if TESTING:
            return {
                "data": [
                    {
                        "id": "CS 125",
                        "title": "search systems",
                        "description": "Another class yea",
                        "prerequisites": [],
                        "corequisites": [],
                        "antirequisites": [],
                        "units": 4,
                        "quarter": "Fall",
                    },
                    {
                        "id": "CS 161",
                        "title": "Algorithms",
                        "description": "Some class yea",
                        "prerequisites": [],
                        "corequisites": [],
                        "antirequisites": [],
                        "units": 4,
                        "quarter": "Fall",
                    },
                ],
                "message": "prefilled temp data",
            }
        print("Received /api/allClassesData: Fetching all classes...")
        courses = list(db.get_collection("courses").find())

        util.stringify_ids(courses)

        print(f"Successfully fetched {len(courses)} classes")
        return {"data": courses}

    except Exception as e:
        print(f"Error fetching all classes: {e}")
        return {"data": [], "status": "error", "message": "Failed to fetch all classes"}


@app.get("/api/courseInfo")
async def api_course_info(courseid: str = None):
    """
    Returns the course information for a given course id
    """

    try:
        print(f"Received /api/courseInfo with courseid: {courseid}")
        course = db.get_collection("courses").find_one({"id": courseid})
        if course:
            course["_id"] = str(course["_id"])
            return {"data": course, "status": "ok", "message": "Course info"}
        else:
            return {"data": None, "status": "error", "message": "Course not found"}
    except Exception as e:
        print(f"Error fetching course info: {e}")
        return {
            "data": None,
            "status": "error",
            "message": "Failed to fetch course info",
        }


@app.get("/api/recommendedClasses")
async def api_recommended_classes(username: str):
    """
    Returns the recommended classes for a given user
    """

    # return {"data": [], "status": "ok", "message": "Recommended classes"}

    try:
        print("Received /api/recommendedClasses: Fetching recommended classes...")
        courses = list(db.get_collection("courses").find())
        print(f"Successfully fetched {len(courses)} classes")
        print("courses: ", courses)

        print(f"Received /api/recommendedClasses with username: {username}")
        user_info = db.get_collection("users").find_one({"username": username})

        if user_info:
            print("user_info: ", user_info)
            courses = util.narrow_down_courses(courses, user_info)
            recommended_classes = gemini.recommend_class(user_info, courses, None)
            print(f"Gemini output: {recommended_classes}")
            return {
                "data": recommended_classes,
                "status": "ok",
                "message": "Recommended classes",
            }
        else:
            return {
                "data": None,
                "status": "error",
                "message": "User not found",
            }

    except Exception as e:
        print(f"Error fetching recommended classes: {e}")
        return {
            "data": None,
            "status": "error",
            "message": "Failed to fetch recommended classes",
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


@app.get("/api/interestsList")
async def api_interests_list():

    keywords = list(db.get_collection("keywords").find())

    stringify_ids(keywords)

    return {
        "data": keywords,
        "status": "ok",
        "message": "Interests list",
    }


@app.post("/api/login")
async def api_login(request: LoginRequest):

    username = request.username

    try:
        print(f"Received /api/login with username: {username}")
        # Find user, exclude _id for clean JSON response
        user_info = db.get_collection("users").find_one(
            {"username": username}, {"_id": 0}
        )

        if user_info:
            print("user_info found: ", user_info)
            return {
                "data": user_info,
                "status": "ok",
                "message": "User info",
            }
        else:
            print(f"User {username} not found, creating new user.")
            new_user = {
                "username": username,
                "completedClasses": [],
                "interests": [],
                "specialization": "",
                "quartersLeft": 4,
            }
            # Insert the new user
            db.get_collection("users").insert_one(new_user)

            # Remove _id which insert_one adds, so we can return clean JSON
            if "_id" in new_user:
                del new_user["_id"]

            return {
                "data": new_user,
                "status": "ok",
                "message": "New user created",
            }
    except Exception as e:
        print(f"Error processing login: {e}")
        return {
            "data": None,
            "status": "error",
            "message": "Failed to process login",
        }


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
async def api_get_user_info(username: str = None):
    print(f"api_get_user_info called with username: {username}")

    if not username:
        return None

    user_collection = db.get_collection("users")
    user = user_collection.find_one({"username": username}, {"_id": 0})

    if user:
        print(f"User {username}: loading user info from DB")
        return {
            "data": user,
            "status": "ok",
            "message": "User info",
        }

    # Fallback/Default for new users
    return {
        "data": {
            "username": username,
            "completedClasses": [],
            "interests": [],
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