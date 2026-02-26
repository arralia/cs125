# test_util.py
import sys
sys.path.append('.')
from util import fetch_active_courses, narrow_down_courses

def test_fetch_active_courses():
    result = fetch_active_courses()
    print("Result:", result)

def test_narrow_down_courses():
    # Mock course data
    courses = [
        {"id": "COMPSCI161", "prerequisiteTree": {}, "title": "Design and Analysis of Algorithms"},
        {"id": "ICS139W", "prerequisiteTree": {}, "title": "Critical Writing on Information Technology"},
        {"id": "I&C SCI46", "prerequisiteTree": {}, "title": "Data Structure Implementation and Analysis"}
    ]
    # Mock user info
    user_info = {
        "interests": ["Algorithms"],
        "completedClasses": [{"className": "COMPSCI161"}],
        "specialization": None
    }
    try:
        interested, specialization = narrow_down_courses(courses, user_info)
        print("Interested & Eligible:", interested)
        print("Specialization & Eligible:", specialization)
    except Exception as e:
        print("Exception:", e)

if __name__ == "__main__":
    test_fetch_active_courses()
    test_narrow_down_courses()
