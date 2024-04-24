import unittest
from Gibbs_sampling import pwm
from Gibbs_sampling import Gibbs

def round_pwm_results(pwm:list[dict[str,float]]):
    for idx,column in enumerate(pwm):
        for element in column.keys():
            pwm[idx][element]= round(column[element],4)
    
    return pwm


class Test_pwm_gibss_sampling(unittest.TestCase):
    def setUp(self):
        self.test = ['GTAAACAATATTTATAGC', 'AAAATTTACCTTAGAAGG', 'CCGTACTGTCAAGCGTGG', 'TGAGTAAACGACGTCCCA', 'TACTTAACACCCTGTCAA']
        self.seqs_test = [[], ["AAAA","AAAA","AAAA"], ["ACT","TTT","CGC"]]
    def test_pwm_alfabeto(self):
        seq_type = ['DNA', 'RNA', 'PROTEIN', "dna", "RnA","ProtEiN"]
        alfa = ["ACGT", "ACGU","ABCDEFGHIKLMNPQRSTVWYZ","ACGT", "ACGU","ABCDEFGHIKLMNPQRSTVWYZ" ]
        for stype, salfa in zip(seq_type,alfa):
            self.assertEqual(pwm(seq_type=stype).alfabeto(),salfa)

    def test_pwm_alfa_erro(self):
        types = ['Gato', 'Prot', 'Duarte', 'Sporting campeao', 'gymbro', 'portefólio']

        for stype in types:
            with self.assertRaises(AssertionError):
                pwm(seq_type= stype).alfabeto()

    def test_pwm_genarete_pwm(self):
        resultado = [
            [],
            [{"A": 0.5714, "C": 0.1429, "G": 0.1429, "T": 0.1429},
             {"A": 0.5714, "C": 0.1429, "G": 0.1429, "T": 0.1429},
             {"A": 0.5714, "C": 0.1429, "G": 0.1429, "T": 0.1429},
             {"A": 0.5714, "C": 0.1429, "G": 0.1429, "T": 0.1429}],
            [{"A": 0.2857, "C": 0.2857, "G": 0.1429, "T": 0.2857},
             {"A": 0.1429, "C": 0.2857, "G": 0.2857, "T": 0.2857},
             {"A": 0.1429, "C": 0.2857, "G": 0.1429, "T": 0.4286}]]

        for seqs, results in zip(self.seqs_test,resultado):
            pwm_ = round_pwm_results(pwm(seqs).genarete_pwm())    
            self.assertEqual(pwm_,results)

if __name__ == '__main__':
    unittest.main()

