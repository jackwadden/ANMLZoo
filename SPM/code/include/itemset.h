#pragma once
#include "automata.h"

typedef basic_string<int> intstring;

class ItemSet
{
private:
    vector<vector<intstring>> content;
    int byte_to_use;
public:
    ItemSet(istream &);
    int objbyte();
    vector<intstring> getfirstseq();
    void print();
};

void SPMbuild(Automata &, ItemSet &, bool, bool, bool);
void SPMbuild(Automata &, int, int, int, bool, bool, bool);
