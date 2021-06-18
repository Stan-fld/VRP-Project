import random
import pprint

import numpy as np
from sklearn.neighbors import kneighbors_graph
from generation.Vehicle import Vehicle


class DataGeneration:
    data_matrix = []
    data_vehicles: [Vehicle] = []

    def vehicle_generator(self, number_of_vehicle):
        for i in range(number_of_vehicle):
            vh = Vehicle()
            self.data_vehicles.append(vh)
        # test only ––––––––––––––––––––––––––––––––––––––––––––
        # print(len(self.data_vehicles))
        # test only ––––––––––––––––––––––––––––––––––––––––––––

    def is_graph_correct(self, max_neighbor):
        print("new graph")
        for sommet in range(1, len(self.data_matrix) + 1):
            liste = self.data_matrix[sommet - 1]
            voisins = [i for i, value in enumerate(liste) if liste[i]]
            # test only ––––––––––––––––––––––––––––––––––––––––––––
            # display the nb neighboor

            print(len(voisins))
            message = "Le sommet " + str(sommet-1) + " est de degré " + str(len(voisins)) + " (voisins : "
            message += \
            ' '.join([str(v) for v in voisins]) + ")"  #SOLUTION
            print(message)
            # test only ––––––––––––––––––––––––––––––––––––––––––––
            if len(voisins) < 2 or len(voisins) > max_neighbor:
                return False
        return True

    def get_neighbors_of_summit(self, actual_summit, graph = None):
        graph = self.data_matrix if graph is None else graph
        liste = graph[actual_summit] | graph[:,actual_summit]
        return [i for i, value in enumerate(liste) if liste[i]]

    def matrix_generator(self, number_of_summit, max_neighbor):
        graph = np.random.randint(1, size=(number_of_summit, number_of_summit))
        for i in range(number_of_summit):

            dif = int(max_neighbor-len(self.get_neighbors_of_summit(i, graph)))
            print(dif)
            if dif > 0:
                for r in random.sample(range(0, number_of_summit), k=random.randint(1, dif)):
                    while True:
                        print(r)
                        print(len(self.get_neighbors_of_summit(r, graph)))
                        if len(self.get_neighbors_of_summit(r, graph)) < max_neighbor or i == r:
                            graph[i][r] = 1
                            graph[r][i] = 1
                            break
                        else:
                            r = random.sample(range(0, number_of_summit), 1)[0]
        # test only ––––––––––––––––––––––––––––––––––––––––––––
        print(graph)
        # test only ––––––––––––––––––––––––––––––––––––––––––––
        self.data_matrix = graph

    def __init__(self, number_of_summit, number_of_vehicle, max_neighbor):
        # generate the matrix randomly and check for constrains
        self.matrix_generator(number_of_summit, max_neighbor)
        self.is_graph_correct(max_neighbor)
        # generate the vehicles
        self.vehicle_generator(number_of_vehicle)

        # test only ––––––––––––––––––––––––––––––––––––––––––––
        # print(f"number of itteration to generate the graph {i}")
        # print(f"id of the {len(self.data_vehicles)} generated vehicles : ")
        # for v in self.data_vehicles:
        #    pprint.pprint(v.id)
        # test only ––––––––––––––––––––––––––––––––––––––––––––
