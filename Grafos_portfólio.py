#!/usr/bin/env python
# coding: utf-8

# In[1]:


#GRAFOS


# In[5]:


## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:
    def __init__(self, g=None):
        ''' 
        Constructor - takes dictionary to fill the graph as input; default is None 
        
        Parameters:
            g (dict): Dictionary to fill the graph. Default is None.
        '''
        self.graph = g if g else {}  # Initialize graph with provided dictionary or empty dictionary if None
        self.id = self.id_graph() if g else None  # Calculate graph ID if dictionary provided
        if g:
            for vertex, neighbors in g.items():
                self.add_vertex(vertex)  # Add vertex to graph
                for neighbor in neighbors:
                    if isinstance(neighbor, tuple):
                        self.add_edge(vertex, neighbor[0], neighbor[1])  # Add weighted edge
                    else:
                        self.add_edge(vertex, neighbor)  # Add unweighted edge

    def print_graph(self):
        ''' 
        Prints the content of the graph as adjacency list 
        '''
        for v in self.graph.keys():
            print(v, " -> ", self.graph[v])  # Print vertex and its neighbors



    ## get basic info

    def id_graph(self):
        '''
        Determines the type of graph based on the presence of weighted edges.

        Returns:
            str: Returns 'grw' if the graph contains weighted edges, 'gr' otherwise.
        '''
        has_weighted_edges = False

        # Iterate over each vertex and its neighbors in the graph
        for key in self.graph.keys():
            for neighbor in self.graph[key]:
                # Check if the neighbor is a tuple, indicating a weighted edge
                if isinstance(neighbor, tuple):
                    has_weighted_edges = True
                    break

        # Return 'grw' if the graph contains weighted edges, 'gr' otherwise
        return 'grw' if has_weighted_edges else 'gr'
    

    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())
    
        
    def get_edges(self): 
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                if type(d)==tuple:edges.append((v,d[0],d[1]))
                else: edges.append((v,d))
        return edges
    
      
    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())
    
    
      
    ## add nodes and edges    
    
    def add_vertex(self, v):
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():
            self.graph[v] = []
            
            
    def add_edge(self, o, d, p = 'bin'):
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph '''
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        if d not in self.graph[o] and p == 'bin':
            self.graph[o].append(d)
        else: self.graph[o].append((d,p))
            
            

    ## successors, predecessors, adjacent nodes
        
    def get_successors(self, v):
        '''
        Returns a list of successors of a given vertex in the graph.

        Parameters:
            v (object): The vertex for which successors are to be retrieved.

        Returns:
            list: List of successors of the given vertex.
        '''
        if self.id == 'gr':
            # Return the list of successors of the vertex
            return list(self.graph[v])
        else:
            # Iterate over the neighbors of the vertex and extract the successors
            res = []
            for n in self.graph[v]:
                res.append(n[0])
            return res



    def get_predecessors(self, v):
        '''
        Returns a list of predecessors of a given vertex in the graph.

        Parameters:
            v (object): The vertex for which predecessors are to be retrieved.

        Returns:
            list: List of predecessors of the given vertex.
        '''
        if self.id == 'gr':
            # For unweighted graphs, find all nodes where the given vertex is present in their adjacency lists
            res = [i for i in self.graph.keys() if v in self.graph[i]]
        else:
            # For weighted graphs, iterate over each vertex and its neighbors to find the predecessors of the given vertex
            res = []
            for i in self.graph.keys():
                for j in self.graph[i]:
                    if v == j[0]:
                        res.append(i)
        return res


    def get_adjacents(self, v):
        '''
        Returns a list of adjacent vertices of a given vertex in the graph.

        Parameters:
            v (object): The vertex for which adjacent vertices are to be retrieved.

        Returns:
            list: List of adjacent vertices of the given vertex.
        '''
        # Get the list of successors and predecessors of the given vertex
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)

        # Initialize the result list with predecessors
        res = pred

        # Add successors to the result list if they are not already present
        for p in suc:
            if p not in res:
                res.append(p)

        return res

    

    ## degrees    
    
    def out_degree(self, v):
        '''
        Returns the out-degree of a given vertex in the graph.

        Parameters:
            v (object): The vertex for which out-degree is to be calculated.

        Returns:
            int: The out-degree of the given vertex.
        '''
        # Return the number of successors (outgoing edges) of the given vertex
        return len(self.graph[v])

    def in_degree(self, v):
        '''
        Returns the in-degree of a given vertex in the graph.

        Parameters:
            v (object): The vertex for which in-degree is to be calculated.

        Returns:
            int: The in-degree of the given vertex.
        '''
        # Return the number of predecessors (incoming edges) of the given vertex
        return len(self.get_predecessors(v))

    def degree(self, v):
        '''
        Returns the degree of a given vertex in the graph.

        Parameters:
            v (object): The vertex for which degree is to be calculated.

        Returns:
            int: The degree of the given vertex.
        '''
        # Return the number of adjacent vertices (degree) of the given vertex
        return len(self.get_adjacents(v))

    

    ## BFS and DFS searches    
    
    def reachable_bfs(self, v):
        '''
        Performs a breadth-first search (BFS) traversal starting from a given vertex in the graph.

        Parameters:
            v (object): The starting vertex for the BFS traversal.

        Returns:
            list: A list of vertices reachable from the starting vertex v in the graph.
        '''
        l = [v]  # Initialize the queue with the starting vertex
        res = []  # Initialize the list to store reachable vertices
        while len(l) > 0:
            node = l.pop(0)  # Dequeue a vertex from the queue
            if node != v:
                res.append(node)  # Add the vertex to the list if it's not the starting vertex
            for elem in self.graph[node]:
                if elem not in res and elem not in l and elem != node:
                    l.append(elem)  # Enqueue the adjacent vertices if they haven't been visited yet
        return res

        
    def reachable_dfs(self, v):
        '''
        Performs a depth-first search (DFS) traversal starting from a given vertex in the graph.

        Parameters:
            v (object): The starting vertex for the DFS traversal.

        Returns:
            list: A list of vertices reachable from the starting vertex v in the graph.
        '''
        l = [v]  # Initialize the stack with the starting vertex
        res = []  # Initialize the list to store reachable vertices
        while len(l) > 0:
            node = l.pop(0)  # Pop a vertex from the stack
            if node != v:
                res.append(node)  # Add the vertex to the list if it's not the starting vertex
            s = 0
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem)  # Push the adjacent vertices onto the stack if they haven't been visited yet
                    s += 1
        return res
    
    
    def distance(self, s, d):
        '''
        Finds the shortest distance between two vertices in the graph using breadth-first search (BFS).

        Parameters:
            s (object): The source vertex.
            d (object): The destination vertex.

        Returns:
            int or None: The shortest distance between vertices s and d in the graph, or None if no path exists.
        '''
        if s == d:
            return 0
        l = [(s, 0)]  # Initialize the queue with the source vertex and its distance
        visited = [s]  # Initialize the list of visited vertices
        while len(l) > 0:
            node, dist = l.pop(0)  # Dequeue a vertex and its distance from the queue
            for elem in self.graph[node]:
                if elem == d:
                    return dist + 1  # If the destination vertex is found, return the distance
                elif elem not in visited:
                    l.append((elem, dist + 1))  # Enqueue adjacent vertices with updated distance
                    visited.append(elem)  # Mark the vertex as visited
        return None  # If no path exists between s and d, return None

        
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

        Parameters:
            s (object): The source vertex.
            d (object): The destination vertex.

        Returns:
            list or None: The shortest path between vertices s and d in the graph as a list of vertices, 
                          or None if no path exists.
        '''
        if s == d:
            return []  # If source and destination are the same, return an empty list
        l = [(s, [])]  # Initialize the queue with the source vertex and an empty path
        visited = [s]  # Initialize the list of visited vertices
        while len(l) > 0:
            node, path = l.pop(0)  # Dequeue a vertex and its path from the queue
            for elem in self.graph[node]:
                if elem == d:
                    return path + [node, elem]  # If the destination vertex is found, return the path
                elif elem not in visited:
                    l.append((elem, path + [node]))  # Enqueue adjacent vertices with updated path
                    visited.append(elem)  # Mark the vertex as visited
        return None  # If no path exists between s and d, return None


