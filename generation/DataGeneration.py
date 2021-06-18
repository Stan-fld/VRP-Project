import random
import pprint

import numpy as np
from sklearn.neighbors import kneighbors_graph

from generation.Segment import Segment
from generation.Summit import Summit
from generation.Vehicle import Vehicle
from matplotlib import pyplot as plt


class DataGeneration:
    warehouse = 0
    data_matrix = []
    data_segment: [[Segment]] = []
    data_summit: [Summit] = []
    data_vehicles: [Vehicle] = []

    def vehicle_generator(self, number_of_vehicle):

        for i in range(number_of_vehicle):
            # Create a vehicle
            vh = Vehicle()
            # Load the vehicle (predefined items)
            vh.load()
            # Store the vehicle in data
            self.data_vehicles.append(vh)
        # test only ––––––––––––––––––––––––––––––––––––––––––––
        # print(len(self.data_vehicles))
        # test only ––––––––––––––––––––––––––––––––––––––––––––

    def is_graph_correct(self, max_neighbor):
        print("new graph")
        neighbors = []
        for sommet in range(1, len(self.data_matrix) + 1):
            liste = self.data_matrix[sommet - 1]
            voisins = [i for i, value in enumerate(liste) if liste[i]]
            # test only ––––––––––––––––––––––––––––––––––––––––––––
            # display the nb neighboor
            neighbors.append(len(voisins))
            print(len(voisins))
            message = "Le sommet " + str(sommet - 1) + " est de degré " + str(len(voisins)) + " (voisins : "
            message += \
                ' '.join([str(v) for v in voisins]) + ")"  # SOLUTION
            print(message)
            # test only ––––––––––––––––––––––––––––––––––––––––––––

        plt.hist(neighbors)
        plt.title('neighbor')
        plt.show()

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
            # Check the diffrence between the predefined amount of neighbor and the actual
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
        # test only ––––––––––––––––––––––––––––––––––––––––––––
        '''
        plt.hist(rd)
        plt.title('rd')
        plt.show()
        print(graph)
        '''
        # test only ––––––––––––––––––––––––––––––––––––––––––––
        self.data_matrix = graph

    def __init__(self, number_of_summit, number_of_vehicle, max_neighbor):
        # Generate the warehouse id
        self.warehouse = random.randint(0,number_of_summit)

        # Generate empty data_segment
        self.data_segment = [[None for j in range(number_of_summit)] for i in range(number_of_summit)]

        # generate the matrix randomly and check for constrains
        self.matrix_generator(number_of_summit, max_neighbor)
        self.data_summit[self.warehouse].set_kind(1)

        # generate the vehicles
        self.vehicle_generator(number_of_vehicle)
        print(self.data_vehicles[0].kind)
        for s in self.data_segment:
            for ss in s:
                print(ss)

        for smt in self.data_summit:
            print(smt)
        # test only ––––––––––––––––––––––––––––––––––––––––––––
        # self.is_graph_correct(max_neighbor)
        # print(f"number of itteration to generate the graph {i}")
        # print(f"id of the {len(self.data_vehicles)} generated vehicles : ")
        # for v in self.data_vehicles:
        #    pprint.pprint(v.id)
        # test only ––––––––––––––––––––––––––––––––––––––––––––
