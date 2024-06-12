from EvolAlgorithm import EvolAlgorithm
from Popul import PopulInt, PopulReal
from MotifFinding import MotifFinding
from MyMotifs import MyMotifs
import subprocess


def createMatZeros(nl, nc):
    res = []
    for _ in range(0, nl):
        res.append([0]*nc)
    return res


def printMat(mat):
    for i in range(0, len(mat)):
        for j in range(len(mat[i])):
            print(f"{mat[i][j]:.3f}", end=' ')
        print()


class EAMotifsInt (EvolAlgorithm):
    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = len(self.motifs)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulInt(self.popsize, indsize,
                              maxvalue, [])


    def evaluate(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            fit = self.motifs.score(sol)
            ind.setFitness(fit)


class EAMotifsReal(EvolAlgorithm):
    def _init_(self, popsize, numits, noffspring, filename):

        self.motifs_finding = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = self.motifs.motifSize * len(self.motifs.alphabet)
        EvolAlgorithm._init_(self, popsize, numits, noffspring, indsize)


    def initPopul(self, motSize, nSymb): 
        self.popul = PopulReal(self.popsize, motSize*nSymb)


    def evaluate(self, indivs):
       for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            # criar motifs
            pwm = self.vec_to_pwm(sol)
            mtf = MyMotifs(pwm=pwm, alphabet=self.motifs_finding.alphabet)
            s = []
            for j in range(len(self.motifs_finding.seqs)):
                seq = self.motifs_finding.seqs[j].seq
                p = self.motifs.mostProbableSeq(seq)
                s.append(p)
            fit = self.motifs_finding.score(sol)
            ind.setFitness(fit)
    

if __name__ == "__main__":
    def test1():
        ea = EAMotifsInt(100, 1000, 50, "EvolAlgorithm/exemploMotifs.txt")
        ea.run()
        ea.printBestSolution()


    def test2():
        ea = EAMotifsReal(100, 2000, 50, "EvolAlgorithm/exemploMotifs.txt", 2)
        ea.run()
        ea.printBestSolution()

    test1()
    test2()
    
    print("Metricas de Codigo:")
    print("\nMetrica cyclomatic complexity:")
    print(subprocess.call(["radon","cc","EvolAlgorithm/EAMotifs.py", "-s"]))
    print("\nMetrica maintainability index:")
    print(subprocess.call(["radon","mi","EvolAlgorithm/EAMotifs.py", "-s"]))
    print("\nMetrica raw:")
    print(subprocess.call(["radon","raw","EvolAlgorithm/EAMotifs.py", "-s"]))