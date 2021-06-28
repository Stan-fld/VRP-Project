import json
import unittest
import uuid

import networkx as nx
from matplotlib import pyplot as plt

from generation.DataGeneration import DataGeneration


class GenerationTest(unittest.TestCase):
    # Mock data
    dt = DataGeneration(number_of_summit=10, number_of_vehicle=10, max_neighbor=6, number_of_kind_of_item=4)

    def test_generate_matrix(self):
        self.assertEqual(len(self.dt.data_vehicles), 10)
        self.assertEqual(len(self.dt.data_summit), 10)
        self.assertEqual(len(self.dt.data_matrix), 10)

    def test_all_point_linked(self):
        self.assertTrue(nx.is_strongly_connected(self.dt.to_di_graph()))

    def generate_graphs_of_neighbors(self):
        neighbors = []
        for sommet in range(1, len(self.dt.data_matrix) + 1):
            liste = self.dt.data_matrix[sommet - 1]
            voisins = [i for i, value in enumerate(liste) if liste[i]]
            neighbors.append(len(voisins))
        plt.hist(neighbors)
        plt.title('Number(s) of neighbor(s)')
        plt.savefig(f'../graphs/NBN_{str(uuid.uuid4())[:4]}.png', transparent=True)

    def test_json_output(self):
        jso = self.dt.toJSON()
        success = True
        self.assertTrue(success)
