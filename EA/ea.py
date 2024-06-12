import random; import subprocess


class ea_motif_finder:
    def __init__(self, sequences: list[str], motif_length:int, sequence_type:str='DNA', population_size:int=100, generations:int=500, mutation_rate:float=0.01):
        """
        Initialize the motif finder with the provided parameters.

        Parameters:
        --------------
        sequences (list): 
            A list of DNA or protein sequences.
        motif_length (int): 
            The length of the motif to be found.
        sequence_type (str, optional):
             The type of sequences, either 'DNA' or 'PROTEIN'. Defaults to 'DNA'.
        population_size (int, optional):
             The size of the population for the genetic algorithm. Defaults to 100.
        generations (int, optional):
             The number of generations for the genetic algorithm. Defaults to 500.
        mutation_rate (float, optional):
             The mutation rate for the genetic algorithm. Defaults to 0.01.

        Returns:
        None
        """
        self.sequences = sequences
        self.sequence_type = sequence_type.upper()
        self.motif_length = motif_length
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.validate_sequence_type()
        self.validate_sequences()
        self.validate_motif_length()


    def validate_sequence_type(self):
        """
        Validates the sequence type.

        Parameters:
        --------------
        self (object): 
            The instance of the class.

        Returns:
        -------------
        None
            If the sequence type is valid, it returns None.
            If the sequence type is invalid, it raises a ValueError.

        Raises:
        ----------------
        ValueError:
            If the sequence type is not 'DNA' or 'PROTEIN'.
        """
        if self.sequence_type.upper() not in ['DNA', 'PROTEIN']:
            raise ValueError("sequence_type must be either 'DNA' or 'PROTEIN'.")
        

    def validate_sequences(self):
        """
        Validates the sequences given.

        Parameters:
        --------------
        self (object): 
            The instance of the class.

        Returns:
        -------------
        None
            If the sequences are valid, it returns None.
            If the sequences are invalid, it raises a ValueError.

        Raises:
        ----------------
        ValueError:
            If the sequences are not a list of strings.
            If the sequences contain characters other than valid DNA or protein characters.

        """
        if not isinstance(self.sequences, list) or not all(isinstance(seq, str) for seq in self.sequences):
            raise ValueError("Sequences should be a list of strings.")
        
        dna_alfa = set('ACGT')
        protein_alfa = set('ACDEFGHIKLMNPQRSTVWY')

        for seq in self.sequences:
            if self.sequence_type == 'DNA' and not set(seq.upper()).issubset(dna_alfa):
                raise ValueError("DNA sequences should only contain characters: A, C, G, T.")
            elif self.sequence_type == 'PROTEIN' and not set(seq.upper()).issubset(protein_alfa):
                raise ValueError("Protein sequences should only contain valid amino acid characters.")


    def validate_motif_length(self):
        """
        Validates the motif length against the length of the sequences.

        Parameters:
        --------------
        self (object): 
            The instance of the class.

        Returns:
        -------------
        None
            If the motif length is valid, it returns None.
            If the motif length is invalid, it raises a ValueError.

        Raises:
        ----------------
        ValueError:
            If the motif length is greater than the length of any sequence provided.

        """
        if any(len(seq) < self.motif_length for seq in self.sequences):
            raise ValueError("Motif length cannot be greater than the length of any sequence provided.")


    def initialize_population(self)->list[list[int]]:
        """
        Initializes the population for the genetic algorithm.

        Parameters:
        --------------
        self (object): 
            The instance of the class.

        Returns:
        -------------
        population (list[list[int]]): 
            A list of individuals, where each individual is represented as a list of starting indices for motifs in the sequences.

        """
        population = []
        for _ in range(self.population_size):
            individual = []
            individual = [random.randint(0, len(seq) - self.motif_length) for seq in self.sequences]
            population.append(individual)
        return population


    def build_consensus(self, motifs:list[str])->str:
        """
        Constructs a consensus sequence from a set of motifs.

        Parameters:
        --------------
        self (object): 
            The instance of the class.
        motifs (list[str]): 
            A list of motifs, where each motif is represented as a string.

        Returns:
        -------------
        consensus (str): 
            A consensus sequence, which is a string representing the most common character at each position across all motifs.

        """
        consensus = []
        for i in range(self.motif_length):
            column = [motif[i] for motif in motifs]
            consensus.append(max(set(column), key=column.count))
        return ''.join(consensus)


    def match_score(self, motif:str, consensus:str)->int:
        """
        Calculates the match score between a motif and a consensus sequence.

        Parameters:
        --------------
        self (object): 
            The instance of the class.
        motif (str): 
            A motif, represented as a string.
        consensus (str): 
            A consensus sequence, represented as a string.

        Returns:
        -------------
        score (int): 
            The match score, which is the number of positions where the motif and consensus sequences match.

        """
        return sum(1 for a, b in zip(motif, consensus) if a == b)


    def fitness(self, individual:list[int])->int:
        """
        Calculates the fitness of an individual in the population.

        Parameters:
        --------------
        self (object): 
            The instance of the class.
        individual (list[int]): 
            An individual, represented as a list of starting indices for motifs in the sequences.

        Returns:
        -------------
        score (int): 
            The fitness score of the individual, which is calculated as the sum of match scores between the motifs and the consensus sequence.

        """
        motifs = [seq[start:start + self.motif_length] for seq, start in zip(self.sequences, individual)]
        consensus = self.build_consensus(motifs)
        score = sum(self.match_score(motif, consensus) for motif in motifs)
        return score


    def select_parents(self, population:list[list[int]], fitnesses:list[int]):
        """
        Selects two parents from the population based on their fitness scores.

        Parameters:
        --------------
        self (object): 
            The instance of the class.
        population (list): 
            A list of individuals, where each individual is represented as a list of starting indices for motifs in the sequences.
        fitnesses (list): 
            A list of fitness scores corresponding to each individual in the population.

        Returns:
        -------------
        parents (list): 
            A list containing two selected parent individuals.

        """
        total_fitness = sum(fitnesses)
        selection_probs = [fit / total_fitness for fit in fitnesses]
        parents_indices = random.choices(range(self.population_size), weights=selection_probs, k=2)
        return [population[parents_indices[0]], population[parents_indices[1]]]


    def crossover(self, parent1:list[int], parent2:list[int])->list[int]:
        """
        Performs crossover operation on two parent individuals to generate a child individual.

        Parameters:
        --------------
        self (object): 
            The instance of the class.
        parent1 (list[int]): 
            The first parent individual, represented as a list of starting indices for motifs in the sequences.
        parent2 (list[int]): 
            The second parent individual, represented as a list of starting indices for motifs in the sequences.

        Returns:
        -------------
        child (list[int]): 
            A child individual generated by combining parts of the parent individuals.

        """
        crossover_point = random.randint(1, len(parent1) - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child


    def mutate(self, individual:list[int])->list[int]:
        """
        Performs mutation operation on an individual.

        Parameters:
        --------------
        self (object): 
            The instance of the class.
        individual (list[int]): 
            The individual to be mutated, represented as a list of starting indices for motifs in the sequences.

        Returns:
        -------------
        individual (list[int]): 
            The mutated individual.

        Notes:
        ----------------
        The mutation operation involves randomly selecting a sequence index and changing the starting index of the motif in that sequence.
        The new starting index is chosen randomly within the valid range for that sequence.
        The mutation operation is performed with a probability equal to the mutation rate specified during class initialization.
        """
        if random.random() < self.mutation_rate:
            seq_index = random.randint(0, len(individual) - 1)
            individual[seq_index] = random.randint(0, len(self.sequences[seq_index]) - self.motif_length)
        return individual


    def run(self)->tuple[list[str], str]:
        """
        Runs the evolutionary algorithm to find the best motifs.

        Parameters:
        --------------
        self (object): 
            The instance of the class.

        Returns:
        -------------
        best_motifs (list[str]): 
            The best motifs found by the genetic algorithm.
        consensus (str): 
            The consensus sequence of the best motifs.

        Notes:
        ----------------
        The genetic algorithm is performed for the specified number of generations.
        In each generation, the fitness of each individual in the population is calculated.
        Parents are selected based on their fitness scores.
        A child individual is generated by combining parts of the parent individuals through crossover.
        The child individual may undergo mutation.
        The new population replaces the old population.
        The best individual and its fitness score are updated at the end of each generation.
        The process continues until the specified number of generations is reached.
        """
        population = self.initialize_population()
        best_individual, best_fitness = None,-1

        for generation in range(self.generations):
            fitnesses = [self.fitness(individual) for individual in population]
            new_population = []

            for _ in range(self.population_size):
                parent1, parent2 = self.select_parents(population, fitnesses)
                child = self.crossover(parent1, parent2); self.mutate(child)
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
    best_motifs, consensus = ea_motif_finder(sequences, motif_length).run()

    print("\nBest Motifs:", best_motifs)
    print("Consensus Sequence:", consensus)

    print("\nMetricas de Codigo:")
    print("\nMetrica cyclomatic complexity:")
    print(subprocess.call(["radon","cc","EA/ea.py", "-s"]))
    print("\nMetrica maintainability index:")
    print(subprocess.call(["radon","mi","EA/ea.py", "-s"]))
    print("\nMetrica raw:")
    print(subprocess.call(["radon","raw","EA/ea.py", "-s"]))
