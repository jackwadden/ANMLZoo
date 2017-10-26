CC=g++-5
FLAGS=-O3 --std=c++11 -pthread -DDEBUG=false -Wall -Werror
VASIM=../../../VASim
MNRL=$(VASIM)/libs/MNRL/C++
LIBMNRL=$(MNRL)/libmnrl.a
PUGI=$(VASIM)/libs/pugixml/src
LIBVASIM=$(VASIM)/libvasim.a
IDIRS=-I $(VASIM)/include -I $(MNRL)/include -I $(PUGI) -I ./include
CCFILES=$(shell find ./src -name "*.cpp")
ATR=../../../ATR
VPR=../../../VTR/vpr

all:
	$(CC) $(IDIRS) $(FLAGS) $(CCFILES) $(LIBVASIM) $(LIBMNRL)  -o spm

log:
	$(CC) $(IDIRS) $(FLAGS) $(CCFILES) $(LIBVASIM) $(LIBMNRL) > log.txt 2>&1

test: all
	./spm f n test.txt

blif:
	$(VASIM)/vasim -Ox --enforce-fanin 8 --blif SPM_16B_5X4_spm_C.anml

vpr:
	$(VPR)/vpr $(ATR)/archs/d480.xml automata_0.blif \
	--allow_unrelated_clustering off \
	--sweep_dangling_blocks off \
	--timing_tradeoff 0 \
	--beta_clustering 0 \
	--cluster_seed_type max_inputs \
	--alpha_clustering 0 \
	--timing_analysis off \
	--disp on

clean:
	@rm -f spm
	@rm -f *.log
	@rm -f *.mnrl *.anml
	@rm -f *.blif *.ps *.net
