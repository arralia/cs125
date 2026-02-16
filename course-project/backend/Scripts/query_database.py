import pymongo
import certifi

load_dotenv()

if __name__ == "__main__":
    
    client = pymongo.MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client["cs125"]
    print(db)
    print(db.list_collection_names())

    users = db.users.find()
    for user in users:
        print(user)


