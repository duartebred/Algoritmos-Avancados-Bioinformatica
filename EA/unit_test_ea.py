import unittest
from ea import ea_motif_finder


class Test_ea_motif_finder(unittest.TestCase):
    def setUp(self):
        self.dna_sequences = [
            "ATGCGATGACCTGACTGA",
            "TGCATGCATGCACTGATG",
            "ATGCGATGCCGTAGCTAG",
            "ATGCATGCATGCATGCAT",
            "TGCATGCGTACGTGCTAG"
        ]
        self.protein_sequences = [
            "MVLSEGEWQLVLHVWAKV",
            "KVLSEGEWQLVHVWAKVE",
            "MVLSEGEWQLVHVWAKVS",
            "MVLSEGEWQLVHVWAKVG",
            "MVLSEGEWQLVHVWAKVD"
        ]
        self.short_dna_sequences = [
            "ATGC",
            "GCAT",
            "CATG",
            "ATGC"
        ]
        self.identical_dna_sequences = [
            "ATGCGATGACCTGACTGA",
            "ATGCGATGACCTGACTGA",
            "ATGCGATGACCTGACTGA",
            "ATGCGATGACCTGACTGA",
            "ATGCGATGACCTGACTGA"
        ]
        self.motif_length = 5

    def test_dna_sequences(self):
        ga_motif_finder = ea_motif_finder(self.dna_sequences, self.motif_length, generations=100)
        best_motifs, consensus = ga_motif_finder.run()
        self.assertEqual(len(consensus), self.motif_length)
        for motif in best_motifs:
            self.assertTrue(any(motif in seq for seq in self.dna_sequences))

    def test_protein_sequences(self):
        ga_motif_finder = ea_motif_finder(self.protein_sequences, self.motif_length, generations=100)
        best_motifs, consensus = ga_motif_finder.run()
        self.assertEqual(len(consensus), self.motif_length)
        for motif in best_motifs:
            self.assertTrue(any(motif in seq for seq in self.protein_sequences))

    def test_short_dna_sequences(self):
        ga_motif_finder = ea_motif_finder(self.short_dna_sequences, 3, generations=100)
        best_motifs, consensus = ga_motif_finder.run()
        self.assertEqual(len(consensus), 3)
        for motif in best_motifs:
            self.assertTrue(any(motif in seq for seq in self.short_dna_sequences))


    def test_different_lengths(self):
        different_length_sequences = [
            "ATGCGATGACCTGACTGA",
            "TGCATGCATGCACTGAT",
            "ATGCGATGCCGTAGC",
            "ATGCATGCATGCATGCAT",
            "TGCATGCGTACGTGCTAG"
        ]
        ga_motif_finder = ea_motif_finder(different_length_sequences, self.motif_length, generations=100)
        best_motifs, consensus = ga_motif_finder.run()
        self.assertEqual(len(consensus), self.motif_length)
        for motif in best_motifs:
            self.assertTrue(any(motif in seq for seq in different_length_sequences))

if __name__ == '__main__':
    unittest.main()
