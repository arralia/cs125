from main import db
import http.client
import json
import urllib

conn = http.client.HTTPSConnection("anteaterapi.com")


def clean_course_name(courses: list[str]) -> list[str]:
    for course in courses:
        course["id"] = course["id"].replace("I&C SCI", "ICS ").replace("COMPSCI", "CS ")
    return courses


def get_only_upper_divs(courses: list[dict]) -> list[dict]:
    """Return only courses whose IDs begin with COMPSCI."""
    return [
        course
        for course in courses
        if course["id"].startswith("COMPSCI")
    ]


class UserIneligibleForAllCSUpperDivsError(Exception):
    """Raised when a user is ineligible for all CS upper-division courses."""
    pass


def fetch_active_courses(year: str, season: str) -> set:
    """Gets the course offerings for the specified quarter through AnteaterAPI"""

    departments = ["COMPSCI", "I&C SCI"]
    all_courses = set()
    for dept in departments:
        encoded_dept = urllib.parse.quote(dept)
        conn.request(
            "GET",
            f"/v2/rest/websoc?year={year}&quarter={season}&department={encoded_dept}",
        )
        res = conn.getresponse()
        data = res.read()
        response_data = json.loads(data.decode("utf-8"))
        # Extract and combine courses from response_data as needed
        for school in response_data["data"]["schools"]:
            for department in school["departments"]:
                for course in department["courses"]:
                    course_id = (
                        course["deptCode"].replace(" ", "") + course["courseNumber"]
                    )
                    all_courses.add(course_id)
    print(
        f"Fetched {len(all_courses)} active courses in the I&SCI and COMPSCI deptsfrom AnteaterAPI for {season} {year}"
    )

    if not all_courses:
        # If list is empty, we parsed wrong or the API didn't fetch correctly
        raise Exception(
            f"Failed to fetch active courses for term {season} {year} from AnteaterAPI"
        )
    return all_courses


def fetch_five_most_recent_quarters() -> list[tuple[str, str]]:
    conn.request("GET", "/v2/rest/websoc/terms")
    res = conn.getresponse()
    data = res.read()
    response_data = json.loads(data.decode("utf-8"))
    recent_quarters = []
    if response_data.get("ok"):
        # The first five elements in the data field should be the five most recent quarters in chronological order, from my observations
        for i in range(5):
            most_recent_quarter = response_data.get("data")[i].get("shortName")
            recent_quarters.append(tuple(most_recent_quarter.split()))
            # tuple[0] is year (2026), and tuple[1] is season (Fall)
        return recent_quarters
    raise Exception("Failed to fetch most recent term information")


def narrow_down_courses(courses: list, user_info: dict, next_quarter_only: bool = True) -> tuple[set, set]:
    """This function will take the courses data from the database
    and return the courses that are relevant to the user's context.
    We never want to return NO courses here. Only case where that will
    happen is if the user is ineligible for every single CS upper div."""
    allCourseIds = set(course["id"] for course in courses)
    completedClasses = user_info.get("completedClasses", [])

    print("running narrow_down_courses")

    # Get the courses in courses param that user is eligible for, based on their completed classes
    eligibleCourses = get_eligible_courses(completedClasses, courses)
    if not eligibleCourses:
        # If user has no completed classes and they're ineligible for all CS upper divs...
        # TODO: Potentially up our game to suggest it some ICS classes that they should take to unlock upper divs
        raise Exception("User is ineligible for all CS upper div courses.")
    
    # Check the user's interests (mapped to keywords) and get the courses that are categorized under their interests.
    # Can be empty, in that case no courses to give any extra weight to which is fine
    interestedCourses = get_interested_courses(user_info.get("interests", []))
    print(f"interestedCourses: {interestedCourses}")
    if not interestedCourses:
        # If user has no selected interests, consider all courses as interested
        print("User has no selected interest tags.")
        interestedCourses = allCourseIds.copy()

    # Get the user's specialization courses: required for their spec or a list of options they need to choose from. 
    # Can be empty, in that case no courses to give any extra weight to which is fine
    requiredSpecCourses, optionsSpecCourses, neededNum = get_specialization_courses(
        user_info.get("specialization", ""), completedClasses
    )
    specializationCourses = requiredSpecCourses | optionsSpecCourses
    if not specializationCourses:
        specializationCourses = allCourseIds.copy()
    
    # added by gemini to remove completed classes that the user took, this part
    # bascially just formats the completed classes properly 
    completed = {
        c["className"].replace(" ", "") for c in user_info.get("completedClasses", [])
    }

    if next_quarter_only:
        activeCourses = fetch_active_courses()
        print(
            f"{len((interestedCourses & eligibleCourses) - activeCourses)} interested and eligible courses are not active for this quarter; {len((specializationCourses & eligibleCourses) - activeCourses)} specialization and eligible courses are not active for this quarter"
        )
        return (interestedCourses & eligibleCourses & activeCourses) - completed, (specializationCourses & eligibleCourses & activeCourses) - completed

    return (interestedCourses & eligibleCourses) - completed, (specializationCourses & eligibleCourses) - completed

