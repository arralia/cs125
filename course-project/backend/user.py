
import util


class User:
    def __init__(self, database, username):
        self.db = database
        self.username = username

    def get_user_info(self):
        return self.db.get_collection("users").find_one({"username": self.username})

    def get_completed_classes(self):
        return self.db.get_collection("users").find_one({"username": self.username})["completedClasses"]

    def get_interests(self):
        return self.db.get_collection("users").find_one({"username": self.username})["interests"]

    def get_specialization(self):
        return self.db.get_collection("users").find_one({"username": self.username})["specialization"]

    def get_quarters_left(self):
        return self.db.get_collection("users").find_one({"username": self.username})["quartersLeft"]

    def update_user_info(self, user_info):
        self.db.get_collection("users").update_one({"username": self.username}, {"$set": user_info})

    def retrieve_recommended_classes(self, quater : str) -> dict:
        """
        Retrieves the recommended classes for the user for the given quarter
        """
        
        courses = util.fetch_active_courses()
        filtered_courses = util.narrow_down_courses(courses, self.get_user_info())        
        return filtered_courses
    