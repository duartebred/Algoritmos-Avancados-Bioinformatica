import unittest
from BWT import BWT


class TestBWT(unittest.TestCase):

    def setUp(self):
        self.seqs_to_encode = "mississippi banana orangotango otorrinolaringologista".split(" ")
        self.sort_matrix =[["$mississippi", "i$mississipp", "ippi$mississ", "issippi$miss",
                            "ississippi$m", "mississippi$", "pi$mississip", "ppi$mississi",
                            "sippi$missis", "sissippi$mis", "ssippi$missi", "ssissippi$mi"],
                            ["$banana", "a$banan", "ana$ban","anana$b","banana$","na$bana","nana$ba"],
                            ["$orangotango", "ango$orangot", "angotango$or", "go$orangotan", "gotango$oran",
                             "ngo$orangota", "ngotango$ora", "o$orangotang", "orangotango$", "otango$orang",
                             "rangotango$o", "tango$orango"],
                             ["$otorrinolaringologista", "a$otorrinolaringologist", "aringologista$otorrinol",
                              "gista$otorrinolaringolo", "gologista$otorrinolarin", "ingologista$otorrinolar",
                              "inolaringologista$otorr", "ista$otorrinolaringolog", "laringologista$otorrino",
                              "logista$otorrinolaringo", "ngologista$otorrinolari", "nolaringologista$otorri",
                              "ogista$otorrinolaringol", "olaringologista$otorrin", "ologista$otorrinolaring",
                              "orrinolaringologista$ot", "otorrinolaringologista$", "ringologista$otorrinola",
                              "rinolaringologista$otor", "rrinolaringologista$oto", "sta$otorrinolaringologi",
                              "ta$otorrinolaringologis", "torrinolaringologista$o"]
                            ]
        self.bwt_expected = ["ipssm$pissii", "annb$aa", "otrnnaag$goo", "atlonrrgooiilngt$aroiso"]  

        self.bwt = ["A$", "ABCD$", "AAABBBCCC$","ABCDABCD$", "AAAAAAAAAAAAAAAAAAAAABBBCD$"]
        self.occ = [["A1", "$1"], ["A1", "B1", "C1", "D1", "$1"], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3',
                    'C1', 'C2', 'C3', '$1'],['A1', 'B1', 'C1', 'D1', 'A2', 'B2', 'C2', 'D2', '$1'],
                    ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11',
                     'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'B01',
                     'B02', 'B03', 'C01', 'D01', '$01']]


    def test_sorted_matrix(self):
        
        for seq_to_encode,sorted_matrix in zip(self.seqs_to_encode,self.sort_matrix):
            self.assertEqual(BWT(seq_to_encode).matriz_ordenada(),sorted_matrix,
                             f"The {seq_to_encode} should be sorted as {sorted_matrix} insted of {BWT(seq_to_encode).matriz_ordenada()}")

    
    def test_construirBWT(self):
        for seq_to_encode,bwt in zip(self.seqs_to_encode,self.bwt_expected):
            self.assertEqual(BWT(seq_to_encode).construir_BWT(),bwt,
                             f"The {seq_to_encode} should be encoded to {bwt} insted of {BWT(seq_to_encode).construir_BWT()}")


    def test_ocorrências(self):
        for bwt,occ in zip(self.bwt,self.occ):
            self.assertEqual(BWT(bwt,encoded=True).ocorrencias(bwt),occ,
                             f"The {bwt} should have the folliwing ocorrences to {occ} insted of {BWT(bwt,encoded=True).ocorrencias(bwt)}")


    def test_obterSequenciaOriginal(self):
        for bwt,seq_to_encode in zip(self.bwt_expected,self.seqs_to_encode):
            self.assertEqual(BWT(bwt,encoded=True).obter_seq_original(),seq_to_encode,
                             f"The {bwt} should be decoded to {seq_to_encode} insted of {BWT(bwt,encoded=True).obter_seq_original()}")

    def test_suffix_array_empty_string(self):
        seqs = ["","A","AAAA","ABCD","ABBA"]
        expected = [[],[0],[3, 2, 1, 0],[0, 1, 2, 3],[3, 0, 2, 1]]
        
        for seq, exp in zip(seqs,expected):
            self.assertEqual(BWT(seq).suffix_array(seq), exp,
                             f"The sequence {seq} should have the suffix array {exp} insted of {BWT(seq).suffix_array(seq)}")


    def test_pattern(self):
        seq = "TAGACAGAGA$"
        patterns =["AGA", "T", "A", "TAG", "GACAG"]
        expected_results = [[1,5,7],[0], [1, 3, 5, 7, 9], [0],
                            [2]]
        
        classe = BWT(seq)

        for pattern, exp_result in zip(patterns,expected_results):
            self.assertEqual(classe.procuraPadraoBWT(pattern),exp_result,
                             f"The pattern {pattern} should have the following results {exp_result} insted of {classe.procuraPadraoBWT(pattern)}")


if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
