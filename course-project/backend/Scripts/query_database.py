import pymongo
import certifi

if __name__ == "__main__":
    
    client = pymongo.MongoClient("mongodb+srv://dev_db_user:upperdivrecommender@cs125.qalr6fc.mongodb.net/", tlsCAFile=certifi.where())
    db = client["cs125"]
    print(db)
    print(db.list_collection_names())

    users = db.users.find()
    for user in users:
        print(user)


