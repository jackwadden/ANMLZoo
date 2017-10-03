CC=g++-5
FLAGS=-O3 --std=c++11 -pthread -DDEBUG=false -Wall -Werror
VASIM=../../../VASim
MNRL=$(VASIM)/libs/MNRL/C++
LIBMNRL=$(MNRL)/libmnrl.a
PUGI=$(VASIM)/libs/pugixml/src
LIBVASIM=$(VASIM)/libvasim.a
IDIRS=-I $(VASIM)/include -I $(MNRL)/include -I $(PUGI) -I ./include
CCFILES=$(shell find ./src -name "*.cpp")

all:
	$(CC) $(IDIRS) $(FLAGS) $(CCFILES) $(LIBVASIM) $(LIBMNRL)  -o spm

log:
	$(CC) $(IDIRS) $(FLAGS) $(CCFILES) $(LIBVASIM) $(LIBMNRL) > log.txt 2>&1

test:
	./spm r 4 4 2 --NO
	./spm r 4 4 2 --NC
	./spm r 4 4 2

clean:
	@rm -f spm
	@rm -f *.mnrl
	@rm -f *.anml
