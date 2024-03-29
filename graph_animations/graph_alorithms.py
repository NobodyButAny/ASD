import random
import timeit
from typing import Any

# parsed = [
#     [1, 2],  # 0
#     [0, 3],  # 1
#     [0, 3],  # 2
#     [1, 2, 6],  # 3
#     [5],  # 4
#     [4],  # 5
#     [3]
# ]

graph_nested_list = list[list[int]]
graph_adjacency_matrix = list[list[int]]


def to_nested_list(matr: graph_adjacency_matrix) -> graph_nested_list:
    res = [[] for row in matr]
    for i, row in enumerate(matr):
        for j, el in enumerate(row):
            if el == 1:
                res[i].append(j)
    return res


def to_adj_matrix(nested_list: graph_nested_list, undirected=True) -> graph_adjacency_matrix:
    res = [[0 for i in nested_list] for i in nested_list]
    for i, row in enumerate(nested_list):
        for el in row:
            res[i][el] = 1
            if undirected:
                res[el][i] = 1
    return res


def to_connection_list(nested_list: graph_nested_list) -> tuple[list, list]:
    """
    Returns:
        vertices - list of vertex indices

        edges - list of connections (vertex, vertex)
    """
    vertices_ = [i for i in range(len(nested_list))]
    edges_ = [(vert, peer) for vert, con in enumerate(nested_list) for peer in con]
    return vertices_, edges_


def from_connection_list(vertices: list, edges: list, undirected=True) -> graph_nested_list:
    vertices_ = vertices.copy()
    edges_ = edges.copy()
    if 0 not in vertices_:
        for i, _ in enumerate(vertices_):
            vertices_[i] -= 1
        for i, edge in enumerate(edges_):
            edges_[i] = tuple(i - 1 for i in edge)
    res = [[] for i in vertices_]
    for edge in edges_:
        res[edge[0]].append(edge[1])
        if undirected:
            res[edge[1]].append((edge[0]))
    return res


def print_paths(graph: graph_nested_list):
    print(*[f"{i} -> {el}" for i, el in enumerate(graph)], sep='\n')


def flatten(nest: list) -> list:
    return [el for ls in nest for el in ls]


class WeightedGraph:
    def __init__(self):
        self.__vertices = []
        self.__edges = []

    def add_vertices(self, *vert):
        for i in vert:
            self.__vertices.append(i)

    def add_edges(self, *edges):
        for fr, t, w in edges:
            if fr == t:
                continue
            if fr not in self.__vertices:
                self.__vertices.append(fr)
            if t not in self.__vertices:
                self.__vertices.append(t)
            self.__edges.append((fr, t, w))

    def remove_vertex(self, vert):
        if vert not in self.__vertices:
            return
        self.__vertices.remove(vert)
        for edge in self.__edges:
            a, b, _ = edge
            if a == vert or b == vert:
                self.__edges.remove(edge)

    def get_vertices(self):
        return self.__vertices.copy()

    def get_edges(self) -> list[tuple[Any, Any, int]]:
        return self.__edges.copy()

    def __getitem__(self, item):
        return self.__vertices[item]

    def __str__(self):
        res = ''
        res += "vertices: "
        res += str(self.__vertices) + '\n'
        res += "edges:\n"
        for i in self.__edges:
            res += str(i) + '\n'
        return res

    def to_nested_list(self) -> graph_nested_list:
        res = [[] for i in range(max(self.__vertices) + 1)]
        for from_, to_, _ in self.__edges:
            res[from_].append(to_)
            res[to_].append(from_)
        return res

    def to_nested_dist_list(self) -> list[list[int]]:
        res = [[] for i in range(max(self.__vertices) + 1)]
        for from_, to_, weight in self.__edges:
            res[from_].append([to_, weight])
            res[to_].append([from_, weight])
        return res


class BFS:
    @staticmethod
    def bfs(graph: graph_nested_list, s: int = 0) -> list[int]:
        queue = [s]
        dist = [-1 for i in graph]
        dist[s] = 0
        while queue:
            vertex = queue.pop(0)
            for adj in graph[vertex]:
                if dist[adj] == -1:
                    queue.append(adj)
                    dist[adj] = dist[vertex] + 1
        return dist

    @staticmethod
    def bfs_components_proper(graph: graph_nested_list):
        components = [[]]
        queue = [0]
        visited = [False for i in graph]
        visited[0] = True
        while queue:
            vert = queue.pop()
            components[-1].append(vert)
            for adj in graph[vert]:
                if not visited[adj]:
                    queue.append(adj)
                    visited[adj] = True
            if (not queue) and (False in visited):
                queue.append(visited.index(False))
                visited[visited.index(False)] = True
                components.append([])
        return components

    @staticmethod
    def bfs_components(graph: graph_nested_list) -> list:
        components = []
        visited = []
        prev = BFS.bfs(graph)
        components.append([i for i, el in enumerate(prev) if el != -1])
        while -1 in prev:
            try:
                while (nx := prev.index(-1)) in visited:
                    prev[nx] = 0
            except ValueError:
                break

            prev = BFS.bfs(graph, nx)
            components.append([i for i, el in enumerate(prev) if el != -1])
            visited = flatten(components)
        return components


