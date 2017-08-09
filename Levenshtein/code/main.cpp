//Written by Jeffrey Udall 
//2017 University of Virginia

/*Levenshtein wiring algorithm based on:
T. Tracy II, M. Stan, N. Brunelle, J. Wadden, K. Wang, K. Skadron, G. Robins, 
"Nondeterministic Finite Automata in Hardware - the Case of the Levenshtein Automaton" 
University of Virginia, Charlottesville, VA, 
Proceedings of the Workshop on Architectures and Systems for Big Data (ASBD), 
in conjunction with ISCA, 
June 2015.
/*

/*
Dependances, including automata.h, from
VASim by Jack Wadden
https://github.com/jackwadden/VASim
*/

#include "automata.h"

#include <string>
#include <sstream>
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;



//RAND functs
string randDNA (int width); //DNA
string randalpha (int width); //Alpha-numeric

void usage(char * argv); // Usage info funct


/***************************
           Leven 
***************************/

int main(int argc, char * argv[]) {

	if (argc < 4 || 6 < argc){ // Check if allowed amount of arguments
		cout << "\n  ERROR: Not enough input arguments" << endl;
		usage(argv[0]);	// [Print help doc] //
	}

	// Check to make sure mode is one of the three allowed
	else if ((*argv[1] == 's') || ( *argv[1] == 'f') || (*argv[1] == 'r')){ 

		// Parse input //
		char mode = *argv[1]; // Set mode
		string stringfilewidth = argv[2];
		string lev_dist = argv[3]; // Get lev edit dist from input
		string lev_iter = argv[5]; // Get number of iterations for rand from input

		int i, j; // set counting vars

		string p; // set pattern string var
		int width; // set width var
		int d; // set edit dist var
		int iter; // Make iter var

		string stemp; // set temp string
		string filename; // delare filename string
		string prand; // make rand pattern string var
		string rand_type; // set rand type string

		string outname; // set output file name string

		Automata ap; // make automata file


	/***************************
	*	STRING options
	***************************/
		iter = 1; // Set iterations to one
		
		if (mode == 's'){ 
			cout << "\n  Mode: STRING" << endl;

			p = stringfilewidth;
			cout << "  Pattern = " << p << endl;

			width = p.length(); // Get pattern length for array width
			cout << "  Pattern width = " << width << endl; // Print out width

			d = (int)lev_dist[0]-48; // put edit dist into an integer variable
			if (d > 5){ // Make sure edit dist 5 or less to keep reasonable for AP chip
				cout << "  ERROR: Leven edit dist too large!\n\t Must 5 or less" << endl;
				exit(EXIT_FAILURE);					
			}cout << "  Edit dist: " << d << endl;
	
			outname = p + "_d" + lev_dist; // set output name to pattern name
		}

	/***************************
	*	FILE options
	***************************/
		else if (mode == 'f'){ 
			cout << "\n  Mode: FILE" << endl;

			filename = stringfilewidth; // Get file name from command line input

			d = (int)lev_dist[0]-48; // put edit dist into an integer variable
			if (d > 5){ // Make sure edit dist 5 or less to keep reasonable for AP chip
				cout << "  ERROR: Leven edit dist too large!\n\t Must 5 or less" << endl;
				exit(EXIT_FAILURE);					
			}cout << "  Edit dist: " << d << endl;

			ifstream pfile(filename); // open input file into pattern string

			if (pfile.is_open() == 0){ // Check to see if file is open
				cout << "  ERROR: Unable to open file! \n\t Please check file name and try again." << endl;
				exit(EXIT_FAILURE);
			}

			iter=0; // set iterations to zero
			for(; ; ){ // Loop to get number of lines = iterations
				getline(pfile, stemp);
				if (stemp == ""){
					break;
				}
				++iter; // increase iterations
			}cout << "  Iterations: " << iter << endl;

			pfile.clear();
			pfile.seekg(0, ios::beg); // Set reading location to begining of file

			  /*---------------------------/
			 /   Get maximum line width   /
			/---------------------------*/
			int width_max; // make max width var
			int width_line[iter];

			// Find length of each line
			for (i = 0; i < iter; ++i){
				getline(pfile, stemp);
				width_line[i] = stemp.length(); // Get pattern length for array width
			}

			// Find longest line
			width_max = width_line[0];
			for (i=0; i<iter; i++){
				if (width_line[i] > width_max) 
					width_max = width_line[i];
			}
			width = width_max; // Set width var to max width of strings from file

			pfile.close(); // Close pfile

			outname = filename + "_d" + lev_dist; // set output name to file name
		}

	/***************************
	*	RANDOM options
	***************************/
		else if (mode == 'r'){ 
			cout << "\n  Mode: RANDOM" << endl;

			// Set vars
			string lev_width = stringfilewidth; // Get levenshtein width from input

			stringstream rand_width(lev_width); // Get width from command line argument
			if(rand_width) { // Check if width input is a number
				rand_width >> width; // If so, set width variable
				if (width >= 50){ // Check that width is less than 50 - to keep reasonable for AP chip
					cout << "  ERROR: Pattern too wide!\n\t Must be less than 50 characters" << endl;
					exit(EXIT_FAILURE);					
				}
			}else{ // Output error and end program
				cout << "  ERROR: Improper width!\n\t Must be number amount" << endl;
				exit(EXIT_FAILURE);
			}cout << "  Width: " << width << endl;


			d = (int)lev_dist[0]-48; // Put edit distance into an int
			if (d > 5){ // Make sure edit dist 5 or less to keep reasonable for AP chip
				cout << "  ERROR: Leven edit dist too large!\n\t Must 5 or less" << endl;
				exit(EXIT_FAILURE);					
			}	cout << "  Edit dist: " << d << endl;

			rand_type = argv[4]; // Get random mode type - DNA or alphanum

			stringstream rand_iters(lev_iter); // Get iterations from command line argument
			if(rand_iters) { // Check if iteration input is a number
				rand_iters >> iter; // If so, set iter variable
				if (iter >= 100){ // Make sure iterations less than 100 - to keep reasonable for AP chip
					cout << "  ERROR: Too many iterations!\n\t Must be less than 100" << endl;
					exit(EXIT_FAILURE);					
				}
			}else{ // Output error and end program
				cout << "  ERROR: Improper iterations!\n\t Must be number amount" << endl;
				exit(EXIT_FAILURE);
			}cout << "  Iterations: " << iter << endl;



			// Check if rand type is correct
			if ((rand_type != "DNA") && (rand_type != "alphanum")){ 
				cout << "  ERROR: Incorrect random mode type!\n\t Must be 'DNA' or 'alphanum'" << endl;
				exit(EXIT_FAILURE);
			}

			srand(time(NULL)); // update seed for random numbers

			outname = rand_type + "_w" + lev_width + "_d" + lev_dist+ "_x" + lev_iter; // set output name to file name

		}

/***************************
*	Make Levenshtein
***************************/

		int i_name[4]; // STE index name variable of size 4 
					   // [iterations][edit dist][width][char/star]
		string STE_name; // string for final STE name
		ostringstream convert_n; // var used to convert number into string
		string STE_symbol; // temp string for STE symbol (char or star)

		// Start states
		string start = "all-input"; // string for start state "all"
		string off = "none"; // string for start state "none"

		ifstream patfile(filename); // open input file again for ANML file

		//  **[ Make 3D array of STEs ]** //
		STE *index[iter][d + 1][width + 1][2];
		//  Size is: [iterations], [edit dist + 1], [max string width + 1], [2 - char or star]

		/*---------------------------
		 	Create ANML file
		---------------------------*/
		int w = 0; // set iteration count flag
		//int c = 0; // Make counting var for pattern characters

		// ANML Loop - over num of iterations
		for (w = 0; w < iter; ++w){ 

			if (mode != 's'){ // FILE and RAND options for loop
				p.clear(); // Clear pattern var

				if (mode == 'f'){ // Get FILE pattern
					getline(patfile, stemp);
					p = stemp;
					width = p.length(); // Get pattern width
				}

				if (mode == 'r'){ // Get RAND pattern
					// Make random strings
					if (rand_type == "DNA") // Check if rand type is DNA
						p = randDNA(width); // run rand DNA funct
					else if (rand_type == "alphanum") // Check if rand type is alpha-numeric
						p = randalpha(width); // run rand alpha funct
				}
				cout << "  Pattern[" << w+1 << "]: " << p << endl;
			}


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
					if ( (j > 9) && (w > 9)) // If 10 or higher don't add 0 in front
						convert_n << i_name[0] << i_name[1] << i_name[2] << i_name[3];
					else if( (j > 9) && (w <= 9)) // If iter smaller than 10, add 0 in front
						convert_n << "0" << i_name[0] << i_name[1] << i_name[2] << i_name[3];
					else if( (j <= 9) && (w > 9)) // If width smaller than 10, add 0 in front
						convert_n << i_name[0] << i_name[1] << "0" << i_name[2] << i_name[3];
					else  //If width and iter smaller than 10, add 0 in front of both
						convert_n << "0" << i_name[0] << i_name[1] << "0" << i_name[2] << i_name[3];

					STE_name = convert_n.str(); // Copy STE name into STE_name var
					//cout << "  char STE name: " << STE_name << endl;

					convert_n = ostringstream(); // Clear temp stream string
					STE_symbol = p[j-1]; // Get STE symbol from p string

					if (j == i+1)  // Set starting and late start blocks
						// Make new STE with name, symbol, and start values
						index[w][i][j][1] = new STE(STE_name, STE_symbol, start);

					else  // Set non-starting blocks
						// Make new STE with name, symbol, and start values
						index[w][i][j][1] = new STE(STE_name, STE_symbol, off);
			}	}	

			//Populate star STEs  - index [w][y][x][0]
			for (i = 1; i <= d; ++i) {// loop over edit distance
				for (j = 0; j <= width; ++j) { // loop over width

					// Create STE name
					i_name[0] = w; i_name[1] = i; i_name[2] = j; i_name[3] = 0; 

					// Put STE name into temp string
					if ( (j > 9) && (w > 9)) // If 10 or higher don't add 0 in front
						convert_n << i_name[0] << i_name[1] << i_name[2] << i_name[3];
					else if( (j > 9) && (w <= 9)) // If iter smaller than 10, add 0 in front
						convert_n << "0" << i_name[0] << i_name[1] << i_name[2] << i_name[3];
					else if( (j <= 9) && (w > 9)) // If width smaller than 10, add 0 in front
						convert_n << i_name[0] << i_name[1] << "0" << i_name[2] << i_name[3];
					else  //If width and iter smaller than 10, add 0 in front of both
						convert_n << "0" << i_name[0] << i_name[1] << "0" << i_name[2] << i_name[3];

					STE_name = convert_n.str(); // Clear temp stream string
					//cout << "  star STE name: " << STE_name << endl;

					convert_n = ostringstream(); // clear stream string

					if ((i == 1) && (j == 0)) // Set simple starting error block
						index[w][i][j][0] = new STE(STE_name, "*", start);

					else if (j == i)  // Set starting error blocks
						index[w][i][j][0] = new STE(STE_name, "*", start);

					else  // Set non-starting blocks
						index[w][i][j][0] = new STE(STE_name, "*", off);
			}	}	


			/*---------------------------
				  Set Reporting STEs
			 ---------------------------*/
			//Set reporting char STEs - index [y][x][1]
			int rep_dist = width-d; // Make and set reporting distance var for chars

			for (i = 0; i <= d; ++i) {
				for (j = rep_dist; j <= width; ++j) 
					index[w][i][j][1]->setReporting(true);
				++rep_dist; // increase report distance for next row
			}
			//Set reporting star STEs  - index [y][x][0]
			rep_dist = width-d+1; // Set reporting distance var for stars
			for (i = 1; i <= d; ++i) {
				for (j = rep_dist; j <= width; ++j) 
					index[w][i][j][0]->setReporting(true);
				++rep_dist; // increase report distance for next row
			}

			/*---------------------------
			   Add STEs to data structure
			 ---------------------------*/
			// char STEs
			for (i = 0; i <= d; ++i) {
				for (j = 1; j <= width; ++j) 
					ap.rawAddSTE(index[w][i][j][1]);
			}	
			// star STEs
			for (i = 1; i <= d; ++i) {
				for (j = 0; j <= width; ++j) 
					ap.rawAddSTE(index[w][i][j][0]);
			}	


			/*---------------------------
			 * Add edges between STEs
			 ---------------------------*/
			// *** MATCH edges *** //
			for (i = 0; i <= d; ++i) { // char STEs
				for (j = 1; j < width; ++j) 
					ap.addEdge(index[w][i][j][1], index[w][i][j+1][1]);
			}	
			for (i = 1; i <= d; ++i) { //star STEs
				for (j = 0; j < width; ++j) 
					ap.addEdge(index[w][i][j][0], index[w][i][j + 1][1]);
			}	


			// *** INSERTION edges *** //
			for (i = 0; i < d; ++i) { // char STEs
				for (j = 1; j <= width; ++j) 
					ap.addEdge(index[w][i][j][1], index[w][i+1][j][0]);
			}	
			if (d > 1) { // Only use these edges if d > 1
				for (i = 1; i < d; ++i) {  // star STEs
					for (j = 0; j <= width; ++j) 
						ap.addEdge(index[w][i][j][0], index[w][i + 1][j][0]);
			}	}	


			// *** SUBSTITUTION edges *** //
			for (i = 0; i < d; ++i) { // char STEs
				for (j = 1; j < width; ++j) 
					ap.addEdge(index[w][i][j][1], index[w][i+1][j+1][0]);
			}	
			if (d > 1) { // Only use these edges if d > 1
				for (i = 1; i < d; ++i) { // star STEs
					for (j = 0; j < width; ++j) 
						ap.addEdge(index[w][i][j][0], index[w][i + 1][j + 1][0]);
			}	}	


			// *** DELETE+MATCH edges *** //
			for (i = 0; i < d; ++i) { // Only use these edges if d > 1
				for (j = 1; j <= (width - 2); ++j)  // char STEs
						ap.addEdge(index[w][i][j][1], index[w][i + 1][j + 2][1]);
			} 
			if (d > 1) { // Only use these edges if d > 1
				for (i = 1; i < d; ++i) { // star STEs
					for (j = 0; j <= width-d; ++j) 
						ap.addEdge(index[w][i][j][0], index[w][i + 1][j + 2][1]);
			}	}


			// *** DELETE+SUBSTITUTION edges *** //
			if (d > 1) { // Only use these edges if d > 1
				for (i = 0; i <= (d - 2); ++i) { // char STEs
					for (j = 1; j <= (width - d); ++j)
						ap.addEdge(index[w][i][j][1], index[w][i + 2][j + 2][0]);
			}	}
			if (d > 2){ // Only use these edges if d > 2
				for (i = 1; i < d-2; ++i) { // star STEs
					for (j = 0; j < width; ++j)
						ap.addEdge(index[w][i][j][0], index[w][i + 2][j + 2][0]);
			}	}

		}

	patfile.close(); // Close pattern file

    /*---------------------------------
     * Export automaton as anml file
     ---------------------------------*/
	string ANMLname = "leven_";
	ANMLname += outname + ".anml";
	ap.automataToANMLFile(ANMLname);
    cout <<"\n  ANML file created = '" << ANMLname << "'"<< endl;

