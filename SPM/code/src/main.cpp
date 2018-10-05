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

	if ((argc >= 5 && argc <= 8 && (*argv[1] == 's' || *argv[1] == 'f') && (*argv[2] == 'n')) ||
		(argc >= 5 && argc <= 8 && *argv[1] == 'r')) {
		Automata ap; // initialize automata

		// 3 modes: "s" accepts string input, "f" accepts file input, "r" generates random automata
		char mode = *argv[1];

		// 1 format: "norm" accepts string like 3 -1 -2 44 7 -1 5 -1 -2.
		//char format = *argv[2];

		string strarg0 = argv[3];
		string strarg1 = argv[4];


		intstring p; // store input pattern from command line

		/**********************************************************
		string input from command line (need to be enclosed by *" "*)
		s n {SPString} {DataString} [-NO] [--fsm] [--NC]
		**********************************************************/
		if (mode == 's') {
			stringstream ss(strarg0);
			ItemSet itemset(ss, "ss");

			/* SPM build */
			Automata ap;
			//SPMbuild(ap, itemset);
		}
		/**********************************************************
		file input
		f n {SPFile} {DataFile} [-NO] [--fsm] [--NC]
		**********************************************************/
		else if (mode == 'f') {
			ifstream pfile(strarg0);
			ifstream qfile(strarg1);
			if (pfile.is_open() == 0 || qfile.is_open() == 0) { // Check to see if file is open
				cout << "  ERROR: Unable to open file! \n\t Please check file name and try again." << endl;
				exit(EXIT_FAILURE);
			}

			ItemSet SPFile(pfile, "SPFile");
			ItemSet DataFile(qfile, "DataFile");
			SPFile.objbytealign(DataFile);
			pfile.close();
			qfile.close();


			/* SPM build */
			bool optimized = true, is_fsm = false, NC = false;

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

			Automata ap;
			SPMbuild(ap, SPFile, optimized, is_fsm, NC);

			stringstream namess;
			string name;
			namess << "SPMfile";

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
				cout <<"  Corresponding data file created = `" << (name +".input") << "'" << endl;
			
			/* DataFile convert */
			ofstream outfile((name + ".input"), fstream::out | fstream::trunc);
			DataFile.DataFileConvert(outfile);
			outfile.close();
		}
		/**********************************************************
		random generator
		r {itemsize} {entry} {objbyte} [-O] [--fsm] [--NC]
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
			Automata ap;
			SPMbuild(ap, item_num, entry_num, objbyte, optimized, is_fsm, NC);

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
	ap - input ap
	itemset - build SPM according to this
	optimized - apply optimization to save one STE in each entry if set
	is_fsm - generate automata for frequent set mining if set, for sequential pattern mining otherwise.
	NC - no counter STE if set
***************************/
void SPMbuild(Automata &ap, ItemSet &itemset, bool optimized, bool is_fsm, bool NC)
{
	/***************************
	element creation and addition to network, parameters are set
	***************************/

	string STE_name;
	STE *STE_temp;

	int objbyte = itemset.objbyte();
	vector<intstring> sequence = itemset.getfirstseq();

	STE *entry_elem;
	vector<STE *> placeholder_elem;
	vector<STE *> item_elem;

	// entry element
	if (optimized) {
		entry_elem = new STE("entry", "[\\xFE]", "start-of-data");
	}
	else {
		entry_elem = new STE("entry", "[\\xFE]", "all-input");
	}
	ap.rawAddSTE(entry_elem);

	int itemcnt = 0;
	for (auto i = sequence.begin(); i != sequence.end(); i++) {
			for (auto j = i->begin(); j != i->end(); j++) {
			// placeholder
			for (int k = 0; k < objbyte; k++) {
				STE_name = "p" + to_string(itemcnt) + "_" + to_string(k);
				if (j == i->begin())
					STE_temp = new STE(STE_name, "[\\x00-\\xFD]", "none");
				else
					STE_temp = new STE(STE_name, "[\\x00-\\xFC]", "none");
				placeholder_elem.push_back(STE_temp);
			}

			// item
			vector<string> steval = STEval(*j, objbyte);
			for (int k = 0; k < objbyte; k++) {
				STE_name = "i" + to_string(itemcnt) + "_" + to_string(k);
				STE_temp = new STE(STE_name, steval[k], "none");
				item_elem.push_back(STE_temp);
			}

			itemcnt++;
		}
		// delimiter placeholder
		for (int k = 0; k < objbyte; k++) {
			STE_name = "p" + to_string(itemcnt) + "_" + to_string(k);
			STE_temp = new STE(STE_name, "[\\x00-\\xFC]", "none");
			placeholder_elem.push_back(STE_temp);
		}
		// delimiter
		for (int k = 0; k < objbyte; k++) {
			STE_name = "i" + to_string(itemcnt) + "_" + to_string(k);
			STE_temp = new STE(STE_name, "[\\xFD]", "none");
			item_elem.push_back(STE_temp);
		}

		itemcnt++;
	}
	int STEcnt = itemcnt * objbyte;
	// change last placeholder & item element to sequence delimiter placeholder & sequence delimiter
	// note that there will be only one STE for last sequence delimiter, so even though we added that
	// much items for convenience, only one STE will be actually added to AP.
	for (int k = 1; k <= objbyte; k++) {
		placeholder_elem[STEcnt - k]->setSymbolSet("[\\x00-\\xFD]");
	}
	item_elem[STEcnt - objbyte]->setSymbolSet("[\\xFE]");

	if (NC)
		item_elem[STEcnt - objbyte]->setReporting(true);

	// add placeholder and item STE vector to AP
	for (int i = 0; i < STEcnt; i++)
		ap.rawAddSTE(placeholder_elem[i]);
	for (int i = 0; i < STEcnt - objbyte + 1; i++)
		ap.rawAddSTE(item_elem[i]);

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

		ap.addEdge(item_elem[STEcnt - objbyte], CNT_temp);
		ap.addEdge(CNT_temp, REP_temp);
	}


	// Entry->placeholder->item
	ap.addEdge(entry_elem, placeholder_elem[0]);
	ap.addEdge(entry_elem, item_elem[0]);
	if (optimized)
		ap.addEdge(placeholder_elem[objbyte - 1], entry_elem);

	// placeholder->placeholder; placeholder->item; item->next_item; item->next_placeholder
	for (int i = 0; i < itemcnt; i++) {
		// P[i][0] -> P[i][1] -> ... -> P[i][objbyte - 1] -> P[i][0]
		for (int j = 0; j < objbyte; j++) {
			ap.addEdge(
				placeholder_elem[i * objbyte + j % objbyte],
				placeholder_elem[i * objbyte + (j + 1) % objbyte]);
		}

		// P[i][objbyte - 1] -> I[i][0]
		ap.addEdge(placeholder_elem[i * objbyte + objbyte - 1], item_elem[i * objbyte]);

		// I[i][0] -> I[i][1] -> ... -> I[i][objbyte - 1] (except for the last one)
		if (i < itemcnt - 1) {
			for (int j = 0; j < objbyte - 1; j++) {
				ap.addEdge(item_elem[i * objbyte + j], item_elem[i * objbyte + (j + 1)]);
			}
		}

		// I[i][objbyte - 1] -> P[i + 1][0], I[i][objbyte - 1] -> I[i + 1][0]
		if (i < itemcnt - 1) {
			ap.addEdge(item_elem[(i + 1) * objbyte - 1], placeholder_elem[(i + 1) * objbyte]);
			ap.addEdge(item_elem[(i + 1) * objbyte - 1], item_elem[(i + 1) * objbyte]);
		}
	}
	cout << "itemcnt" << itemcnt << endl;
}

