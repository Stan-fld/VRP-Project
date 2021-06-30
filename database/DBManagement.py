import numpy as np
from bson import json_util
from database import DBConnection as db
from generation.DataGeneration import DataGeneration
from generation.Segment import Segment
from generation.Summit import Summit
from generation.Vehicle import Vehicle

name = 'data_project'


def store_data(data: DataGeneration):
    # Delete data from Gridfs collections
    for collection in db.fs_collections:
        collection.delete_many({})

    # Explicit BSON conversion from JSON.
    json_str = json_util.dumps(data.toJSON())

    # Store new data with Gridfs
    db.fs.put(json_str, encoding='utf-8', filename=name)


def get_stat_from_mongo():
    # print(db.stat_colletion.count())
    return db.stat_colletion.find()


def get_number_of_stored_stat():
    return db.stat_colletion.count()


def store_stat_to_mongo(stat):
    db.stat_colletion.insert_one(stat)


def get_data_generation() -> DataGeneration:
    # Get last data generated
    data_generation = db.fs.get_last_version(name).read()

    # Explicit BSON to JSON conversion.
    json_object = json_util.loads(data_generation)

    # Create an object DataGeneration
    data = DataGeneration(number_of_summit=100, number_of_vehicle=10, max_neighbor=5, number_of_kind_of_item=4,
                          progressbar=False)
    for k, v in json_object.items():
        if k == 'warehouse':
            data.warehouse = v
        elif k == 'data_matrix':
            data.data_matrix = np.array(v)
        elif k == 'data_segment':
            # Convert data segment JSON to object Segment
            data.data_segment = (
                [[Segment(origin=x['origin'], destination=x['destination']) if x != 'null' else None for x in z] for z
                 in v])
        elif k == 'data_vehicles':
            # Convert data segment JSON to object Vehicle
            data.data_vehicles = [Vehicle(kind=x['kind']) for x in v]
        elif k == 'data_summit':
            # Convert data segment JSON to object Summit
            data.data_summit = [Summit(id=x['id']) for x in v]
        else:
            print('Error in data transformation')
    return data
