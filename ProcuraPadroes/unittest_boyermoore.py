import unittest
from BoyerMoore import BoyerMoore  


class TestBoyerMoore(unittest.TestCase):
    
    def setUp(self):
        self.pattern = "ana"
        self.text = "bananarama"
        self.bm = BoyerMoore(self.pattern)
    
    def test_create_bad_character_table(self):
        expected_table = {'a': 2, 'n': 1}
        self.assertEqual(self.bm.bad_character_rule, expected_table, "Bad character table does not match expected.")

    def test_search(self):
        expected_positions = [1]
        positions = self.bm.search(self.text)
        self.assertEqual(positions, expected_positions, "Search did not find the correct pattern positions.")


if __name__ == '__main__':
    unittest.main()
