import subprocess

class ReactionGraph:
    """
    A class to represent and analyze given reactions reaction network.

    """

    def __init__(self, reactions):

        self.reaction_dict = self.parse_reactions(reactions)
        self.metabolite_reaction_graph, self.metabolite_metabolite_graph, self.reaction_reaction_graph = self.ReactionGraphs()

    def parse_reactions(self, reactions):
        """
        Parses the input reactions string into a dictionary.

        """
        reactions = reactions.strip().split("\n")
        reaction_dict = {}

        for reaction in reactions:
            parts = reaction.split(": ")
            rec_id = parts[0]
            reaction_dict[rec_id] = parts[1]

        return reaction_dict

    def ReactionGraphs(self):
        """
        Constructs the metabolite-reaction, metabolite-metabolite, and reaction-reaction graphs.

        Returns a tuple containing three dictionaries representing the metabolite-reaction,
            metabolite-metabolite, and reaction-reaction graphs.
        """
        met_reaction_graph = {}
        metabolite_set = set()
        reaction_set = set()

        for rec_id, equation in self.reaction_dict.items():
            if " <=> " in equation:
                reactants, products = equation.split(" <=> ")
                reversible = True
            elif " => " in equation:
                reactants, products = equation.split(" => ")
                reversible = False
            reactants = reactants.split(" + ")
            products = products.split(" + ")

            # Add to reaction set
            reaction_set.add(rec_id)

            # Map reactants to reactions
            for reactant in reactants:
                if reactant not in met_reaction_graph:
                    met_reaction_graph[reactant] = []
                met_reaction_graph[reactant].append(rec_id)
                metabolite_set.add(reactant)

            # Map products to reactions
            for product in products:
                if product not in met_reaction_graph:
                    met_reaction_graph[product] = []
                met_reaction_graph[product].append(rec_id)
                metabolite_set.add(product)

            # Map reactions to products, and reactants if reversible
            if rec_id not in met_reaction_graph:
                met_reaction_graph[rec_id] = []
            met_reaction_graph[rec_id].extend(products)
            if reversible:
                met_reaction_graph[rec_id].extend(reactants)

        # Create metabolite-metabolite graph
        metabolite_metabolite_graph = {met: [] for met in metabolite_set}
        for met in metabolite_set:
            reactions = [r for r in met_reaction_graph[met] if r.startswith("R")]
            connected_metabolites = set()
            for r in reactions:
                connected_metabolites.update(met_reaction_graph[r])
            connected_metabolites.discard(met)
            metabolite_metabolite_graph[met] = list(connected_metabolites)

        # Create reaction-reaction graph
        reaction_reaction_graph = {r: [] for r in reaction_set}
        for r in reaction_set:
            connected_reactions = set()
            for met in met_reaction_graph[r]:
                if met in met_reaction_graph:
                    connected_reactions.update([nr for nr in met_reaction_graph[met] if nr.startswith("R")])
            connected_reactions.discard(r)
            reaction_reaction_graph[r] = list(connected_reactions)

        return met_reaction_graph, metabolite_metabolite_graph, reaction_reaction_graph

    def print_ReactionGraphic(self):
        """
        Prints the metabolite-reaction, metabolite-metabolite, and reaction-reaction graphs.
        """
        metabolites = sorted([m for m in self.metabolite_reaction_graph if not m.startswith("R")])
        reactions = sorted([r for r in self.metabolite_reaction_graph if r.startswith("R")])

        print("Metabolite-Reaction Graph:")
        for key, value in self.metabolite_reaction_graph.items():
            print(f"{key} -> {value}")
        print("Reactions:", reactions)
        print("Metabolites:", metabolites)

        print("\nMetabolite-Metabolite Graph:")
        for key, value in self.metabolite_metabolite_graph.items():
            print(f"{key} -> {value}")

        print("\nReaction-Reaction Graph:")
        for key, value in self.reaction_reaction_graph.items():
            print(f"{key} -> {value}")



if __name__ == "__main__":
    # Example
    reactions = """
    R1: M1 + M2 => M3
    R2: M3 <=> M4 + M5 + M6
    R3: M5 => M7
    R4: M7 => M8
    """

    reaction_graph = ReactionGraph(reactions)
    reaction_graph.print_ReactionGraphic()


    print("Metricas de Codigo:")
    print("\nMetrica cyclomatic complexity:")
    print(subprocess.call(["radon","cc","Redes Metabólicas/ReactionGraph.py", "-s"]))
    print("\nMetrica maintainability index:")
    print(subprocess.call(["radon","mi","Redes Metabólicas/ReactionGraph.py", "-s"]))
    print("\nMetrica raw:")
    print(subprocess.call(["radon","raw","Redes Metabólicas/ReactionGraph.py", "-s"]))
