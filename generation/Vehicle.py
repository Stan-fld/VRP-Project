import random
import uuid


class Vehicle:
    id = 0
    kind = 0
    load = []
    max_speed = 0

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

    def __init__(self):
        self.id = str(uuid.uuid4())[:8]
        self.kind = random.randint(0, 3)
        self.load()
        self.max_speed = random.randint(20, 100)

    def deliver_object(self, kind, qtt):
        for k, v in self.stock:
            if v['kind'] == kind and v.qtt >= qtt:
                v.qtt -= qtt