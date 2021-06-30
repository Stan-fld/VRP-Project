import json
import os
import time
from time import sleep

from database import DBManagement as dbm
from generation.DataGeneration import DataGeneration
from pathfinding.PathFinding import average_weight
from pdf.RoadMap import RoadMap


def clearConsole(): os.system('cls' if os.name in ('nt', 'dos') else 'clear')


if __name__ == '__main__':
    data = None

    while True:

        print("What do you want to do?")
        print('{:.<5s}{:<10}'.format("0", "Exit"))
        print('{:.<5s}{:<10}'.format("1", "Generate and store in DB"))
        print('{:.<5s}{:<10}'.format("2", "Retrieve data from the DB"))
        print('{:.<5s}{:<10}'.format("3", "Calculate + RoadMap"))
        print('{:.<5s}{:<10}'.format("4", "Generate stat data"))
        print('{:.<5s}{:<10}'.format("5", "Compute stat data"))
        while (inp := (input("Enter your choice :"))) not in ["0", "1", "2", "3", "4", "5"]:
            print("Please enter a correct number")
        clearConsole()
        if inp == "0":  # quitter
            print("Thank you for using our software !")
            print("It will close in three seconds...")
            sleep(3)
            quit(0)
        elif inp == "1":  # Generate + store
            data = DataGeneration(number_of_summit=500, number_of_vehicle=10, max_neighbor=5, number_of_kind_of_item=4)
            clearConsole()
            print('The data is being stored, please be patient !')
            dbm.store_data(data)
            # data.display()
        elif inp == "2":  # Load from DB
            print('Data recovery, please wait')
            data = dbm.get_data_generation()
            # data.display()
            clearConsole()
            '''start = time.time()
            data.pf.do(data, "fw", 50)
            end = time.time()
            print(end - start)'''

        elif inp == "3":  # Pathfinding + RoadMap
            if data is not None:
                print('Path calculation, please wait')
                start = time.time()
                data.pf.do(data, "dj", 10)
                end = time.time()
                print(end - start)
                clearConsole()
                print('Generation of the pdf, please wait')
                # todo call the pathfinding here
                roadmap_instance = RoadMap('test')
                roadmap_instance.generate(data)
            else:
                print("The data is not loaded, please generate or import it (1 or 2)\n")
        elif inp == "4":  # stat mode
            for i in range(10):
                summits = 50
                vehicles = 10
                neighbors = 3
                for y in range(10):
                    for z in range(20):
                        print(z)
                        bdd_entry = {"summits": summits, "vehicles": vehicles, "neighbors": neighbors}
                        start = time.time()
                        data = DataGeneration(number_of_summit=summits, number_of_vehicle=vehicles, max_neighbor=neighbors,
                                              number_of_kind_of_item=4, progressbar=False)
                        end = time.time()
                        bdd_entry['generation'] = end - start
                        start = time.time()
                        data.pf.do(data, "dj", 10)
                        end = time.time()
                        bdd_entry['pathfinding_dj'] = end - start
                        bdd_entry['average_weight_dj'] = average_weight(data)
                        start = time.time()
                        data.pf.do(data, "fw", 10)
                        end = time.time()
                        bdd_entry['pathfinding_fw'] = end - start
                        bdd_entry['average_weight_fw'] = average_weight(data)
                        start = time.time()
                        roadmap_instance = RoadMap('test')
                        roadmap_instance.generate(data)
                        end = time.time()
                        bdd_entry['roadmap'] = end - start
                        del data.data_segment
                        del data.data_vehicles
                        del data.data_matrix
                        del data.pf
                        del roadmap_instance
                        del data
                        print("store to MongoDB")
                        dbm.store_stat_to_mongo(json.loads(json.dumps(bdd_entry)))
                        # Store to file as backup if network link down
                        file_object = open('dump.json', 'a')
                        file_object.write(",\n"+json.dumps(bdd_entry))
                        file_object.close()
                        neighbors += 1
                    vehicles += 1
                summits += 5
        elif inp == "5":
            stats = dbm.get_stat_from_mongo()
            # todo use the data from bdd to create stat analysis
            pass