/***************************
Random SPM build function, add an automaton to *ap*
Parameter:
	ap - input ap
	item_num - number of items
	entry_num - number of entry STEs
	objbyte - length of item No.
	optimized - apply optimization to save one STE in each entry if set
	is_fsm - generate automata for frequent set mining if set, for sequential pattern mining otherwise.
	NC - no counter STE if set
***************************/
void SPMbuild(Automata &ap, int item_num, int entry_num, int objbyte, bool optimized, bool is_fsm, bool NC)
{
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
	ap.addEdge(item_elem[item_num * objbyte - 1], last_p);
	ap.addEdge(item_elem[item_num * objbyte - 1], last_i);
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

}

vector<string> STEval(int num, int objbyte)
{
	vector<string> result;
	int val;
	for (; objbyte > 0; objbyte--) {
		val = num % 253;
		num /= 253;
		stringstream ss;
		ss << setfill('0') << setw(2);
		ss << hex << uppercase << val;
		result.push_back("[\\x" + ss.str() + "]");
	}
	return result;
}



/***************************
Usage info function, pop up on invalid input.
Parameter:
	argv - file name
***************************/
void usage(char *argv)
{
	cout << endl;
	cout << "  ANMLZoo SPM generator usage:" << endl;
	cout << "    f n {SPFile} {DataFile} [-NO] [--NC]" << endl;
	cout << "  SPFile - This file shall contain the sequential pattern user would like to mine in Datafile." << endl;
	cout << "  DataFile - This file shall contain the data to be mined in, and is converted to a form which AP generated by this program is able to mine." << endl;
	cout << "  --NO - no optimization if set (optimization will save one STE in each entry)" << endl;
	cout << "  --NC - no counter STE if set" << endl;
	cout << "  Redundant parameters are placeholders for future functions." << endl;
}
