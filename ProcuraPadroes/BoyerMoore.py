class BoyerMoore:
    def __init__(self, pattern):
        self.pattern = pattern
        self.pattern_length = len(pattern)
        self.bad_character_rule = self.create_bad_character_table()
        self.good_suffix_rule = self.create_good_suffix_table()

    def create_bad_character_table(self):
        table = {}
        for i in range(len(self.pattern)):
            table[self.pattern[i]] = i
        return table

    def create_good_suffix_table(self):
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

    def is_prefix(self, p):
        for i in range(p, len(self.pattern)):
            if self.pattern[i] != self.pattern[len(self.pattern) - 1 - i + p]:
                return False
        return True

    def length_of_suffix(self, p):
        length = 0
        i = p
        j = len(self.pattern) - 1
        while i >= 0 and self.pattern[i] == self.pattern[j]:
            length += 1
            i -= 1
            j -= 1
        return length

    def search(self, text):
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

# Test the implementation
pattern = input("Enter the pattern: ")
sequence = input("Enter the sequence: ")
bm = BoyerMoore(pattern)
result = bm.search(sequence)
print("Pattern occurs at positions:", result)