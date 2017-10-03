/*
	Dependances:
		VASim by Jack Wadden - https://github.com/jackwadden/VASim
*/

#include "automata.h"

#include "common.h"
#include "itemset.h"

/***************************
main function of SPM.
***************************/
int main(int argc, char *argv[])
{

	if ((argc == 4 && (*argv[1] == 's' || *argv[1] == 'f') && (*argv[2] == 'n')) ||
		(argc >= 5 && argc <= 8 && *argv[1] == 'r')) {
		Automata ap; // initialize automata

		// 3 modes: "s" accepts string input, "f" accepts file input, "r" generates random automata
		char mode = *argv[1];

		// 1 format: "norm" accepts string like 3 -1 -2 44 7 -1 5 -1 -2.
		//char format = *argv[2];

		string stringfileiter = argv[3];

		intstring p; // store input pattern from command line

		/**********************************************************
		string input from command line (need to be enclosed by *" "*)
		**********************************************************/
		if (mode == 's') {
			stringstream ss(stringfileiter);
			ItemSet itemset(ss);
			itemset.print();
			/* SPM build */
			SPMbuild(itemset);
		}
		/**********************************************************
		file input
		**********************************************************/
		else if (mode == 'f') {
			ifstream pfile(stringfileiter);
			if (pfile.is_open() == 0) { // Check to see if file is open
				cout << "  ERROR: Unable to open file! \n\t Please check file name and try again." << endl;
				exit(EXIT_FAILURE);
			}

			ItemSet itemset(pfile);
			itemset.print();
			pfile.close();
			/* SPM build */
			SPMbuild(itemset);
		}
		/**********************************************************
		random generator
		r itemsize entry objbyte [-O] [--fsm] [--NC]
		**********************************************************/
		else {
			int item_num = atoi(argv[2]);
			int entry_num = atoi(argv[3]);
			int objbyte = atoi(argv[4]);

			bool optimized = true, is_fsm = false, NC = false;

			if(entry_num > item_num) {
				cout << "  ERROR: Max size of sequence should be larger than the number of entries." << endl;
				exit(EXIT_FAILURE);
			}
			if (objbyte > 2) {
				cout << "  ERROR: Object size exceeds limit." << endl;
				exit(EXIT_FAILURE);
			}

			for (int i = 5; i < argc; i++) {
				string optionalarg = argv[i];
				if (optionalarg == "--NO") optimized = false;
				else if (optionalarg == "--fsm") is_fsm = true;
				else if (optionalarg == "--NC") NC = true;
				else {
					cout << "  ERROR: Invalid argument " << i << "!" << endl;
					exit(EXIT_FAILURE);
				}
			}
			SPMbuild(item_num, entry_num, objbyte, optimized, is_fsm, NC);
		}



	}
	else {
		usage(argv[0]); // print help doc
	}
	return 0;
}

/***************************
SPM build function
Parameter:
	argv - file name
***************************/
void SPMbuild(ItemSet &itemset)
{

}

