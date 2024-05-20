
from Grafos import MyGraph
import re



class ReactionGraph(MyGraph):
    def __init__(self, reactions=None):
        super().__init__() 
        if reactions:
            self.parse_reactions(reactions)
        
    def add_reaction(self, reaction, reactants, products, reversible=False):
        self.add_vertex(reaction)
        
        for metabolite in reactants:
            self.add_vertex(metabolite)
            self.add_edge(metabolite, reaction)

            if reversible:
                self.add_edge(reaction, metabolite)
                
        for metabolite in products:
            self.add_vertex(metabolite)
            self.add_edge(reaction, metabolite)

            if reversible:
                self.add_edge(metabolite, reaction)


    def parse_reactions(self, reactions, split_reactions=False):
        for reaction in reactions.splitlines():
            match = re.match(r"\s*(\w+)\s*:\s*(.*?)\s*(=>|<=>)\s*(.*)\s*", reaction)

            if match:
                reaction_name, reactants, reaction_type, products = match.groups()

                reactants = re.split(r'\s*\+\s*', reactants)
                products = re.split(r'\s*\+\s*', products)

                reversible = reaction_type == "<=>"

                if split_reactions and reversible:
                    self.add_reaction(reaction_name + "_f", reactants, products)
                    self.add_reaction(reaction_name + "_b", products, reactants)
                else:
                    self.add_reaction(reaction_name, reactants, products, reversible)


    def construct_metabolite_graph(self):
        metabolite_graph = MyGraph()
        for node in self.get_nodes():
            if node[0] == 'M':
                for successor in self.get_successors(node):
                    if successor[0] == 'R':
                        for metabolite in self.get_successors(successor):
                            if metabolite[0] == 'M':
                                metabolite_graph.add_edge(node, metabolite)
        return metabolite_graph



reacoes = """
R1: M1 + M2 => M3
R2: M3 + M4 <=> M5 + M6
R3: M5 => M7
"""

print("Reaction Graph")
reaction_graph = ReactionGraph(reacoes)
reaction_graph.print_graph()
#falta corrigir um bug nesta parte e adicionar o metodo de met-met e reaction-reaction e adicionar mais exemplos e já adiciono o fix no grafos.py a decumentaçao faço quando acabar tudo

