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
    item_to_deliver = {}

    def __init__(self, predefined_neighbors, id):
        self.available_time_slot = [random.randint(2, 9), random.randint(13, 23)]
        self.id = id
        self.neighbors = predefined_neighbors
        self.kind = 0
        self.item_to_deliver = {"kind": random.randint(0, 3), "qtt": random.randint(1, 5)}

    def set_warehouse(self):
        self.kind = 1

    def toJSON(self):
        """
        serialize the object in json
        """
        return {"id": self.id, "available_time_slot": self.available_time_slot, "predefined_neighbors": self.predefined_neighbors, "kind": self.kind, "item_to_deliver": self.item_to_deliver}

    def __str__(self):
        if self.kind == 0:
            return f"Sommet {self.id} de type Adresse, items : {self.item_to_deliver.get('qtt')} d'objet n°{self.item_to_deliver.get('kind')}"
        else:
            return f"Sommet {self.id} de type DEPOT ⌂⌂⌂⌂⌂"

    def str_as_stopover(self):
        return f"Sommet {self.id} intermédiaire"
