import random
import uuid


class Segment:
    id = 0
    # Max speed allowed
    speed_limit = 0
    # Kind of vehicles authorized
    authorized_vehicle = []
    # Cost to drive it
    price = 0
    # id of summit
    origin = 0
    destination = 0
    # % by the speed is reduced for each hour of the day
    trafic: [float] = []
    # Length of the road (in meter)
    length = 0

    def __init__(self, origin, destination):
        self.speed_limit = random.randint(20, 100)
        self.id = str(uuid.uuid4())[:8]
        self.authorized_vehicle = random.sample(range(0, 3), k=random.randint(1, 3))
        self.price = random.randint(0, 3)
        self.origin = origin
        self.destination = destination
        self.trafic = [random.randint(0, 50)/100 for x in range(23)]
        self.length = random.randrange(100, 10000, 1)

    def toJSON(self):
        """
        serialize the object in json
        """
        return {"id": self.id, "speed_limit": self.speed_limit, "authorized_vehicle": self.authorized_vehicle, "price": self.price, "origin": self.origin, "destination": self.destination, "length": self.length}

    def __str__(self):
        return f"Segement {self.id} du point {self.origin} vers {self.destination}, vitesse max {self.speed_limit}, cout {self.price}, vehicules authorisés {self.authorized_vehicle}"
