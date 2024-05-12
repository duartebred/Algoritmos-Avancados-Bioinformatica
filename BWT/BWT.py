
class BWT:

    def __init__(self, seqOriginal):

        self.seqOriginal = seqOriginal
        self.listaSequenciaOriginal = []
        
    def criarMatriz(self, seq):
        matriz = []
        for indice in range(len(seq)):

            matriz.append(seq)

            seq = seq[-1] + seq[:len(seq)-1]

        return matriz

    def ordenarMatriz(self, matriz):

        return sorted(matriz)

    
    def imprimirMatriz(self, matriz):

        for linha in matriz:

            print(linha)

    def construirBWT(self, matriz):

        bwt = ""

        for linha in matriz:

            bwt += linha[-1]

        return bwt

    def criarPrimeiraColuna(self, bwt):

        return sorted(bwt)

    def criarUltimaColuna(self, bwt):

        lista = []

        for item in bwt:

            lista.append(item)

        return lista

    def criarDicionarioOcorrencias(self, bwt):
        
        self.dicionarioOcorrencias = {letra: -1 for letra in bwt}
        
    def decidirCaracter(self, item, chave, lista):

        if item == chave:

            self.dicionarioOcorrencias[chave] += 1
            lista.append(item + str(self.dicionarioOcorrencias[chave]))
            
        

    def preencherLista(self, listaSequencias, listaConcatenada):
        
        for item in listaSequencias:
            
            for chave in self.dicionarioOcorrencias.keys():

                self.decidirCaracter(item, chave, listaConcatenada)

        for chave in self.dicionarioOcorrencias.keys():

            self.dicionarioOcorrencias[chave] = -1
        
                
    def obterSequenciaOriginal(self, letra, comprimentoUltimaColuna, primeiraColuna, ultimaColuna):
        
        indice= -1

        for item in ultimaColuna:

            indice += 1
            
            if item == letra:

                self.listaSequenciaOriginal.append(letra[0])

                letra = primeiraColuna[indice]
            
            if len(self.listaSequenciaOriginal) == comprimentoUltimaColuna:
                
                return

        self.obterSequenciaOriginal(letra, comprimentoUltimaColuna, primeiraColuna, ultimaColuna)

    def SequenciaOriginalEmString(self):

        seqOriginal = ''.join(self.listaSequenciaOriginal)

        seqOriginal = seqOriginal[1:len(seqOriginal)] + seqOriginal[0]

        return seqOriginal

    def suffix_array(self, seq):

        self.suffix_array = sorted(range(len(seq)), key=lambda i: seq[i:])

        return self.suffix_array

    
    def procuraPadraoBWT(self, pattern):

        bwt = self.construirBWT(self.ordenarMatriz(self.criarMatriz(self.seqOriginal)))
        sorted_bwt = sorted(bwt)
        suffix_array = self.suffix_array
        
        # Criação do array de contagem
        count = {char: [0] * (len(bwt) + 1) for char in set(bwt)}
        for i in range(1, len(bwt) + 1):
            for char in count:
                count[char][i] = count[char][i - 1]
            count[bwt[i - 1]][i] += 1

        # Criação do array de primeira ocorrência
        first_occurrence = {}
        for i, char in enumerate(sorted_bwt):
            if char not in first_occurrence:
                first_occurrence[char] = i

        # Algoritmo de pesquisa FM
        top = 0
        bottom = len(bwt) - 1
        while top <= bottom:
            if pattern:
                symbol = pattern[-1]
                pattern = pattern[:-1]
                if count[symbol][bottom + 1] > count[symbol][top]:
                    top = first_occurrence[symbol] + count[symbol][top]
                    bottom = first_occurrence[symbol] + count[symbol][bottom + 1] - 1
                else:
                    return []
            else:
                return sorted([suffix_array[i] for i in range(top, bottom + 1)])

        return []
    

if __name__ == "__main__":
    seq = 'TAGACAGAGA$'
    print('Calcular a Bwt a partir de ' + seq)
    print()
    print('Matriz desordenada')
    print()
    classe = BWT(seq)
    matriz_nao_ordenada = classe.criarMatriz(seq)
    classe.imprimirMatriz(matriz_nao_ordenada)
    print()
    print('Matriz Ordenada')
    print()
    matriz_ordenada = classe.ordenarMatriz(matriz_nao_ordenada)
    classe.imprimirMatriz(matriz_ordenada)
    print()
    bwt = classe.construirBWT(matriz_ordenada)
    print('BWT = ' + bwt)
    
    classe.criarDicionarioOcorrencias(bwt)
    print()
    print('Calcular a sequencia original a partir de ' + bwt)
    print()
    primeiraColuna = classe.criarPrimeiraColuna(bwt)
    print('Primeura Coluna: ' + str(primeiraColuna))
    print()
    ultimaColuna = classe.criarUltimaColuna(bwt)
    print('Última Coluna: ' + str(ultimaColuna))
    print()
    listaConcatenadaPrimeiraColuna = []
    classe.preencherLista(primeiraColuna, listaConcatenadaPrimeiraColuna)
    print('Primeira Coluna Numerada: \n\n' + str(listaConcatenadaPrimeiraColuna))
    print()
    listaConcatenadaUltimaColuna = []
    classe.preencherLista(ultimaColuna, listaConcatenadaUltimaColuna)
    print('Ultima Coluna Numerada: \n\n' + str(listaConcatenadaUltimaColuna))
    print()
    comprimentoUltimaColuna = len(listaConcatenadaUltimaColuna)
    classe.obterSequenciaOriginal('$0', comprimentoUltimaColuna, listaConcatenadaPrimeiraColuna, listaConcatenadaUltimaColuna)
    sequenciaOriginal = classe.SequenciaOriginalEmString()
    print('SequenciaOriginal: ' + sequenciaOriginal)
    print()
    padrao = 'AGA'
    print('Procurar o padrão: ' + padrao)
    print()
    arraySufixos = classe.suffix_array(seq)
    print(arraySufixos)
    print()

    print(classe.procuraPadraoBWT(padrao))
