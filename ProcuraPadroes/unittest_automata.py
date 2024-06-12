import unittest
from Automata import Automata


class TestAutomata(unittest.TestCase):
    """
    Test case class for the Automata class.

    Attributes:
        alfabeto (list): A list of characters representing the alphabet used in the automaton.
        padrao (str): The pattern string that the automaton will search for in the sequences.
        automata (Automata): An instance of the Automata class initialized with the alphabet and pattern.

    Methods:
        test_tabela_transicoes: Tests the correctness of the transition table construction.
        test_aplica_automato: Tests the application of the automaton on a sequence.
        test_posicoes_match: Tests the identification of pattern positions in a sequence.
        test_nenhum_match: Tests the behavior when no matches are found in a sequence.
    """
    
    def setUp(self):
        self.alfabeto = ['a', 'c']
        self.padrao = 'aca'
        self.automata = Automata(self.alfabeto, self.padrao)

    def test_tabela_transicoes(self):
        expected_transitions = {
            (0, 'a'): 1,
            (0, 'c'): 0,
            (1, 'a'): 1,
            (1, 'c'): 2,
            (2,'a'):  3,
            (2, 'c'): 0}
        self.assertDictEqual(self.automata.transicoes, expected_transitions)

    def test_aplica_automato(self):
        sequencia = 'cacaacaa'
        expected_states = [0,1,2,3,1,2,3,1]
        self.assertEqual(self.automata.aplicaAutomato(sequencia), expected_states)

    def test_posicoes_match(self):
        sequencia = 'cacaacaa'
        expected_positions = [1, 4]
        self.assertEqual(self.automata.posicoesMatch(sequencia), expected_positions)
        
    def test_nenhum_match(self):
        sequencia = 'accccc'
        expected_positions = []
        self.assertEqual(self.automata.posicoesMatch(sequencia), expected_positions)

if __name__ == '__main__':
    unittest.main()