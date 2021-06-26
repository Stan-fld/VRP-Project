import networkx as nx
import numpy as np
import progressbar


class PathFinding:
    bar = progressbar.ProgressBar(max_value=100)
    solutions = []

    def __init__(self, number_of_summit):
        self.p2p_array = [[[] for j in range(number_of_summit)] for i in range(number_of_summit)]

    def find_best_solution(self):
        pass

    def do(self, data, fx):
        def func(u, v, d):
            nonlocal data
            if data.data_segment[u][v] is None:
                return 0
            return data.data_segment[u][v].price

        def djikstra(g, frm, to):
            return nx.shortest_path(g, frm, to, func)[1:]

        def floyd_warshall(p, frm, to):
            return nx.reconstruct_path(frm, to, p)[1:]

        def vrp(f, g, frm, to, p):
            if f == "fw":
                return floyd_warshall(p, frm, to)
            else:
                return djikstra(g, frm, to)

        smt_arr = [[] for x in range(data.number_of_kind_of_item)]
        g = data.to_di_graph()
        vh_arr = [[] for x in range(data.number_of_kind_of_item)]
        # sor tthe vehicles by kind
        for i, x in enumerate(data.data_vehicles):
            vh_arr[x.kind].append(data.data_vehicles.index(x))
        # sort the summits by item kind
        for smt in data.data_summit:
            smt_arr[smt.item_to_deliver.get('kind')].append(smt.id)
        # split the stop for each vehicles
        for i, s in enumerate(smt_arr):
            tp = np.array_split(np.array(s),len(vh_arr[i]))
            for z, x in enumerate(vh_arr[i]):
                data.data_vehicles[x].itinerary = tp[z].tolist() + [data.data_summit[data.warehouse[data.data_vehicles[x].kind]].id]
        # generate data for the algo
        if fx == "fw":
            predecessors, _ = nx.floyd_warshall_predecessor_and_distance(g)
        else:
            predecessors = None
        # loop on all the vehicle itineraries, finding the shortest pah between stops
        for vh in data.data_vehicles:
            vh.full_itinerary.append(data.data_summit[data.warehouse[vh.kind]].id)
            for i in vh.itinerary:
                if vh.stock - data.data_summit[i].item_to_deliver.get('qtt') < 0 and data.data_summit[i].kind == 0:
                    vh.load()
                    vh.full_itinerary += vrp(fx, g, vh.full_itinerary[-1], data.data_summit[data.warehouse[vh.kind]].id, predecessors)
                vh.full_itinerary += vrp(fx, g, vh.full_itinerary[-1], i, predecessors)
                vh.stock -= data.data_summit[i].item_to_deliver.get('qtt')

        # Print the resulting itineraries (full and stops only)
        for vh in data.data_vehicles:
            for i in vh.itinerary:
                print(f"{i}", "-> ", end = '')
            print("\n___________ full :")
            for i in vh.full_itinerary:
                print(f"{i}", "-> ", end = '')
            print("\n_______________________________")

