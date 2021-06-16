import random
import pprint


class DataGeneration:
    def matrix_generator(self: int):
        graph = []
        i = 0
        for item in range(1, self + 1):
            line = [random.choice([1, 0]) for i in range(1, self + 1)]
            line[i] = 0
            graph.append(line)
            i += 1
        pprint.pprint(graph)
