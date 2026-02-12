def extract_course_info(courses: list):
    """This function will take the courses data from the database 
    and just return a new json that only has the course ID and 
    title"""
    return [
        {
            "id": course["id"],
            "className": course["className"],
            "description": course["description"],
        }
        for course in courses
    ]
