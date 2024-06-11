import subprocess

## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node


class MyGraph:
    """
    This class implements a graph structure with methods to manipulate and analyze the graph. It supports directed,
    undirected, and weighted edges.

    Parameters
    ----------
    g : dict, optional
        A dictionary representing the graph where keys are vertex identifiers and values are lists of adjacent
        vertices or tuples (vertex, weight) for weighted edges. Default is None, initializing an empty graph.

    Attributes
    ----------
    graph : dict
        Stores the graph where keys are vertices and values are lists of adjacent vertices or tuples for weighted edges.
    id : str
        Identifier for the type of graph, either 'gr' for graphs without weighted edges or 'grw' for graphs with weighted edges.
    """

    def __init__(self, g = None) -> None:
        """
        Initializes the MyGraph class with an optional graph dictionary. If no dictionary is provided, an empty graph is initialized.

        Parameters
        ----------
        g 
            A dictionary to initialize the graph. The dictionary keys are vertices and values are lists of adjacent vertices
            or tuples for weighted edges. Default is None.
        """
        self.graph = g if g else {}  
        self.id = self.id_graph() if g else None  
        if g:
            for vertex, neighbors in g.items():
                self.add_vertex(vertex)  
                for neighbor in neighbors:
                    if isinstance(neighbor, tuple):
                        self.add_edge(vertex, neighbor[0], neighbor[1])  
                    else:
                        self.add_edge(vertex, neighbor)  

    def print_graph(self):
        """
        Prints the content of the graph in the form of an adjacency list. Each vertex and its edges are displayed.
        """
        for v in self.graph.keys():
            print(v, " -> ", self.graph[v])  


    def id_graph(self) -> str:
        """
        Determines the type of the graph based on the presence of weighted edges in the adjacency list.

        Returns
        -------
        str
            Returns 'grw' if any of the edges are weighted (i.e., tuple format), otherwise returns 'gr'.
        """
        has_weighted_edges = False

        for key in self.graph.keys():
            for neighbor in self.graph[key]:
                if isinstance(neighbor, tuple):
                    has_weighted_edges = True
                    break

        return 'grw' if has_weighted_edges else 'gr'
    

    def get_nodes(self) -> list:
        """
        Retrieves a list of all nodes in the graph.

        Returns
        -------
        List
            A list containing all the nodes (vertices) of the graph.
        """
        return list(self.graph.keys())
    
        
    def get_edges(self) -> list:
        """
        Retrieves all edges in the graph. Edges are returned as a list of tuples. If the graph is weighted, tuples include weights.

        Returns
        -------
        List
            A list of tuples representing the edges. Each tuple is (origin, destination) for unweighted edges,
            or (origin, destination, weight) for weighted edges.
        """
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                if type(d)==tuple:edges.append((v,d[0],d[1]))
                else: edges.append((v,d))
        return edges
    
      
    def size(self) -> tuple[int, int]:
        """
        Retrieves the size of the graph in terms of the number of nodes and the number of edges.

        Returns
        -------
        Tuple[int, int]
            A tuple containing two integers: the number of nodes and the number of edges.
        """
        return len(self.get_nodes()), len(self.get_edges())


    def add_vertex(self, v):
        """
        Adds a vertex to the graph if it does not already exist.

        Parameters
        ----------
        v
            The vertex identifier to add to the graph.
        """
        if v not in self.graph.keys():
            self.graph[v] = []
            
            
    def add_edge(self, o, d, p = 'bin'):
        """
        Adds an edge to the graph. Vertices are added to the graph if they do not exist. If the graph is weighted and a weight is provided, it is used; otherwise, the edge is considered unweighted.

        Parameters
        ----------
        o 
            The origin vertex identifier.
        d 
            The destination vertex identifier.
        p 
            The weight of the edge if the graph is weighted. Defaults to None for unweighted graphs.
        """

        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        if d not in self.graph[o] and p == 'bin':
            self.graph[o].append(d)
        else: self.graph[o].append((d,p))
            
        
    def get_successors(self, v) -> list:
        """
        Returns a list of successors of a given vertex in the graph. If the graph is weighted, only vertex identifiers are returned.

        Parameters
        ----------
        v 
            The vertex identifier for which successors are to be retrieved.

        Returns
        -------
        List
            A list of successors of the given vertex. For weighted graphs, successors are returned without weights.
        """
        if self.id == 'gr':
            return list(self.graph[v])
        else:
            res = []
            for n in self.graph[v]:
                res.append(n[0])
            return res


    def get_predecessors(self, v) -> list:
        '''
        Returns a list of predecessors of a given vertex in the graph.

        Parameters
        ----------
        v 
            The vertex for which predecessors are to be retrieved.

        Returns
        -------
        list
            List of predecessors of the given vertex.
        '''
        if self.id == 'gr':
            res = [i for i in self.graph.keys() if v in self.graph[i]]
        else:
            res = []
            for i in self.graph.keys():
                for j in self.graph[i]:
                    if v == j[0]:
                        res.append(i)
        return res


    def get_adjacents(self, v) -> list:
        '''
        Returns a list of adjacent vertices of a given vertex in the graph.

        Parameters
        ----------
        v 
            The vertex for which adjacent vertices are to be retrieved.

        Returns
        -------
        list
            List of adjacent vertices of the given vertex.
        '''
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)

        res = pred

        for p in suc:
            if p not in res:
                res.append(p)

        return res 
    

    def out_degree(self, v) -> int:
        '''
        Returns the out-degree of a given vertex in the graph.

        Parameters
        ----------
        v
            The vertex for which out-degree is to be calculated.

        Returns
        -------
        int
            The out-degree of the given vertex.
        '''
        return len(self.graph[v])

    def in_degree(self, v) -> int:
        '''
        Returns the in-degree of a given vertex in the graph.

        Parameters
        ----------
        v
            The vertex for which in-degree is to be calculated.

        Returns
        -------
        int
            The in-degree of the given vertex.
        '''
        return len(self.get_predecessors(v))

    def degree(self, v) -> int:
        '''
        Returns the degree of a given vertex in the graph.

        Parameters
        ----------
        v
            The vertex for which degree is to be calculated.

        Returns
        -------
        int
            The degree of the given vertex.
        '''
        return len(self.get_adjacents(v))

        
    def reachable_bfs(self, v) -> list:
        '''
        Performs a breadth-first search (BFS) traversal starting from a given vertex in the graph.

        Parameters
        ----------
        v
            The starting vertex for the BFS traversal.

        Returns
        -------
        list
            A list of vertices reachable from the starting vertex v in the graph.
        '''
        l = [v]  
        res = []  
        while len(l) > 0:
            node = l.pop(0)  
            if node != v:
                res.append(node)  
            for elem in self.graph[node]:
                if elem not in res and elem not in l and elem != node:
                    l.append(elem)  
        return res

        
    def reachable_dfs(self, v) -> list:
        '''
        Performs a depth-first search (DFS) traversal starting from a given vertex in the graph.

        Parameters
        ----------
        v
            The starting vertex for the DFS traversal.

        Returns
        -------
        list
            A list of vertices reachable from the starting vertex v in the graph.
        '''
        l = [v]  
        res = []  
        while len(l) > 0:
            node = l.pop(0)  
            if node != v:
                res.append(node)  
            s = 0
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem)  
                    s += 1
        return res
    
    
    def distance(self, s, d):
        '''
        Finds the shortest distance between two vertices in the graph using breadth-first search (BFS).

        Parameters
        ----------
        s 
            The source vertex.
        d 
            The destination vertex.

        Returns
        -------
        int or None
            The shortest distance between vertices s and d in the graph, or None if no path exists.
        '''
        if s == d:
            return 0
        l = [(s, 0)]  
        visited = [s]  
        while len(l) > 0:
            node, dist = l.pop(0)  
            for elem in self.graph[node]:
                if elem == d:
                    return dist + 1  
                elif elem not in visited:
                    l.append((elem, dist + 1))  
                    visited.append(elem)  
        return None  

        
    def shortest_path(self, s, d):
        
        if s == d: return []
        l = [(s, [])]
        visited = [s]
        while len(l) > 0:
            node, preds = l.pop(0)
            for elem in self.graph[node]:
                if elem == d:
                    return preds + [node, elem]
                elif elem not in visited:
                    l.append((elem, preds + [node]))
                    visited.append(elem)
        return None
        
    def shortest_path(self, s, d):
        '''
        Finds the shortest path between two vertices in the graph using breadth-first search (BFS).

        Parameters
        ----------
        s
            The source vertex.
        d
            The destination vertex.

        Returns
        -------
        list or None
            The shortest path between vertices s and d in the graph as a list of vertices, or None if no path exists.
        '''
        if s == d:
            return []  
        l = [(s, [])]  
        visited = [s]  
        while len(l) > 0:
            node, path = l.pop(0)  
            for elem in self.graph[node]:
                if elem == d:
                    return path + [node, elem]  
                elif elem not in visited:
                    l.append((elem, path + [node]))  
                    visited.append(elem)  
        return None  


    def node_has_cycle(self, v) -> bool:
        '''
        Checks if there is a cycle containing a given vertex in the graph using breadth-first search (BFS).

        Parameters
        ----------
        v
            The vertex to check for cycles.

        Returns
        -------
        bool
            True if there is a cycle containing vertex v, False otherwise.
        '''
        l = [v]  
        visited = [v]  
        while len(l) > 0:
            node = l.pop(0)  
            for elem in self.graph[node]:
                if elem == v:
                    return True  
                elif elem not in visited:
                    l.append(elem)  
                    visited.append(elem)  
        return False 


    def has_cycle(self) -> bool:
        '''
        Checks if the graph contains at least one cycle using breadth-first search (BFS).

        Returns
        -------
        bool
            True if the graph contains at least one cycle, False otherwise.
        '''
        res = False  
        for v in self.graph.keys():
            if self.node_has_cycle(v):
                return True  
        return res  


    def is_in_tuple_list(tl, val):
        '''
        Checks if a value is present in the first element of each tuple in a list of tuples.

        Parameters
        ----------
        tl
            The list of tuples to search.
        val
            The value to search for.

        Returns
        -------
        bool
            True if the value is found in any tuple's first element, False otherwise.
        '''
        res = False  
        for (x, y) in tl:
            if val == x:
                return True  
        return res  


