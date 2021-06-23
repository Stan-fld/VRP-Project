import random
import uuid

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from generation.Segment import Segment
from generation.Summit import Summit
from generation.Vehicle import Vehicle


class DataGeneration:
    warehouse = 0
    data_matrix = []
    data_segment: [[Segment]] = []
    data_summit: [Summit] = []
    data_vehicles: [Vehicle] = []

    def vehicle_generator(self, number_of_vehicle, number_of_summit) -> None:
        # Generate X vehicle(s)
        for i in range(number_of_vehicle):
            # Create a vehicle
            vh = Vehicle(number_of_summit)
            # Load the vehicle (predefined items)
            vh.load()
            # Store the vehicle in data_vehicle
            self.data_vehicles.append(vh)

    # This function uses a path-width algorithm
    # to know if there is a path between two summits.
    # the graph is represented by the adjacency matrix

    def exist_path(self, u, v) -> bool:
        n = len(self.data_matrix) - 1  # number of summits in the graph
        line = []
        visits = [False] * n

        # add the first summit to the queue
        line.append(u)
        while line:
            # remove the top of the stack and tagged as visited
            current = line.pop(0)
            visits[current] = True

            # visit adjacent summits
            for i in range(n):
                # if there is an edge between u and i and
                # the summit i is not yet visited
                if self.data_matrix[current][i] > 0 and not visits[i]:
                    # add i to the queue tagged as visited
                    line.append(i)
                    visits[i] = True

                # If summit i is the desired summit (i = v)
                # then there is a path from u to i(v)
                elif self.data_matrix[current][i] > 0 and i == v:
                    return True
        return False

    def is_graph_correct(self):
        n = len(self.data_matrix) - 1  # number of summits
        for i in range(n):
            for j in range(i + 1, n):
                if not self.exist_path(i, j):
                    return False
        return True

    def get_neighbors_of_summit(self, actual_summit, graph=None) -> [bool]:
        graph = self.data_matrix if graph is None else graph
        liste = graph[actual_summit]
        return [i for i, value in enumerate(liste) if liste[i]]

    def matrix_generator(self, number_of_summit, max_neighbor) -> None:
        rd = (np.random.randn(number_of_summit) * (max_neighbor / 4) + max_neighbor / 2)
        rd = [abs(round(x, 0)) if x >= 1 else 1 for x in rd]
        # Generate an empty matrix (only 0 in it), in order to populate it later
        graph = np.random.randint(1, size=(number_of_summit, number_of_summit))
        for i in range(number_of_summit):
            # Create and store a summit object
            self.data_summit.append(Summit(rd[i]))
            # Check the difference between the predefined amount of neighbor and the actual
            dif = int(rd[i] - len(self.get_neighbors_of_summit(i, graph)))
            if dif > 0:
                for r in random.sample(range(0, number_of_summit), k=random.randint(1, dif)):
                    z = 0
                    while True:
                        if (len(self.get_neighbors_of_summit(r, graph)) < rd[r] and i != r) or (z > 5 and (rd[r] < max_neighbor or rd[i] < max_neighbor)):
                            # Add a segment in data_segment and in the adjacency matrix
                            self.data_segment[i][r] = Segment(i, r)
                            self.data_segment[r][i] = Segment(r, i)
                            graph[i][r] = 1
                            graph[r][i] = 1
                            break
                        else:
                            z += 1
                            if z > 10:
                                break

                            r = random.sample(range(0, number_of_summit), 1)[0]

        self.data_matrix = graph

    def display(self, save=False) -> None:
        # Convert the matrix array into an numpy matrix
        M = np.array(self.data_matrix)
        # Generate the figure
        G2 = nx.DiGraph(M)
        plt.figure()
        options = {
            'node_color': 'yellow',
            'node_size': 100,
            'edge_color': 'tab:grey',
            'with_labels': True
        }
        nx.draw(G2, **options)
        if save:
            # Save it
            plt.savefig(f'graphs/MAP_{str(uuid.uuid4())[:4]}.png')
        else:
            # Show the figure
            plt.show()
        plt.close()

    def toJSON(self):
        """
        serialize the object in json
        """
        return {"warehouse": self.warehouse, "data_matrix": [[int(y) for y in x] for x in self.data_matrix], "data_segment": [[x.toJSON() if type(x) is Segment else "null" for x in z] for z in self.data_segment], "data_vehicles": [x.toJSON() for x in self.data_vehicles], "data_summit": [x.toJSON() for x in self.data_summit]}

    def __init__(self, number_of_summit, number_of_vehicle, max_neighbor):
        # Generate the warehouse id
        self.warehouse = random.randint(0, number_of_summit - 1)
        y = 0
        while True:
            # Generate empty data_segment
            self.data_segment = [[None for j in range(number_of_summit)] for i in range(number_of_summit)]
            self.data_matrix = []
            self.data_summit = []
            # generate the matrix randomly and check for constrains
            self.matrix_generator(number_of_summit, max_neighbor)
            if self.is_graph_correct():
                break
            else:
                y += 1
        print(y) # todo stan optimise ici

        # Set the warehouse as is in teh data_summit list
        self.data_summit[self.warehouse].set_kind(1)

        # generate the vehicles
        self.vehicle_generator(number_of_vehicle, number_of_summit)
