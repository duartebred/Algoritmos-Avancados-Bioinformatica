import graphviz
from pprint import pprint
class Trees:
    
    def __init__(self, listaPalavras):

        self.listaPalavras = listaPalavras
        self.trie = {}


    def inserir(self):

        for palavra in self.listaPalavras:
            t = self.trie
            for letra in palavra:

                if letra not in t:

                    t[letra] = {}
                t = t[letra]

            t['$'] = 0

        return self.trie, t
    
    def procurar(self, palavra):

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
    
    def apagar(self, palavra):
        
        def _apagar(nodo, palavra, i):
            
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
        
    
    def vistaGrafica(self, nodo=None, dot=None, parent=None, edge_label=''):

        if nodo is None:
            nodo = self.trie

        if dot is None:

            dot = graphviz.Digraph('Trie', comment='Visualização da Trie')

        for chave, valor in nodo.items():
            
            if chave == '$':
                                
                continue
            
            dot.node(chave, chave)
            
            if parent is not None:
                
                dot.edge(parent, chave, label=edge_label)
                
            self.vistaGrafica(valor, chave, edge_label=chave)

        #print(dot.source)

        return dot
    

t = Trees(['ar', 'amora', 'amor', 'braquio'])
t.inserir()
print(t.procurar('amora'))
pprint(t.trie)
G = t.vistaGrafica()
G.view()
