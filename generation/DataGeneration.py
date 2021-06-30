import os
import random
import uuid

import networkx as nx
import numpy as np
import progressbar
from matplotlib import pyplot as plt

from generation.Segment import Segment
from generation.Summit import Summit
from generation.Vehicle import Vehicle
from pathfinding.PathFinding import PathFinding


def clearConsole(): os.system('cls' if os.name in ('nt', 'dos') else 'clear')


class DataGeneration:
    warehouse = 0
    data_matrix = []
    data_segment: [[Segment]] = [[]]
    data_summit: [Summit] = []
    data_vehicles: [Vehicle] = []
    bar = progressbar.ProgressBar(max_value=100)
    pf = PathFinding(0)
    number_of_kind_of_item = 0

    def vehicle_generator(self, number_of_vehicle, number_of_summit) -> None:
        def gv(kind):
            # Create a vehicle
            vh = Vehicle(kind)
            # Load the vehicle (predefined items)
            vh.load()
            # Store the vehicle in data_vehicle
            self.data_vehicles.append(vh)

        for i in range(self.number_of_kind_of_item):
            gv(i)
        # Generate X vehicle(s)
        for i in range(number_of_vehicle - self.number_of_kind_of_item):
            gv(random.randint(0, 3))

    def matrix_generator(self, number_of_summit, max_neighbor) -> None:
        isc = False
        while not isc:
            graph = nx.watts_strogatz_graph(number_of_summit, max_neighbor, 1)
            q = 0
            mat = nx.adj_matrix(graph)
            g2 = nx.DiGraph(mat)
            isc = nx.is_strongly_connected(g2)
        self.data_matrix = mat.toarray()
        xx = 0
        self.data_segment = []
        for x in self.data_matrix:
            tm = []
            yy = 0
            for y in np.nditer(x):
                if y == 1:
                    self.bar.update(q * 50 / int(len(self.data_matrix) ^ 2))
                    tm.append(Segment(xx, yy))
                else:
                    tm.append(None)
                yy += 1
            self.data_segment.append(tm)
            xx += 1
            q += 1
        for i in range(number_of_summit):
            self.bar.update(50 + i * 50 / number_of_summit)
            self.data_summit.append(Summit(i))
        # Convert graph to 2nd array adjacency matrix

    def display(self, save=False) -> None:
        # Convert the matrix array into an numpy matrix
        M = np.array(self.data_matrix)
        # Generate the figure
        G2 = nx.DiGraph(M)
        plt.figure()
        # Set node size by type
        node_sizes = [3000 if x.kind == 1 else 1600 for x in self.data_summit]
        # Set color map
        cmap = ['darkorange' if x.kind == 1 else 'dodgerblue' for x in self.data_summit]
        # Draw the graph and specify our characteristics
        lbl = [
            f'Dépot \ntype: {self.warehouse.index(x.id)}' if x.kind == 1 else f'Adresse \n{self.data_summit.index(x)}'
            for x in self.data_summit]
        nx.draw(G2, with_labels=True, node_color=cmap,
                node_size=node_sizes, font_size=8, font_weight="bold", width=0.75,
                edgecolors='gray', labels={i: lbl[i] for i in range(len(lbl))})
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
        return {
            "warehouse": self.warehouse,
            "data_matrix": [[int(y) for y in x] for x in self.data_matrix],
            "data_segment": [[x.toJSON() if type(x) is Segment else "null" for x in z] for z in self.data_segment],
            "data_vehicles": [x.toJSON() for x in self.data_vehicles],
            "data_summit": [x.toJSON() for x in self.data_summit]
        }

    def __init__(self, number_of_summit, number_of_vehicle, max_neighbor, number_of_kind_of_item, progressbar = True):
        self.pf = PathFinding(number_of_summit)
        if progressbar:
            clearConsole()
            self.bar.start()
        self.number_of_kind_of_item = number_of_kind_of_item
        # Generate the warehouse id
        self.warehouse = [random.randint(0, number_of_summit - 1) for x in range(self.number_of_kind_of_item)]
        # empty all arrays
        self.data_matrix = []
        self.data_summit = []
        self.data_segment = []
        # generate the matrix randomly and check for constrains
        self.matrix_generator(number_of_summit, max_neighbor)

        # self.data_matrix = [[z*random.randint(0, 10) for z in x]for x in self.data_matrix]
        # Set the warehouse as is in teh data_summit list
        for i in self.warehouse:
            self.data_summit[i].set_warehouse()

        # generate the vehicles
        self.vehicle_generator(number_of_vehicle, number_of_summit)
        if progressbar:
            self.bar.finish()
        print("Les données on été générées")

    def to_di_graph(self):
        # Convert the matrix array into an numpy matrix
        M = np.array(self.data_matrix)
        # Generate the figure
        return nx.DiGraph(M)

    def to_graph(self):
        # Convert the matrix array into an numpy matrix
        M = np.array(self.data_matrix)
        # Generate the figure
        return nx.Graph(M)
