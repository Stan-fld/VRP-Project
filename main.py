from generation.DataGeneration import DataGeneration
from algorithmic.GeneticDistribution import GeneticDistribution

if __name__ == '__main__':

    data = DataGeneration(number_of_summit=10, number_of_vehicle=10, max_neighbor=6)
    a = GeneticDistribution(data.data_matrix, data.data_segment, data.data_summit, data.data_vehicles)
    data.display()
