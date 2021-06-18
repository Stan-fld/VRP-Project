import random
import uuid


class Summit:
    id = 0
    # Time slot where the client is available
    available_time_slot = []
    # predefined neighbors (normal distribution)
    predefined_neighbors = 0
    # address = 0
    # warehouse = 1
    kind = 0
    item_to_deliver = [] # Todo add generation here

    def __init__(self, predefined_neighbors):
        self.available_time_slot = [random.randint(2, 9), random.randint(13, 23)]
        self.id = str(uuid.uuid4())[:8]
        self.predefined_neighbors = predefined_neighbors

    def set_kind(self, kind):
        self.kind = kind

    def __str__(self):
        return f"Sommet {self.id} de type {self.kind}, plage horaire : {self.available_time_slot[0]}h à {self.available_time_slot[1]}h"
