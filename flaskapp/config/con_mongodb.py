import pymongo
import os
def con():
    try:
        connection = os.getenv('MONGO_CONNECTION_STRING')
        myclient = pymongo.MongoClient(connection)
        print("MongoDB connected successfully")
        return myclient["register-authenticate"]
    except:
        print("Error Connecting Database")