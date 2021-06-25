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
    data_segment: [[Segment]] = []
    data_summit: [Summit] = []
    data_vehicles: [Vehicle] = []
    bar = progressbar.ProgressBar(max_value=100)
    pf = PathFinding(0)

    def vehicle_generator(self, number_of_vehicle, number_of_summit) -> None:
        # Generate X vehicle(s)
        for i in range(number_of_vehicle):
            # Create a vehicle
            vh = Vehicle(number_of_summit)
            # Load the vehicle (predefined items)
            vh.load()
            # Store the vehicle in data_vehicle
            self.data_vehicles.append(vh)

    def matrix_generator(self, number_of_summit, max_neighbor) -> None:
        graph = nx.watts_strogatz_graph(number_of_summit, max_neighbor, 1)
        q = 0
        mat = nx.adj_matrix(graph)
        for x, y in graph.edges():
            self.bar.update(q * 50 / len(graph.edges()))
            self.data_segment[x][y] = Segment(x, y)
            q += 1
        for i in range(number_of_summit):
            self.bar.update(50 + i * 50 / number_of_summit)
            self.data_summit.append(Summit([k for k in graph[i].keys()], i))
        # Convert graph to 2nd array adjacency matrix
        self.data_matrix = mat.toarray()

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
        lbl = ['Dépot' if x.kind == 1 else f'Adresse \n{self.data_summit.index(x)}' for x in self.data_summit]
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
        return {"warehouse": self.warehouse, "data_matrix": [[int(y) for y in x] for x in self.data_matrix], "data_segment": [[x.toJSON() if type(x) is Segment else "null" for x in z] for z in self.data_segment], "data_vehicles": [x.toJSON() for x in self.data_vehicles], "data_summit": [x.toJSON() for x in self.data_summit]}

    def __init__(self, number_of_summit, number_of_vehicle, max_neighbor):
        clearConsole()
        self.df = PathFinding(number_of_summit)
        self.bar.start()
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

            # Convert the matrix array into an numpy matrix
            M = np.array(self.data_matrix)

            # Generate the figure
            g = nx.DiGraph(M)
            # if graph is connected the generation is considered good
            print(nx.is_strongly_connected(self.to_di_graph()))
            print("_____")
            print(nx.is_strongly_connected(g))
            if nx.is_strongly_connected(g):
                break
        #
        #self.data_matrix = [[z*random.randint(0, 10) for z in x]for x in self.data_matrix]
        # Set the warehouse as is in teh data_summit list
        self.data_summit[self.warehouse].set_warehouse()

        # generate the vehicles
        self.vehicle_generator(number_of_vehicle, number_of_summit)
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
