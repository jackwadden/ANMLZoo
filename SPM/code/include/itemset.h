#pragma once

typedef basic_string<int> intstring;

class ItemSet
{
private:
    vector<vector<intstring>> content;
    int byte_to_use;
public:
    ItemSet(istream &);
    void print();
};

void SPMbuild(ItemSet &);
void SPMbuild(int, int, int, bool, bool, bool);
