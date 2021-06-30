import certifi
import gridfs
from pymongo import MongoClient


def mongo_con():
    try:
        cluster = MongoClient(
            'mongodb+srv://Admin:admin@cluster0.xgnbt.mongodb.net/DBProject?retryWrites=true&w=majority', tlsCAFile=certifi.where())
        return cluster
    except Exception as e:
        print('Error in mongo connection:*', e)


db = mongo_con()['DBProject']
fs = gridfs.GridFS(db)
fs_collections = [db['fs.chunks'], db['fs.files']]
stat_colletion = db['stats']

#db_collections = [db['warehouse'], db['matrix'], db['segment'], db['vehicles'], db['summit']]
