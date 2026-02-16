# boilerplate code from gemini

import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        db_name = "cs125"

        try:
            print(f"Trying to connect to MongoDB at {mongo_uri}")
            # On macOS, Python often fails to verify SSL certificates for MongoDB Atlas.
            # tlsCAFile=certifi.where() tells the client to use the root certificates
            # provided by the certifi package to safely verify the connection.
            self.client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
            self.db = self.client[db_name]
            # Send a ping to confirm a successful connection
            self.client.admin.command("ping")
            print(f"Successfully connected to MongoDB at {mongo_uri}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise e

    def get_collection(self, name):
        if self.db is None:
            self.connect()
        return self.db[name]

    def update_username(self, userid, user_info):
        if self.db is None:
            print("Error: Not connected to database")
            return
        self.db.users.update_one({"userid": userid}, {"$set": user_info}, upsert=True)

    def update_user_info(self, userid, user_info):
        self.db.users.update_one({"userid": userid}, {"$set": user_info}, upsert=True)


if __name__ == "__main__":
    db = Database()
    db.connect()
    print(list(db.get_collection("courses").find()))
