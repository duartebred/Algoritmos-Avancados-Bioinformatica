"""
Autor: André Ramos e Ricardo Oliveira 

Implementação do algotitmo de Alinhamentos contra referências (BWTs)
Código escrito por André Ramos e Ricardo Oliveira com auxílio de Duarte Velho

Documentação e type hiting gerada por Ricardo Oliveira
"""


import subprocess; import re

def imprimir_matriz(matriz : list[str]) -> None:
    """
    Prints a matrix of strings line by line.

    Parameters:
    -------------
    matriz (list[str]): 
        A list of strings representing a matrix. Each string represents a row in the matrix.

    Returns:
    ---------
    None
    """

    for linha in matriz: print(linha)


class BWT:

    """
    Initializes a new instance of the Burrows-Wheeler Transform (BWT) class.

    Parameters:
    --------------------
    seq_original (str): 
        The original sequence for which the BWT will be computed.
        
    encoded (bool, optional): 
        A flag indicating whether the input sequence is already encoded. Defaults to False.

    Returns:
        None
    """
    def __init__(self, seq_original : str, encoded = False) -> None:

        self.seq_original = seq_original
        self.matrix_ord = self.matriz_ordenada()
        if encoded: self.bwt = seq_original
        else: self.bwt = self.construir_BWT()
        self.listaSequenciaOriginal = []
        self.encoded = encoded
        

    def matriz_ordenada(self) -> list[str]:
        """
        Generates a sorted matrix of the rotations of the original sequence.
        The function first checks if the original sequence already contains the end-of-string marker '$'.
        If not, it appends '$' to the sequence. Then, it creates a matrix by cycling the original sequence.
        Each row in the matrix represents a rotation of the original sequence.
        The matrix is then sorted in lexicographical order.

        Parameters:
        -------------
        self (BWT): 
            An instance of the BWT class.

        Returns:
        ---------
        list[str]:
            A sorted matrix of strings representing all rotations of the original sequence.
        
        Raises:
        ---------
        AssertionError:
            If the input sequence is not a string.
        """
        
        assert isinstance(self.seq_original,str),"The input sequence must be a string"

        if self.seq_original.find('$') == -1:
            self.seq_original = self.seq_original + '$'
        
        seq = self.seq_original
        matriz = []

        for _ in range(len(seq)):

            matriz.append(seq)
            seq = seq[-1] + seq[:len(seq)-1]

        return sorted(matriz)


    def construir_BWT(self) -> str:
        """
        Constructs the Burrows-Wheeler Transformed (BWT) of the original sequence.

        Parameters:
        -------------
        self (BWT): 
            An instance of the BWT class. The sorted roation matrix is stored in self.matrix_ord.

        Returns:
        ---------
        str:
            A string representing the Burrows-Wheeler Transformed (BWT) of the original sequence.
            The BWT is constructed by concatenating the last characters of each row in the sorted matrix.
        """

        return "".join([linha[-1] for linha in self.matrix_ord])


    def ocorrencias(self,seq:str)->list[str]:
        """
        Counts the occurrences of each character in the given sequence and returns a list of strings.
        Each string in the list represents a character followed by its count, with leading zeros added if necessary.

        Parameters:
        -------------
        seq (str): 
            The sequence for which the occurrences will be counted.

        Returns:
        ---------
        list[str]:
            A list of strings representing the occurrences of each character in the sequence.
        """
        assert len(seq) != 0, "The input sequence must be non-empty."
        maximo = len(str(max([seq.count(elem) for elem in set(seq)])))
        counts = {elem:0 for elem in set(seq)}
        res = []

        for elem in seq:
            counts[elem] += 1

            if len(str(counts[elem])) != maximo and len(str(counts[elem]))==1:
                zeros = "0"*(maximo-len(str(counts[elem])))
                res.append(elem+zeros+str(counts[elem]))
            
            elif len(str(counts[elem])) != maximo and len(str(counts[elem]))>1:
                zeros = "0"*(maximo-len(str(counts[elem])))
                res.append(elem+ str(counts[elem])+zeros)
            
            else: res.append(elem+str(counts[elem]))
        
        return res
        
               
    def obter_seq_original(self) -> str:

        """
        This method is used to obtain the original sequence from the Burrows-Wheeler Transformed (BWT).
        It uses the occurrence counts of characters in the first and last columns of the sorted matrix.

        Parameters:
        -----------
        self (BWT): An instance of the BWT class. The bwt is stored in self.bwt.

        Returns:
        --------
        str: The original sequence obtained from the BWT.

        """
        
        first_col_count = self.ocorrencias(sorted(self.bwt))
        last_col_counts = self.ocorrencias(self.bwt)

        for string in last_col_counts:
            match = re.search(r'^[$\d]+', string)
            
            if match != None:
                idx = last_col_counts.index(string)
                elem_stop = last_col_counts[idx]
                break
        
        res = ""

        while first_col_count[idx] != elem_stop:
            elem = re.findall(r'^[\w]', first_col_count[idx])
            if len(elem) != 0:
                res = res + elem[0]
            idx = last_col_counts.index(first_col_count[idx])
        
        return res


    def suffix_array(self, seq : str) -> list[int]:
        """
        Computes the suffix array of a given string. The suffix array is a sorted array of all suffixes of the input string.
        Each suffix is represented by its starting index in the original string.

        Parameters:
        -----------
        seq (str): 
            The input string for which the suffix array will be computed.

        Returns:
        --------
        list[int]: 
            A sorted list of integers representing the starting indices of all suffixes of the input string.
            The suffixes are sorted in lexicographical order.
        """

        suffix_array = sorted(range(len(seq)), key=lambda i: seq[i:])

        return suffix_array

    
    def procuraPadraoBWT(self, pattern : str) -> list[int]:
        """
        This method is used to find the positions of a pattern in the original sequence using the Burrows-Wheeler Transform (BWT).
        It implements the Boyer-Moore algorithm for string matching in the BWT.

        Parameters:
        -----------
        pattern (str): 
            The pattern to be searched in the original sequence.

        Returns:
        --------
        list[int]: 
            A list of positions where the pattern is found in the original sequence. If the pattern is not found, an empty list is returned.
        """

        sorted_bwt = sorted(self.bwt)
        suffix_array = self.suffix_array(self.seq_original)
        
        count = {char: [0] * (len(self.bwt) + 1) for char in set(self.bwt)}
        for i in range(1, len(self.bwt) + 1):
            for char in count:
                count[char][i] = count[char][i - 1]
            count[self.bwt[i - 1]][i] += 1

        first_occurrence = {}
        for i, char in enumerate(sorted_bwt):
            if char not in first_occurrence:
                first_occurrence[char] = i

        top = 0
        bottom = len(self.bwt) - 1
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
    seq = "TAGACAGAGA$"
    bwt = BWT("TAGACAGAGA$").construir_BWT()
    print(f'Calculating Bwt from: {seq}')
    print("BWT:",BWT(seq).construir_BWT())
    print('\nSorted matrix:\n')
    imprimir_matriz(BWT(seq).matriz_ordenada())

    print(f"\nDecoding BWT: {bwt}")
    print(BWT(bwt,encoded=True).obter_seq_original())

    print("\nOcorrence of each element in the BWT:")
    print(BWT("AAAAAAAAAAAAAAAAAAAAABBBCD$",encoded=True).ocorrencias("AAAAAAAAAAAAAAAAAAAAABBBCD$"))

    print("\nRestoring the original sequence after being encoded")
    print(BWT(seq,encoded=False).obter_seq_original())

    pattern = "AGA"
    print(f"\nFinding the position of the pattern {pattern} on sequence {seq}")
    print(BWT(seq).procuraPadraoBWT(pattern))

    pattern = "T"
    print(f"\nFinding the position of the pattern {pattern} on sequence {seq}")
    print(BWT(seq).procuraPadraoBWT(pattern))
    

    print("Metricas de Codigo:")
    print("\nMetrica cyclomatic complexity:")
    print(subprocess.call(["radon","cc","BWT/BWT_final.py", "-s"]))
    print("\nMetrica maintainability index:")
    print(subprocess.call(["radon","mi","BWT/BWT_final.py", "-s"]))
    print("\nMetrica raw:")
    print(subprocess.call(["radon","raw","BWT/BWT_final.py", "-s"]))