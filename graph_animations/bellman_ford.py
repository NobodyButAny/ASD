from dataclasses import dataclass
from enum import Enum
from random import randint
from typing import Generic, TypeVar, Union

from manim import Scene, Graph, Text, FadeOut, Create

from graph_alorithms import *

inf = float('inf')
T = TypeVar('T')


@dataclass
class Result(Generic[T]):
    result: T


class OK(Result[T]):
    pass


class Error(Result[T]):
    pass


def bellman_ford(graph: WeightedGraph, source) -> Union[OK[tuple], Error[list]]:
    vertices = graph.get_vertices()
    edges = graph.get_edges()
    dist = {v: inf for v in vertices}
    prev = {v: None for v in vertices}
    dist[source] = 0

    for i in range(len(vertices) - 1):
        for edge in edges:
            a, b, weight = edge
            for _ in range(2):
                if dist[a] != inf and dist[a] + weight < dist[b]:
                    dist[b] = dist[a] + weight
                    prev[b] = a
                a, b = b, a

    for edge in edges:
        a, b, weight = edge
        if dist[a] != inf and dist[a] + weight < dist[b]:
            prev[b] = a
            visited = [False for i in vertices]
            visited[b] = True
            while not visited[a]:
                visited[a] = True
                a = prev[a]
            negative_cycle = [a]
            b = prev[a]
            while b != a:
                negative_cycle.append(b)
                b = prev[b]
            return Error(negative_cycle)
    return OK((dist, prev))


class MainScene(Scene):
    def bellman_ford_animation(self, graph: WeightedGraph, graph_repr: Graph, source):
        vertices = graph.get_vertices()
        edges = graph.get_edges()
        dist = {v: inf for v in vertices}
        prev = {v: None for v in vertices}
        dist[source] = 0
        # visuals
        labels = {}
        self.add(graph_repr)
        for vert in graph_repr.vertices:
            label = Text(str(dist[vert])).scale(0.5).next_to(graph_repr.vertices[vert])
            labels[vert] = label
            self.add(label)
        # relax
        for i in range(len(vertices) - 1):
            for edge in edges:
                a, b, weight = edge
                for _ in range(2):
                    if dist[a] != inf and dist[a] + weight < dist[b]:
                        dist[b] = dist[a] + weight
                        self.play(FadeOut(labels[b]))
                        labels[b] = Text(str(dist[b])).scale(0.5).next_to(graph_repr.vertices[b])
                        self.play(Create(labels[b]))
                        prev[b] = a
                    a, b = b, a

    def construct(self):
        test = WeightedGraph()
        vertices = [0, 1, 2, 3, 4, 5, 6, 7]
        edges = [(0, 6), (0, 7), (1, 2), (1, 3), (1, 4),
                 (1, 7), (2, 3), (5, 0), (5, 1), (5, 2),
                 (6, 1), (6, 3)]
        test.add_vertices(*vertices)
        for a, b in edges:
            test.add_edges((a, b, 2))
        print(test)
        print("Graph components: ")
        print(DFS.dfs_components(test.to_nested_list()), '\n')

        graph_visual = Graph(
            test.get_vertices(),
            [(a, b) for a, b, w in test.get_edges()],
            layout='kamada_kawai',
            labels=True
        )
        self.bellman_ford_animation(test, graph_visual, 0)

        match bellman_ford(test, 0):
            case OK(result):
                dist, path = result
                for k in dist:
                    print(k, dist[k])
            case Error(result):
                cycle = result
