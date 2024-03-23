class BWT: 
    def __init__(self, seq): 
        self.bwt = self.buildbwt(seq) 

    def buildbwt(self, text): 
        ls = [ ]
        for i in range(len(text)):
            ls.append(text[i:]+text[:i])
        ls.sort()
        res = "" 
        for i in range(len(text)):
            res += ls[i][len(text)-1]
        return res



    def get_first_col (self):
        firstcol = []
        for c in self.bwt: 
            firstcol.append(c)
        firstcol.sort() 
        return firstcol


    def find_ith_occ(self, l, elem, index):
    # index é o numero de ordem de elem na lista l
    # ex.: index == 3 significa terceira ocorrencia de elem em l
        j,k = 0,0
        while k < index and j < len(l):
            if l[j] == elem:
                k = k +1
                if k == index:
                    return j
            j += 1 
        return -1


    def inverse_bwt(self):
        firstcol = self.get_first_col()
        res = ""
        c = "$" 
        occ = 1
        for i in range(len(self.bwt)):
            pos = self.find_ith_occ(self.bwt, c, occ)
            c = firstcol[pos]
            occ = 1
            k = pos-1
            while firstcol[k] == c and k >= 0: 
                occ += 1
                k -= 1
            res += c 
        return res


def test():
    seq = "TAGACAGAGA$"
    bw = BWT(seq)
    print ('bwt:', bw.bwt)
    print('seq.original:',bw.inverse_bwt())
test()
