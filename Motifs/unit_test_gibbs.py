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


def pwm_dna(seq_type:str, pseudo:float):
    assert isinstance(seq_type,str)
    assert seq_type.upper() == "DNA",f"A sequência biológica deve ser DNA"
    assert isinstance(pseudo,int) or isinstance(pseudo,float)
    assert pseudo in [0,1,2]
    
    if pseudo == 0:
        pwm_0=[
               [],
               [{"A": 1.0000, "C": 0.0000, "G": 0.0000, "T": 0.0000},
                {"A": 1.0000, "C": 0.0000, "G": 0.0000, "T": 0.0000},
                {"A": 1.0000, "C": 0.0000, "G": 0.0000, "T": 0.0000},
                {"A": 1.0000, "C": 0.0000, "G": 0.0000, "T": 0.0000}],
               [{"A": 0.3333, "C": 0.3333, "G": 0.0000, "T": 0.3333 },
                {"A": 0.0000, "C": 0.3333, "G": 0.3333, "T": 0.3333},
                {"A": 0.0000, "C": 0.3333, "G": 0.0000, "T": 0.6667}],
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
                 [{"A": 0.2727, "C": 0.2727, "G": 0.1818, "T": 0.2727},
                  {"A": 0.1818, "C": 0.2727, "G": 0.2727, "T": 0.2727},
                  {"A": 0.1818, "C": 0.2727, "G": 0.1818, "T": 0.3636}]]
        
        return pwm_2


def pwm_proteina(seq_type:str, pseudo: float):
    assert isinstance(seq_type,str)
    assert seq_type.upper() == "PROTEINA",f"A sequência biológica deve ser do tipo proteína"
    assert isinstance(pseudo,int) or isinstance(pseudo,float)
    assert pseudo in [0,1,2]
    
    if pseudo == 0:
        pwm_0=[
            [],
            [{"A": 0.2500, "B": 0.0000, "C": 0.0000, "D": 0.2500, "E": 0.0000, "F": 0.0000, "G": 0.2500, "H": 0.0000, "I": 0.0000,
              "K": 0.0000, "L": 0.2500, "M": 0.0000, "N": 0.0000, "P": 0.0000, "Q": 0.0000, "R": 0.0000, "S": 0.0000, "T": 0.0000,
              "V": 0.0000, "W": 0.0000, "Y": 0.0000, "Z": 0.0000},
             {"A": 0.0000, "B": 0.0000, "C": 0.0000, "D": 0.0000, "E": 0.2500, "F": 0.0000, "G": 0.0000, "H": 0.2500, "I": 0.0000,
              "K": 0.0000, "L": 0.0000, "M": 0.2500, "N": 0.0000, "P": 0.0000, "Q": 0.0000, "R": 0.2500, "S": 0.0000, "T": 0.0000, 
              "V": 0.0000, "W": 0.0000, "Y": 0.0000, "Z": 0.0000},
             {"A": 0.0000, "B": 0.0000, "C": 0.0000, "D": 0.0000, "E": 0.0000, "F": 0.2500, "G": 0.0000, "H": 0.0000, "I": 0.2500,
              "K": 0.0000, "L": 0.0000, "M": 0.0000, "N": 0.5000, "P": 0.0000, "Q": 0.0000, "R": 0.0000, "S": 0.0000, "T": 0.0000,
              "V": 0.0000, "W": 0.0000, "Y": 0.0000, "Z": 0.0000}]]
        
        return pwm_0

    if pseudo == 1:
        pwm_1 = [
            [],
            [{"A": 0.0769, "B": 0.0385, "C": 0.0385, "D": 0.0769, "E": 0.0385, "F": 0.0385, "G": 0.0769, "H": 0.0385, "I": 0.0385,
              "K": 0.0385, "L": 0.0769, "M": 0.0385, "N": 0.0385, "P": 0.0385, "Q": 0.0385, "R": 0.0385, "S": 0.0385, "T": 0.0385,
              "V": 0.0385, "W": 0.0385, "Y": 0.0385, "Z": 0.0385},
              {"A": 0.0385, "B": 0.0385, "C": 0.0385, "D": 0.0385, "E": 0.0769, "F": 0.0385, "G": 0.0385, "H": 0.0769, "I": 0.0385,
               "K": 0.0385, "L": 0.0385, "M": 0.0769, "N": 0.0385, "P": 0.0385, "Q": 0.0385, "R": 0.0769, "S": 0.0385, "T": 0.0385, 
               "V": 0.0385, "W": 0.0385, "Y": 0.0385, "Z": 0.0385},
             {"A": 0.0385, "B": 0.0385, "C": 0.0385, "D": 0.0385, "E": 0.0385, "F": 0.0769, "G": 0.0385, "H": 0.0385, "I": 0.0769,
              "K": 0.0385, "L": 0.0385, "M": 0.0385, "N": 0.1154, "P": 0.0385, "Q": 0.0385, "R": 0.0385, "S": 0.0385, "T": 0.0385,
              "V": 0.0385, "W": 0.0385, "Y": 0.0385, "Z": 0.0385}]]
        
        return pwm_1
    
    if pseudo == 2:
        pwm_2 = [
            [],
            [{"A": 0.0625, "B": 0.0417, "C": 0.0417, "D": 0.0625, "E": 0.0417, "F": 0.0417, "G": 0.0625, "H": 0.0417, "I": 0.0417,
              "K": 0.0417, "L": 0.0625, "M": 0.0417, "N": 0.0417, "P": 0.0417, "Q": 0.0417, "R": 0.0417, "S": 0.0417, "T": 0.0417,
              "V": 0.0417, "W": 0.0417, "Y": 0.0417, "Z": 0.0417},
              {"A": 0.0417, "B": 0.0417, "C": 0.0417, "D": 0.0417, "E": 0.0625, "F": 0.0417, "G": 0.0417, "H": 0.0625, "I": 0.0417,
               "K": 0.0417, "L": 0.0417, "M": 0.0625, "N": 0.0417, "P": 0.0417, "Q": 0.0417, "R": 0.0625, "S": 0.0417, "T": 0.0417, 
               "V": 0.0417, "W": 0.0417, "Y": 0.0417, "Z": 0.0417},
             {"A": 0.0417, "B": 0.0417, "C": 0.0417, "D": 0.0417, "E": 0.0417, "F": 0.0625, "G": 0.0417, "H": 0.0417, "I": 0.0625,
              "K": 0.0417, "L": 0.0417, "M": 0.0417, "N": 0.0833, "P": 0.0417, "Q": 0.0417, "R": 0.0417, "S": 0.0417, "T": 0.0417,
              "V": 0.0417, "W": 0.0417, "Y": 0.0417, "Z": 0.0417}]]
        
        return pwm_2


