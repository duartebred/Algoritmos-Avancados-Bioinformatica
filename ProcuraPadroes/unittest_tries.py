import unittest 
from Tries import Trees

class TestTrees(unittest.TestCase):
    """
    Test case class for the Trees class.

    Attributes:
        words (list): A list of words to be inserted into the trie for testing.
        tree (Trees): An instance of the Trees class initialized with the list of words.
    
    Methods:
        test_inserir: Tests the insertion of words into the trie.
        test_procurar_existente: Tests the searching for existing words in the trie.
        test_procurar_inexistente: Tests the searching for non-existing words in the trie.
        test_apagar_existente: Tests the deletion of existing words from the trie.
        test_apagar_inexistente: Tests the deletion of non-existing words from the trie.
    """
    def setUp(self):
        self.words = ['hello', 'world', 'python', 'programming', 'tree', 'test']
        self.tree = Trees(self.words)
        self.tree.inserir()

    def test_inserir(self):
        trie, last_node = self.tree.inserir()
        self.assertIsInstance(trie, dict)
        self.assertIsInstance(last_node, dict)

    def test_procurar_existente(self):
        for word in self.words:
            self.assertTrue(self.tree.procurar(word))

    def test_procurar_inexistente(self):
        self.assertFalse(self.tree.procurar('banana'))

    def test_apagar_existente(self):
        word_to_delete = 'tree'
        self.tree.apagar(word_to_delete)
        self.assertFalse(self.tree.procurar(word_to_delete))

    def test_apagar_inexistente(self):
        word_to_delete = 'apple'
        self.tree.apagar(word_to_delete) 

if __name__ == '__main__':
    unittest.main()