import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
from passlib.context import CryptContext
from database import Database
import gemini
import util
from user import User

# Workaround for SSL certificate verification issues on macOS
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

TESTING = False

# Load environment variables from .env
load_dotenv()

gemini = gemini.Gemini()

db = Database()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

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
    password: str


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
async def api_recommended_classes(username: str | None = None):
    """
    Returns the recommended classes for a given user
    """

    # return {"data": [], "status": "ok", "message": "Recommended classes"}

    try:
        print("Received /api/recommendedClasses: Fetching recommended classes...")
        courses = list(db.get_collection("courses").find())
        print(f"Successfully fetched {len(courses)} classes")

        print(f"Received /api/recommendedClasses with username: {username}")
        user_info = db.get_collection("users").find_one({"username": username})
        print("user_info: ", user_info)
        if user_info:
            # Sets of course IDs returned. Likely need to enrich them before passing into gemini (like difficulty)
            courses, specialization_courses = util.narrow_down_courses(
                courses, user_info
            )
            recommended_classes = gemini.recommend_class(
                user_info, courses, specialization_courses
            )
            print(f"Gemini output: {recommended_classes}")
            return {
                "data": recommended_classes,
                "status": "ok",
                "message": "Recommended classes",
            }
        else:
            active_course_ids = util.fetch_active_courses()
            active_courses = [
                {"id": course["id"], "title": course["title"]}
                for course in courses
                if course["id"] in active_course_ids
            ]
            return {
                "data": active_courses,
                "status": "error",
                "message": "User not found, recommending all active courses instead",
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

    specializations = list(db.get_collection("specializations").find())
    util.stringify_ids(specializations)

    return {
        "data": specializations,
        "status": "ok",
        "message": "Specialization info",
    }


@app.get("/api/interestsList")
async def api_interests_list():

    keywords = list(db.get_collection("keywords").find())
    util.stringify_ids(keywords)
    print("Number of keywords: ", len(keywords))

    return {
        "data": keywords,
        "status": "ok",
        "message": "Interests list",
    }


@app.post("/api/login")
async def api_login(request: LoginRequest):

    username = request.username
    password = request.password

    try:
        print(f"Received /api/login with username: {username}")
        # Find user, exclude _id for clean JSON response
        user_info = db.get_collection("users").find_one({"username": username})

        if user_info:
            print("user_info found: ", user_info)
            # Verify password
            stored_password = user_info.get("password")
            if stored_password and pwd_context.verify(password, stored_password):
                # Remove password from response and stringify _id
                if "_id" in user_info:
                    user_info["_id"] = str(user_info["_id"])
                if "password" in user_info:
                    del user_info["password"]

                return {
                    "data": user_info,
                    "status": "ok",
                    "message": "Login successful",
                }
            else:
                return {
                    "data": None,
                    "status": "error",
                    "message": "Invalid password or username",
                }
        else:
            return {
                "data": None,
                "status": "error",
                "message": "Invalid password or username",
            }

    except Exception as e:
        print(f"Error processing login: {e}")
        return {
            "data": None,
            "status": "error",
            "message": "Failed to process login",
        }


@app.post("/api/register")
async def api_register(request: LoginRequest):
    username = request.username
    password = request.password

    try:
        print(f"Received /api/register with username: {username}")
        # Check if user already exists
        existing_user = db.get_collection("users").find_one({"username": username})

        if existing_user:
            return {
                "data": None,
                "status": "error",
                "message": "Username already exists",
            }

        # Hash the password
        hashed_password = pwd_context.hash(password)

        new_user = {
            "username": username,
            "password": hashed_password,
            "completedClasses": [],
            "interests": [],
            "specialization": "",
            "quartersLeft": 4,
        }

        # Insert the new user
        db.get_collection("users").insert_one(new_user)

        # Prepare user info for response (exclude password and _id)
        if "_id" in new_user:
            del new_user["_id"]
        if "password" in new_user:
            del new_user["password"]

        return {
            "data": new_user,
            "status": "ok",
            "message": "User registered successfully",
        }
    except Exception as e:
        print(f"Error processing registration: {e}")
        return {
            "data": None,
            "status": "error",
            "message": "Failed to register user",
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
