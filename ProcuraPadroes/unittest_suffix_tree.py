import unittest
from Suffix_tree import SuffixTree

class TestSuffixTree(unittest.TestCase):
    """
    Test case class for the SuffixTree class.

    Attributes:
        st (SuffixTree): An instance of the SuffixTree class.
        examples (list): A list of example strings for testing.
    
    Methods:
        test_build_suffix_tree: Tests the construction of the suffix tree.
        test_find_pattern: Tests the pattern search functionality of the suffix tree.
        test_get_repeats: Tests the retrieval of repeated substrings from the suffix tree.
    """
    def setUp(self):
        self.st = SuffixTree()
        self.examples = ["abcde$", "mississippi$"]

    def test_build_suffix_tree(self):
        for example in self.examples:
            self.st.build_suffix_tree(example)


    def test_find_pattern(self):
        for example in self.examples:
            self.st.build_suffix_tree(example)
            patterns = ["abc", "bcd", "xyz", "issi", "ppi", "banana"]
            for pattern in patterns:
                result = self.st.find_pattern(pattern)


    def test_get_repeats(self):
        for example in self.examples:
            self.st.build_suffix_tree(example)
            min_length = 2
            min_repeats = 2
            repeats = self.st.get_repeats(min_length, min_repeats)


if __name__ == '__main__':
    unittest.main()