class DFS:
    @staticmethod
    def dfs(graph: graph_nested_list, start: int, visited=None):
        if visited is None:
            visited = []
        queue = [start]
        while queue:
            vert = queue.pop()
            if vert in visited:
                continue
            visited.append(vert)
            for adj in graph[vert]:
                if adj not in visited:
                    queue.append(adj)
        return visited

    @staticmethod
    def dfs_recursive(graph: graph_nested_list, start: int, visited=None):
        if visited is None:
            visited = [False for _ in graph]
        visited[start] = True
        for adj in graph[start]:
            if not visited[adj]:
                DFS.dfs_recursive(graph, adj, visited)
        return visited

    @staticmethod
    def dfs_trace(graph: graph_nested_list, from_: int, to_: int, visited=None):
        if from_ == to_:
            return True
        if visited is None:
            visited = [False] * len(graph)
        visited[from_] = True
        for adj in graph[from_]:
            if not visited[adj]:
                if DFS.dfs_trace(graph, adj, to_, visited):
                    return True
        return False

    @staticmethod
    def dfs_recursive_memo(graph: graph_nested_list, start: int, visited=None, memo=None):
        if visited is None:
            visited = [False for _ in graph]
        if memo is None:
            memo = []
        visited[start] = True
        memo.append(start)
        for adj in graph[start]:
            if not visited[adj]:
                DFS.dfs_recursive_memo(graph, adj, visited, memo)
        return visited, memo

    @staticmethod
    def dfs_components(graph: graph_nested_list):
        if len(graph) == 0:
            return 0
        components = []
        visited, memo = DFS.dfs_recursive_memo(graph, 0)
        components.append(memo)
        while False in visited:
            visited, memo = DFS.dfs_recursive_memo(graph, visited.index(False), visited)
            components.append(memo)
        return components

    @staticmethod
    def dfs_strong_components(graph: graph_nested_list):
        components = []
        in_component = [False] * len(graph)
        for i in range(len(graph)):
            if not in_component[i]:
                component = [i]
                for j in range(i + 1, len(graph)):
                    if (
                            not in_component[j]
                            and DFS.dfs_trace(graph, i, j)
                            and DFS.dfs_trace(graph, j, i)
                    ):
                        in_component[j] = True
                        component.append(j)
                components.append(component)
        return components


directed_graph = [
    [1],  # 0
    [2, 3],  # 1
    [0, 6],  # 2
    [4, 5, 6],  # 3
    [5],  # 4
    [3],  # 5
    []  # 6
]

matrix = [
    [0, 1, 1, 0, 0, 0],
    [1, 0, 0, 1, 0, 0],
    [1, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1, 0],
]

parsed = to_nested_list(matrix)


# print(parsed)
# print(*to_adj_matrix(parsed), sep='\n', end='\n \n')
# print(*to_connection_list(parsed), sep='\n')


def test_speed():
    dumb_bfs_components = timeit.timeit(
        lambda: BFS.bfs_components(parsed),
        number=50000
    )
    print(f"dumb_bfs_components: {dumb_bfs_components}")
    proper_bfs_components = timeit.timeit(
        lambda: BFS.bfs_components_proper(parsed),
        number=50000
    )
    print(f"proper_bfs_components: {proper_bfs_components}")
    iterative_dfs = timeit.timeit(
        lambda: DFS.dfs(parsed, random.randint(0, len(parsed) - 1)),
        number=50000
    )
    print("--")
    print(f"iterative_dfs: {iterative_dfs}")
    recursive_dfs = timeit.timeit(
        lambda: DFS.dfs_recursive(parsed, random.randint(0, len(parsed) - 1)),
        number=50000
    )
    print(f"recursive_dfs: {recursive_dfs}")
    memo_dfs = timeit.timeit(
        lambda: DFS.dfs_recursive_memo(parsed, random.randint(0, len(parsed) - 1)),
        number=50000
    )
    print(f"memo_dfs: {memo_dfs}")
    print("--")
    components_dfs = timeit.timeit(
        lambda: DFS.dfs_components(parsed),
        number=50000
    )
    print(f"dfs_components: {components_dfs}")
    strong_components_dfs = timeit.timeit(
        lambda: DFS.dfs_strong_components(directed_graph),
        number=50000
    )
    print(f"dfs_strong_components: {strong_components_dfs}")

# test_speed()
# print("--")
# print("Graph:")
# print_paths(parsed)
# print("--")
# print(BFS.bfs(parsed))
# print(DFS.dfs_components(parsed))
# print(BFS.bfs_components(parsed))
# print(DFS.dfs_strong_components(oriented_graph))
