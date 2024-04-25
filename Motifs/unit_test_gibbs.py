import unittest
from Gibbs_sampling import pwm
from Gibbs_sampling import Gibbs

def round_pwm_results(pwm:list[dict[str,float]]):
    """
    Rounds the values in a position weight matrix (PWM) to four decimal digits.

    Parameters
    -------------
    - pwm list[dict[str, float]]: 
        A list of dictionaries representing a PWM. Each dictionary represents a position in the PWM,
        where keys are biological bases shuhc as nucleotides and the values are the corresponding probabilities.

    Returns
    ------------
    - list[dict[str, float]]: 
        A PWM with values rounded to four decimal digits.

    Example:
    >>> pwm = [{'A': 0.123456, 'C': 0.234567, 'G': 0.345678, 'T': 0.456789}]
    >>> rounded_pwm = round_pwm_results(pwm)
    >>> print(rounded_pwm)
    [{'A': 0.1235, 'C': 0.2346, 'G': 0.3457, 'T': 0.4568}]
    """
    for idx,column in enumerate(pwm):
        for element in column.keys():
            pwm[idx][element]= round(column[element],4)
    
    return pwm


def pwm_DNA(seq_type:int, pseudo:float):
    assert seq_type == "DNA",f"A sequência biológica deve ser DNA"
    assert isinstance(seq_type,str)
    assert isinstance(pseudo,int) or isinstance(pseudo,float)
    assert pseudo in [0,1,2]
    
    if pseudo == 0:
        pwm_0=[
               [],
               [{"A": 1.0000 , "C":0.0000 , "G":0.0000 , "T":0.0000},
                {"A": 1.0000 , "C":0.0000 , "G":0.0000 , "T":0.0000},
                {"A": 1.0000 , "C":0.0000 , "G":0.0000 , "T":0.0000},
                {"A": 1.0000 , "C":0.0000 , "G":0.0000 , "T":0.0000}],
               [{"A":, "C": , "G": , "T": },
                {"A": 0.1429, "C": 0.2857, "G": 0.2857, "T": 0.2857},
                {"A": 0.1429, "C": 0.2857, "G": 0.1429, "T": 0.4286}],
               ]
        
        return pwm_0

    if pseudo == 1:
        pwm_1 = [
                [],
                [{"A": 0.5714, "C": 0.1429, "G": 0.1429, "T": 0.1429},
                 {"A": 0.5714, "C": 0.1429, "G": 0.1429, "T": 0.1429},
                 {"A": 0.5714, "C": 0.1429, "G": 0.1429, "T": 0.1429},
                 {"A": 0.5714, "C": 0.1429, "G": 0.1429, "T": 0.1429}],
                [{"A": 0.2857, "C": 0.2857, "G": 0.1429, "T": 0.2857},
                 {"A": 0.1429, "C": 0.2857, "G": 0.2857, "T": 0.2857},
                 {"A": 0.1429, "C": 0.2857, "G": 0.1429, "T": 0.4286}]]
        return pwm_1
    
    if pseudo == 2:
        pwm_2 = [
                 [],
                 [{"A": 0.4545, "C": 0.1818, "G": 0.1818, "T": 0.1818},
                  {"A": 0.4545, "C": 0.1818, "G": 0.1818, "T": 0.1818},
                  {"A": 0.4545, "C": 0.1818, "G": 0.1818, "T": 0.1818},
                  {"A": 0.4545, "C": 0.1818, "G": 0.1818, "T": 0.1818}],
                 []]
        
        return pwm_2


class Test_pwm_gibss_sampling(unittest.TestCase):
    def setUp(self):
        self.test = ['GTAAACAATATTTATAGC', 'AAAATTTACCTTAGAAGG', 'CCGTACTGTCAAGCGTGG', 'TGAGTAAACGACGTCCCA', 'TACTTAACACCCTGTCAA']
        self.seqs_DNA = [[], ["AAAA","AAAA","AAAA"], ["ACT","TTT","CGC"]]
        
    def test_pwm_alfabeto(self):
        seq_type = ['DNA', 'RNA', 'PROTEIN', "dna", "RnA","ProtEiN"]
        alfa = ["ACGT", "ACGU","ABCDEFGHIKLMNPQRSTVWYZ","ACGT", "ACGU","ABCDEFGHIKLMNPQRSTVWYZ" ]
        for stype, salfa in zip(seq_type,alfa):
            self.assertEqual(pwm(seq_type=stype).alfabeto(),salfa)

    def test_pwm_alfa_erro(self):
        types = ['Gato', 'Prot', 'Duarte', 'Sporting campeao', 'gymbro', 'portefólio',""]

        for Type in types:
            with self.assertRaises(AssertionError):
                pwm(seq_type= Type).alfabeto()

    def test_pwm_genarete_pwm(self):
        pseudo = [0,1,2]
        for idx,seq_DNA in enumerate(self.seqs_DNA):
            for pcount in pseudo:   
                self.assertEqual(round_pwm_results(pwm(seq_DNA,pseudo=pcount).generate_pwm()), pwm_DNA("DNA", pseudo= pcount)[idx],
                                 msg=f"Erro para a sequeência {seq_DNA} para a pseudocontagem de {pcount}")

if __name__ == '__main__':
    unittest.main()

