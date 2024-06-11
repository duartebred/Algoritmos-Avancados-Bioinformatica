import graphviz
from pprint import pprint
import subprocess

class Trees:

    """
    This class provides methods for managing a Trie (prefix tree) structure, used for efficient retrieval of words and prefixes.
    It allows insertion of words, searching for a word, deleting words, and visualizing the trie structure.

    Parameters
    ----------
    listaPalavras : list[str]
        A list of words to be inserted into the trie.

    Attributes
    ----------
    listaPalavras : list[str]
        Stores the list of words used to populate the trie.
    trie : dict[str, any]
        The trie data structure implemented as a nested dictionary.

    """
    
    def __init__(self, listaPalavras : list[str]) -> None:

        self.listaPalavras = listaPalavras
        self.trie = {}


    def inserir(self) -> tuple[dict[str, any], dict[str, any]]:
        """
        Inserts all words from the initial list into the trie and returns the entire trie and the last node modified.

        Parameters
        ----------
        None

        Returns
        -------
        tuple[dict[str, any], dict[str, any]]
            Returns a tuple containing the entire trie after insertion of all words and the last modified node in the trie.
        
        """

        for palavra in self.listaPalavras:
            t = self.trie
            for letra in palavra:

                if letra not in t:

                    t[letra] = {}
                t = t[letra]

            t['$'] = 0

        return self.trie, t
    
    def procurar(self, palavra : str) -> bool:
        """
        Searches for a specific word in the trie and returns True if the word exists, otherwise False.

        Parameters
        ----------
        palavra : str
            The word to be searched in the trie.

        Returns
        -------
        bool
            True if the word is found in the trie, otherwise False.

        """

        t = self.trie
        
        for letra in palavra:
            
            if letra not in t:
                
                return False
            
            t = t[letra]
        # No caso de se querer a string completa utiliza-se:
        if '$' in t:
            
             
            return True
            
        else:
            
            return False
    
    def apagar(self, palavra : str) -> None:
        """
        Deletes a specific word from the trie, if it exists.

        Parameters
        ----------
        palavra : str
            The word to be deleted from the trie.

        Returns
        -------
        None

        """
        
        def _apagar(nodo : dict, palavra : str, i : int) -> bool:
            """
            Recursively deletes a word from the trie, checking each character individually.

            Parameters
            ----------
            nodo : dict
                The current node in the trie being modified.
            palavra : str
                The word that is to be deleted from the trie.
            i : int
                The current index in the word being processed.

            Returns
            -------
            bool
                Returns True if the current node can be deleted after the word is removed, otherwise False.

            """
            
            if i == len(palavra):
                
                if '$' in nodo:
                    
                    del nodo['$']
                    
                return '$' not in nodo
            
            if palavra[i] in nodo:
                
                if _apagar(nodo[palavra[i]], palavra, i + 1):
                    
                    del nodo[palavra[i]]
                    
                return len(nodo.keys()) == 0
            
            return False

        _apagar(self.trie, palavra, 0)
        
    
    def vistaGrafica(self, dot = None, nodo = None, parent = None, edge_label : str = '') -> graphviz.Digraph:
        """
        Generates a graphical representation of the trie using graphviz for visualization purposes.

        Parameters
        ----------
        dot : graphviz.Digraph, optional
            The graphviz object to which the trie nodes will be added. If None, a new graph is created.
        nodo : dict, optional
            The current node in the trie being visualized. If None, starts from the root of the trie.
        parent : str, optional
            The identifier of the parent node in the graph. Used to connect nodes in the graph.
        edge_label : str, optional
            The label for the edge connecting the parent node to the current node.

        Returns
        -------
        graphviz.Digraph
            The graphviz object containing the visual representation of the trie.

        """

        if nodo is None:
            nodo = self.trie

        if dot is None:
            dot = graphviz.Digraph('Trie', comment='Visualização da Trie')
            dot.node("Trie", '', shape='point')

        for chave, valor in nodo.items():

            # Cria um nó sem rótulo
            node_id = (parent + "_" if parent is not None else "") + chave
            print(parent, node_id)
            dot.node(node_id, '', shape='point')

            if parent is not None:
                dot.edge(parent, node_id, label=edge_label)
            else:
                dot.edge("Trie", node_id, label=edge_label)

            if chave != '$':
              self.vistaGrafica(dot, valor, node_id, edge_label=chave)

        return dot
    

if __name__ == "__main__":
    
    t = Trees(['ar', 'amora', 'amor', 'braquio'])
    t.inserir()
    print(t.procurar('amora'))  
    pprint(t.trie)
    G = t.vistaGrafica()
    G.view()

    print("Metricas de Codigo:")
    print("\nMetrica cyclomatic complexity:")
    print(subprocess.call(["radon","cc","Procura Padrões/Tries.py", "-s"]))
    print("\nMetrica maintainability index:")
    print(subprocess.call(["radon","mi","Procura Padrões/Tries.py", "-s"]))
    print("\nMetrica raw:")
    print(subprocess.call(["radon","raw","Procura Padrões/Tries.py", "-s"]))