import unittest
from Grafos import MyGraph

class TestMyGraph(unittest.TestCase):

    def setUp(self):
        self.graph = MyGraph()

    def test_graph_basic_operations(self):
        self.graph.add_vertex('A')
        self.graph.add_edge('A', 'B')
        edges = self.graph.get_edges()
        nodes = self.graph.get_nodes()
        size = self.graph.size()
        
        self.assertEqual(edges, [('A', 'B')])
        self.assertIn('A', self.graph.get_nodes())
        self.assertEqual(nodes, ['A', 'B'])
        self.assertEqual(size, (2, 1))
        
    def test_get_successors_predecessors_and_adjacents(self):
        self.graph.add_vertex('A')
        self.graph.add_vertex('B')
        self.graph.add_edge('A', 'B')
        adjacents = self.graph.get_adjacents('A')
        successors = self.graph.get_successors('A')
        predecessors = self.graph.get_predecessors('B')
        self.assertEqual(successors, ['B'])
        self.assertEqual(predecessors, ['A'])
        self.assertEqual(adjacents, ['B'])
        
    def test_out_degree(self):
        self.graph.add_vertex('A')
        self.graph.add_vertex('B')
        self.graph.add_edge('A', 'B')
        out_degree = self.graph.out_degree('A')
        self.assertEqual(out_degree, 1)
        
    def test_in_degree(self):
        self.graph.add_vertex('A')
        self.graph.add_vertex('B')
        self.graph.add_edge('A', 'B')
        in_degree = self.graph.in_degree('B')
        self.assertEqual(in_degree, 1)
        
    def test_degree(self):
        self.graph.add_vertex('A')
        self.graph.add_vertex('B')
        self.graph.add_vertex('C')
        self.graph.add_edge('A', 'B')
        self.graph.add_edge('B', 'C')
        degree = self.graph.degree('B')
        self.assertEqual(degree, 2)
        
    def test_reachable_bfs(self):
        self.graph.add_vertex('A')
        self.graph.add_vertex('B')
        self.graph.add_vertex('C')
        self.graph.add_vertex('D')
        self.graph.add_edge('A', 'B')
        self.graph.add_edge('B', 'C')
        self.graph.add_edge('A', 'D')
        reachable = self.graph.reachable_bfs('A')
        self.assertEqual(reachable, ['B', 'D','C'])
        
    def test_reachable_dfs(self):
        self.graph.add_vertex('A')
        self.graph.add_vertex('B')
        self.graph.add_vertex('C')
        self.graph.add_edge('A', 'B')
        self.graph.add_edge('B', 'C')
        reachable = self.graph.reachable_dfs('A')
        self.assertEqual(reachable, ['B', 'C'])
        
    def test_distance(self):
        self.graph.add_vertex('A')
        self.graph.add_vertex('B')
        self.graph.add_vertex('C')
        self.graph.add_edge('A', 'B')
        self.graph.add_edge('B', 'C')
        distance = self.graph.distance('A', 'C')
        self.assertEqual(distance, 2)
        
    def test_shortest_path(self):
        self.graph.add_vertex('A')
        self.graph.add_vertex('B')
        self.graph.add_vertex('C')
        self.graph.add_edge('A', 'B')
        self.graph.add_edge('B', 'C')
        path = self.graph.shortest_path('A', 'C')
        self.assertEqual(path, ['A', 'B', 'C'])
        
    def test_node_has_cycle(self):
        self.graph.add_vertex('A')
        self.graph.add_vertex('B')
        self.graph.add_vertex('C')
        self.graph.add_edge('A', 'B')
        self.graph.add_edge('B', 'C')
        self.graph.add_edge('C', 'A')
        self.assertTrue(self.graph.node_has_cycle('A'))
        
    def test_has_cycle(self):
        self.graph.add_vertex('A')
        self.graph.add_vertex('B')
        self.graph.add_vertex('C')
        self.graph.add_edge('A', 'B')
        self.graph.add_edge('B', 'C')
        self.graph.add_edge('C', 'A')
        self.assertTrue(self.graph.has_cycle())
        

if __name__ == '__main__':
    unittest.main()
