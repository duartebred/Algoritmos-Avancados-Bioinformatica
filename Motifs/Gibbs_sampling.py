# w-> window size of the motif
# t -> size of each sequence, all sequences have the same length
# n -> number of sequences


class pwm:
    """
    This class stores all the functions needed to generate the position weight matrix of a list of sequences. It also includes the function 
    to calculate the probability of a sequence being generated by the PWM
    
    Parameters
    ------------
    seqs: list[str]
        The list of sequences used to generate the PWM
    
    seq_type: str
        The type of the biological sequences used to generate the PWM
        
    pseudo: int
        Value of pseudocount to prevent matrix entries to have value of 0
    
    """
    def __init__(self, seqs: list[str] =None, seq_type: str = 'DNA', pseudo: int =1) -> None:
        self.seqs = seqs
        self.seq_type = seq_type
        self.pseudo = pseudo
        #self.pwm = self.genarete_pwm()

    def alfabeto(self) -> str:
        """
        Returns the alphabet for the given sequence type

        Returns
        -------
        str
            Alphabet of the given sequence type
        
        Raises
        ------
        AssertionError
            If the sequence is not a valid biological sequence
            
        """
        valid_type = ['DNA', 'RNA', 'PROTEIN']

        assert isinstance(self.seq_type,str), 'The sequence type must be a string'
        assert self.seq_type.upper() in valid_type, f' The seq type {self.seq_type} is not a valid biological sequence'

        if self.seq_type.upper() == "DNA":
            return "ACGT"
        elif self.seq_type.upper() == "RNA":
            return "ACGU"
        else:
            return "ABCDEFGHIKLMNPQRSTVWYZ"

    def generate_pwm(self) -> list[dict[str, float]]:
        """
        Genaretes a position weight matrix (PWM) from a list of aligned sequences
                
        Returns
        -------
        list[dict[str, float]]
            Probabillity of each letter in the alphabet being present in a specific position
        
        Raises
        ------
        AssertionError
            - If the sequences are not given in a list
            - If the lengths of at least one of the sequences differ from the rest
            - If at least one elemet of the sequences is not present in the alphabet
            
        """
        # Check if sequences are provided in a list
        assert isinstance(self.seqs, list), 'Sequences must be a list'
        # Check if all sequences have the same length
        assert all(len(self.seqs[0])==len(seq)for seq in self.seqs), 'As sequencias devem possuir o mesmo tamanho'
        # Obtain the alphabet
        alphabet = self.alfabeto()
        # Check if  each element in sequences is in the alphabet
        for seq in self.seqs:
            for pos, elem in enumerate(seq):
                assert elem in alphabet, f"The element '{elem}' at position {pos + 1} in sequence {seq} is not in the alphabet of {self.seq_type}. Please ensure all elements are in uppercase."

        # Initializing list to store the resulting PWM
        resulting_pwm= []

        # Calculate frequencies for each position
        for coluna in list(zip(*self.seqs)):
            contagem = {elem:(coluna.count(elem) + self.pseudo) / (len(self.seqs) + len(alphabet) * self.pseudo) for elem in alphabet}
            resulting_pwm.append(contagem)
        return resulting_pwm
    
    def prob_seq(self, seq: str)->float:
        """
        Calculate the probability of a givens sequence being genareted by the PWM
        Esta função calcula a probabilidade de uma determinada sequencia ter sido gerada pela PWM

        Parameters
        ---------
        seq:str
            Sequence to calculate the probability of being generated by the PWM


        Returns
        -------
        float
            Probability of the provided sequence being generated by the PWM

        Raises
        ------
        AssertionError
            If the length of the sequence is not equal to the length of the PWM
        """
        pwm= self.generate_pwm()
        # Check if the length of the sequence is smaller or have the length of the PWM
        assert len(seq) <= len(pwm), f"The sequence '{seq}' is not the same length as the PWM"

        # Initialize product to store probability
        product = 1

        # Calculate the probability of the sequence
        for index, elem in enumerate(seq):
            product *= pwm[index][elem]
        
        return product
    

