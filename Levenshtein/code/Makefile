CC=g++-5
FLAGS=-O3 --std=c++11 -pthread -DDEBUG=false
VASIM=../../../VASim
MNRL=$(VASIM)/libs/MNRL/C++
LIBMNRL=$(MNRL)/libmnrl.a
PUGI=$(VASIM)/libs/pugixml/src
LIBVASIM=$(VASIM)/libvasim.a
IDIRS=-I $(VASIM)/include -I $(MNRL)/include -I $(PUGI)

all:
	$(CC) $(IDIRS) $(FLAGS)  main.cpp $(LIBVASIM) $(LIBMNRL)  -o leven
