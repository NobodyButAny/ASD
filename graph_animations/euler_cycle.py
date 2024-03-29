from manim import Scene, Graph, Create, ShowPassingFlash, BLUE, FadeOut, FadeToColor, GRAY, Flash

from graph_alorithms import *


def euler_cycle_heirholzer(graph_in: graph_nested_list):
    graph = graph_in.copy()
    edge_count = {}

    if len(graph) == 0:
        return []
    for i in range(len(graph)):
        edge_count[i] = len(graph[i])

    curr_path = [0]
    curr_v = 0
    cycle = []

    while curr_path:
        if edge_count[curr_v]:
            curr_path.append(curr_v)

            next_v = graph[curr_v][-1]
            edge_count[curr_v] -= 1
            graph[curr_v].pop()

            curr_v = next_v
        else:
            cycle.append(curr_v)
            curr_v = curr_path[-1]
            curr_path.pop()

    return list(reversed(cycle))


if __name__ == "__main__":
    test1 = [
        [1],
        [2],
        [0]
    ]
    test2 = [
        [1, 6],
        [2],
        [0, 3],
        [4],
        [2, 5],
        [0],
        [4]
    ]
    # cycle1 = euler_cycle_heirholzer(test1)
    # print(cycle1)
    # cycle2 = euler_cycle_heirholzer(test2)
    # print(cycle2)


class MainScene(Scene):
    def construct(self):
        graph = [
            [1, 6],
            [2],
            [0, 3],
            [4],
            [2, 5],
            [0],
            [4]
        ]
        vert, edges = to_connection_list(graph)
        print(vert, edges)
        cycle = euler_cycle_heirholzer(graph)
        graph_repr = Graph(
            vert,
            edges,
            labels=True,
            layout='kamada_kawai',
        )
        self.play(Create(graph_repr), run_time=3)

        self.play(Flash(graph_repr.vertices[cycle[0]]))

        for i in range(len(cycle) - 1):
            fr, to = cycle[i], cycle[i + 1]
            edge = graph_repr.edges[fr, to]
            self.play(FadeToColor(edge, color=GRAY))
            self.play(
                ShowPassingFlash(
                    edge.copy().set_color(BLUE),
                    time_width=0.7
                ),
                run_time=1
            )
            self.play(FadeOut(edge))
