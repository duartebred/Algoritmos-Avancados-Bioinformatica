"""
Autor: Duarte Velho

Implementação do algotitmo de Redes biológicas
Código escrito por Duarte velho com auxílio de João Ferreira

Documentação e type hiting gerada por Duarte Velho
"""

import subprocess
import sys
import os
from graphviz import Digraph

caminho_grafos = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Grafos')
sys.path.append(caminho_grafos)

from Grafos import MyGraph


class MetabolicNetwork(MyGraph):
    def __init__(self, reactions : dict[str, dict[str, list[str]]]):
        super().__init__()
        self.reactions = reactions

    def metabolitos(self) -> list[str]:
        """
        Returns a list of all the unique metabolites present in the reactions, both consumed and produced.

        Returns
        -------
        List[str]
            Ordered list of unique metabolites.
        """
        
        todos_metabolitos = set()
        for reacao in self.reactions.values():
            todos_metabolitos.update(reacao['cons'])
            todos_metabolitos.update(reacao['prod'])
        return sorted(list(todos_metabolitos))

    def consome(self, react: str) -> list[str]:
        """
        Returns the list of metabolites consumed by a specific reaction.

        Parameters
        ----------
        react : str 
            The reaction identifier.

        Returns
        -------
        List[str]
            List of metabolites consumed by the reaction.
        """
        return self.reactions[react]['cons']

    def produz(self, react: str) -> list[str]:
        """
        Returns the list of metabolites produced by a specific reaction.

        Parameters
        ----------
        react : str
            The reaction identifier.

        Returns
        -------
        List[str] 
            List of metabolites produced by the reaction.
        """
        return self.reactions[react]['prod']

    def consomem(self, met: str) -> list[str]:
        """
        Returns a list of reactions that consume a specific metabolite.

        Parameters
        ----------
        met : str
            The specified metabolite.

        Returns
        -------
        List[str]
            List of reactions that consume the metabolite.
        """
        return [react for react, val in self.reactions.items() if met in val['cons']]

    def produzem(self, met: str) -> list[str]:
        """
        Returns a list of reactions that produce a specific metabolite.

        Parameters
        ----------
        met : str
            The specified metabolite.

        Returns
        -------
        List[str] 
            List of reactions that produce the metabolite.
        """
        return [react for react, val in self.reactions.items() if met in val['prod']]

    def mlig(self, met: str) -> list[str]:
        """
        Returns a list of metabolites that are produced by reactions that consume a specific metabolite.

        Parameters
        ----------
        met : str
            Metabolite consumed.

        Returns
        -------
        List[str]
            Ordered list of new metabolites produced.
        """
        reacoes_consumidoras = self.consomem(met)
        produtos = set()
        for react in reacoes_consumidoras:
            produtos.update(self.reactions[react]['prod'])
        return sorted(list(produtos))

    def rlig(self, react: str) -> list[str]:
        """
        Returns a list of reactions that consume metabolites produced by the specified reaction.

        Parameters
        ----------
        react : str
            Identifier of the reaction of interest.

        Returns
        -------
        List[str]
            Ordered list of reactions that consume the products of the specified reaction.
        """
        produtos = set(self.produz(react))
        reacoes_consomidoras = set()
        for met in produtos:
            reacoes_consomidoras.update(self.consomem(met))
        return sorted(list(reacoes_consomidoras))
    
    def ativadas_por(self, *metabolitos: list[str]) -> list[str]:
        """
        Returns a list of reactions activated by a specified set of metabolites. 
        A reaction is considered activated if all its consumed metabolites are present in the given set.

        Parameters
        ----------
        *metabolitos : List[str]
            List of metabolites that should activate the reactions.

        Returns
        -------
        List[str]
            List of reactions activated by the specified metabolites.
        """
        metabolitos_set = set(metabolitos)
        return [react for react, val in self.reactions.items() if set(val['cons']).issubset(metabolitos_set)]

    def produzidos_por(self, *lista_reacoes: list[str]) -> list[str]:
        """
        Returns a list of all the metabolites produced by the specified reactions.

        Parameters
        ----------
        *lista_reacoes : List[str])
            List of reaction identifiers.

        Returns
        -------
        List[str]
            Ordered list of all the metabolites produced by the specified reactions.
        """
        produtos = set()
        for react in lista_reacoes:
            produtos.update(self.produz(react))
        return sorted(list(produtos))
    
    def m_ativ(self, *metabolitos: list[str]) -> list[str]:
        """
        Returns a list of all metabolites resulting from reactions activated by an initial list of metabolites.
        The function takes into account additional reactions that can be activated by the products of the initial reactions.

        Parameters
        ----------
        *metabolitos : List[str]
            Initial list of metabolites.

        Returns
        -------
        List[str]
            Ordered list of all metabolites resulting from activated reactions.
        """

        if not metabolitos or not all(isinstance(m, str) for m in metabolitos):
            return []
        metabolitos_ativos = set(metabolitos)
        ativados = set()
        while True:
            novas_reacoes = set(self.r_ativ(*metabolitos_ativos)) - ativados
            if not novas_reacoes:
                break
            ativados.update(novas_reacoes)
            for react in novas_reacoes:
                metabolitos_ativos.update(self.produz(react))
        return sorted(list(metabolitos_ativos))

    def r_ativ(self, *metabolitos: list[str]) -> list[str]:
        """
        Returns a total list of all the reactions activated by an initial list of metabolites.
        The function iterates until no new reactions can be activated by the products of previously activated reactions.

        Parameters
        ----------
        *metabolitos : List[str] 
            Initial list of metabolites.

        Returns
        -------
        List[str]
            List of all the reactions activated directly or indirectly by the specified metabolites.
        """
        if not metabolitos or not all(isinstance(m, str) for m in metabolitos):
            return []
        ativadas = set()
        novos_metabolitos = set(metabolitos)
        while True:
            novas_ativadas = set(self.ativadas_por(*novos_metabolitos)) - ativadas
            if not novas_ativadas:
                break
            ativadas.update(novas_ativadas)
            for react in novas_ativadas:
                novos_metabolitos.update(self.produz(react))
        return sorted(ativadas)
    
    def visualize_network(self) -> None:
        """
        It visualizes the metabolic network as a directed graph, where reactions are represented as boxes and 
        metabolites as ellipses. Consumption connections are shown in red, while production connections are shown in green.

        Parameters
        ----------
        self

        Returns
        -------
        None
            The function creates a graphic visualization file and opens the generated visualization in a suitable viewer.
        """
        dot = Digraph(comment='Metabolic Network')

        for react in self.reactions:
            dot.node(react, react, shape='box', color='lightblue2', style='filled')
            for met in self.reactions[react]['cons']:
                dot.node(met, met, shape='ellipse', color='grey', style='filled')
                dot.edge(met, react, color='red')  
            for met in self.reactions[react]['prod']:
                dot.node(met, met, shape='ellipse', color='grey', style='filled')
                dot.edge(react, met, color='green')  

        dot.render('output/metabolic_network.gv', view=True)

        return dot

