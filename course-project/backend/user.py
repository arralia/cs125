import util


class User:
    def __init__(self, database, username):
        self.db = database
        self.username = username
        self.data = None
        self.user_filters = {}

    def load(self):
        """Fetch user data from the database and cache it."""
        self.data = self.db.get_collection("users").find_one(
            {"username": self.username}
        )
        return self.data

    def set_user_filters(self, user_filters):
        self.user_filters = user_filters

    def get_user_filters(self):
        return self.user_filters

    def refresh(self):
        """Force a refresh of the cached user data."""
        return self.load()

    def get_user_info(self):
        """Returns the cached user data, loading it if necessary."""
        if self.data is None:
            self.load()
        return self.data

    def get_completed_classes(self):
        info = self.get_user_info()
        return info.get("completedClasses", []) if info else []

    def get_interests(self):
        info = self.get_user_info()
        return info.get("interests", []) if info else []

    def get_specialization(self):
        info = self.get_user_info()
        return info.get("specialization", "") if info else ""

    def get_quarters_left(self):
        info = self.get_user_info()
        return info.get("quartersLeft", 0) if info else 0

    def update_user_info(self, user_info):
        """Update user info in DB and sync local cache."""
        try:
            self.db.get_collection("users").update_one(
                {"username": self.username}, {"$set": user_info}, upsert=True
            )
            # Update local cache
            if self.data is None:
                self.load()
            if self.data:
                self.data.update(user_info)
            return True
        except Exception as e:
            print(f"Error updating user info: {e}")
            return False

    def retrieve_recommended_classes(self, quarter: str = None) -> list:
        """
        Retrieves the recommended classes for the user for the given quarter
        """
        # Fetching all courses to pass to narrow_down_courses
        # Note: In a larger app, you'd probably want to cache this list as well
        courses = list(self.db.get_collection("courses").find())
        return util.narrow_down_courses(courses, self.get_user_info())