class Gibbs (pwm):
    """
    Contains all the functions needed to do motif search using the Gibbs sampling algorithm
    """
    def __init__(self, list_seqs: list[str], w: int, seq_type='DNA', pseudo=1):
        """
        Initialize Gibbs sampler.

        Parameters
        ----------
        list_seqs : list[str]
            List of input sequences.
        w : int
            Motif length.
        seq_type : str, optional
            Biological type of sequences (default is 'DNA').
        pseudo : int, optional
            Pseudo count for PWM (default is 1).
        """
        self.seqs = list_seqs
        self.w = w
        self.seq_type = seq_type
        self.pseudo = pseudo
        
    def random_init_pos(self) -> list[int]:
        """
        Gives random positions to initialize motif search.

        Returns
        -------
        list[int]
            List of random initial positions.

        Raises
        ------
        AssertionError
            If the sequences are not provided in a list.
        """
        import random

        # CHeck if sequences is a list
        assert isinstance(self.seqs,list), 'Sequences must be a list'

        # Get the length of each sequence and the total number of sequences
        t = len(self.seqs[0])  
        n = len(self.seqs)  

        # Calculate the maximum possible position to from a motif with length w
        max_pos = t - self.w 

        # Choose random positions between 0 and max_pos for each sequence
        positions = [random.randint(0, max_pos) for _ in range(n)]

        return positions
    
    def random_seq(self) -> int:
        """
        Generate a random integer representing the sequence index.

        Returns
        -------
        int
            Randomly generated sequence index.

        Raises
        ------
        AssertionError
            If the sequences are not provided in a list.
        """
        import random

        # Check if sequences are in a list
        assert isinstance(self.seqs,list), 'Sequences must be provided in a list'
        
        # Get the number of sequences
        n = len(self.seqs)

        # Generate a random sequence index
        sequence_index = random.randint(0, n - 1)

        return sequence_index
    
    def new_seqs(self, pos: list[int], seq_idx: int) -> tuple[list[str], str]:
        """
        Generate subsequences of length w based on given positions excluding one of the sequences.

        Parameters
        ----------
        pos : list[int]
            List of positions.
        seq_idx : int
            Index of the sequence to be excluded.

        Returns
        -------
        tuple[list[str], str]
            Tuple containing the subsequences and excluded sequence.
        """
        assert isinstance(pos,list) and isinstance(seq_idx,int)

        novas_seqs = [self.seqs[idx][P:P + self.w] for idx, P in enumerate(pos) if idx != seq_idx]  # create the motifs with the size w
        return novas_seqs, self.seqs[seq_idx]
    
    def prob(self, pos: list[int], seq_idx: int, first=True):
        """
        Calculate probabilities of each position for a sequence.

        Parameters
        ----------
        pos : list[int]
            List of positions.
        seq_idx : int
            Index of the sequence.
        first : bool, optional
            Boolean flag to indicate if it's the first run (default is True).

        Returns
        -------
        list[float]
            List of probabilities.
        """
        if first:
            possible_motiff, seq_excluded = self.new_seqs(pos, seq_idx)

        else:
            possible_motiff = [seq[pos[idx]: pos[idx] + self.w] for idx, seq in enumerate(self.seqs) if idx != seq_idx]
            seq_excluded = self.seqs[seq_idx]

        #super().__init__(possible_motiff, self.seq_type, self.pseudo)
        t = len(self.seqs[0])
        max_pos = t - self.w
        seqs_pwm = pwm(possible_motiff, self.seq_type, self.pseudo).genarete_pwm()
        prob = []

        for I in range(max_pos + 1):
            seq = seq_excluded[I:I + self.w]
            prob.append(self.prob_seq(seq, seqs_pwm))

        return [prob[I] / sum(prob) for I in range(len(prob))]

    def roulette_wheel(self, probs: list[float]):
        """
        Randomly selects a sequence  based on probabilities.

        Parameters
        -----------
        probs List[float]: 
            List of probabilities for each index.

        Returns
        ----------
        int: 
            The selected index.

        Raises
        ----------
        AssertionError:
            If the sum of the list of probabilities is not 1
        """
        import random
        assert (round(sum(probs), 0) == 1)
        pos = [I for I in range(len(probs))]

        return random.choices(pos, probs, k=1)

    def score(self, off: list[int]) -> int:
        alfa=self.alfabeto()
        snips = [self.seqs[I][p:p + self.w] for I, p in enumerate(off)]
        return sum(max({x: s.count(x) for x in alfa}.values()) for s in zip(*snips))

    def gibbs_sampling(self):
        pos = self.random_init_pos()
        first_run, max_sc, contador = True, 0, 0

        while True:
            seq_idx = self.random_seq()

            if first_run:
                probs, first_run = self.prob(pos, seq_idx), False
            
            else: probs = self.prob(pos, seq_idx, first=False)

            pos[seq_idx] = self.roulette_wheel(probs)[0]

            if self.score(pos) > max_sc:
                best_off, max_sc, contador = pos.copy(), self.score(pos), 0 

            else:
                contador += 1
                if contador >=50: break

        return best_off, max_sc
