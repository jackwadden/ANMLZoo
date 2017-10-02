#include "common.h"
#include "itemset.h"

/***************************
Normalize decimal number expression to char expression, throw error on invalid expression.
Parameter:
	decexp - input decimial number expression
Return value:
	bool - true when decexp is valid
	string - normalized expression when bool == true
***************************/

ItemSet::ItemSet(istream &is)
{
	int in;
	vector<intstring> result;
	int itemcnt = 0, setcnt = 0, seqcnt = 0;
	int maxno = -1;
	result.push_back(intstring());
	while (is >> in) {
		if (in >= 0) {
			itemcnt++;
			if (in >= maxno) maxno = in;
			result.back() += in;
		}
		else if (in == -1) {
			if (itemcnt == 0) {
				cout << "  ERROR: Empty set at sequence number " << seqcnt << "!" << endl;
				exit(EXIT_FAILURE);
			}
			itemcnt = 0;
			setcnt++;
			result.push_back(intstring());
		}
		else if (in == -2) {
			result.pop_back();
			content.push_back(result);
			result.clear();
			if (setcnt == 0) {
				cout << "  ERROR: Empty sequence at sequence number " << seqcnt << "!" << endl;
				exit(EXIT_FAILURE);
			}
			seqcnt++;
			result.push_back(intstring());
		}
		else {
			cout << "  ERROR: Invalid integer at sequence number " << seqcnt << "!" << endl;
			exit(EXIT_FAILURE);
		}
	}
	if (in != -2) {
		cout << "  ERROR: Invalid input file ending!" << endl;
		exit(EXIT_FAILURE);
	}
	if (is.bad()) {
		cout << "  ERROR: Corrupted input file!" << endl;
		exit(EXIT_FAILURE);
	}
	if (maxno >= 64009) {
		cout << "  ERROR: Item No. exceeds maximum!" << endl;
		exit(EXIT_FAILURE);
	}
	else if (maxno >= 253) {
		byte_to_use = 2;
	}
	else {
		byte_to_use = 1;
	}
}

void ItemSet::print()
{
	for (int i = 0; i < (int)content.size(); i++) {
		cout << "<";
		for (int j = 0; j < (int)content[i].size(); j++) {
			cout << "{";
			for (int k = 0; k < (int)content[i][j].size(); k++)
				cout << content[i][j][k] << " ";
			cout << "}, ";
		}
		cout << ">" << endl;
	}
}
