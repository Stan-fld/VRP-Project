import random
import pprint

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

    def is_graph_correct(self, max_neighbour):
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
            if len(voisins) < 2 or len(voisins) > max_neighbour:
                return False
        return True

    def matrix_generator(self, summit):
        graph = []
        i = 0
        for item in range(1, summit + 1):
            line = [random.choice([1, 0]) for i in range(1, summit + 1)]
            line[i] = 0
            graph.append(line)
            i += 1
        # test only ––––––––––––––––––––––––––––––––––––––––––––
        pprint.pprint(graph)
        # test only ––––––––––––––––––––––––––––––––––––––––––––
        self.data_matrix = graph

    def __init__(self, number_of_summit, number_of_vehicle, max_neighbour):
        success = False
        i = 0
        while not success:
            self.matrix_generator(number_of_summit)
            success = self.is_graph_correct(max_neighbour)
            i += 1
        self.vehicle_generator(number_of_vehicle)

        # test only ––––––––––––––––––––––––––––––––––––––––––––
        # print(f"number of itteration to generate the graph {i}")
        # print(f"id of the {len(self.data_vehicles)} generated vehicles : ")
        # for v in self.data_vehicles:
        #    pprint.pprint(v.id)
        # test only ––––––––––––––––––––––––––––––––––––––––––––
