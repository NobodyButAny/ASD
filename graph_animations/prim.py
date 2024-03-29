from random import randint

from leftist_heap import *
from graph_alorithms import *


def prim_mst(graph: WeightedGraph):
    mst = WeightedGraph()
    graph_adj = graph.to_nested_dist_list()
    queue = LeftistHeap()
    queue.insert([0, (graph[0], graph[0])])
    used = {v: False for v in graph.get_vertices()}
    while not queue.is_empty():
        candidate = queue.pop_min()
        dist, (prev, vert) = candidate
        if used[vert]:
            continue
        used[vert] = True
        mst.add_edges((prev, vert, dist))
        for adj, dist in graph_adj[vert]:
            if not used[adj]:
                queue.insert([dist, (vert, adj)])
    return mst


if __name__ == "__main__":
    test = WeightedGraph()
    test.add_vertices(range(6))
    for i in range(12):
        test.add_edges((randint(0, 6), randint(0, 6), randint(1, 10)))
    print("Graph: ", test, sep='\n')
    print("MST: ", prim_mst(test), sep='\n')
