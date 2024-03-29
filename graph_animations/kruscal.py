from typing import Any

from disjoint_set_union import DisjointSetUnion
from graph_alorithms import *
from random import randint


def kruscal_mst(graph: WeightedGraph):
    forest = WeightedGraph()
    edges = sorted(graph.get_edges(), key=lambda x: x[2])
    components = DisjointSetUnion()
    components.add_disjoint_set(graph.get_vertices())
    for edge in edges:
        from_, to_, weight = edge
        if components.leader(from_) != components.leader(to_):
            components.unite(from_, to_)
            forest.add_edges(edge)
    return forest


if __name__ == "__main__":
    test = WeightedGraph()
    test.add_vertices(range(6))
    for i in range(12):
        test.add_edges((randint(0, 6), randint(0, 6), randint(1, 10)))
    forest = kruscal_mst(test)
    print("Test: \n", test)
    print("Forest: \n", forest)
    print("Components: ")
    print(BFS.bfs_components_proper(test.to_nested_list()), BFS.bfs_components_proper(forest.to_nested_list()))
