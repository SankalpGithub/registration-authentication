import pymongo

def con():
    try:
        myclient = pymongo.MongoClient("mongodb+srv://sankalp2004gaikwad:sankalpMongodb%402004gaikwad@cluster0.rhfrqdl.mongodb.net/")
        print("MongoDB connected successfully")
        return myclient["attendence"]
    except:
        print("Error Connecting Database")