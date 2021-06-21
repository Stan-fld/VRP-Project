from generation.DataGeneration import DataGeneration

if __name__ == '__main__':

    data = DataGeneration(number_of_summit=10, number_of_vehicle=10, max_neighbor=6)
    data.display()
