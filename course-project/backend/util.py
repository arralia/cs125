
from main import db

def narrow_down_courses(courses: list, user_info: dict) -> list:
    """This function will take the courses data from the database 
    and just return the courses that are relevant to the user's context"""
    allCourseIds = set(course["id"] for course in courses)

    # Check the user's interests (mapped to keywords) and get the courses that are categorized under their interests
    interestedCourses = get_interested_courses(user_info.get("interests"))
    if not interestedCourses:
        # If user has no selected interests, consider all courses as interested
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
        specializationCourses = allCourseIds.copy()

    # return [
    #     {
    #         "id": course["id"],
    #         "title": course["title"],
    #     }
    #     for course in ( (interestedCourses & eligibleCourses) | (specializationCourses & eligibleCourses) )
    # ]

    # Return the courses that they're eligible for and interested in combined with the courses that they're eligible for and count towards their specialization
    return (interestedCourses & eligibleCourses),(specializationCourses & eligibleCourses) 

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
        db.get_collection("specializations").find_one({"specialization_name": specialization})
        specializations = list(db.get_collection("specializations").find())
        specialCourses = [c for c in specializations if c["specialization_name"] == specialization]
        specialCourses = specialCourses[0]["courses"] if specialCourses else []
        for course in specialCourses:
             specializationCourses.add(course["id"])
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