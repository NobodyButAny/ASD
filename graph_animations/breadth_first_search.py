from manim import *
import graph_alorithms as ga
from graph_alorithms import graph_nested_list


class MainScene(Scene):
    def bfs(self, graph: graph_nested_list, graph_visual: Graph, s=0):
        queue = [s]
        dist = [-1 for i in graph]
        dist[s] = 0
        self.play(FadeToColor(graph_visual[s + 1], color=GOLD))
        while queue:
            vertex = queue.pop(0)
            for adj in graph[vertex]:
                if dist[adj] == -1:
                    queue.append(adj)
                    dist[adj] = dist[vertex] + 1

                    length_label = MathTex(str(dist[adj]), color=BLACK)
                    length_label.move_to(graph_visual[adj + 1].get_center())

                    try:
                        edge = graph_visual.edges[adj + 1, vertex + 1]
                    except:
                        edge = graph_visual.edges[vertex + 1, adj + 1]
                    self.play(ShowPassingFlash(
                        edge.copy().set_color(YELLOW).set_z_index(2),
                        time_width=1.0
                    ))
                    self.play(
                        FadeIn(length_label),
                        Circumscribe(graph_visual[adj + 1])
                    )

    def construct(self):
        vertices = [1, 2, 3, 4, 5, 6, 7, 8]
        edges = [(1, 7), (1, 8), (2, 3), (2, 4), (2, 5),
                 (2, 8), (3, 4), (6, 1), (6, 2),
                 (6, 3), (7, 2), (7, 4)]
        graph = Graph(vertices, edges,
                      layout='kamada_kawai',
                      layout_scale=3,
                      vertex_config={"radius": MathTex('a').height}
                      )
        self.play(Create(graph), run_time=2)
        self.bfs(ga.from_connection_list(vertices, edges), graph)
        self.wait(1)