class Test_pwm_gibss_sampling(unittest.TestCase):
    def setUp(self):
        self.test = ['GTAAACAATATTTATAGC', 'AAAATTTACCTTAGAAGG', 'CCGTACTGTCAAGCGTGG', 'TGAGTAAACGACGTCCCA', 'TACTTAACACCCTGTCAA']
        self.seqs_DNA = [[], ["AAAA","AAAA","AAAA"], ["ACT","TTT","CGC"]]
        self.seqs_proteina = [[], ["ARN", "DEF", "GHI", "LMN"]]
       
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
        # passar isto para uma função visto que são dois pedaços de código iguais
        for idx,seq_DNA in enumerate(self.seqs_DNA):
            for pcount in pseudo:   
                self.assertEqual(round_pwm_results(pwm(seq_DNA,pseudo=pcount).generate_pwm()), pwm_dna("DNA", pseudo= pcount)[idx],
                    msg=f"Erro para a sequência {seq_DNA} na pseudocontagem de {pcount}")

        for idx,seq_proteina in enumerate(self.seqs_proteina):
            for pcount in pseudo:
                expected_pwm =  pwm_proteina("proteina", pseudo= pcount)[idx]
                generated_pwm = round_pwm_results(pwm(seq_proteina, seq_type="protein", pseudo=pcount).generate_pwm())
                self.assertEqual(generated_pwm, expected_pwm, msg=f"Erro para a sequência {seq_proteina} para na pseudocontagem de {pcount}")
    
    def test_pwm_prob_seq(self):
        pass


class Test_gibbs(unittest.TestCase):

    def test_new_seqs():
        pass


if __name__ == '__main__':
    unittest.main()

