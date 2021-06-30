import copy

import networkx as nx
import numpy as np
import progressbar

def average_weight(data):
    wg = 0
    for vh in data.data_vehicles:
        for i, sm in enumerate(vh.full_itinerary):
            if i < len(vh.full_itinerary) - 1:
                wg += data.data_segment[sm][vh.full_itinerary[i + 1]].price
    return wg


class PathFinding:
    bar = progressbar.ProgressBar(max_value=100)
    solutions = []

    def __init__(self, number_of_summit):
        pass

    def find_best_solution(self, data):
        av_weight = []
        for dt in self.solutions:
            wg = 0
            for vh in dt:
                for i, sm in enumerate(vh.full_itinerary):
                    if i < len(vh.full_itinerary) - 1:
                        wg += data.data_segment[sm][vh.full_itinerary[i + 1]].price
            av_weight.append(wg / len(dt))
        idx_bets_solution = av_weight.index(min(av_weight))
        return self.solutions[idx_bets_solution]

    def do(self, data, fx, number_of_loop=20):
        self.solutions = []

        def func(u, v, d = None):
            nonlocal data
            if data.data_segment[u][v] is None:
                return np.inf
            return data.data_segment[u][v].price

        def djikstra(g, frm, to):
            return nx.shortest_path(g, frm, to, func)[1:]

        def floyd_warshall(p, frm, to):
            return nx.reconstruct_path(frm, to, p)[1:]

        def a_star(g, frm, to):
            return nx.astar_path(g, frm, to, func)[1:]

        def vrp(f, g, frm, to, p):
            if f == "fw":
                return floyd_warshall(p, frm, to)
            elif f == "astar":
                return a_star(g, frm, to)
            else:
                return djikstra(g, frm, to)

        g = data.to_di_graph()
        # generate data for the algo
        if fx == "fw":
            predecessors, _ = nx.floyd_warshall_predecessor_and_distance(g)
        else:
            predecessors = None
        for i in range(number_of_loop):
            rand_summit = copy.deepcopy(data.data_summit)
            # shuffle the array of summit
            np.random.shuffle(rand_summit)
            np.random.shuffle(rand_summit)
            np.random.shuffle(rand_summit)
            smt_arr = [[] for x in range(data.number_of_kind_of_item)]

            vh_arr = [[] for x in range(data.number_of_kind_of_item)]
            # store the vehicles by kind
            for i, x in enumerate(data.data_vehicles):
                vh_arr[x.kind].append(data.data_vehicles.index(x))
            # sort the summits by item kind
            for smt in rand_summit:
                if smt.kind == 0:
                    smt_arr[smt.item_to_deliver.get('kind')].append(smt.id)
            # split the stop for each vehicles
            for t, s in enumerate(smt_arr):
                tp = np.array_split(np.array(s), len(vh_arr[t]))
                for z, x in enumerate(vh_arr[t]):
                    data.data_vehicles[x].itinerary = tp[z].tolist() + [
                        data.data_summit[data.warehouse[data.data_vehicles[x].kind]].id]
            # loop on all the vehicle itineraries, finding the shortest pah between stops
            vh_arr_cp = [copy.deepcopy(x) for x in data.data_vehicles]
            for vh in vh_arr_cp:
                vh.full_itinerary = [data.data_summit[data.warehouse[vh.kind]].id]
                for i in vh.itinerary:
                    if vh.stock - data.data_summit[i].item_to_deliver.get('qtt') < 0 and data.data_summit[i].kind == 0:
                        vh.load()
                        vh.full_itinerary += vrp(fx, g, vh.full_itinerary[-1],
                                                 data.data_summit[data.warehouse[vh.kind]].id, predecessors)
                    vh.full_itinerary += vrp(fx, g, vh.full_itinerary[-1], i, predecessors)
                    vh.stock -= data.data_summit[i].item_to_deliver.get('qtt')

            self.solutions.append(vh_arr_cp)
        # Store the best solution
        data.data_vehicles = self.find_best_solution(data)
