from time import sleep

from generation.DataGeneration import DataGeneration
from pdf.RoadMap import RoadMap

if __name__ == '__main__':
    for i in range(40):
        data = DataGeneration(number_of_summit=10, number_of_vehicle=10, max_neighbor=5)
        #data.display()
        #print(data.toJSON())
        #print(i)
    #radmap_instance = RoadMap('test')
    #radmap_instance.generate(data)