## cycles
    def node_has_cycle(self, v):
        '''
        Checks if there is a cycle containing a given vertex in the graph using breadth-first search (BFS).

        Parameters:
            v (object): The vertex to check for cycles.

        Returns:
            bool: True if there is a cycle containing vertex v, False otherwise.
        '''
        l = [v]  # Initialize the queue with the given vertex
        visited = [v]  # Initialize the list of visited vertices
        while len(l) > 0:
            node = l.pop(0)  # Dequeue a vertex from the queue
            for elem in self.graph[node]:
                if elem == v:
                    return True  # If a cycle containing v is found, return True
                elif elem not in visited:
                    l.append(elem)  # Enqueue adjacent vertices if they haven't been visited yet
                    visited.append(elem)  # Mark the vertex as visited
        return False  # If no cycle containing v is found, return False


    def has_cycle(self):
        '''
        Checks if the graph contains at least one cycle using breadth-first search (BFS).

        Returns:
            bool: True if the graph contains at least one cycle, False otherwise.
        '''
        res = False  # Initialize the result variable to False
        for v in self.graph.keys():
            if self.node_has_cycle(v):
                return True  # If any vertex has a cycle, return True
        return res  # If no vertex has a cycle, return False



    def is_in_tuple_list(tl, val):
        '''
        Checks if a value is present in the first element of each tuple in a list of tuples.

        Parameters:
            tl (list of tuples): The list of tuples to search.
            val (object): The value to search for.

        Returns:
            bool: True if the value is found in any tuple's first element, False otherwise.
        '''
        res = False  # Initialize the result variable to False
        for (x, y) in tl:
            if val == x:
                return True  # If the value is found in any tuple's first element, return True
        return res  # If the value is not found in any tuple's first element, return False


