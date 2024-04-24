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
        ]

        #pwm_ = round_pwm_results(pwm(["A","A","A"]).genarete_pwm())
        pwm_ = round_pwm_results(pwm(self.test).genarete_pwm())
        self.assertEqual(pwm_,resultado)

if __name__ == '__main__':
    unittest.main()

