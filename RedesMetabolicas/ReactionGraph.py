import subprocess

class ReactionGraph:
    """
    This class represents and analyzes a network of chemical reactions. It constructs three types of graphs:
    metabolite-reaction, metabolite-metabolite, and reaction-reaction based on the reactions provided.

    Parameters
    ----------
    reactions : str
        A string containing multiple reactions, each one defined by a unique reaction ID followed by
        the reaction equation separated by ": ". Reactions are separated by new lines.

    Attributes
    ----------
    reaction_dict : dict[str, str]
        A dictionary where keys are reaction IDs and values are the corresponding reaction equations.

    metabolite_reaction_graph : dict[str, list[str]]
        A dictionary representing the graph of metabolites to reactions.

    metabolite_metabolite_graph : dict[str, list[str]]
        A dictionary representing connections between metabolites based on shared reactions.

    reaction_reaction_graph : dict[str, list[str]]
        A dictionary showing connections between reactions that share common metabolites.
    """

    def __init__(self, reactions : str) -> None:
        """
        Initializes the ReactionGraph by parsing the provided reaction data and constructing the necessary graphs.

        Parameters
        ----------
        reactions : str
            Reactions formatted as a multiline string.
        """

        self.reaction_dict = self.parse_reactions(reactions)
        self.metabolite_reaction_graph, self.metabolite_metabolite_graph, self.reaction_reaction_graph = self.ReactionGraphs()

    def parse_reactions(self, reactions : str) -> dict[str, str]:
        """
        Parses the input reactions into a dictionary mapping reaction IDs to reaction equations.

        Parameters
        ----------
        reactions : str
            A string of reactions separated by new lines.

        Returns
        -------
        dict[str, str]
            A dictionary with reaction IDs as keys and reaction equations as values.
        """
        reactions = reactions.strip().split("\n")
        reaction_dict = {}

        for reaction in reactions:
            parts = reaction.split(": ")
            rec_id = parts[0]
            reaction_dict[rec_id] = parts[1]

        return reaction_dict

    def ReactionGraphs(self) -> tuple[dict[str, list[str]], dict[str, list[str]], dict[str, list[str]]]:
        """
        Constructs the metabolite-reaction, metabolite-metabolite, and reaction-reaction graphs based on the parsed reactions.

        Returns
        -------
        tuple
            A tuple of three dictionaries, each representing a different type of graph.
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

            reaction_set.add(rec_id)

            for reactant in reactants:
                if reactant not in met_reaction_graph:
                    met_reaction_graph[reactant] = []
                met_reaction_graph[reactant].append(rec_id)
                metabolite_set.add(reactant)

            for product in products:
                if product not in met_reaction_graph:
                    met_reaction_graph[product] = []
                met_reaction_graph[product].append(rec_id)
                metabolite_set.add(product)

            if rec_id not in met_reaction_graph:
                met_reaction_graph[rec_id] = []
            met_reaction_graph[rec_id].extend(products)
            if reversible:
                met_reaction_graph[rec_id].extend(reactants)

        metabolite_metabolite_graph = {met: [] for met in metabolite_set}
        for met in metabolite_set:
            reactions = [r for r in met_reaction_graph[met] if r.startswith("R")]
            connected_metabolites = set()
            for r in reactions:
                connected_metabolites.update(met_reaction_graph[r])
            connected_metabolites.discard(met)
            metabolite_metabolite_graph[met] = list(connected_metabolites)

        reaction_reaction_graph = {r: [] for r in reaction_set}
        for r in reaction_set:
            connected_reactions = set()
            for met in met_reaction_graph[r]:
                if met in met_reaction_graph:
                    connected_reactions.update([nr for nr in met_reaction_graph[met] if nr.startswith("R")])
            connected_reactions.discard(r)
            reaction_reaction_graph[r] = list(connected_reactions)

        return met_reaction_graph, metabolite_metabolite_graph, reaction_reaction_graph

    def print_ReactionGraphic(self) -> None:
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
    print(subprocess.call(["radon","cc","RedesMetabolicas/ReactionGraph.py", "-s"]))
    print("\nMetrica maintainability index:")
    print(subprocess.call(["radon","mi","RedesMetabolicas/ReactionGraph.py", "-s"]))
    print("\nMetrica raw:")
    print(subprocess.call(["radon","raw","RedesMetabolicas/ReactionGraph.py", "-s"]))