if __name__ == "__main__":
    graph = MyGraph()

    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_vertex('C')

    graph.add_edge('A', 'B')
    graph.add_edge('B', 'C')
    graph.add_edge('C', 'A')

    print("Graph:")
    graph.print_graph()

    print("\nGraph nodes:")
    print(graph.get_nodes())

    print("\nGraph edges:")
    print(graph.get_edges())

    print("\nGraph size:")
    print("Number of nodes:", graph.size()[0])
    print("Number of edges:", graph.size()[1])

    print("\nSuccessors of 'A':")
    print(graph.get_successors('A'))

    print("\nPredecessors of 'B':")
    print(graph.get_predecessors('B'))

    print("\nNodes adjacent to 'C':")
    print(graph.get_adjacents('C'))

    print("\nOut-degree of 'B':")
    print(graph.out_degree('B'))

    print("\nIn-degree of 'C':")
    print(graph.in_degree('C'))

    print("\nDegree of 'A':")
    print(graph.degree('A'))

    print("\nDoes the graph have a cycle?")
    print(graph.has_cycle())

    print("Metricas de Codigo:")
    print("\nMetrica cyclomatic complexity:")
    print(subprocess.call(["radon","cc","Grafos/Grafos.py", "-s"]))
    print("\nMetrica maintainability index:")
    print(subprocess.call(["radon","mi","Grafos/Grafos.py", "-s"]))
    print("\nMetrica raw:")
    print(subprocess.call(["radon","raw","Grafos/Grafos.py", "-s"]))
