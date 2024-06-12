"""
Autor: Duarte Velho

Implementação do algotitmo de Grafos Pesados, com a implementação do algoritmo de Dijkstra 
para encontrar o caminho mais curto entre dois vértices de um grafo.
Código escrito por Duarte Velho que teve por código base, o retirado dos powerpoints das aulas (autoria de Rui Mendes)

Documentação e type hiting gerada por Duarte Velho
"""

import subprocess
import graphviz
import heapq
from Grafos import MyGraph

class WeightedGraph(MyGraph):
    """
    This class extends MyGraph to implement a weighted graph with methods to manipulate and analyze the graph.
    It provides methods to add vertices and edges, print the graph, visualize it using Graphviz, and find shortest paths using Dijkstra's algorithm.

    Attributes
    ----------
    graph : Dict[str, List[Tuple[str, int]]]
        Stores the graph where keys are vertex identifiers and values are lists of tuples (vertex, weight) representing weighted edges.

    """
    def __init__(self, g : dict[str, list[tuple[str, int]]] = {}):
        """
        Initializes the WeightedGraph with an optional graph dictionary.

        Parameters
        ----------
        g : Dict[str, List[Tuple[str, int]]], optional
            A dictionary to initialize the graph where keys are vertices and values are lists of edges with weights. 
            Defaults to an empty dictionary.
        """
        self.graph = g  

    def print_graph(self):
        """
        Prints the graph in the adjacency list format, where each vertex is shown along with its edges 
        and corresponding weights.
        """
        for v in self.graph.keys():
            print(v, " -> ", self.graph[v])

    def add_vertex(self, v : str):
        """
        Adds a vertex to the graph if it does not already exist.

        Parameters
        ----------
        v : str
            The vertex identifier to be added to the graph.
        """
        if v not in self.graph:
            self.graph[v] = []

    def add_edge(self, o : str, d : str, w : int):
        """
        Adds a weighted edge to the graph. If the origin or destination vertices do not exist, they are created.

        Parameters
        ----------
        o : str
            The origin vertex identifier.
        d : str
            The destination vertex identifier.
        w : int
            The weight of the edge.
        """
        if o not in self.graph:
            self.add_vertex(o)
        if d not in self.graph:
            self.add_vertex(d)
        self.graph[o].append((d, w))

    def get_edges(self) -> list[tuple[str, str, int]]:
        """
        Retrieves all edges in the graph as a list of tuples.

        Returns
        -------
        List[Tuple[str, str, int]]
            A list containing all edges in the graph, each represented as a tuple (origin, destination, weight).
        """
        edges = []
        for v in self.graph.keys():
            for (d, w) in self.graph[v]:
                edges.append((v, d, w))
        return edges
    
    def visualize(self):
        """
        Generates a visual representation of the graph using Graphviz and saves it as a PNG image.
        """
        dot = graphviz.Digraph(comment='Weighted Graph', format='png')  
        for v in self.graph:
            dot.node(v, v)  
        for v in self.graph:
            for (d, w) in self.graph[v]:
                dot.edge(v, d, label=str(w))  
        dot.render('output/weighted_graph', view=True)

    def dijkstra(self, start : str) -> dict[str, float]:
        """
        Implements Dijkstra's algorithm to find the shortest path from a starting vertex to all other vertices in the graph.

        Parameters
        ----------
        start : str
            The starting vertex for calculating shortest paths.

        Returns
        -------
        Dict[str, float]
            A dictionary where keys are vertex identifiers and values are the shortest distances from the start vertex.
        """
        min_heap = []
        visited = set()
        distances = {vertex: float('infinity') for vertex in self.graph}
        distances[start] = 0

        heapq.heappush(min_heap, (0, start))

        while min_heap:
            current_distance, current_vertex = heapq.heappop(min_heap)

            if current_vertex in visited:
                continue

            visited.add(current_vertex)

            for neighbor, weight in self.graph[current_vertex]:
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(min_heap, (distance, neighbor))

        return distances

def main():
    g = {
        'A': [('B', 2), ('C', 5)],
        'B': [('C', 1), ('D', 4)],
        'C': [('D', 1)],
        'D': [],
        'E': [('F', 3)],
        'F': [('C', 3)]
    }
    graph = WeightedGraph(g)
    graph.print_graph()
    print("Edges in the graph:", graph.get_edges())
    distances = graph.dijkstra('A')
    print("Shortest paths from 'A':", distances)
    graph.visualize()

if __name__ == "__main__":
    main()

    print("Metricas de Codigo:")
    print("\nMetrica cyclomatic complexity:")
    print(subprocess.call(["radon","cc","Grafos/grafos_pesados.py", "-s"]))
    print("\nMetrica maintainability index:")
    print(subprocess.call(["radon","mi","Grafos/grafos_pesados.py", "-s"]))
    print("\nMetrica raw:")
    print(subprocess.call(["radon","raw","Grafos/grafos_pesados.py", "-s"]))