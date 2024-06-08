#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"></ul></div>

# In[12]:


import unittest


# In[13]:


get_ipython().run_line_magic('run', 'BWT.py')


# In[14]:


class TestBWT(unittest.TestCase):

    def setUp(self):
        self.bwt_instance = BWT("banana$")
        
    def test_criarMatriz(self):
        expected_matrix = [
            "banana$",
            "$banana",
            "a$banan",
            "na$bana",
            "ana$ban",
            "nana$ba",
            "anana$b"
        ]
        result = self.bwt_instance.criarMatriz("banana$")
        self.assertEqual(result, expected_matrix)

    def test_ordenarMatriz(self):
        matrix = self.bwt_instance.criarMatriz("banana$")
        expected_sorted_matrix = [
            "$banana",
            "a$banan",
            "ana$ban",
            "anana$b",
            "banana$",
            "na$bana",
            "nana$ba"
        ]
        result = self.bwt_instance.ordenarMatriz(matrix)
        self.assertEqual(result, expected_sorted_matrix)
    
    def test_construirBWT(self):
        sorted_matrix = self.bwt_instance.ordenarMatriz(self.bwt_instance.criarMatriz("banana$"))
        expected_bwt = "annb$aa"
        result = self.bwt_instance.construirBWT(sorted_matrix)
        self.assertEqual(result, expected_bwt)
    
    def test_criarPrimeiraColuna(self):
        bwt = "annb$aa"
        expected_first_column = ["$", "a", "a", "a", "b", "n", "n"]
        result = self.bwt_instance.criarPrimeiraColuna(bwt)
        self.assertEqual(result, expected_first_column)

    def test_criarUltimaColuna(self):
        bwt = "annb$aa"
        expected_last_column = ["a", "n", "n", "b", "$", "a", "a"]
        result = self.bwt_instance.criarUltimaColuna(bwt)
        self.assertEqual(result, expected_last_column)
    
    def test_obterSequenciaOriginal(self):
        bwt = "annb$aa"
        primeira_coluna = self.bwt_instance.criarPrimeiraColuna(bwt)
        ultima_coluna = self.bwt_instance.criarUltimaColuna(bwt)
        self.bwt_instance.obterSequenciaOriginal("$", len(bwt), primeira_coluna, ultima_coluna)
        result = self.bwt_instance.SequenciaOriginalEmString()
        expected_seq_original = "banana$"
        self.assertEqual(result, expected_seq_original)

    def test_suffix_array(self):
        seq = "banana$"
        expected_suffix_array = [6, 5, 3, 1, 0, 4, 2]
        result = self.bwt_instance.suffix_array(seq)
        self.assertEqual(result, expected_suffix_array)

    def test_procuraPadraoBWT(self):
        self.bwt_instance = BWT("mississippi$")
        pattern = "ssi"
        expected_positions = [2, 5]
        
        self.bwt_instance.suffix_array(self.bwt_instance.seqOriginal)
        
        result = self.bwt_instance.procuraPadraoBWT(pattern)
        self.assertEqual(result, expected_positions)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)

