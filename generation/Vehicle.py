import random
import uuid

import numpy as np


class Vehicle:
    id = 0
    kind = 0
    load = []
    max_speed = 0
    itinerary = []
    full_itinerary = []
    stock = {}

    def load(self):
        # scooter
        if self.kind == 0:
            self.stock = 1000
        elif self.kind == 1:
            self.stock = 200
        elif self.kind == 2:
            self.stock = 100
        else:
            self.stock = 50

    def __init__(self, kind):
        self.id = str(uuid.uuid4())[:8]
        self.kind = kind
        self.load()
        self.max_speed = random.randint(20, 100)

    def toJSON(self):
        """
        serialize the object in json
        """
        return {"id": self.id, "kind": self.kind, "load": self.stock, "max_speed": self.max_speed}

    def deliver_object(self, kind, qtt):
        for k, v in self.stock:
            if v['kind'] == kind and v.qtt >= qtt:
                v.qtt -= qtt
