import os
import time
from time import sleep

from pymongo import database

from database import DBConnection
from generation.DataGeneration import DataGeneration
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
        while (inp := (input("Entrez votre choix :"))) not in ["0", "1", "2", "3"]:
            print("Veuillez entrer un chiffre correcte")
        clearConsole()
        if inp == "0":  # quitter
            print("Merci d'avoir utilisé notre logiciel !")
            print("Il se fermera dans 3 secondes...")
            sleep(3)
            quit(0)
        elif inp == "1":  # Generate + store
            data = DataGeneration(number_of_summit=100, number_of_vehicle=10, max_neighbor=5, number_of_kind_of_item=4)
            #DBConnection.infos_collection.insert_one(data.toJSON())
            data.display()
            #clearConsole()
        elif inp == "2":  # Load from DB
            clearConsole()
            start = time.time()
            data.pf.do(data, "fw", 100)
            end = time.time()
            print(end - start)
            '''start = time.time()
            data.pf.do(data, "dj", 100)
            end = time.time()
            print(end - start)'''

        elif inp == "3":  # Pathfinding + RoadMap
            if data is not None:
                # todo call the pathfinding here
                radmap_instance = RoadMap('test')
                radmap_instance.generate(data)
            else:
                print("Les données ne sont pas chargées merci de les générer ou de les importer (1 ou 2)\n")
