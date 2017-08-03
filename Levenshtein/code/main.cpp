#include "automata.h"

#include <string>
#include <sstream>
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

void usage(char * argv); // Usage info funct

int main(int argc, char * argv[]) {

if (argc < 4 || 6 < argc){ // If argc is smaller than 4 bigger than 6 print help document
	cout << "\n  ERROR: Not enough input arguments" << endl;
	// [Print help doc] //
	usage(argv[0]);
}
/***************************
*	STRING options
***************************/
else if (*argv[1] == 's'){ // argc should be s for string option
	cout << "\n  Mode: STRING" << endl;
	int i, j, k; // set counting vars
	Automata ap; // make automata file

    //Parse command line options
	string p = argv[2]; // get pattern string
	cout << "  Pattern = " << p << endl;
	string lev_dist = argv[3]; // get levenshtein distance
	//cout << "  Edit dist = " << lev_dist << endl;
	int d=(int)lev_dist[0]-48; // put levenshtein distance into an integer variable
	//cout << "d = " << d << endl;

	int width = p.length(); // Get pattern length for array width

	cout << "  Pattern width = " << width << endl; // Print out width
	cout << "  Edit distance = " << lev_dist << endl; //Print out edit dist

	if (width <= d){ // Check to make sure width of pattern is bigger than edit distance
			cout << "\nERROR: String pattern width must be larger than edit distance!" << endl;
		exit(EXIT_FAILURE);
	}

	// Make 3D array of STEs
	// Index size is [iterations = 1], [lev dist + 1], [max string width + 1], [2 - char or star]
	STE *index[1][d + 1][width + 1][2];


	// Make Levenshtein //
	int w = 0; // set iteration flag to 0 for string mode 
	int i_name[4]; // STE index name variable of size 4 - [iterations][edit dist][width][char/star]
	string STE_name; // string for final STE name
	ostringstream convert_n; // var used to convert number into string
	string STE_symbol; // temp string for STE symbol (char or star)

	// Start states
	string start = "all-input"; // string for start state "all"
	string off = "none"; // string for start state "none"


    /*---------------------------
          Populate STE array
     ---------------------------*/

	// Populate char STEs - index [w][y][x][1]

	for (i = 0; i <= d; i=i+1) { // loop over edit distance
		for (j = 1; j <= width; j = j+1) { // loop over width
			// Create STE name
			i_name[0] = w; i_name[1] = i; i_name[2] = j; i_name[3] = 1;
			// Put STE name into temp string
			convert_n << i_name[0] << i_name[1] << i_name[2] << i_name[3]; 
			STE_name = convert_n.str(); // Copy STE name into STE_name var
			convert_n = ostringstream(); // Clear temp stream string
			STE_symbol = p[j-1]; // Get STE symbol from p string

			// starting and late start blocks
			if (j == i+1) { 
				// Make new STE with name, symbol, and start values
				index[w][i][j][1] = new STE(STE_name, STE_symbol, start);

			// non-starting blocks
			}else { 
				// Make new STE with name, symbol, and start values
				index[w][i][j][1] = new STE(STE_name, STE_symbol, off);
	}	}	}

	//Populate star STEs  - index [w][y][x][0]
	for (i = 1; i <= d; ++i) {// loop over edit distance
		for (j = 0; j <= width; ++j) { // loop over width
			// Create STE name
			i_name[0] = w; i_name[1] = i; i_name[2] = j; i_name[3] = 0; 
			// Put STE name into temp string
			convert_n << i_name[0] << i_name[1] << i_name[2] << i_name[3]; 
			STE_name = convert_n.str(); // Clear temp stream string
			convert_n = ostringstream(); // clear stream string

			//set simple starting error block
			if ((i == 1) && (j == 0)) {  
				index[w][i][j][0] = new STE(STE_name, "*", start);

			//set starting error blocks
			}else if (j == i) { 
				index[w][i][j][0] = new STE(STE_name, "*", start);

			//set non-starting blocks
			}else { 
				index[w][i][j][0] = new STE(STE_name, "*", off);
	}	}	}


	/*---------------------------
	      Set Reporting STEs
	 ---------------------------*/
	//Set reporting char STEs - index [y][x][1]
	int rep_dist = width-d; // Make and set reporting distance var for chars
	for (i = 0; i <= d; ++i) {
		for (j = rep_dist; j <= width; ++j) {
			index[w][i][j][1]->setReporting(true);
		}
		++rep_dist; // increase report distance before going up to next error level
	}
	//Set reporting star STEs  - index [y][x][0]
	rep_dist = width-d+1; // Set reporting distance var for stars
	for (i = 1; i <= d; ++i) {
		for (j = rep_dist; j <= width; ++j) {
			index[w][i][j][0]->setReporting(true);
		}
		++rep_dist; // increase report distance before going up to next error level
	}

	/*---------------------------
	   Add STEs to data structure
	 ---------------------------*/
	// char STEs
	for (i = 0; i <= d; ++i) {
		for (j = 1; j <= width; ++j) {
			ap.rawAddSTE(index[w][i][j][1]);
	}	}
	// star STEs
	for (i = 1; i <= d; ++i) {
		for (j = 0; j <= width; ++j) {
			ap.rawAddSTE(index[w][i][j][0]);
	}	}


	/*---------------------------
	 * Add edges between STEs
	 ---------------------------*/
	// *** MATCH edges *** //
	for (i = 0; i <= d; ++i) { // char STEs
		for (j = 1; j < width; ++j) {
			ap.addEdge(index[w][i][j][1], index[w][i][j+1][1]);
	}	}
	for (i = 1; i <= d; ++i) { //star STEs
		for (j = 0; j < width; ++j) {
			ap.addEdge(index[w][i][j][0], index[w][i][j + 1][1]);
	}	}


	// *** INSERTION edges *** //
	for (i = 0; i < d; ++i) { // char STEs
		for (j = 1; j <= width; ++j) {
			ap.addEdge(index[w][i][j][1], index[w][i+1][j][0]);
	}	}
	if (d > 1) { // Only use these edges if d > 1
		for (i = 1; i < d; ++i) {  // star STEs
			for (j = 0; j <= width; ++j) {
				ap.addEdge(index[w][i][j][0], index[w][i + 1][j][0]);
	}	}	}


	// *** SUBSTITUTION edges *** //
	for (i = 0; i < d; ++i) { // char STEs
		for (j = 1; j < width; ++j) {
			ap.addEdge(index[w][i][j][1], index[w][i+1][j+1][0]);
	}	}
	if (d > 1) { // Only use these edges if d > 1
		for (i = 1; i < d; ++i) { // star STEs
			for (j = 0; j < width; ++j) {
				ap.addEdge(index[w][i][j][0], index[w][i + 1][j + 1][0]);
	}	}	}


	// *** DELETE+MATCH edges *** //
	for (i = 0; i < d; ++i) { // Only use these edges if d > 1
		for (j = 1; j <= (width - 2); ++j) { // char STEs
				ap.addEdge(index[w][i][j][1], index[w][i + 1][j + 2][1]);
	}	} 
	if (d > 1) { // Only use these edges if d > 1
		for (i = 1; i < d; ++i) { // star STEs
			for (j = 0; j <= width-d; ++j) {
				ap.addEdge(index[w][i][j][0], index[w][i + 1][j + 2][1]);
	}	}	}


	// *** DELETE+SUBSTITUTION edges *** //
	if (d > 1) { // Only use these edges if d > 1
		for (i = 0; i <= (d - 2); ++i) { // char STEs
			for (j = 1; j <= (width - d); ++j) {
				ap.addEdge(index[w][i][j][1], index[w][i + 2][j + 2][0]);
	}	}	}
	if (d > 2){ // Only use these edges if d > 2
		for (i = 1; i < d-2; ++i) { // star STEs
			for (j = 0; j < width; ++j) {
				ap.addEdge(index[w][i][j][0], index[w][i + 2][j + 2][0]);
	}	}	}

    /*---------------------------------
     * Export automaton as anml file
     ---------------------------------*/
	string ANMLname = "leven.anml";
	ap.automataToANMLFile(ANMLname);
    cout <<"\n  ANML file created = '" << ANMLname << "'"<< endl;

}

/***************************
*	FILE options
***************************/
else if (*argv[1] == 'f'){ // argc should be f for file option
	cout << "\n  Mode: FILE" << endl;
	
	int i, j, k, w; // set counting vars

	Automata ap; // make automata file

    //Parse command line options
	string filename = argv[2]; // get file name from input
	string lev_dist = argv[3]; // get levenshtein distance
	int d=(int)lev_dist[0]-48; // put levenshtein distance into an integer variable
	string tempSTR;

	//string pfile;	// make pattern string var
	ifstream pfile(filename); // open input file into pattern string

	if (pfile.is_open()){ // check if file open

		// Get line count for number of iterations
		int iter=0; // make iteration var
		//iter = count(istream_iterator<char>(pfile), istream_iterator<char>(),'\n');

		string pline;

		while (1==1){
			getline(pfile, tempSTR);
			if (tempSTR == ""){
				break;
			}
			pline= pline + tempSTR + "\n";
			++iter;
		}
		cout << "  Iterations: " << iter << endl;
		//cout << "  pline: " << pline << endl;

		pfile.clear();
		pfile.seekg(0, std::ios::beg); // Set reading location back to begining of file

		 //------------------------//
		// Get maximum line width //
	   //------------------------//
		int width_max; // make max width var
		int c=0; // Make counting var
		int width_line[iter];


		// Find length of each line
		for (w = 0; w < iter; ++w){
			getline(pfile, tempSTR);
			//pfile >> pline;
			//cout << "  tempSTR: " << tempSTR << endl;
			width_line[w] = tempSTR.length(); // Get pattern length for array width
			pline = ""; // Clear temp stream string
			//cout << "  Line width: " << width_line[w] << endl;
		}

		// Find longest line
		width_max = width_line[0];
		for (i=0; i<iter; i++){
			if (width_line[i] > width_max) {
				width_max = width_line[i];
			}
		}
		//cout << "  Max width: "<< width_max << endl;

		pfile.clear();
		pfile.seekg(0, std::ios::beg); // Set reading location back to begining of file


		// Make 3D array of STEs
		// Index size is [iterations], [lev dist + 1], [max string width + 1], [2 - char or star]
		STE *index[iter][d + 1][width_max + 1][2]; 


		// Make Levenshtein //

		int width; // Set width var
		string p; // Set pattern var (FILE and RAND modes will have many patterns)

		int i_name[4]; // STE index name variable of size 4 - [iterations][edit dist][width][char/star]
		string STE_name; // string for final STE name
		ostringstream convert_n; // var used to convert number into string
		string STE_symbol; // temp string for STE symbol (char or star)

		// Start states
		string start = "all-input"; // string for start state "all"
		string off = "none"; // string for start state "none"


		/*---------------------------
		     	Create ANML file
		---------------------------*/

		// loop over iterations
		for (w = 0; w < iter; ++w){ 

			p = ""; // Clear p var
			pfile >> p; // Get line into pattern var

			c++; // Increase c count once more to move past '\n' character
			cout << "  Pattern[" << w+1 << "]: " << p << endl;

			width = p.length(); // Get pattern length for array width
			//cout << "\n  Width: " << width << "\n" << endl;

		if (width <= d){ // Check to make sure width of pattern is bigger than edit distance
			cout << "\nERROR: String pattern width must be larger than edit distance!" << endl;
			cout << "  Width: " << width << endl;
			cout << "  Edit dist: " << d << endl;
			exit(EXIT_FAILURE);
		}

			/*---------------------------
			      Populate STE array
			 ---------------------------*/
			// Populate char STEs - index [w][y][x][1]

			for (i = 0; i <= d; i=i+1) { // loop over edit distance
				for (j = 1; j <= width; j = j+1) { // loop over width
					// Create STE name
					i_name[0] = w; i_name[1] = i; i_name[2] = j; i_name[3] = 1; 
					// Put STE name into temp string
					convert_n << i_name[0] << i_name[1] << i_name[2] << i_name[3]; 
					STE_name = convert_n.str(); // Copy STE name into STE_name var
					convert_n = ostringstream(); // Clear temp stream string
					STE_symbol = p[j-1]; // Get STE symbol from p string


					// starting and late start blocks
					if (j == i+1) { 
						// Make new STE with name, symbol, and start values
						index[w][i][j][1] = new STE(STE_name, STE_symbol, start);

					// non-starting blocks
					}else { 
						// Make new STE with name, symbol, and start values
						index[w][i][j][1] = new STE(STE_name, STE_symbol, off);
			}	}	}

			//cout << "  Populate char STEs for iter[" << w+1 << "]: "<< endl;

			//Populate star STEs  - index [w][y][x][0]
			for (i = 1; i <= d; ++i) {// loop over edit distance
				for (j = 0; j <= width; ++j) { // loop over width
					// Create STE name
					i_name[0] = w; i_name[1] = i; i_name[2] = j; i_name[3] = 0;
					// Put STE name into temp string 
					convert_n << i_name[0] << i_name[1] << i_name[2] << i_name[3]; 
					STE_name = convert_n.str(); // Clear temp stream string
					convert_n = ostringstream(); // clear stream string

					//set simple starting error block
					if ((i == 1) && (j == 0)) {  
						index[w][i][j][0] = new STE(STE_name, "*", start);

					//set starting error blocks
					}else if (j == i) { 
						index[w][i][j][0] = new STE(STE_name, "*", start);

					//set non-starting blocks
					}else { 
						index[w][i][j][0] = new STE(STE_name, "*", off);
			}	}	}

			//cout << "  Populate star STEs for iter[" << w+1 << "]: "<< endl;

			/*---------------------------
			  	 Set Reporting STEs
			 ---------------------------*/
			//Set reporting char STEs - index [y][x][1]
			int rep_dist = width-d; // Make and set reporting distance var for chars
			for (i = 0; i <= d; ++i) {
				for (j = rep_dist; j <= width; ++j) {
					index[w][i][j][1]->setReporting(true);
				}
				++rep_dist; // increase report distance before going up to next error level
			}
			//Set reporting star STEs  - index [y][x][0]
			rep_dist = width-d+1; // Set reporting distance var for stars
			for (i = 1; i <= d; ++i) {
				for (j = rep_dist; j <= width; ++j) {
					index[w][i][j][0]->setReporting(true);
				}
				++rep_dist; // increase report distance before going up to next error level
			}

			//cout << "  Set reporting STEs for iter[" << w+1 << "]: "<< endl;

			/*---------------------------
			   Add STEs to data structure
			 ---------------------------*/
			// char STEs
			for (i = 0; i <= d; ++i) {
				for (j = 1; j <= width; ++j) {
					ap.rawAddSTE(index[w][i][j][1]);
			}	}
			// star STEs
			for (i = 1; i <= d; ++i) {
				for (j = 0; j <= width; ++j) {
					ap.rawAddSTE(index[w][i][j][0]);
			}	}

			//cout << "  Add STEs to AP for iter[" << w+1 << "]: "<< endl;

			/*---------------------------
			    Add edges between STEs
			 ---------------------------*/
			// *** MATCH edges *** //
			for (i = 0; i <= d; ++i) { // char STEs
				for (j = 1; j < width; ++j) {
					ap.addEdge(index[w][i][j][1], index[w][i][j+1][1]);
			}	}
			for (i = 1; i <= d; ++i) { //star STEs
				for (j = 0; j < width; ++j) {
					ap.addEdge(index[w][i][j][0], index[w][i][j + 1][1]);
			}	}


			// *** INSERTION edges *** //
			for (i = 0; i < d; ++i) { // char STEs
				for (j = 1; j <= width; ++j) {
					ap.addEdge(index[w][i][j][1], index[w][i+1][j][0]);
			}	}
			if (d > 1) { // Only use these edges if d > 1
				for (i = 1; i < d; ++i) {  // star STEs
					for (j = 0; j <= width; ++j) {
						ap.addEdge(index[w][i][j][0], index[w][i + 1][j][0]);
			}	}	}


			// *** SUBSTITUTION edges *** //
			for (i = 0; i < d; ++i) { // char STEs
				for (j = 1; j < width; ++j) {
					ap.addEdge(index[w][i][j][1], index[w][i+1][j+1][0]);
			}	}
			if (d > 1) { // Only use these edges if d > 1
				for (i = 1; i < d; ++i) { // star STEs
					for (j = 0; j < width; ++j) {
						ap.addEdge(index[w][i][j][0], index[w][i + 1][j + 1][0]);
			}	}	}

	
			// *** DELETE+MATCH edges *** //
			for (i = 0; i < d; ++i) { // Only use these edges if d > 1
				for (j = 1; j <= (width - 2); ++j) { // char STEs
						ap.addEdge(index[w][i][j][1], index[w][i + 1][j + 2][1]);
			}	} 
			if (d > 1) { // Only use these edges if d > 1
				for (i = 1; i < d; ++i) { // star STEs
					for (j = 0; j <= width-d; ++j) {
						ap.addEdge(index[w][i][j][0], index[w][i + 1][j + 2][1]);
			}	}	}
	

			// *** DELETE+SUBSTITUTION edges *** //
			if (d > 1) { // Only use these edges if d > 1
				for (i = 0; i <= (d - 2); ++i) { // char STEs
					for (j = 1; j <= (width - d); ++j) {
						ap.addEdge(index[w][i][j][1], index[w][i + 2][j + 2][0]);
			}	}	}
			if (d > 2){ // Only use these edges if d > 2
				for (i = 1; i < d-2; ++i) { // star STEs
					for (j = 0; j < width; ++j) {
						ap.addEdge(index[w][i][j][0], index[w][i + 2][j + 2][0]);
			}	}	}

			//cout << "  Add edges to AP for iter[" << w+1 << "]: "<< endl;

		}

		/*--------------------------------
		  Export automaton as anml file
		 --------------------------------*/
		string ANMLname = "leven.anml";
		ap.automataToANMLFile(ANMLname);
    	cout <<"\n  ANML file created = '" << ANMLname << "'"<< endl;

	
	}else // If file can't be open return error
		cout << "ERROR: Unable to open file" << endl;

	pfile.close();
}

/***************************
*	RANDOM options
***************************/
else if (*argv[1] == 'r'){ // argc should be r for string option
	cout << "\n  Mode: RANDOM - " << argv[4] << endl;

	int i, j, k; // set counting vars

	Automata ap; // make automata file

    //Parse command line options
	string lev_width = argv[2]; // Get width from input
	int width=(int)lev_width[0]-48; // Put width into an integer var
	string lev_dist = argv[3]; // Get levenshtein distance
	int d=(int)lev_dist[0]-48; // Put levenshtein distance into an integer var
	string rand_type = argv[4]; // Get random mode type - DNA or alphanum
	string lev_iter = argv[5]; // Get number of iterations
	int iter=(int)lev_iter[0]-48; // Put number of iterations into an integer var

	if (width <= d){ // Check to make sure width of pattern is bigger than edit distance
			cout << "\nERROR: String pattern width must be larger than edit distance!" << endl;
			cout << "  Width: " << width << endl;
			cout << "  Edit dist: " << d << endl;
		exit(EXIT_FAILURE);
	}

	string prand; // make pattern string var
	int DNAval, alphanumval; // set vars for random number assignment
	char alphanumchar; // set var for random alpha-numeric character

	srand(time(NULL)); // update seed for random number

	// [Make random pattern string] //
	if (rand_type == "DNA"){ // Check if rand type is DNA
    	for(i = 0; i < iter; ++i){ // Loop over number of iterations
        	for(j = 0; j < width; ++j){ // Fill with random string sequence
            	DNAval = (rand() % 4); // set DNA value to a random nucleobase
				//cout << "DNAval: " << DNAval << endl;
            	switch(DNAval) {
					case 0 :
						prand[(i*width)+i+j] = 'A'; // adenine
						//cout << "prand case 0: " << prand[(i*width)+i+j] << endl;
						break;
					case 1 :
						prand[(i*width)+i+j] = 'T'; // thymine
						//cout << "prand case 1: " << prand[(i*width)+i+j] << endl;
						break;
					case 2 :
						prand[(i*width)+i+j] = 'G'; // guanine
						//cout << "prand case 2: " << prand[(i*width)+i+j] << endl;
						break;
					default:
						prand[(i*width)+i+j] = 'C'; // cytosine
						//cout << "prand default: " << prand[(i*width)+i+j] << endl;
						break;
			}	}
				prand[((i+1)*width)+(i*1)] = '\n'; // Set new line to indicate new Levenshtein iteration
		}

	}
	else if (rand_type == "alphanum"){ // Check if rand type is alpha-numeric

		int alphanum[62]; // vector of alpha numeric ACCII codes
		
		for(i=0; i<10; ++i){ // Add 0-9
			alphanum[i] = i+48;
		}
		for (i=0; i<26; ++i){ // Add uppercase letters
			alphanum[i+10] = i+65;
		}
		for (i=0; i<26; ++i){  // Add lowercase letters
			alphanum[i+36] = i+97;	
		}

		/*
		for (i=0; i<62; ++i){  // Print out all alpha-numeric ASCII characters
			printf("%c ",alphanum[i]);	
		}
		printf("\n");
		*/

    	for(i = 0; i < iter; ++i){ // Loop over number of iterations
        	for(j = 0; j < width; ++j){ // Fill with random string sequence
            	//alphanumval = (rand() % 62); // set alphanum value to a random number between 0-61
				alphanumchar = char(alphanum[(rand() % 62)]); // set alphanum value to a random char from array
				prand[(i*width)+i+j] = alphanumchar; // set alphanum value to a random character
			}
			prand[((i+1)*width)+(i*1)] = '\n'; // Set new line to indicate new Levenshtein iteration
		}

	}
	else { // If rand type is not valid exit program
		cout << "ERROR: Incorrect rand mode option - must be 'DNA' or 'alphanum'" << endl;
		exit(EXIT_FAILURE);
	}	

	// Make 4D array of STEs
	// Index size is [iterations], [lev dist + 1], [max string width + 1], [2 - char or star]
	//STE *index[iter][d + 1][width + 1][2]; 


	// Make Levenshtein //

	string p; // Set pattern var (FILE and RAND modes will have many patterns)

	int i_name[4]; // STE index name variable of size 4 - [iterations][edit dist][width][char/star]
	string STE_name; // string for final STE name
	ostringstream convert_n; // var used to convert number into string
	string STE_symbol; // temp string for STE symbol (char or star)

	// Start states
	string start = "all-input"; // string for start state "all"
	string off = "none"; // string for start state "none"

	/*---------------------------
	    Create ANML file
	---------------------------*/
	int w; // iteration count var
	int c=0; // Make counting var for pattern characters. Set to zero to start at pattern[c].

	string stemp; // temp string var
	
	// loop over iterations
	for (w = 0; w < iter; ++w){

		// Make 3D array of STEs
		// Index size is [iterations], [lev dist + 1], [max string width + 1], [2 - char or star]
		STE *index[iter][d + 1][width + 1][2];  

		p=""; // clear p string before grabing next random string iteration

		i=0; // Reset i value to zero before while loop
		while (prand[c] != '\n'){ // Grab characters from pattern string
			//cout << "prand[" << c << "]: "<< prand[c] << endl;
			stemp = prand[c]; // set temp string to char
			//cout << "temp string: " << stemp << endl;
			p=p+stemp; // Copy characters in pattern string into p string
			//cout << "Pattern [" << c << "]: "<< p << endl;
			c++;
		}
		c++; // Increase c count once more to move past '\n' character

		cout << "  Pattern[" << w+1 << "]: " << p << endl;

		width = p.length(); // Get pattern length for array width
		//cout << "\n  Width: " << width << "\n" << endl;


	    /*---------------------------
	      	 Populate STE array
	     ---------------------------*/
		// Populate char STEs - index [w][y][x][1]


		for (i = 0; i <= d; i=i+1) { // loop over edit distance

			for (j = 1; j <= width; j = j+1) { // loop over width
				// Create STE name
				i_name[0] = w; i_name[1] = i; i_name[2] = j; i_name[3] = 1;
				// Put STE name into temp string 
				convert_n << i_name[0] << i_name[1] << i_name[2] << i_name[3]; 
				STE_name = convert_n.str(); // Copy STE name into STE_name var
				convert_n = ostringstream(); // Clear temp stream string
				STE_symbol = p[j-1]; // Get STE symbol from p string

				// starting and late start blocks
				if (j == i+1) { 
					// Make new STE with name, symbol, and start values
					index[w][i][j][1] = new STE(STE_name, STE_symbol, start);

				// non-starting blocks
				}else { 
					// Make new STE with name, symbol, and start values
					index[w][i][j][1] = new STE(STE_name, STE_symbol, off);
		}	}	}

		//Populate star STEs  - index [w][y][x][0]
		for (i = 1; i <= d; ++i) {// loop over edit distance
			for (j = 0; j <= width; ++j) { // loop over width
				// Create STE name
				i_name[0] = w; i_name[1] = i; i_name[2] = j; i_name[3] = 0; 
				// Put STE name into temp string
				convert_n << i_name[0] << i_name[1] << i_name[2] << i_name[3]; 
				STE_name = convert_n.str(); // Clear temp stream string
				convert_n = ostringstream(); // clear stream string

				//set simple starting error block
				if ((i == 1) && (j == 0)) {  
					index[w][i][j][0] = new STE(STE_name, "*", start);

				//set starting error blocks
				}else if (j == i) { 
					index[w][i][j][0] = new STE(STE_name, "*", start);

				//set non-starting blocks
				}else { 
					index[w][i][j][0] = new STE(STE_name, "*", off);
		}	}	}


		/*---------------------------
		      Set Reporting STEs
		 ---------------------------*/
		//Set reporting char STEs - index [y][x][1]
		int rep_dist = width-d; // Make and set reporting distance var for chars
		for (i = 0; i <= d; ++i) {
			for (j = rep_dist; j <= width; ++j) {
				index[w][i][j][1]->setReporting(true);
			}
			++rep_dist; // increase report distance before going up to next error level
		}
		//Set reporting star STEs  - index [y][x][0]
		rep_dist = width-d+1; // Set reporting distance var for stars
		for (i = 1; i <= d; ++i) {
			for (j = rep_dist; j <= width; ++j) {
				index[w][i][j][0]->setReporting(true);
			}
			++rep_dist; // increase report distance before going up to next error level
		}

		/*---------------------------
		  Add STEs to data structure
		 ---------------------------*/
		// char STEs
		for (i = 0; i <= d; ++i) {
			for (j = 1; j <= width; ++j) {
				ap.rawAddSTE(index[w][i][j][1]);
		}	}
		// star STEs
		for (i = 1; i <= d; ++i) {
			for (j = 0; j <= width; ++j) {
				ap.rawAddSTE(index[w][i][j][0]);
		}	}


		/*---------------------------
		    Add edges between STEs
		 ---------------------------*/
		// *** MATCH edges *** //
		for (i = 0; i <= d; ++i) { // char STEs
			for (j = 1; j < width; ++j) {
				ap.addEdge(index[w][i][j][1], index[w][i][j+1][1]);
		}	}
		for (i = 1; i <= d; ++i) { //star STEs
			for (j = 0; j < width; ++j) {
				ap.addEdge(index[w][i][j][0], index[w][i][j + 1][1]);
		}	}


		// *** INSERTION edges *** //
		for (i = 0; i < d; ++i) { // char STEs
			for (j = 1; j <= width; ++j) {
				ap.addEdge(index[w][i][j][1], index[w][i+1][j][0]);
		}	}
		if (d > 1) { // Only use these edges if d > 1
			for (i = 1; i < d; ++i) {  // star STEs
				for (j = 0; j <= width; ++j) {
					ap.addEdge(index[w][i][j][0], index[w][i + 1][j][0]);
		}	}	}


		// *** SUBSTITUTION edges *** //
		for (i = 0; i < d; ++i) { // char STEs
			for (j = 1; j < width; ++j) {
				ap.addEdge(index[w][i][j][1], index[w][i+1][j+1][0]);
		}	}
		if (d > 1) { // Only use these edges if d > 1
			for (i = 1; i < d; ++i) { // star STEs
				for (j = 0; j < width; ++j) {
					ap.addEdge(index[w][i][j][0], index[w][i + 1][j + 1][0]);
		}	}	}

	
		// *** DELETE+MATCH edges *** //
		for (i = 0; i < d; ++i) { // Only use these edges if d > 1
			for (j = 1; j <= (width - 2); ++j) { // char STEs
					ap.addEdge(index[w][i][j][1], index[w][i + 1][j + 2][1]);
		}	} 
		if (d > 1) { // Only use these edges if d > 1
			for (i = 1; i < d; ++i) { // star STEs
				for (j = 0; j <= width-d; ++j) {
					ap.addEdge(index[w][i][j][0], index[w][i + 1][j + 2][1]);
		}	}	}
	

		// *** DELETE+SUBSTITUTION edges *** //
		if (d > 1) { // Only use these edges if d > 1
			for (i = 0; i <= (d - 2); ++i) { // char STEs
				for (j = 1; j <= (width - d); ++j) {
					ap.addEdge(index[w][i][j][1], index[w][i + 2][j + 2][0]);
		}	}	}
		if (d > 2){ // Only use these edges if d > 2
			for (i = 1; i < d-2; ++i) { // star STEs
				for (j = 0; j < width; ++j) {
					ap.addEdge(index[w][i][j][0], index[w][i + 2][j + 2][0]);
		}	}	}

	}

    /*--------------------------------
      Export automaton as anml file
     --------------------------------*/
	string ANMLname = "leven.anml";
	ap.automataToANMLFile(ANMLname);
    cout <<"\n  ANML file created = '" << ANMLname << "'"<< endl;
 
}

/***************************
*	Input errors
***************************/
else // Print help document
	// [Print help doc] //
	usage(argv[0]);

return 0;
}