def get_weighted_courses(courses: list, user_info: dict) -> list[dict]:
    """Returns a list of courses sorted by relevance to the user, where relevance is determined by:
       - Courses that are both in the user's interests and specialization get highest weight
       - Courses that are in the user's specialization but not interests get second highest weight
       - Courses that are in the user's interests but not specialization get third highest weight
       - All other courses get lowest weight
    """
    interested, specialization = narrow_down_courses(courses, user_info)
    # We want narrow_down_courses to only return interested courses if exist or specialization courses if exist
    weighted_courses = []
    for course in courses:
        course_id = course["id"]
        if course_id in interested and course_id in specialization:
            weight = 3
        elif course_id in specialization:
            weight = 2
        elif course_id in interested:
            weight = 1
        else:
            weight = 0
        weighted_courses.append((weight, course))
    
    # Sort by weight (descending) and then by course title (ascending)
    weighted_courses.sort(key=lambda x: (-x[0], x[1]["title"]))
    
    return [course for weight, course in weighted_courses]


def get_interested_courses(interests: list) -> set:
    """Return a set of course IDs related to the user's selected interest keywords."""
    # Extract courses that are in user's interests
    interestedCourses = set()
    if interests:
        for interest_dict in interests:
            # Safely extract the keyword string from the dict
            keyword_str = interest_dict.get("interests")
            if not keyword_str:
                continue

            # Query the db for that specific keyword document
            keyword_doc = db.get_collection("keywords").find_one(
                {"keyword": keyword_str}
            )
            if keyword_doc and "courses" in keyword_doc:
                for course in keyword_doc["courses"]:
                    interestedCourses.add(course.get("id"))
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
    else:
        # If user has no completed classes and they're ineligible for all CS upper
        # TODO: Potentially up our game to suggest it some ICS classes that they should take to unlock upper divs
        raise UserIneligibleForAllCSUpperDivsError(
            "User is ineligible for all CS upper div courses."
        )
    return eligibleCourses


def get_specialization_courses(specialization: str, completed: list) -> tuple[set,set,int]:
    """Return course IDs that can satisfy a user's specialization requirements.
       The first set in the tuple is utterly important required courses that take higher priority than the
       second set in the tuple, which is for their specialization but not strictly necessary.
    
    Uses specialization schema:
    - required_courses always count
    - elective_courses count only when neededNum > 0
    - if neededNum > 0 and elective_courses is empty, treat as unrestricted
      (e.g., General CS Track where essentially any upper-div course can count)
    """
    # If user does not have a specialization or is General CS, all upper divs count.
    # Return empty sets and rest of logic is handled by caller.
    if not specialization or specialization == "General CS Track":
        return set(), set(), 0

    specialization_doc = db.get_collection("specializations").find_one(
        {"specialization_name": specialization}
    )
    needed_num = specialization_doc.get("neededNum") # assuming this gets parsed as an integer correctly
    required_courses = specialization_doc.get("required_courses")
    elective_courses = specialization_doc.get("elective_courses")

    completed_ids = set()
    # Completed could be none if user has no completed classes, so we check before processing
    if completed:
        completed_ids.update({c["className"] for c in completed})

    # The required courses listed under this user's specialization that they haven't completed yet. These take high priority
    necessary_spec_courses = {
        course.get("code")
        for course in required_courses
        if course.get("code") not in completed_ids
    }

    choose_spec_courses = set()
    for course in {c.get("code") for c in elective_courses}:
        if course in completed_ids:
            # If user has already completed one of the elective courses in the select-n-of-list, decrement the needed_num
            needed_num -= 1
        else:
            # Otherwise, add it to the list of courses to rank/recommend
            choose_spec_courses.add(course)

    # Either of these two courses sets can be empty, but when they're not, weight them higher for ranking
    return (necessary_spec_courses, choose_spec_courses, needed_num)


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


# takes the class list given from the front end form, and
# and checks if they do not have like a name selected or if the name is empty
# then removes them
def clean_empty_classes(courses: list):
    new_courses = []
    for course in courses:
        if course.get("className") == "" or course.get("className") is None:
            continue
        new_courses.append(course)
    return new_courses


def clean_empty_interests(interests: list):
    new_interests = []
    print("interests: ", interests)
    for interest in interests:
        if interest.get("interests") == "" or interest.get("interests") is None:
            continue
        new_interests.append(interest)
    return new_interests
