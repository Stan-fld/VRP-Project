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

        print("Que voulez vous faire ? ")
        print('{:.<5s}{:<10}'.format("0", "Quitter"))
        print('{:.<5s}{:<10}'.format("1", "Générer et stocker en BDD"))
        print('{:.<5s}{:<10}'.format("2", "Récuperer les données depuis la BDD"))
        print('{:.<5s}{:<10}'.format("3", "Calculer + RoadMap"))
        print('{:.<5s}{:<10}'.format("4", "Generate stat data"))
        print('{:.<5s}{:<10}'.format("5", "compute stat data"))
        while (inp := (input("Entrez votre choix :"))) not in ["0", "1", "2", "3"]:
            print("Veuillez entrer un chiffre correcte")
        clearConsole()
        if inp == "0":  # quitter
            print("Merci d'avoir utilisé notre logiciel !")
            print("Il se fermera dans 3 secondes...")
            sleep(3)
            quit(0)
        elif inp == "1":  # Generate + store
            data = DataGeneration(number_of_summit=500, number_of_vehicle=10, max_neighbor=5, number_of_kind_of_item=4)
            dbm.store_data(data)
            # data.display()
            clearConsole()
        elif inp == "2":  # Load from DB
            data = dbm.get_data_generation()
            #data.display()
            clearConsole()
            '''start = time.time()
            data.pf.do(data, "fw", 50)
            end = time.time()
            print(end - start)'''

        elif inp == "3":  # Pathfinding + RoadMap
            if data is not None:
                start = time.time()
                data.pf.do(data, "dj", 10)
                end = time.time()
                print(end - start)
                # todo call the pathfinding here
                roadmap_instance = RoadMap('test')
                roadmap_instance.generate(data)
            else:
                print("Les données ne sont pas chargées merci de les générer ou de les importer (1 ou 2)\n")
        elif inp == "4": # stat mode
            for i in range(10):
                summits = 500
                vehicles = 10
                neighbors = 3
                for y in range(100):
                    for z in range(20):
                        bdd_entry = {"summits": summits, "vehicles": vehicles, "neighbors": neighbors}
                        start = time.time()
                        data = DataGeneration(number_of_summit=1000, number_of_vehicle=10, max_neighbor=5, number_of_kind_of_item=4)
                        end = time.time()
                        bdd_entry['generation'] = end-start
                        start = time.time()
                        data.pf.do(data, "dj", 10)
                        end = time.time()
                        bdd_entry['pathfinding_dj'] = end-start
                        start = time.time()
                        data.pf.do(data, "fw", 10)
                        end = time.time()
                        bdd_entry['roadmap'] = end-start
                        bdd_entry['average_weight'] = average_weight(data)
                        start = time.time()
                        roadmap_instance = RoadMap('test')
                        roadmap_instance.generate(data)
                        end = time.time()
                        bdd_entry['roadmap'] = end-start
                        #todo stoto into stat collection

                        neighbors += 1
                    vehicles += 1
                summits += 500
        elif inp == "5":
            # todo use the data from bdd to create stat analysis
            pass