void usage(char * argv) { // Usage information funct

    cout <<"\n  USAGE:  "
	<< argv << " [MODE] [string/file/width] [edit dist] [r DNA or alphanum] [r iterations]"<< endl;

    cout <<"\n\t       [MODE]:\t"<< "Choose mode of operation:"<< endl;
    cout <<"\t\t        's' for STRING - Enter pattern string directly in command line for single Lev automaton"<< endl;
    cout <<"\t\t        'f' for FILE - Import text file with list of strings; each line becomes a Lev automaton"<< endl;
    cout <<"\t\t        'r' for RANDOM - Create random DNA or alpha-numeric strings for multiple Lev automata"<< endl; 

    cout <<"\n  [string/file/width]:\t"<< "Enter pattern string characters (STRING mode)"<< endl;
    cout <<"\t\t  \t"<< "Enter file name (FILE mode)"<< endl;
    cout <<"\t\t  \t"<< "Enter pattern width (number of characters) (RANDOM mode)"<< endl;

    cout <<"\n\t  [edit dist]:\t"<< "Enter edit distance for Lev automata. *NOTE* Must be LESS than string pattern width!"<< endl;
    cout <<"\n  [r DNA or alphanum]:\t"<< "Type of random string <-ONLY APPLIES TO RANDOM MODE"<< endl;
    cout <<"\t\t  \t"<< "'DNA' - String of DNA nucleotides A, T, G, or C"<< endl;
    cout <<"\t\t  \t"<< "'alphanum' - String of alpha-numeric characters"<< endl;

    cout <<"\n       [r iterations]:\t"<< "Enter amount of Lev automata iterations <-ONLY APPLIES TO RANDOM MODE"<< endl;

    cout <<"\n\n  Detailed MODE Usage:"<< endl;
    cout <<"\n  For STRING:\t"<< argv <<" s [pattern string] [edit dist]"<< endl;
    cout <<"     example:\t"<< argv <<" s wahoo 2 "<< endl;
    cout <<"\t\t"<< "This will make a Lev automaton of width=5 with edit dist of d=2"<< endl;
    cout <<"\t\t"<< "(w)(a)(h)(o)(o)"<< endl;

    cout <<"\n    For FILE:\t"<< argv <<" f [pattern stings file name] [edit dist]"<< endl;
    cout <<"     example:\t"<< argv <<" f pattern.txt 3"<< endl;
    cout <<"\t\t"<< "This will make a Lev automaton for each line of chars in file with edit dist of d=3"<< endl;
    cout <<"\t\t"<< "*NOTE* Any empty line will abort importing pattern strings"<< endl;

    cout <<"\n  For RANDOM:\t"<< argv <<" r [width] [edit dist] [DNA or alphanum] [iterations]"<< endl;
    cout <<"     example:\t"<< argv <<" r 5 2 DNA 15"<< endl;
    cout <<"\t\t"<< "This will make 15 random Lev automata of 5 DNA chars each with edit dist of d=2"<< endl;
    cout <<"     example:\t"<< argv <<" r 5 2 alphanum 2"<< endl;
    cout <<"\t\t"<< "This will make 2 random lev automata"<< endl;
    cout <<"\t\t"<< "each 5 alpha-numeric chars long with a lev dist of 2"<< endl;

}




//VASim code:
/*
 * Outputs automata to ANML file
 *  meant to be called after optimization passes
 *
void Automata::automataToANMLFile(string out_fn) {

    string str = "";

    // xml header
    str += "<anml version=\"1.0\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n";
    str += "<automata-network id=\"vasim\">\n";

    for(auto el : elements) {
        str += el.second->toANML();
        str += "\n";
    }

    // xml footer
    str += "</automata-network>\n";
    str += "</anml>\n";

    // write NFA to file
    writeStringToFile(str, out_fn);
}
 */







