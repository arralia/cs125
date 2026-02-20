
from main import db
import http.client
import json
import urllib
import re

conn = http.client.HTTPSConnection("anteaterapi.com")

def fetch_active_courses() -> set:
    """Gets the course offerings for the most recently released WebSOC quarter through AnteaterAPI"""

    year, season = fetch_most_recent_quarter()
    departments = ["COMPSCI", "I&C SCI"]
    all_courses = set()
    for dept in departments:
        encoded_dept = urllib.parse.quote(dept)
        conn.request("GET", f"/v2/rest/websoc?year={year}&quarter={season}&department={encoded_dept}")
        res = conn.getresponse()
        data = res.read()
        response_data = json.loads(data.decode("utf-8"))
        # Extract and combine courses from response_data as needed
        for school in response_data["data"]["schools"]:
            for department in school["departments"]:
                for course in department["courses"]:
                    course_id = course["deptCode"].replace(" ", "") + course["courseNumber"] 
                    all_courses.add(course_id)
    print(f"Fetched {len(all_courses)} active courses in the I&SCI and COMPSCI deptsfrom AnteaterAPI for {season} {year}")
    
    if not all_courses:
        # If list is empty, we parsed wrong or the API didn't fetch correctly
        raise Exception(f"Failed to fetch active courses for term {season} {year} from AnteaterAPI")
    return all_courses
    
def fetch_most_recent_quarter() -> list[str]:
    conn.request("GET", "/v2/rest/websoc/terms")
    res = conn.getresponse()
    data = res.read()
    response_data = json.loads(data.decode("utf-8"))
    if response_data.get("ok"):
        # The first element in the data field should be the most recent quarter, from my observations
        most_recent_quarter = response_data.get("data")[0].get("shortName")
        quarter_info = most_recent_quarter.split()
        return quarter_info
    raise Exception("Failed to fetch most recent term information")

def narrow_down_courses(courses: list, user_info: dict) -> list:
    """ This function will take the courses data from the database 
        and return the courses that are relevant to the user's context.
        We never want to return NO courses here. Only case where that will 
        happen is if the user is ineligible for every single CS upper div."""
    allCourseIds = set(course["id"] for course in courses)

    # Check the user's interests (mapped to keywords) and get the courses that are categorized under their interests
    interestedCourses = get_interested_courses(user_info.get("interests"))
    if not interestedCourses:
        # If user has no selected interests, consider all courses as interested
        print("User has no selected interest tags.")
        interestedCourses = allCourseIds.copy()

    # Check the prerequisiteTrees of the courses to make sure that this user has completed it
    eligibleCourses = get_eligible_courses(user_info.get("completedClasses"), courses)
    if not eligibleCourses:
        # If user has no completed classes and they're ineligible for all CS upper 
        # TODO: Potentially up our game to suggest it some ICS classes that they should take to unlock upper divs
        raise Exception("User is ineligible for all CS upper div courses.")

    # Get the user's specialization courses
    specializationCourses = get_specialization_courses(user_info.get("specialization"))
    if not specializationCourses:
        # If user has no specialization, consider all courses as specialization courses
        print("User has no specialization courses.")
        specializationCourses = allCourseIds.copy()

    # return [
    #     {
    #         "id": course["id"],
    #         "title": course["title"],
    #     }
    #     for course in ( (interestedCourses & eligibleCourses) | (specializationCourses & eligibleCourses) )
    # ]

    activeCourses = fetch_active_courses()
    print(f'{len((interestedCourses&eligibleCourses) - activeCourses)} interested and eligible courses are not active for this quarter; {len((specializationCourses&eligibleCourses) - activeCourses)} specialization and eligible courses are not active for this quarter')
    
    return (interestedCourses & eligibleCourses & activeCourses),(specializationCourses & eligibleCourses & activeCourses) 

def get_interested_courses(interests: list) -> set:
    """Return a set of course IDs related to the user's selected interest keywords."""
    # Extract courses that are in user's interests
    interestedCourses = set()
    if interests:
        # the keywords collection in our database
        keywords = db.get_collection("keywords").find_one()
        for keyword in interests:
            keyword_courses = [k for k in keywords["keywords"] if k["keyword"] == keyword]
            for course in keyword_courses[0]["courses"]:
                interestedCourses.add(course["id"])
    return interestedCourses

def get_eligible_courses(completed: list, courses: list) -> set:
    """Return a set of course IDs that the user is eligible for based on their stored completedClasses list."""
    eligibleCourses = set()
    if completed:
        # might be unnecessary space removal but just in case
        completed = {c["className"].replace(" ", "") for c in completed}
        for course in courses:
            # If the user has completed all prerequisites in this course
            tree = course.get("prerequisiteTree", {})
            if satisfies_prereqs(tree, completed):
                eligibleCourses.add(course["id"])
    return eligibleCourses

def get_specialization_courses(specialization: str) -> set:
    """Return the course IDs that count towards a user's spec. Can return empty set if user has no spec."""
    specializationCourses = set()
    if specialization:
        specialization_doc = db.get_collection("specializations").find_one({"specialization_name": specialization})
        if specialization_doc:
            # TODO: will likely need to subtract any courses they've already taken which decreases the required number of
            # elective_courses we suggest. Maybe add it anyways? Definitely add more weight to the required_courses
            # in their specialization, and secondary ranking to electice courses.
            # Link to issue: https://github.com/users/arralia/projects/2/views/1?pane=issue&itemId=158633000&issue=arralia%7Ccs125%7C22

            # Add all required courses
            for course in specialization_doc.get("required_courses", []):
                specializationCourses.add(course["code"])
            # Add all elective courses (user can choose from any of these)
            for course in specialization_doc.get("elective_courses", []):
                specializationCourses.add(course["code"])
    return specializationCourses

def satisfies_prereqs(tree: dict, completed: set) -> bool:
    if not tree:
        return True  # no prereqs

    if "courseId" in tree:
        return tree["courseId"] in completed

    if "AND" in tree:
        return all(satisfies_prereqs(t, completed) for t in tree["AND"])

    if "OR" in tree:
        return any(satisfies_prereqs(t, completed) for t in tree["OR"])

    return True

# Modifies the list directly
def stringify_ids(courses: list):
    for course in courses:
            course["_id"] = str(course["_id"])