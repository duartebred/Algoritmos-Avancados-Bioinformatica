import random; import subprocess


class ea_motif_finder:
    def __init__(self, sequences, motif_length, sequence_type='DNA', population_size=100, generations=500, mutation_rate=0.01):
        self.sequences = sequences
        self.sequence_type = sequence_type.upper()
        self.motif_length = motif_length
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.validate_sequences()
        self.validate_motif_length()

    def validate_sequences(self):
        if not isinstance(self.sequences, list) or not all(isinstance(seq, str) for seq in self.sequences):
            raise ValueError("Sequences should be a list of strings.")
        
        valid_dna_chars = set('ACGT')
        valid_protein_chars = set('ACDEFGHIKLMNPQRSTVWY')

        for seq in self.sequences:
            if self.sequence_type == 'DNA' and not set(seq.upper()).issubset(valid_dna_chars):
                raise ValueError("DNA sequences should only contain characters: A, C, G, T.")
            elif self.sequence_type == 'PROTEIN' and not set(seq.upper()).issubset(valid_protein_chars):
                raise ValueError("Protein sequences should only contain valid amino acid characters.")

    def validate_motif_length(self):
        if any(len(seq) < self.motif_length for seq in self.sequences):
            raise ValueError("Motif length cannot be greater than the length of any sequence provided.")

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            individual = []
            individual = [random.randint(0, len(seq) - self.motif_length) for seq in self.sequences]
            population.append(individual)
        return population


    def build_consensus(self, motifs):
        consensus = []
        for i in range(self.motif_length):
            column = [motif[i] for motif in motifs]
            consensus.append(max(set(column), key=column.count))
        return ''.join(consensus)


    def match_score(self, motif, consensus):
        return sum(1 for a, b in zip(motif, consensus) if a == b)


    def fitness(self, individual):
        motifs = [seq[start:start + self.motif_length] for seq, start in zip(self.sequences, individual)]
        consensus = self.build_consensus(motifs)
        score = sum(self.match_score(motif, consensus) for motif in motifs)
        return score


    def select_parents(self, population, fitnesses):
        total_fitness = sum(fitnesses)
        selection_probs = [f / total_fitness for f in fitnesses]
        parents_indices = random.choices(range(self.population_size), weights=selection_probs, k=2)
        return [population[parents_indices[0]], population[parents_indices[1]]]


    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, len(parent1) - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child


    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            seq_index = random.randint(0, len(individual) - 1)
            individual[seq_index] = random.randint(0, len(self.sequences[seq_index]) - self.motif_length)
        return individual


    def run(self):
        population = self.initialize_population()
        best_individual = None
        best_fitness = -1

        for generation in range(self.generations):
            fitnesses = [self.fitness(individual) for individual in population]
            new_population = []

            for _ in range(self.population_size):
                parent1, parent2 = self.select_parents(population, fitnesses)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)

            population = new_population
            current_best_fitness = max(fitnesses)
            current_best_individual = population[fitnesses.index(current_best_fitness)]

            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_individual = current_best_individual

            print(f"Generation {generation + 1}, Best Fitness: {best_fitness}")

        best_motifs = [seq[start:start + self.motif_length] for seq, start in zip(self.sequences, best_individual)]
        return best_motifs, self.build_consensus(best_motifs)


if __name__=='__main__':
    sequences = [
        "ATGCGATGACCTGACTGA",
        "TGCATGCATGCACTGATG",
        "ATGCGATGCCGTAGCTAG",
        "ATGCATGCATGCATGCAT",
        "TGCATGCGTACGTGCTAG"
    ]

    motif_length = 10
    ga_motif_finder = ea_motif_finder(sequences, motif_length)
    best_motifs, consensus = ga_motif_finder.run()

    print("\nBest Motifs:", best_motifs)
    print("Consensus Sequence:", consensus)

    print("\nMetricas de Codigo:")
    print("\nMetrica cyclomatic complexity:")
    print(subprocess.call(["radon","cc","EA/ea.py", "-s"]))
    print("\nMetrica maintainability index:")
    print(subprocess.call(["radon","mi","EA/ea.py", "-s"]))
    print("\nMetrica raw:")
    print(subprocess.call(["radon","raw","EA/ea.py", "-s"]))
