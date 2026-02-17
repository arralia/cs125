
def extract_course_info(courses: list, user_info: dict) -> list:
    """This function will take the courses data from the database 
    and just return a new json that only has the course ID and 
    title of courses that are relevant to the user's context"""

    interestedCourses = get_interested_courses(user_info.get("interests"), courses)

    # Check the prerequisiteTrees of the courses to make sure that this user has completed it
    eligibleCourses = get_eligible_courses(user_info.get("completedClasses"), courses)


    # Get the user's specialization courses. Can be empty set.
    specializationCourses = get_specialization_courses(user_info.get("specialization"), courses)


    return [
        {
            "id": course["id"],
            "title": course["title"],
        }
        for course in ( (interestedCourses & eligibleCourses) | (specializationCourses & eligibleCourses) )
    ]

def get_interested_courses(interests: list, courses: list) -> set:
    """This function will return a set of course IDs that the user is interested in. Can return empty set."""
    # Extract courses that are in user's interests
    interestedCourses = set()
    # Dictionary storing keywords in our db
    # keywords = json.loads(TODO extract keywords from api/interestsList())

    for keyword in user_info["interests"]:
        keyword_courses = [k for k in keywords["keywords"] if k["keyword"] == keyword]
        for course in keyword_courses[0]["courses"]:
            interestedCourses.add(course["id"])

    return interestedCourses

def get_eligible_courses(completed: list, courses: list) -> set:
    # Check the prerequisiteTrees of the courses to make sure that this user has completed it
    eligibleCourses = set()
    # might be unnecessary space removal but just in case
    completed = {c["className"].replace(" ", "") for c in completed}

    for course in courses:
         # If the user has completed all prerequisites in this course
        tree = course.get("prerequisiteTree", {})
        if satisfies_prereqs(tree, completed):
            eligibleCourses.add(course["id"])
    return eligibleCourses

def get_specialization_courses(specialization: str, courses: list) -> set:
    """This function will return a set of course IDs that are relevant to the user's specialization. Can return empty set."""
    specializationCourses = set()
    if specialization:
        # TODO: get api call to specializations collection to get the list of courses for this specialization
        specialCourses = [c for c in specializations if c["specialization_name"] == user_info.get("specialization")]
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

