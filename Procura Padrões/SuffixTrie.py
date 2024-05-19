class SuffixTree:
    def __init__(self):
        self.root = {}
        self.end = '$'
        self.index = 0

    def build_suffix_tree(self, text):
        for i in range(len(text)):
            self._add_suffix(text[i:] + self.end, i)

    def _add_suffix(self, suffix, index):
        node = self.root
        for char in suffix:
            if char not in node:
                node[char] = {}
            node = node[char]
        node[self.end] = index

    def find_pattern(self, pattern):
        node = self.root
        for char in pattern:
            if char in node:
                node = node[char]
            else:
                return None
        return self._collect_leaves(node)

    def _collect_leaves(self, node):
        result = []
        if self.end in node:
            result.append(node[self.end])
        else:
            for child in node.values():
                result.extend(self._collect_leaves(child))
        return result

    def print_tree(self):
        self._print_node(self.root)

    def _print_node(self, node, indent=""):
        for char, child in node.items():
            if char == self.end:
                print(f"{indent}{char} -> {child}")
            else:
                print(f"{indent}{char} ->")
                self._print_node(child, indent + "  ")

    def get_repeats(self, min_length, min_repeats):
        repeats = []
        self._find_repeats(self.root, "", repeats, min_length, min_repeats)
        return repeats

    def _find_repeats(self, node, prefix, repeats, min_length, min_repeats):
        for char, child in node.items():
            if char == self.end:
                continue
            new_prefix = prefix + char
            leaves = self._collect_leaves(child)
            if len(leaves) >= min_repeats and len(new_prefix) >= min_length:
                repeats.append((new_prefix, leaves))
            self._find_repeats(child, new_prefix, repeats, min_length, min_repeats)


def main():
    # Create a SuffixTree instance and build it using a sample text
    st = SuffixTree()
    text = "bananaban$"
    st.build_suffix_tree(text)

    # Print the entire suffix tree
    print("Suffix Tree:")
    st.print_tree()

    # Test pattern search in the suffix tree
    patterns = ["banana", "ana", "nab", "ban"]
    for pattern in patterns:
        result = st.find_pattern(pattern)
        if result:
            print(f"Pattern '{pattern}' found at positions: {result}")
        else:
            print(f"Pattern '{pattern}' not found in the tree.")

    # Print repeats
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