void SPMbuild(int item_num, int entry_num, int objbyte, bool optimized, bool is_fsm, bool NC)
{

	Automata ap;
	/***************************
	element creation and addition to network, parameters are set
	***************************/
	// entry elements
	vector<STE *> entry_elem;
	string STE_name;
	STE *STE_temp;

	for (int i = 0; i < entry_num; i++) {
		STE_name = "e" + to_string(i);
		if (optimized) {
			STE_temp = new STE(STE_name, "[\\xFF]", "start-of-data");
		}
		else {
			STE_temp = new STE(STE_name, "[\\xFF]", "all-input");
		}
		entry_elem.push_back(STE_temp);
	}
	for (int i = 0; i < entry_num; i++) {
		ap.rawAddSTE(entry_elem[i]);
	}

	// placeholder elements
	vector<STE *> placeholder_elem;
	for (int i = 0; i < item_num * objbyte; i++) {
		STE_name = "p" + to_string(i);
		STE_temp = new STE(STE_name, "[\\x00-\\xFD]", "none");
		placeholder_elem.push_back(STE_temp);
	}
	for (int i = 0; i < item_num * objbyte; i++) {
		ap.rawAddSTE(placeholder_elem[i]);
	}
	// item elements
	vector<STE *> item_elem;
	for (int i = 0; i < item_num * objbyte; i++) {
		STE_name = "i" + to_string(i);
		STE_temp = new STE(STE_name, "[\\x0A]", "none");
		item_elem.push_back(STE_temp);
	}
	for (int i = 0; i < item_num * objbyte; i++) {
		ap.rawAddSTE(item_elem[i]);
	}
	// last placeholder & item elements
	STE *last_p, *last_i;
	last_p = new STE("last_p", "[\\x00-\\xFD]", "none");
	last_i = new STE("last_i", "[\\xFE]", "none");
	if (NC)
		last_i->setReporting(true);

	ap.rawAddSTE(last_p);
	ap.rawAddSTE(last_i);


	/***************************
	element connections
	***************************/

	//  create/connect reporter and counter
	if (!NC) {
		Counter *CNT_temp;
		STE *REP_temp;
		CNT_temp = new Counter("Counter", 1000, "pulse");
		REP_temp = new STE("Reporter", "[\\xFF]", "none");
		REP_temp->setReporting(true);
		ap.rawAddSpecialElement(CNT_temp);
		ap.rawAddSTE(REP_temp);

		ap.addEdge(last_i, CNT_temp);
		ap.addEdge(CNT_temp, REP_temp);
	}

	// last item
	ap.addEdge(item_elem[item_num - 1], last_p);
	ap.addEdge(item_elem[item_num - 1], last_i);
	ap.addEdge(last_p, last_i);

	// Entry->placeholder->item
	for (int i = 0; i < entry_num; i++) {
		ap.addEdge(entry_elem[i], placeholder_elem[i * objbyte]);
		ap.addEdge(entry_elem[i], item_elem[i * objbyte]);
		if (optimized)
			ap.addEdge(placeholder_elem[i * objbyte + objbyte - 1], entry_elem[i]);
	}

	// placeholder->placeholder; placeholder->item; item->next_item; item->next_placeholder
	for (int i = 0; i < item_num; i++) {
		// P[i][0] -> P[i][1] -> ... -> P[i][objbyte - 1] -> P[i][0]
		for (int j = 0; j < objbyte; j++) {
			ap.addEdge(
				placeholder_elem[i * objbyte + j % objbyte],
				placeholder_elem[i * objbyte + (j + 1) % objbyte]);
		}

		// P[i][objbyte - 1] -> I[i][0]
		ap.addEdge(placeholder_elem[i * objbyte + objbyte - 1], item_elem[i * objbyte]);

		// I[i][0] -> I[i][1] -> ... -> I[i][objbyte - 1]
		for (int j = 0; j < objbyte - 1; j++) {
			ap.addEdge(item_elem[i * objbyte + j], item_elem[i * objbyte + (j + 1)]);
		}

		// I[i][objbyte - 1] -> P[i + 1][0], I[i][objbyte - 1] -> I[i + 1][0]
		if (i < item_num - 1) {
			ap.addEdge(item_elem[(i + 1) * objbyte - 1], placeholder_elem[(i + 1) * objbyte]);
			ap.addEdge(item_elem[(i + 1) * objbyte - 1], item_elem[(i + 1) * objbyte]);
		}
	}

	/***************************
	network output to file (ANML & MNRL)
	***************************/
	stringstream namess;
	string name;
	namess << "SPM_" << (objbyte * 8) << "B_" << (item_num + 1) << "X" << entry_num;

	if (!optimized) namess << "_NO";
	if (is_fsm)
		namess << "_fsm";
	else
		namess << "_spm";
	if (!NC)
		namess << "_C";
	else
		namess << "_NC";
	name = namess.str();
	ap.automataToANMLFile(name + ".anml");
    	cout <<"\n  ANML file created = `" << (name + ".anml") << "'"<< endl;
	ap.automataToMNRLFile(name + ".mnrl");
    	cout <<"\n  MNRL file created = `" << (name + ".mnrl") << "'"<< endl;
}

/***************************
Usage info function, pop up on invalid input.
Parameter:
	argv - file name
***************************/
void usage(char *argv)
{
	cout << "Placeholder" << endl;
}
