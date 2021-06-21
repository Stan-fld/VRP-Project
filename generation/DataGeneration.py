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

    def vehicle_generator(self, number_of_vehicle):
        # Generate X vehicle(s)
        for i in range(number_of_vehicle):
            # Create a vehicle
            vh = Vehicle()
            # Load the vehicle (predefined items)
            vh.load()
            # Store the vehicle in data_vehicle
            self.data_vehicles.append(vh)

    def is_graph_correct(self, max_neighbor):  # todo stan ajoute ici
        pass

    def get_neighbors_of_summit(self, actual_summit, graph=None):
        graph = self.data_matrix if graph is None else graph
        liste = graph[actual_summit] | graph[:, actual_summit]
        return [i for i, value in enumerate(liste) if liste[i]]

    def matrix_generator(self, number_of_summit, max_neighbor):
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
                    while True:
                        if len(self.get_neighbors_of_summit(r, graph)) < rd[i] and i != r:
                            # Add a segment in data_segment and in the adjacency matrix
                            self.data_segment[i][r] = Segment(i, r)
                            self.data_segment[r][i] = Segment(r, i)
                            graph[i][r] = 1
                            graph[r][i] = 1
                            break
                        else:
                            r = random.sample(range(0, number_of_summit), 1)[0]
        self.data_matrix = graph

    def display(self, save=False):
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

    def toJSON(self):
        return {"warehouse": self.warehouse, "data_matrix": [[*x] for x in self.data_matrix], "data_segment": [[x.toJSON() if type(x) is Segment else "null" for x in z] for z in self.data_segment], "data_vehicles": [x.toJSON() for x in self.data_vehicles], "data_summit": [x.toJSON() for x in self.data_summit]}

    def __init__(self, number_of_summit, number_of_vehicle, max_neighbor):
        # Generate the warehouse id
        self.warehouse = random.randint(0, number_of_summit-1)

        # Generate empty data_segment
        self.data_segment = [[None for j in range(number_of_summit)] for i in range(number_of_summit)]

        # generate the matrix randomly and check for constrains
        self.matrix_generator(number_of_summit, max_neighbor)
        # Set the warehouse as is in teh data_summit list
        self.data_summit[self.warehouse].set_kind(1)

        # generate the vehicles
        self.vehicle_generator(number_of_vehicle)
