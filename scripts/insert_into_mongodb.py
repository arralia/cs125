import json
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

def insert_ics_courses_to_mongodb(mongo_uri="mongodb+srv://dev_db_user:upperdivrecommender@cs125.qalr6fc.mongodb.net/", db_name="cs125", collection_name="keywords"):
    """
    Insert json data into MongoDB.
    
    Args:
        mongo_uri: MongoDB connection string (default: MongoDB Atlas)
        db_name: Database name (default: cs125)
        collection_name: Collection name (default: courses)
    """
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ping')
        print(f"✓ Connected to MongoDB at {mongo_uri}")
        
    except (ConnectionFailure, ServerSelectionTimeoutError):
        print(f"✗ Failed to connect to MongoDB at {mongo_uri}")
        print("Make sure MongoDB is running and the URI is correct.")
        sys.exit(1)
    
    try:
        # Get database and collection
        db = client[db_name]
        collection = db[collection_name]
        
        # Load CS Upper Div Courses data
        with open('../data/Keywords.json', 'r') as f:
            data = json.load(f)
        
        courses = data.get("keywords", [])
        
        if not courses:
            print("✗ No courses found in Keywords.json")
            sys.exit(1)
        
        print(f"Loaded {len(courses)} courses from Keywords.json")

        result = collection.insert_many(courses)
        print(f"✓ Inserted {len(result.inserted_ids)} courses into {db_name}.{collection_name}")
        
        # Print sample inserted course
        if result.inserted_ids:
            sample = collection.find_one({"_id": result.inserted_ids[0]})
            print(f"\nSample inserted course:")
            print(f"  ID: {sample.get('id')}")
            print(f"  Title: {sample.get('title')}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    
    finally:
        client.close()
        print("✓ MongoDB connection closed")

if __name__ == "__main__":
    # Default connection
    insert_ics_courses_to_mongodb()
    
    # To use custom MongoDB URI, uncomment and modify:
    # insert_ics_courses_to_mongodb(mongo_uri="mongodb://username:password@host:port")
