
class Automata:

    def __init__(self, alfabeto, padrao):
        self.alfabeto = alfabeto
        self.padrao = padrao
        self.transicoes = {}
        self.tabelaTransicoes()


    def tabelaTransicoes(self):
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
                        
                        
    def aplicaAutomato(self, sequencia):
        estado = 0
        estados = []
        for car in sequencia:
            estado = self.transicoes[(estado, car)]
            estados.append(estado)
            if estado == len(self.padrao):
                estado = 0
        return estados    


    def posicoesMatch(self, sequencia):
        listaEstados = self.aplicaAutomato(sequencia)
        listaMatchs = []
        for i in range(len(listaEstados)):
            if listaEstados[i] == len(self.padrao):
                posicaoMatch = i - len(self.padrao) + 1
                listaMatchs.append(posicaoMatch)
        return listaMatchs        


teste = Automata(('a', 'c', 'g', 't'), 'acc')
for tr in teste.transicoes:
    print (tr, ': ', teste.transicoes[tr])
print(teste.aplicaAutomato('aaccttgtgccattgtacca'))
print(teste.posicoesMatch('aaccttgtgccattgtacca'))
