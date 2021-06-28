from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://Admin:admin@cluster0.xgnbt.mongodb.net/DBProject?retryWrites=true&w=majority")
db = cluster["DBProject"]

db_collections = [db["warehouse"], db["matrix"], db["segment"], db["vehicles"], db["summit"]]
