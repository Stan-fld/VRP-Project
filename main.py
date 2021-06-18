import random

import numpy as np
from matplotlib import pyplot as plt
import networkx as nx

from generation.DataGeneration import DataGeneration

if __name__ == '__main__':

    data = DataGeneration(number_of_summit=10, number_of_vehicle=10, max_neighbor=6)
    #print(len(data.data_vehicles))
    # print(len(data.data_matrix))
    #data.data_vehicles[2].deliver_object(0,4)
    print(data.data_vehicles[2].stock[0])
    def display():
        M = np.array(data.data_matrix)

        G2 = nx.DiGraph(M)
        plt.figure()

        options = {
            'node_color': 'yellow',
            'node_size': 100,
            'edge_color': 'tab:grey',
            'with_labels': True
        }
        nx.draw(G2, **options)
        plt.show()


    display()
