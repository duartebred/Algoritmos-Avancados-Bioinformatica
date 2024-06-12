"""
Autor: Duarte Velho e André Ramos

Implementação do algotitmo de Procura de padrões: Autómatos finitos
Código escrito por Duarte Velho e André Ramos

Documentação e type hiting gerada por Duarte Velho
"""

import subprocess

class Automata:

    """
    This class implements a finite automaton for pattern matching within text. It constructs a transition table based on a given pattern and alphabet, 
    and provides methods to search for the occurrence of the pattern in any given sequence.

    Parameters
    ----------
    alfabeto : list[str]
        A list of characters representing the alphabet used in the pattern and the sequences.
    padrao : str
        The pattern string that the automaton will search for in the sequences.

    Attributes
    ----------
    alfabeto : list[str]
        Stores the alphabet used in the automaton.
    padrao : str
        Stores the pattern for which the automaton searches.
    transicoes : dict[tuple[int, str], int]
        A dictionary representing the state transition table where keys are tuples of state and character, 
        and values are the resultant states after the transition.

    """

    def __init__(self, alfabeto : list[str], padrao : str) -> None:

        self.alfabeto = alfabeto
        self.padrao = padrao
        self.transicoes = {}
        self.tabelaTransicoes()


    def tabelaTransicoes(self) -> None:
        """
        Constructs the state transition table for the automaton based on the specified pattern and alphabet. 
        This table is used to determine the next state for each character and state combination during the pattern search.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """

        for estado in range(len(self.padrao)):
            for caracter in self.alfabeto:
                transicao=(estado, caracter)
                if self.padrao[estado] == caracter:
                    self.transicoes[transicao]=estado+1
                else:
                    if caracter == self.padrao[0]:
                        self.transicoes[transicao]=1
                    else:
                        self.transicoes[transicao]=0
                        
                        
    def aplicaAutomato(self, sequencia : str) -> list[int]:
        """
        Processes a given sequence through the automaton and records the state transitions as the sequence is processed.

        Parameters
        ----------
        sequencia : str
            The sequence on which the automaton is applied.

        Returns
        -------
        list[int]
            A list representing the states of the automaton at each step of processing the sequence.

        """
         
        estado = 0
        estados = []
        for car in sequencia:
            estado = self.transicoes[(estado, car)]
            estados.append(estado)
            if estado == len(self.padrao):
                estado = 0
        return estados    


    def posicoesMatch(self, sequencia : str) -> list[int]:
        """
        Identifies all the starting positions of the given pattern in the sequence using the automaton.

        Parameters
        ----------
        sequencia : str
            The sequence in which to search for the pattern.

        Returns
        -------
        list[int]
            A list of indices representing the starting positions of the pattern within the sequence. If the pattern
            is not found, returns an empty list.

        """
        
        listaEstados = self.aplicaAutomato(sequencia)
        listaMatchs = []
        for i in range(len(listaEstados)):
            if listaEstados[i] == len(self.padrao):
                posicaoMatch = i - len(self.padrao) + 1
                listaMatchs.append(posicaoMatch)
        return listaMatchs        


if __name__ == "__main__":
    teste = Automata(('a', 'c', 'g', 't'), 'acc')

    for tr in teste.transicoes:
        print(tr, ': ', teste.transicoes[tr])

    sequencia = 'aaccttgtgccattgtacca'
    estados = teste.aplicaAutomato(sequencia)
    print(estados)

    posicoes_match = teste.posicoesMatch(sequencia)
    print(posicoes_match)

    print("Metricas de Codigo:")
    print("\nMetrica cyclomatic complexity:")
    print(subprocess.call(["radon","cc","ProcuraPadroes/automatos_finitos.py", "-s"]))
    print("\nMetrica maintainability index:")
    print(subprocess.call(["radon","mi","ProcuraPadroes/automatos_finitos.py", "-s"]))
    print("\nMetrica raw:")
    print(subprocess.call(["radon","raw","ProcuraPadroes/automatos_finitos.py", "-s"]))

