# w-> window size of the motif
# t -> size of each sequence, all sequences have the same length
# n -> number of sequences

seqs = ['GTAAACAATATTTATAGC', 'AAAATTTACCTTAGAAGG', 'CCGTACTGTCAAGCGTGG', 'TGAGTAAACGACGTCCCA', 'TACTTAACACCCTGTCAA']


# selecting randomly the initial position


def random_init_pos(list_seqs: list[str], w: int) -> list[int]:
    import random
    t = len(list_seqs[0])  # length of each seq
    n = len(list_seqs)  # number of seqs
    max_pos = t - w  # last possible position the use to form a seq with length w
    pos = [random.randint(0, max_pos) for _ in range(n)]  # choose random positions between 0 and max_pos

    return pos


def random_seq(list_seqs: list[str]) -> int:
    import random
    n = len(list_seqs)
    return random.randint(0, n - 1)


def new_seqs(list_seqs, w, pos, seq_idx):
    novas_seqs = [list_seqs[i][P:P + w] for i, P in enumerate(pos) if i != seq_idx]  # create the motifs with the size w
    return novas_seqs, seqs[seq_idx], seq_idx


def alfabeto(tipo_seq: str) -> list[str]:
    '''
    Esta função recebe o tipo de uma sequência e devolve o seu respetivo alfabeto

    Parameters
    ---------
    tipo_seq:str
        Tipo válido de uma sequência biológica. Pode assumir os valores de DNA, RNA, protein,
        proteína ou prot

    Returns
    -------
    list(str)
        Composto pelo tipo de sequência e o seu respetivo alfabeto
    
    Raises
    ------
    ValueError
        Quando o tipo de sequência fornecido não é um tipo de sequência biológica válida
    '''
    if tipo_seq.upper() == "DNA":
        DNA = "ACGT"
        return [tipo_seq.upper(), DNA]
    elif tipo_seq.upper() == "RNA":
        RNA = "ACGU"
        return [tipo_seq.upper(), RNA]
    elif tipo_seq.upper() in ["PROTEIN", "PROTEINA", "PROT"]:
        protein = "ABCDEFGHIKLMNPQRSTVWYZ"
        return ["Proteína", protein]
    else:
        raise ValueError(f"O tipo {tipo_seq} não é válido. Os tipos de cadeia válida são: DNA, RNA ou proteina")


def pwm(list_seqs: list[str], tipo_seq: str, pseudo=0) -> list[dict[str, float]]:
    '''
    Esta função recebe uma lista de sequências alinhadas e devolve uma matriz desingada de position weigth matrix (PWM), onde se representa
    a probabilidade de cada letra de um dado alfabeto biológico estar presente numa determinada posição.

    Parameters
    ----------
    list_seqs:list(str)
        Contêm um conjunto de sequências alinhadas em formato de string

    tipo_seq:str
        Tipo da sequencia que se pretende realiazar a PWM. Pode assumir o valor de DNA, RNA, protein, proteína ou prot

    pseudo: int ou float
        Valor a utilizar para realizar a pseudocontagem. Por padrão o valor é 0

    Returns
    -------
    PWM:list(dict)
        Valor da probabilidade de cada letra do alfabeto estar presente em cada posição das sequências
    
    Raises
    ------
    AssertionError
        Quando um elemento de uma das sequências fornecidas não está presente no alfabeto utilizado

        Quando o tamanho das sequências fornecidas é diferente
    '''
    alfa = alfabeto(tipo_seq)

    tamanho = []

    for I, seq in enumerate(list_seqs):
        tamanho.append(len(list_seqs))
        for pos, elem in enumerate(seq):
            assert elem in alfa[
                1], f"Na sequencia {seq}, o elemento {elem} na posição {pos + 1} não se encontra no alfabeto do {alfa[0]}"
        assert tamanho[I] == tamanho[I - 1], f"A sequência {seq} não possui o mesmo tamanho que as restantes"

    elementos_coluna = list(zip(*seqs))

    PWM = []

    for coluna in elementos_coluna:
        contagem = {}
        for elem in alfa[1]:
            contagem[elem] = (coluna.count(elem) + pseudo) / (len(seqs) + len(alfa[1]) * pseudo)

        PWM.append(contagem)

    return PWM


def prob_seq(seq: str, PWM: list[dict[str, float]]):
    '''
    Esta função calcula a probabilidade de uma determinada sequencia ter sido gerada pela PWM

    Parameters
    ---------
    seq:str
        Sequência que se pretende calcular a probabilidade de ter sido gerada pela PWM
    
    PWM:list(dict[str,floar])
        Corresponde às probabilidades de cada elemento aparecer nas várias posições da sequência

    Returns
    -------
    prod:float
        Probabilidade de a sequencia fornecida ter sido gerada pela PWM

    Raises
    ------
    AssertionError
        Quando o tamanho da sequência não é igual ao tamanho da PWM

    '''
    assert len(seq) <= len(PWM), f"A sequência {seq} não é do mesmo tamanho que a PWM"

    prod = 1
    for I, elem in enumerate(seq):
        prod = prod * PWM[I][elem]
    return prod