return 0;
}

/***************************
*	Other input errors
***************************/
else 	
	usage(argv[0]); // [Print help doc] //

return 0;
}



/***************************
      RAND DNA FUNCT
***************************/
string randDNA (int width){ // DNA RAND funct

	int i, j; // set counting vars

	string prand; // make pattern string var
	int DNAval; // set var for random number assignment

        	for(j = 0; j < width; ++j){ // Fill with random string sequence
            	DNAval = (rand() % 4); // set DNA value to a random nucleobase
            	switch(DNAval) {
					case 0 : // adenine
						prand += 'A';
						break;
					case 1 : // thymine
						prand += 'T';
						break;
					case 2 : // guanine
						prand += 'G';
						break;
					default: // cytosine
						prand += 'C';
						break;
			}	}

return prand;
}


/***************************
    RAND ALPHANUM FUNCT
***************************/
string randalpha (int width){ // Alpha-numeric RAND funct

	int i, j; // set counting vars

	string prand; // make pattern string var
	int alphanumval; // set var for random number assignment
	int alphanum[62]; // vector of alpha numeric ACCII codes

	for(i=0; i<10; ++i) // Add 0-9 chars
		alphanum[i] = i+48;
	for (i=0; i<26; ++i) // Add uppercase letters
		alphanum[i+10] = i+65;
	for (i=0; i<26; ++i)  // Add lowercase letters
		alphanum[i+36] = i+97;	
	for(j = 0; j < width; ++j)// Fill with random string sequence
		prand  += char(alphanum[(rand() % 62)]); // set alphanum value to a random char from array

return prand;
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
