import random
import uuid


class Summit:
    id = 0
    # Time slot where the client is available
    available_time_slot = []
    # predefined neighbors (normal distribution)
    predefined_neighbors = []
    # address = 0
    # warehouse = 1
    kind = 0
    item_to_deliver = [] # Todo add generation here

    def __init__(self, predefined_neighbors):
        self.available_time_slot = [random.randint(2, 9), random.randint(13, 23)]
        self.id = str(uuid.uuid4())[:8]
        self.neighbors = predefined_neighbors
        self.kind = 0

    def set_kind(self, kind):
        self.kind = kind

    def toJSON(self):
        """
        serialize the object in json
        """
        return {"id": self.id, "available_time_slot": self.available_time_slot, "predefined_neighbors": self.predefined_neighbors, "kind": self.kind, "item_to_deliver": self.item_to_deliver}

    def __str__(self):
        return f"Sommet {self.id} de type {self.kind}, plage horaire : {self.available_time_slot[0]}h à {self.available_time_slot[1]}h"