def prob(list_seqs: list[str], w, pos, seq_idx, seq_type='DNA', pseudo=1, first=True):
    if first:
        possible_motiff, seq_excluded, _ = new_seqs(list_seqs, w, pos, seq_idx)

    else:
        possible_motiff = [seq[pos[idx]:pos[idx] + w] for idx, seq in enumerate(list_seqs) if idx != seq_idx]
        seq_excluded = seqs[seq_idx]

    t = len(list_seqs[0])
    max_pos = t - w
    PWM = pwm(possible_motiff, seq_type, pseudo)
    prob = []

    for I in range(max_pos + 1):
        seq = seq_excluded[I:I + w]
        prob.append(prob_seq(seq, PWM))

    return [prob[I] / sum(prob) for I in range(len(prob))]

def prob_2(list_seqs: list[str], w, pos, seq_idx, seq_type='DNA', pseudo=1, first=True):
    if first:
        possible_motiff, seq_excluded, _ = new_seqs(list_seqs, w, pos, seq_idx)

    else:
        possible_motiff = [seq[pos[idx]:pos[idx] + w] for idx, seq in enumerate(list_seqs) if idx != seq_idx]
        seq_excluded = seqs[seq_idx]

    t = len(list_seqs[0])
    max_pos = t - w
    PWM = pwm(possible_motiff, seq_type, pseudo)
    prob = []

    for I in range(max_pos + 1):
        seq = seq_excluded[I:I + w]
        prob.append(prob_seq(seq, PWM))

    return prob

def roulette_wheel(probs: list[float]):
    import random
    assert (round(sum(probs), 0) == 1)
    pos = [I for I in range(len(probs))]

    return random.choices(pos, probs, k=1)

def roulette_wheel_2(probs: list[float]):
    import random
    target = random.random() * sum(probs)
    soma = 0

    for I,prob in enumerate(probs):
        soma += prob

        if soma >= target:
            return I

def score(off: list[int], seqs: list[str], w: int) -> int:
    snips = [seqs[I][p:p + w] for I, p in enumerate(off)]
    return sum(max({x: s.count(x) for x in 'ACGT'}.values()) for s in zip(*snips))


def gibbs_sampling_2(list_seqs: list[str], w: int, seq_type='DNA', pseudo=1):
    pos = random_init_pos(list_seqs, w)
    seq_idx = random_seq(list_seqs)

    # first run
    probs = prob_2(list_seqs, w, pos, seq_idx, seq_type, pseudo)
    posicao = roulette_wheel_2(probs)
    pos[seq_idx] = posicao
    max_sc = score(pos, seqs, w)
    best_off = pos.copy()

    # continuing till there's no change in the score after 10 iterations

    contador = 0

    while True:
        seq_idx = random_seq(list_seqs)
        probs = prob(list_seqs, w, pos, seq_idx, seq_type=seq_type, first=False)
        posicao = roulette_wheel_2(probs)
        pos[seq_idx] = posicao

        if score(pos, list_seqs, w) > max_sc:
            best_off = pos.copy()
            max_sc = score(pos, seqs, w)
            contador = 0

        else:
            contador += 1

        if contador >= 100:
            break

    return best_off, max_sc


def gibbs_sampling(list_seqs: list[str], w: int, seq_type='DNA', pseudo=1):
    pos = random_init_pos(list_seqs, w)
    seq_idx = random_seq(list_seqs)

    # first run
    probs = prob(list_seqs, w, pos, seq_idx, seq_type, pseudo)
    posicao = roulette_wheel(probs)
    pos[seq_idx] = posicao[0]
    max_sc = score(pos, seqs, w)
    best_off = pos.copy()

    # continuing till there's no change in the score after 10 iterations

    contador = 0

    while True:

        seq_idx = random_seq(list_seqs)
        probs = prob(list_seqs, w, pos, seq_idx, seq_type=seq_type, first=False)
        posicao = roulette_wheel(probs)
        pos[seq_idx] = posicao[0]

        if score(pos, list_seqs, w) > max_sc:
            best_off = pos.copy()
            max_sc = score(pos, seqs, w)
            contador = 0

        else:
            contador += 1

        if contador >= 1000:
            break

    return best_off, max_sc


x=gibbs_sampling_2(seqs, 8)
print(x)

snips = []
for idx, pos in enumerate(x[0]):
    snips.append(seqs[idx][pos:pos + 8])

for snip in snips:
    print(snip)