# In[7]:


# Creating an instance of MyGraph
graph = MyGraph()

# Adding vertices to the graph
graph.add_vertex('A')
graph.add_vertex('B')
graph.add_vertex('C')

# Adding edges to the graph
graph.add_edge('A', 'B')
graph.add_edge('B', 'C')
graph.add_edge('C', 'A')

# Printing the graph as an adjacency list
print("Graph:")
graph.print_graph()

# Getting the nodes of the graph
print("\nGraph nodes:")
print(graph.get_nodes())

# Getting the edges of the graph
print("\nGraph edges:")
print(graph.get_edges())

# Getting the size of the graph (number of nodes and number of edges)
print("\nGraph size:")
print("Number of nodes:", graph.size()[0])
print("Number of edges:", graph.size()[1])

# Getting the successors of a node
print("\nSuccessors of 'A':")
print(graph.get_successors('A'))

# Getting the predecessors of a node
print("\nPredecessors of 'B':")
print(graph.get_predecessors('B'))

# Getting the nodes adjacent to a node
print("\nNodes adjacent to 'C':")
print(graph.get_adjacents('C'))

# Getting the out-degree of a node
print("\nOut-degree of 'B':")
print(graph.out_degree('B'))

# Getting the in-degree of a node
print("\nIn-degree of 'C':")
print(graph.in_degree('C'))

# Getting the degree of a node (sum of in-degree and out-degree)
print("\nDegree of 'A':")
print(graph.degree('A'))

# Checking if there is a cycle in the graph
print("\nDoes the graph have a cycle?")
print(graph.has_cycle())


# In[ ]:




