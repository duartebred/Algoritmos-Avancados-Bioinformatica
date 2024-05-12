#!/usr/bin/env python
# coding: utf-8

# In[1]:


#GRAFOS


# In[2]:


## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:
    
    def __init__(self, g=None):
        ''' Constructor - takes dictionary to fill the graph as input; default is None '''
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
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print (v, " -> ", self.graph[v])


    ## get basic info

    def id_graph(self):
        for key in self.graph.keys():
            if type(self.graph[key][0]) is tuple: return 'grw'
            else: return 'gr'

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
        if self.id == 'gr': return list(self.graph[v])  # needed to avoid list being overwritten of result of the function is used
        else:
            res=[]
            for n in self.graph[v]:
                res.append(n[0])
            return res


    def get_predecessors(self, v):
        if self.id == 'gr':
            res = [i for i in self.graph.keys() if v in self.graph[i]]
        else:
            res = []
            for i in self.graph.keys():
                for j in self.graph[i]:
                    if v == j[0]:
                        res.append(i)
        return res

    def get_adjacents(self, v):
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)
        res = pred
        for p in suc:
            if p not in res: res.append(p)
        return res

    ## degrees    
    
    def out_degree(self, v):
        return len(self.graph[v])

    def in_degree(self, v):
        return len(self.get_predecessors(v))

    def degree(self, v):
        return len(self.get_adjacents(v))

    ## BFS and DFS searches    
    
    def reachable_bfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            for elem in self.graph[node]:
                if elem not in res and elem not in l and elem != node:
                    l.append(elem)  #Acrescenta sempre no fim!
        return res
        
    def reachable_dfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            s = 0
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem)   # Ele acrescenta sempre no inicio
                    s += 1
        return res    
    
    def distance(self, s, d):
        if s == d: return 0
        l = [(s,0)]
        visited = [s]
        while len(l)>0:
            node, dist = l.pop(0)
            for elem in self.graph[node]:
                if elem == d: return dist + 1
                elif elem not in visited:
                    l.append((elem,dist+1))
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
        
    def reachable_with_dist(self, s):
        res = []
        l = [(s,0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s: res.append((node,dist))
            for elem in self.graph[node]:
                if not is_in_tuple_list(l,elem) and not is_in_tuple_list(res,elem): 
                    l.append((elem,dist+1))
        return res

## cycles
    def node_has_cycle (self, v):
        l = [v]
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v: return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return res

    def has_cycle(self):
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): return True
        return res


def is_in_tuple_list (tl, val):
    res = False
    for (x,y) in tl:
        if val == x: return True
    return res


# In[3]:


# Criando uma instância de MyGraph
graph = MyGraph()

# Adicionando vértices ao grafo
graph.add_vertex('A')
graph.add_vertex('B')
graph.add_vertex('C')

# Adicionando arestas ao grafo
graph.add_edge('A', 'B')
graph.add_edge('B', 'C')
graph.add_edge('C', 'A')

# Imprimindo o grafo como uma lista de adjacências
print("Grafo:")
graph.print_graph()

# Obtendo os nós do grafo
print("\nNós do grafo:")
print(graph.get_nodes())

# Obtendo as arestas do grafo
print("\nArestas do grafo:")
print(graph.get_edges())

# Obtendo o tamanho do grafo (número de nós e número de arestas)
print("\nTamanho do grafo:")
print("Número de nós:", graph.size()[0])
print("Número de arestas:", graph.size()[1])

# Obtendo os sucessores de um nó
print("\nSucessores de 'A':")
print(graph.get_successors('A'))

# Obtendo os predecessores de um nó
print("\nPredecessores de 'B':")
print(graph.get_predecessors('B'))

# Obtendo os nós adjacentes a um nó
print("\nNós adjacentes a 'C':")
print(graph.get_adjacents('C'))

# Obtendo o grau de saída de um nó
print("\nGrau de saída de 'B':")
print(graph.out_degree('B'))

# Obtendo o grau de entrada de um nó
print("\nGrau de entrada de 'C':")
print(graph.in_degree('C'))

# Obtendo o grau de um nó (soma do grau de entrada e saída)
print("\nGrau de 'A':")
print(graph.degree('A'))

# Verificando se há um ciclo no grafo
print("\nO grafo tem ciclo?")
print(graph.has_cycle())


# In[ ]:




