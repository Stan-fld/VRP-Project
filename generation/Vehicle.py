import random
import uuid

import numpy as np


class Vehicle:
    id = 0
    kind = 0
    load = []
    max_speed = 0
    itinerary = []

    def load(self):
        # scooter
        if self.kind == 0:
            self.stock = [{"kind": 0, "qtt": 10},{"kind": 2, "qtt": 10}]
        elif self.kind == 1:
            self.stock = [{"kind": 0, "qtt": 10},{"kind": 2, "qtt": 10}]
        elif self.kind == 2:
            self.stock = [{"kind": 0, "qtt": 10},{"kind": 2, "qtt": 10}]
        else: #kind 3
            self.stock = [{"kind": 0, "qtt": 10},{"kind": 2, "qtt": 10}]

    def __init__(self, number_of_summit):
        self.id = str(uuid.uuid4())[:8]
        self.kind = random.randint(0, 3)
        self.load()
        self.max_speed = random.randint(20, 100)
        self.itinerary = np.random.randint(1, size=(number_of_summit, number_of_summit))

    def toJSON(self):
        """
        serialize the object in json
        """
        return {"id": self.id, "kind": self.kind, "load": self.stock, "max_speed": self.max_speed}

    def deliver_object(self, kind, qtt):
        for k, v in self.stock:
            if v['kind'] == kind and v.qtt >= qtt:
                v.qtt -= qtt
