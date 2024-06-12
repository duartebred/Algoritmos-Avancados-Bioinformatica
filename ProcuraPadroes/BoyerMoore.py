import subprocess

class BoyerMoore:
    """
    This class implements the Boyer-Moore algorithm for pattern matching within text. It precomputes two tables based on the provided pattern:
    the bad character table and the good suffix table, which are used to optimize the searching process by skipping sections of the text that do not match the pattern.

    Parameters
    ----------
    pattern : str
        The pattern string that the Boyer-Moore algorithm will search for in the text.

    """
    def __init__(self, pattern):
        self.pattern = pattern
        self.pattern_length = len(pattern)
        self.bad_character_rule = self.create_bad_character_table()
        self.good_suffix_rule = self.create_good_suffix_table()

    def create_bad_character_table(self) -> dict:
        """
        Creates the bad character shift table used in the Boyer-Moore search algorithm.
        This table maps each character in the pattern to its last occurrence within the pattern.

        Returns
        -------
        dict[str, int]
            The bad character table for the pattern.
        """
        table = {}
        for i in range(len(self.pattern)):
            table[self.pattern[i]] = i
        return table

    def create_good_suffix_table(self) -> list:
        """
        Creates the good suffix shift table used in the Boyer-Moore search algorithm.
        This table is filled with the shifts calculated based on the good suffix rule, 
        which considers how far the search can jump in the text after a partial match is found.

        Returns
        -------
        list[int]
            The good suffix table for the pattern.
        """
        table = [0] * (len(self.pattern) + 1)
        last_prefix_position = len(self.pattern)

        for i in range(len(self.pattern)):
            mirrored_i = len(self.pattern) - 1 - i
            if self.is_prefix(mirrored_i + 1):
                last_prefix_position = mirrored_i + 1
            table[mirrored_i] = last_prefix_position - mirrored_i + len(self.pattern) - 1

        for i in range(len(self.pattern)):
            length_suffix = self.length_of_suffix(i)
            if self.pattern[i - length_suffix] != self.pattern[len(self.pattern) - 1 - length_suffix]:
                table[len(self.pattern) - 1 - length_suffix] = len(self.pattern) - 1 - i + length_suffix

        return table

    def is_prefix(self, p : int) -> bool:
        """
        Determines if the substring of the pattern starting from index `p` is a prefix of the pattern.

        This method is used in calculating the good suffix table to determine how much of the end of the pattern
        can be considered a prefix. This is crucial for optimizing the search by identifying suffix-prefix matches
        which allow for larger skips in the text.

        Parameters
        ----------
        p : int
            The starting index in the pattern from which to check if the subsequent substring is a prefix of the pattern.

        Returns
        -------
        bool
            True if the substring from index `p` to the end is a prefix of the pattern, False otherwise.
        """
        for i in range(p, len(self.pattern)):
            if self.pattern[i] != self.pattern[len(self.pattern) - 1 - i + p]:
                return False
        return True

    def length_of_suffix(self, p : int) -> int:
        """
        Computes the length of the longest suffix of the pattern starting from index `p` that matches a prefix of the pattern.

        This method aids in constructing the good suffix rule table. The length of matching suffix determines how far the pattern
        can potentially be shifted without missing potential matches in subsequent searches.

        Parameters
        ----------
        p : int
            The starting index in the pattern from which to determine the matching suffix length.

        Returns
        -------
        int
            The length of the suffix of the pattern starting from index `p` that matches the prefix of the pattern.
        """
        length = 0
        i = p
        j = len(self.pattern) - 1
        while i >= 0 and self.pattern[i] == self.pattern[j]:
            length += 1
            i -= 1
            j -= 1
        return length

    def search(self, text : str) -> list:
        """
        Searches for all occurrences of the pattern within the given text using the Boyer-Moore pattern matching algorithm.

        Parameters
        ----------
        text : str
            The text in which to search for the pattern.

        Returns
        -------
        list[int]
            A list of starting positions where the pattern is found within the text.
        """
        positions = []
        i = 0
        while i <= len(text) - len(self.pattern):
            shift = 1
            j = len(self.pattern) - 1
            while j >= 0 and self.pattern[j] == text[i + j]:
                j -= 1
            if j < 0:
                positions.append(i)
                i += self.good_suffix_rule[0]
            else:
                bad_character_shift = self.bad_character_rule.get(text[i + j], -1)
                i += max(shift, j - bad_character_shift, self.good_suffix_rule[j + 1])
        return positions


if __name__ == "__main__":

    pattern = input("Enter the pattern: ")
    sequence = input("Enter the sequence: ")
    bm = BoyerMoore(pattern)
    result = bm.search(sequence)
    print("Pattern occurs at positions:", result)

#Input example:
#Padrão: ana
#Sequência: bananarama

    print("Metricas de Codigo:")
    print("\nMetrica cyclomatic complexity:")
    print(subprocess.call(["radon","cc","ProcuraPadroes/BoyerMoore.py", "-s"]))
    print("\nMetrica maintainability index:")
    print(subprocess.call(["radon","mi","ProcuraPadroes/BoyerMoore.py", "-s"]))
    print("\nMetrica raw:")
    print(subprocess.call(["radon","raw","ProcuraPadroes/BoyerMoore.py", "-s"]))