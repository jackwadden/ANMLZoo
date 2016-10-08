from micronap.sdk import *
import sys

# Usage: call "python synthetic_gen.py setActive setMatching freqReport"
# where setActive, setMatching, freqReport should be replaced with the active set size,
# the matching set size, and the report frequency respectively.

# Important: the input for automata produced should be tested on strings of only the symbol 'a'.

# This file creates automata meant to test behavior of automata simulation while varying the
# report frequency, active set, and match set of an automaton. This is done by creating an
# automaton which is shaped like a ring. The number of stages in the ring (that is, the
# perimeter) is given by the report frequency (as one layer is assigned to report). The number
# of STEs in each stage of the ring is given by the matching set size (as each STE in each
# stage is connected with each STE in the next stage). The pattern a state matches on is
# determined by the active set size. The automaton is intended to be tested with the input
# string coming from the a*, so the active set gives the number of states which match on a.



def main():
    A = Anml()
    AN = A.CreateAutomataNetwork(anmlId='artificial_automata')

    # the number of symbols consumed between reports
    frqReport = int(sys.argv[3]) #4

    # the number of STEs active each cycle
    setActive = int(sys.argv[1]) #2

    # the number of STEs matching (with an active signal) each cycle
    # note that this must be at least setActive
    setMatching = int(sys.argv[2]) #3

    countRings = int(sys.argv[4]) #5

    ste_list = dict()
    
    # we have a start state that matches only on '$' to begin the ring "spinning"
    ste_id = 'start'
    pattern = '$'
    start = AnmlDefs.ALL_INPUT
    report = False
    for r in range(countRings):
         ste_list[ste_id+'_ring'+str(r)] = AN.AddSTE(pattern,anmlId=ste_id+'_ring'+str(r),startType=start,match=False)
    
    # create the STE ring
    # STEs sharing the same first index (i) share the same stage in the ring
    for i in range(frqReport):
        for j in range(setMatching):
            ste_id = '_'+str(i)+'_'+str(j)

            # of all of the STEs in the same stage, there will be setActive states which match on 'a'
            if j in range(setActive):
                pattern = 'a'
            else:
                pattern = '[^a]'

            # All STEs of ring rank 0 are reporting states
            # only 1 STE in rank 0 is a start state.
            if i == 0:
                start = AnmlDefs.NO_START
                report = True
            else:
                start = AnmlDefs.NO_START
                report = False
            for r in range(countRings):
                ste_list[ste_id+'_ring'+str(r)] = AN.AddSTE(pattern,anmlId=ste_id+'_ring'+str(r),startType=start,match=report)
    
    # connect the start state to stage 0 of the automaton
    for j in range(setMatching):
        ste_id = 'start'
        ste_id_next = '_0_' + str(j)
        for r in range(countRings):
            AN.AddAnmlEdge(ste_list[ste_id+'_ring'+str(r)], ste_list[ste_id_next+'_ring'+str(r)])
    
    # add in remaining transitions in the ring
    for i in range(frqReport):
        for j in range(setMatching):
            ste_id = '_'+str(i)+'_'+str(j)
            for j2 in range(setMatching):
                ste_id_next = '_'+str((i+1)%frqReport)+'_'+str(j2)
                for r in range(countRings):
                    AN.AddAnmlEdge(ste_list[ste_id+'_ring'+str(r)], ste_list[ste_id_next+'_ring'+str(r)])

    filename = 'synthetic_v0_'+str(setActive)+'_'+str(setMatching)+'_'+str(frqReport)+'_'+str(countRings)

    AN.ExportAnml(filename +'.anml')


    # Produces a regular expression for the produced machine, written to a file
    regex = '/ $('
    for i in range(frqReport):
        regex = regex + ('.' if setMatching > setActive else 'a')
    regex = regex + ')* /'

    regexFile = open(filename + '_regex.txt', 'w')
    regexFile.write(regex)
    

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "Usage: python synthetic_gen.py <Active Set> <Matching Set> <Report Frequency> <Ring Count>"
        sys.exit()
    main()
