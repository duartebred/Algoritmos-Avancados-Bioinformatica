import subprocess

class SuffixTree:
    """
    This class implements a basic suffix tree for storing substrings of a text efficiently.
    It allows building the suffix tree from a given text, searching for patterns, and collecting indexes of substrings.

    Attributes
    ----------
    root : dict
        The root of the suffix tree, represented as a nested dictionary.
    end : str
        Special character used to denote the end of a substring in the tree.
    index : int
        Used to keep track of the position of substrings.
    """

    def __init__(self):
        """
        Initializes the suffix tree with an empty root dictionary, a special end character, and an index counter set to zero.
        """
        self.root = {}
        self.end = '$'
        self.index = 0

    def build_suffix_tree(self, text: str) -> None:
        """
        Builds the suffix tree by adding each suffix of the given text to the tree.

        Parameters
        ----------
        text : str
            The text from which to build the suffix tree.
        """
        for i in range(len(text)):
            self._add_suffix(text[i:] + self.end, i)

    def _add_suffix(self, suffix: str, index: int) -> None:
        """
        Adds a suffix to the tree at a given index.

        Parameters
        ----------
        suffix : str
            The suffix to add to the tree.
        index : int
            The starting position of the suffix in the original text.
        """
        node = self.root
        for char in suffix:
            if char not in node:
                node[char] = {}
            node = node[char]
        node[self.end] = index

    def find_pattern(self, pattern: str) -> list[int]:
        """
        Searches for a given pattern in the suffix tree and returns the starting indices where the pattern is found.

        Parameters
        ----------
        pattern : str
            The pattern to search for in the tree.

        Returns
        -------
        list[int]
            A list of starting indices where the pattern is found, or None if the pattern is not found.
        """
        node = self.root
        for char in pattern:
            if char in node:
                node = node[char]
            else:
                return None
        return self._collect_leaves(node)

    def _collect_leaves(self, node: dict) -> list[int]:
        """
        Collects all indices stored in the leaves of a given node.

        Parameters
        ----------
        node : dict
            The node from which to collect leaves.

        Returns
        -------
        list[int]
            A list of indices collected from the leaves.
        """
        result = []
        if self.end in node:
            result.append(node[self.end])
        else:
            for child in node.values():
                result.extend(self._collect_leaves(child))
        return result

    def print_tree(self) -> None:
        """
        Prints a visual representation of the suffix tree.
        """
        self._print_node(self.root)

    def _print_node(self, node: dict, indent: str = "") -> None:
        """
        Recursively prints each node of the tree with indentation to represent tree structure.

        Parameters
        ----------
        node : dict
            The current node to print.
        indent : str
            The indentation to use for visual hierarchy.
        """
        for char, child in node.items():
            if char == self.end:
                print(f"{indent}{char} -> {child}")
            else:
                print(f"{indent}{char} ->")
                self._print_node(child, indent + "  ")

    def get_repeats(self, min_length: int, min_repeats: int) -> list[tuple[str, list[int]]]:
        """
        Finds and returns patterns in the text that occur a minimum number of times and are of a minimum length.

        Parameters
        ----------
        min_length : int
            The minimum length of the repeat pattern.
        min_repeats : int
            The minimum number of times the pattern must occur.

        Returns
        -------
        list[tuple[str, list[int]]]
            A list of tuples containing the pattern and the list of starting indices where the pattern occurs.
        """
        repeats = []
        self._find_repeats(self.root, "", repeats, min_length, min_repeats)
        return repeats

    def _find_repeats(self, node: dict, prefix: str, repeats: list, min_length: int, min_repeats: int) -> None:
        """
        Recursively searches for repeat patterns within the tree.

        Parameters
        ----------
        node : dict
            The current node in the suffix tree.
        prefix : str
            The accumulated prefix representing the path to the current node.
        repeats : list
            A list to store discovered repeat patterns.
        min_length : int
            Minimum length of repeat patterns to consider.
        min_repeats : int
            Minimum occurrences of a pattern to consider it a repeat.

        """
        for char, child in node.items():
            if char == self.end:
                continue
            new_prefix = prefix + char
            leaves = self._collect_leaves(child)
            if len(leaves) >= min_repeats and len(new_prefix) >= min_length:
                repeats.append((new_prefix, leaves))
            self._find_repeats(child, new_prefix, repeats, min_length, min_repeats)


def main():
    
    st = SuffixTree()
    text = "bananaban$"
    st.build_suffix_tree(text)

   
    print("Suffix Tree:")
    st.print_tree()

    
    patterns = ["banana", "ana", "nab", "ban"]
    for pattern in patterns:
        result = st.find_pattern(pattern)
        if result:
            print(f"Pattern '{pattern}' found at positions: {result}")
        else:
            print(f"Pattern '{pattern}' not found in the tree.")


    min_length = 2
    min_repeats = 2
    repeats = st.get_repeats(min_length, min_repeats)
    if repeats:
        print(f"Patterns of at least length {min_length} repeated at least {min_repeats} times:")
        for repeat in repeats:
            print(f"Pattern '{repeat[0]}' found at positions: {repeat[1]}")
    else:
        print(f"No repeats of length {min_length} occurring at least {min_repeats} times found.")

if __name__ == "__main__":
    main()

    print("Metricas de Codigo:")
    print("\nMetrica cyclomatic complexity:")
    print(subprocess.call(["radon","cc","ProcuraPadroes/Suffix_tree.py", "-s"]))
    print("\nMetrica maintainability index:")
    print(subprocess.call(["radon","mi","ProcuraPadroes/Suffix_tree.py", "-s"]))
    print("\nMetrica raw:")
    print(subprocess.call(["radon","raw","ProcuraPadroes/Suffix_tree.py", "-s"]))