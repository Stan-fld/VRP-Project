import random
import pprint


class DataGeneration:
    data_matrix = []

    def is_graph_correct(self, max_neighbour):
        for sommet in range(1, len(self.data_matrix)+1):
            liste = self.data_matrix[sommet-1]
            voisins = [i for i, value in enumerate(liste) if liste[i]]
            # display the nb neighboor
            print(len(voisins))
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
        #pprint.pprint(graph)
        self.data_matrix = graph

    def data_generator(self, number_of_summit, number_of_vehicle, max_neighbour):
        success = False
        i = 0
        while not success:
            self.matrix_generator(self, number_of_summit)
            success = self.is_graph_correct(self, max_neighbour)
            i += 1
        print(i)
        return success




