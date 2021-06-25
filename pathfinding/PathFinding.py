import networkx as nx
import progressbar


class PathFinding:
    p2p_array = []
    max_hop = 3
    kind_of_object = 4
    bar = progressbar.ProgressBar(max_value=100)
    step_kind = [1000, 200, 100, 50]
    def __init__(self, number_of_summit):
        self.p2p_array = [[[] for j in range(number_of_summit)] for i in range(number_of_summit)]

    def generate_best_road(self, data):

        def func(u, v, d):
            nonlocal data
            if data.data_segment[u][v] is None:
                return 0
            print(data.data_segment[u][v].price)
            return data.data_segment[u][v].price
        self.p2p_array = [[nx.dijkstra_path(data.to_di_graph(), i, j, func) for j in range(len(data.data_matrix))] for i
                          in range(len(data.data_matrix))]

    def do(self, data):
        def func(u, v, d):
            nonlocal data
            if data.data_segment[u][v] is None:
                return 0
            return data.data_segment[u][v].price

        smt_arr = [[data.data_summit[data.warehouse]] for x in range(self.kind_of_object)]
        full_smt_arr = [[data.data_summit[data.warehouse].id] for x in range(self.kind_of_object)]
        smt_sum = [0 for x in range(self.kind_of_object)]
        g = data.to_di_graph()
        for smt in data.data_summit:
            if smt.kind == 0:
                if smt_sum[smt.item_to_deliver.get('kind')] + smt.item_to_deliver.get('qtt') > self.step_kind[smt.item_to_deliver.get('kind')]:
                    smt_sum[smt.item_to_deliver.get('kind')] = 0
                    smt_arr[smt.item_to_deliver.get('kind')].append(data.data_summit[data.warehouse])
                    full_smt_arr[smt.item_to_deliver.get('kind')] += nx.dijkstra_path(g, full_smt_arr[smt.item_to_deliver.get('kind')][-1], data.warehouse, func)[1:]
                print(full_smt_arr[smt.item_to_deliver.get('kind')][-1])
                full_smt_arr[smt.item_to_deliver.get('kind')] += nx.dijkstra_path(g, full_smt_arr[smt.item_to_deliver.get('kind')][-1], smt.id, func)[1:]
                smt_arr[smt.item_to_deliver.get('kind')].append(smt)
                smt_sum[smt.item_to_deliver.get('kind')] += smt.item_to_deliver.get('qtt')

        for x in smt_arr:
            x.append(data.data_summit[data.warehouse])
        for x in full_smt_arr:
            x += nx.dijkstra_path(g, x[-1], data.warehouse, func)[1:]
        print(smt_arr)
        print(full_smt_arr)
        for asm in full_smt_arr:
            print("\n___________")
            sum = 0
            i = 1
            for sm in asm:
                print(sm, "-> ", end = '')

                i += 1
        for asm in smt_arr:
            print("\n___________")
            for sm in asm:
                print(f"{sm.id}", "-> ", end = '')
                # if sm.kind == 1:
                #     sum = 0
                # else:
                #     sum += sm.item_to_deliver.get('qtt')
                # print(f"{sm.id} type {sm.kind} : {sum}")
                # print("|")
