import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# Thresholds from project decision
HARD_MAX = 3.2
MEDIUM_MAX = 3.6


def classify_difficulty(average_gpa: float) -> str:
    if average_gpa < HARD_MAX:
        return "Hard"
    if average_gpa < MEDIUM_MAX:
        return "Medium"
    return "Easy"


def update_courses_with_difficulty(mongo_uri: str = None):
    load_dotenv()

    if mongo_uri is None:
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            print("✗ MONGO_URI environment variable not set")
            sys.exit(1)

    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        print(f"✓ Connected to MongoDB at {mongo_uri}")
    except (ConnectionFailure, ServerSelectionTimeoutError):
        print(f"✗ Failed to connect to MongoDB at {mongo_uri}")
        print("Make sure MongoDB is running and the URI is correct.")
        sys.exit(1)

    updated_count = 0
    skipped_count = 0

    try:
        db = client["cs125"]
        collection = db["courses"]

        courses = collection.find({}, {"id": 1, "averageGPA": 1})
        for course in courses:
            course_id = course.get("id", "<unknown>")
            average_gpa = course.get("averageGPA")

            if average_gpa is None:
                skipped_count += 1
                print(f"Skipped {course_id}: averageGPA is None")
                continue

            difficulty = classify_difficulty(average_gpa)
            # collection.update_one(
            #     {"_id": course["_id"]},
            #     {"$set": {"difficulty": difficulty}},
            # )
            updated_count += 1
            print(
                f"Updated {course_id}: averageGPA={average_gpa} -> difficulty={difficulty}"
            )

        print(
            f"✓ Done. Updated {updated_count} courses. Skipped {skipped_count} courses with missing averageGPA."
        )

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    finally:
        client.close()
        print("✓ MongoDB connection closed")


if __name__ == "__main__":
    update_courses_with_difficulty()
