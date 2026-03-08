import http.client
import json
import re
import urllib
import sys
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# Load environment variables
load_dotenv()

conn = http.client.HTTPSConnection("anteaterapi.com")

def fetch_course_grades(courses):
    """Fetches aggregate grade distribution for each course from AnteaterAPI and returns a dictionary mapping course IDs to grade data.
       Parameter is list of course documents from our courses collection, so IDs are already in the format COMPSCI161 or I&CSCI33.
       
       Returns a dictionary where keys are course IDs and values are the API 'data' list from /v2/rest/grades/aggregateByCourse."""
    course_grades = {}
    for course in courses:
        dept_code, course_number = extract_course_code(course["id"])
        if not dept_code or not course_number:
            raise Exception(f"Struggled to extract dept code and course number from: {course['id']}")

        query_dept = "I&C SCI" if dept_code == "I&CSCI" else dept_code
        encoded_dept = urllib.parse.quote_plus(query_dept)
        conn.request(
            "GET",
            f"/v2/rest/grades/aggregateByCourse?department={encoded_dept}&courseNumber={course_number}",
        )
        # print(f"/v2/rest/grades/aggregateByCourse?department={encoded_dept}&courseNumber={course_number}")
        res = conn.getresponse()
        data = res.read()
        response_data = json.loads(data.decode("utf-8"))
        if response_data.get("ok"):
            course_grades[course["id"]] = response_data.get("data", {})
        else:
            raise Exception(f"Failed to fetch grades for {course['id']}")
    return course_grades


def update_courses_with_data(mongo_uri=None):
    """
    Insert course grade data into the courses MongoDB collection.
    """
    if mongo_uri is None:
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            print("✗ MONGO_URI environment variable not set")
            sys.exit(1)
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ping')
        print(f"✓ Connected to MongoDB at {mongo_uri}")
        
    except (ConnectionFailure, ServerSelectionTimeoutError):
        print(f"✗ Failed to connect to MongoDB at {mongo_uri}")
        print("Make sure MongoDB is running and the URI is correct.")
        sys.exit(1)
    
    try:
        db = client["cs125"]
        collection = db["courses"]

        courses = list(collection.find({}))
        # Get the ID field from each course object (either I&CSCI or COMPSCI followed by 2-4 characters (e.g. I&CSCI33 or COMPSCI142A))
        # Go through this list of course IDs to feed into fetch_course_grades
        stripped_courses = [
            {
                "id": course["id"],
                "title": course["title"],
            }
            for course in courses
        ]
        grades = fetch_course_grades(stripped_courses)
        for courseID, gradeData in grades.items():
            gpa = get_aggregate_gpa(gradeData)
            # Update each course with a new averageGPA field
            collection.update_one({"id": courseID}, {"$set": {"averageGPA": gpa}})
            print(f"Course {courseID} has an average GPA of {gpa}")
            if gpa is None:
                print(f"Course {courseID} has an average GPA of {gpa}")

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    
    finally:
        client.close()
        print("✓ MongoDB connection closed")


def get_aggregate_gpa(grade_data: json) -> float:
    """Get the aggregate GPA from /v2/rest/grades/aggregateByCourse response data."""
    if not grade_data:
        return None
    return grade_data[0].get("averageGPA")


def extract_course_code(text):
    course_pattern = r'([A-Z& ]+)\s*(\d+[A-Z]?)'
    course_match = re.search(course_pattern, text)

    if course_match:
        dept = course_match.group(1).strip()  # remove trailing spaces
        num = course_match.group(2)
        return dept, num

    return None, None

if __name__ == "__main__":
    # Default connection
    update_courses_with_data()