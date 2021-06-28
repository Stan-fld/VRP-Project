from database import DBConnection as db
from generation.DataGeneration import DataGeneration


def store_data(data: DataGeneration):
    for collection in db.db_collections:
        item = data.toJSON(collection.name)
        collection.delete_many({})  # delete old data
        collection.insert_one(item)  # add new data
