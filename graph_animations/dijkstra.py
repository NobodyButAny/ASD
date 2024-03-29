from random import randint

from graph_alorithms import *

inf = 1e7


def dijkstra(graph: WeightedGraph, start: Any):
    dist = {}
    prev = {}
    queue = []
    graph_list = graph.to_nested_dist_list()
    for v in graph.get_vertices():
        dist[v] = inf
        prev[v] = None
        queue.append(v)
    dist[start] = 0

    while queue:
        u = min(queue, key=lambda x: dist[x])
        queue.remove(u)
        for v, w in graph_list[u]:
            if v in queue:
                alt = dist[u] + w
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
    return dist, prev


def parse_path(map, start, to):
    res = []
    while to != start:
        res = [to] + res
        to = map[to]
    return res


if __name__ == "__main__":
    test = WeightedGraph()
    vertices = [0, 1, 2, 3, 4, 5, 6, 7]
    edges = [(0, 6), (0, 7), (1, 2), (1, 3), (1, 4),
             (1, 7), (2, 3), (5, 0), (5, 1), (5, 2),
             (6, 1), (6, 3)]
    test.add_vertices(*vertices)
    for a, b in edges:
        test.add_edges((a, b, randint(1, 7)))
    print(test)
    dist, path = dijkstra(test, 0)
    print(dist, path)
    target = 2
    print(f"Length to {target} from {0}:", dist[target])
    print(f"Path to {target}: ", parse_path(path, 0, 2))