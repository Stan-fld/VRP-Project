import json
import os
import time
from time import sleep

from database import DBManagement as dbm
from generation.DataGeneration import DataGeneration
from pathfinding.PathFinding import average_weight
from pdf.RoadMap import RoadMap
from pdf.StatMap import StatMap
from statistic import Stats


def clearConsole(): os.system('cls' if os.name in ('nt', 'dos') else 'clear')


if __name__ == '__main__':
    data = None

    while True:

        print("What do you want to do?")
        print('{:.<5s}{:<10}'.format("0", "Exit"))
        print('{:.<5s}{:<10}'.format("1", "Generate and store in DB"))
        print('{:.<5s}{:<10}'.format("2", "Retrieve data from the DB"))
        print('{:.<5s}{:<10}'.format("3", "Calculate + RoadMap"))
        print('{:.<5s}{:<10}'.format("4", "Generate additional stat data"))
        print('{:.<5s}{:<10}'.format("5", f"Compute the {dbm.get_number_of_stored_stat()} stat data"))
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
            summ = int(input("Number of summit : "))
            step = int(input("step :"))
            for i in range(10):
                summits = summ
                vehicles = 10
                for y in range(20):
                    neighbors = 3
                    for z in range(10):
                        print((z + 20 * y + i * 10) / 2000)
                        bdd_entry = {"summits": summits, "vehicles": vehicles, "neighbors": neighbors}
                        start = time.time()
                        data = DataGeneration(number_of_summit=summits, number_of_vehicle=vehicles,
                                              max_neighbor=neighbors,
                                              number_of_kind_of_item=4)
                        end = time.time()
                        bdd_entry['generation'] = end - start
                        start = time.time()
                        data.pf.do(data, "dj", 10)
                        end = time.time()
                        bdd_entry['pathfinding_dj'] = end - start
                        print(f"dj : {bdd_entry['pathfinding_dj']}")
                        bdd_entry['average_weight_dj'] = average_weight(data)
                        start = time.time()
                        data.pf.do(data, "astar", 10)
                        end = time.time()
                        bdd_entry['pathfinding_astar'] = end - start
                        print(f"fw : {bdd_entry['pathfinding_astar']}")
                        bdd_entry['average_weight_astar'] = average_weight(data)
                        start = time.time()
                        roadmap_instance = RoadMap('test')
                        roadmap_instance.generate(data)
                        end = time.time()
                        bdd_entry['roadmap'] = end - start
                        print(f"rm : {bdd_entry['roadmap']}")
                        del data.data_segment
                        del data.data_vehicles
                        del data.data_matrix
                        del data.pf
                        del roadmap_instance
                        del data
                        print("store to MongoDB")
                        dbm.store_stat_to_mongo(json.loads(json.dumps(bdd_entry)))
                        neighbors += 1
                    vehicles += 1
                summits += step
        elif inp == "5":
            stat_map = StatMap('statstest')
            # fig = plt.figure()
            # ax = plt.axes(projection='3d')
            # ax.scatter3D(x, y, z, c=z, cmap='BrBG_r')
            stats = dbm.get_stat_from_mongo()

            sm = []
            gn = []
            ng = []
            ptg_dj = []
            avg_w_dj = []
            ptg_astar = []
            sm_astar = []
            ng_astar = []
            for x in stats:
                sm.append(x['summits'])
                gn.append(x["generation"])
                ng.append(x['neighbors'])
                ptg_dj.append(x['pathfinding_dj'])
                avg_w_dj.append(x['average_weight_dj'])
                try:
                    if x['pathfinding_astar']:
                        ptg_astar.append(x['pathfinding_astar'])
                        sm_astar.append(x['summits'])
                        ng_astar.append(x['neighbors'])

                except Exception as e:
                    pass

            # linear regression for number of summit over graph generation time
            b, r = Stats.linear_regression(sm, gn, "Number of summits", "Graph generation time (s)",
                                           "Graph representing a linear regression of \nnumber of summit over graph "
                                           "generation time.",
                                           True)
            stat_map.add_img(r)
            print(f"linear regression fx y ~ {round(b[0], 4)} + {round(b[1], 4)} * x")
            stat_map.add_txt(f"linear regression fx y ~ {round(b[0], 4)} + {round(b[1], 4)} * x")

            # linear regression for number of summit over Pathfinding time with Djikstra.
            b, r = Stats.linear_regression(sm, ptg_dj, "Number of summits", "Pathfinding time with Djikstra (s)",
                                           "Graph representing a linear regression of \nnumber of summit over Pathfinding time with Djikstra.",
                                           True)
            print(f"linear regression fx y ~ {round(b[0], 4)} + {round(b[1], 4)} * x")
            stat_map.add_img(r)
            stat_map.add_txt(f"linear regression fx y ~ {round(b[0], 4)} + {round(b[1], 4)} * x")

            # plotting pathfinding Dijkstra
            r = Stats.stats_pathfinding(sm=sm, ng=ng, ptg=ptg_dj,
                                    title='Graph representing a progression of \nnumber of summit over Dijkstra pathfinding', save=True)
            stat_map.add_img(r)

            # plotting pathfinding A star
            r = Stats.stats_pathfinding(sm=sm_astar, ng=ng_astar, ptg=ptg_astar,
                                    title='Graph representing a progression of \nnumber of summit over A star pathfinding', save=True)
            stat_map.add_img(r)

            # Plotting of the dj fix summits
            r = Stats.stat_dj_fix_summits(True)
            stat_map.add_img(r)

            # Plotting of the dj fix neighbors
            r = Stats.stat_dj_fix_neighbors(True)
            stat_map.add_img(r)

            # Save the PDF file
            stat_map.save()
