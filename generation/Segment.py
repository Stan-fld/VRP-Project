import random
import uuid


class Segment:
    id = 0
    # Cost to drive it
    price = 0
    # id of summit
    origin = 0
    destination = 0

    def __init__(self, origin, destination):
        self.id = str(uuid.uuid4())[:8]
        self.price = random.randint(0, 10)
        self.origin = origin
        self.destination = destination

    def toJSON(self):
        """
        serialize the object in json
        """
        return {"id": self.id, "price": self.price, "origin": self.origin, "destination": self.destination}

    def __str__(self):
        return f"Segement {self.id} du point {self.origin} vers {self.destination}, cout {self.price}"
