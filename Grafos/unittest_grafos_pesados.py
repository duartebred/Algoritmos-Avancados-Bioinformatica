import unittest
from grafos_pesados import WeightedGraph  

class TestWeightedGraph(unittest.TestCase):
    def setUp(self):
        self.graph = WeightedGraph()
        self.vertices = ['A', 'B', 'C', 'D', 'E', 'F']
        self.edges = [('A', 'B', 2), ('A', 'C', 5), ('B', 'C', 1), ('B', 'D', 4), ('C', 'D', 1), ('E', 'F', 3), ('F', 'C', 3)]

        for vertex in self.vertices:
            self.graph.add_vertex(vertex)

        for origin, dest, weight in self.edges:
            self.graph.add_edge(origin, dest, weight)

    def test_add_vertex(self):
        self.graph.add_vertex('G')
        self.assertIn('G', self.graph.graph)
        self.assertEqual(len(self.graph.graph['G']), 0)

    def test_add_edge(self):
        self.graph.add_edge('A', 'E', 10)
        self.assertIn(('E', 10), self.graph.graph['A'])
        self.graph.add_edge('E', 'G', 1)  
        self.assertIn(('G', 1), self.graph.graph['E']) 

    def test_visualize_graph(self):
        self.graph.visualize()  

if __name__ == '__main__':
    unittest.main()