def main():
    reactions = {
        'R01': {'cons': ['M03', 'M05'], 'prod': ['M07']},
        'R02': {'cons': ['M04', 'M05'], 'prod': ['M07', 'M02']},
        'R03': {'cons': ['M08', 'M07', 'M02'], 'prod': ['M04', 'M05']},
        'R04': {'cons': ['M03', 'M04'], 'prod': ['M01']},
        'R05': {'cons': ['M05', 'M08'], 'prod': ['M01', 'M04']},
        'R06': {'cons': ['M08', 'M07'], 'prod': ['M01', 'M05']},
        'R07': {'cons': ['M03', 'M07'], 'prod': ['M06', 'M01']},
        'R08': {'cons': ['M01', 'M05'], 'prod': ['M02', 'M08']},
        'R09': {'cons': ['M07', 'M06'], 'prod': ['M04', 'M08']},
        'R10': {'cons': ['M03', 'M05', 'M04'], 'prod': ['M08', 'M02']}
    }

    network = MetabolicNetwork(reactions)

    commands = [
        ("consomem M02", network.consomem("M02")),
        ("produzem M02", network.produzem("M02")),
        ("consomem M03", network.consomem("M03")),
        ("produz R10", network.produz("R10")),
        ("consome R10", network.consome("R10")),
        ("mlig M01", network.mlig("M01")),
        ("mlig M02", network.mlig("M02")),
        ("rlig R01", network.rlig("R01")),
        ("rlig R03", network.rlig("R03")),
        ("ativadas_por M03 M04", network.ativadas_por("M03", "M04")),
        ("ativadas_por M03 M05", network.ativadas_por("M03", "M05")),
        ("ativadas_por M04 M05", network.ativadas_por("M04", "M05")),
        ("ativadas_por M03 M04 M05", network.ativadas_por("M03", "M04", "M05")),
        ("produzidos_por R01 R02", network.produzidos_por("R01", "R02")),
        ("r_ativ M01 M05", network.r_ativ("M01", "M05")),
        ("r_ativ M03 M05", network.r_ativ("M03", "M05")),
        ("r_ativ M04 M05", network.r_ativ("M04", "M05")),
        ("m_ativ M01 M05", network.m_ativ("M01", "M05"))
    ]

    for i, (label, result) in enumerate(commands, 1):
        print(f"[{i}] ({label}) > {', '.join(result)}")


    network = MetabolicNetwork(reactions)
    network.id_graph()  
    network.visualize_network()

if __name__ == "__main__":
    main()
    print("Metricas de Codigo:")
    print("\nMetrica cyclomatic complexity:")
    print(subprocess.call(["radon","cc","RedesMetabolicas/ReactionGraph.py", "-s"]))
    print("\nMetrica maintainability index:")
    print(subprocess.call(["radon","mi","RedesMetabolicas/ReactionGraph.py", "-s"]))
    print("\nMetrica raw:")
    print(subprocess.call(["radon","raw","RedesMetabolicas/ReactionGraph.py", "-s"]))

