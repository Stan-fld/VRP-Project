import numpy as np


class GeneticDistribution:
    final_matrix = []
    segment_matrix = []
    summit_matrix = []
    vehicles_matrix = []

    def __init__(self, final_matrix, segment_matrix, summit_matrix, vehicles_matrix):
        self.final_matrix = final_matrix
        self.segment_matrix = segment_matrix
        self.summit_matrix = summit_matrix
        self.vehicles_matrix = vehicles_matrix
        print(np.asmatrix(self.final_matrix))
