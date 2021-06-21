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

    def __init__(self, origin, destination):
        self.speed_limit = random.randint(20, 100)
        self.id = str(uuid.uuid4())[:8]
        self.authorized_vehicle = random.sample(range(0, 3), k=random.randint(1, 3))
        self.price = random.randint(0, 3)
        self.origin = origin
        self.destination = destination

    def __str__(self):
        return f"Segment {self.id} du point {self.origin} vers {self.destination}, vitesse max {self.speed_limit}, " \
               f"cout {self.price}, véhicules autorisés {self.authorized_vehicle}"
