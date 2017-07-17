#Written by Matthew Wallace and Deyuan Guo

from curses.ascii import *
import os, sys
import random
import string


# ANML network class
class AP_Network:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.compo = []
    def add_element(self, component):
        self.compo.append(component)
    def output(self):
        out.write('<automata-network id="' + self.id + '" ')
        out.write('name="' + self.name + '" ')
        out.write('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">')
        out.write('\n')
        out.write("<description></description>\n")
        for component in self.compo:
            component.output()
        out.write('</automata-network>\n')
    def dump(self):
        print '----------------------------------------'
        print 'ANML Network with', len(self.compo), 'components.'
        for component in self.compo:
            component.dump();
        print '----------------------------------------'

# ANML component as a container
# chain, star, byteor, stror, more, less, exact, range
class AP_Component:
    def __init__(self):
        self.in_elem = []   #refs
        self.out_elem = []  #refs
        self.elements = []  #refs
    def output(self):
        for e in self.elements:
            e.output()
    def dump(self):
        for e in self.elements:
            e.dump()

# STE class
class AP_STE:
    def __init__(self, id, sym, start=None, report=False):
        self.id = id
        self.sym = sym
        self.start = start
        self.report = report
        self.edges = []
    def type(self):
        return 'STE'
    def add_edge(self, to_id):
        self.edges.append(to_id)
    def output(self):
        out.write('\t<state-transition-element id="' + self.id + '" symbol-set="' + self.sym + '"')
        if self.start != None:
            out.write(' start="' + self.start + '"')
        out.write('>\n')
        if self.report == True:
            out.write('\t\t<report-on-match/>\n')
        for e in self.edges:
            out.write('\t\t<activate-on-match element="' + e + '"/>\n')
        out.write('\t</state-transition-element>\n')
        global use_ste
        use_ste += 1
    def dump(self):
        print 'STE:', self.id, self.sym, self.start, self.report
        print 'Edges: <',
        for e in self.edges:
            print e,
        print '>'


# start-of-data, all-input

# generate motomata structure
def gen_motomata(id, l, d, enc):
    assert len(enc) == l
    compo = AP_Component()
    for i in range(0, d+1):
        for j in range(0, l - d):
            steid = str(id) + '_' + str(i) + '_' + str(j) + 'p'
            stesym = str(enc[j+i])
            ste = AP_STE(steid, stesym)
            if j > 0:
                compo.elements[-1].add_edge(ste.id)
            if i > 0:
                compo.elements[-(l-d+1)].add_edge(ste.id)
            if j == l - d - 1:
                if i == 1:
                    compo.elements[-(2*l-2*d+1)].add_edge(ste.id)
                elif i > 1:
                    compo.elements[-(2*l-2*d+1)].add_edge(ste.id)
                    compo.elements[-(3*l-3*d+1)].add_edge(ste.id)
            compo.elements.append(ste)
        if i == d:
            break
        for j in range(0, l - d + 1):
            steid = str(id) + '_' + str(i) + '_' + str(j) + 'n'
            stesym = '[^' + str(enc[j+i]) + ']'
            ste = AP_STE(steid, stesym)
            if i > 0:
                compo.elements[-(2*l-2*d+1)].add_edge(ste.id)
            if j > 0:
                compo.elements[-(l-d+1)].add_edge(ste.id)
            compo.elements.append(ste)
    compo.elements[0].start = 'all-input'
    compo.elements[l-d].start = 'all-input'
    compo.elements[-1].report = True
    compo.elements[-(l-d+1)].report = True
    network.compo.append(compo)

# generate different subset for different node (for compiling)
def gen_enc(node_id):
    enc = '{'
    j = 0
    while node_id >= 0:
        if node_id % 2 == 1:
            enc = enc + str(j)
            enc = enc + ','
        node_id = node_id / 2
        j = j + 1
        if node_id == 0:
            break
    enc = enc[0:-1] + '}'
    return enc

# generate a random string for motomata (for compiling)
def gen_enc_str(l):
    enc = ''
    for i in range(0, l):
        c = chr(random.randint(48, 172))
        while not (c >= '0' and c <= '9' or c >= 'A' and c <= 'Z' or c >= 'a' and c <= 'z'):
            c = chr(random.randint(48, 172))
        enc = enc + c
    print enc, len(enc)
    return enc

# generate a random DNA string for motomata
def gen_enc_dna_str(l):
    options = {0 : 'A',
               1 : 'T',
               2 : 'G',
               3 : 'C'}
    enc = ''
    for i in range(0, l):
        c = random.randint(0,3)
        enc = enc + options[c]
    print enc, len(enc)
    return enc

# generate all the nodes
def main():
    global network
  
    if Type == 'h':
        network = AP_Network('Motomata', outfile)
        print 'STEs per Node: ', (2*hDist+1)*hLen - 2*hDist*hDist
        for id in range(0, nNode):
            enc = gen_enc_str(hLen)
            gen_motomata(id, hLen, hDist, enc)
        network.output()
    elif Type == 'd':
        network = AP_Network('Motomata', outfile)
        print 'STEs per Node: ', (2*hDist+1)*hLen - 2*hDist*hDist
        for id in range(0, nNode):
            enc = gen_enc_dna_str(hLen)
            gen_motomata(id, hLen, hDist, enc)
        network.output()

# Entry
if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'Usage: python gen.py [s|h] #nodes #l #d'
        sys.exit(0)

    # Config
    outfile = 'out.anml'
    use_ste = 0
    use_cnt = 0
    use_bool = 0
    Type = sys.argv[1]
    nNode = int(sys.argv[2])
    hLen = int(sys.argv[3])
    hDist = int(sys.argv[4])

    if Type == 'd':
        outfile = str(nNode)+'node-'+str(hLen)+'len-'+str(hDist)+'dist-'+'-DNAinput.anml'
    elif Type == 'h':
        outfile = str(nNode)+'node-'+str(hLen)+'len-'+str(hDist)+'dist-'+'-STRinput.anml'

    # Output file
    out = open(outfile, 'w+')
    main()
    print 'Usage: STE', use_ste, 'Counter', use_cnt, 'Boolean', use_bool
