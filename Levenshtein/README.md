# **Levenshtein**

## **Description**

A Levenshtein automoton contains a pattern string (p) and a Levenshtein edit distance (d). Any input string that matches pattern string within the edit distance will report a match. A pattern string is used to populate the Levenshtein automaton STE's with characters. The edit distance is the number of edits - *insert*, *substitute*, or *delete* - that are allowed in any matchine string. 

Levenshtein automata are used to find closely matching strings, for instance a spell checker could use a Levenshtein automata to look for cloesly matching words for a misspelled word.

In order to make a Levenshtein automaton for Micron's Automata Processor (AP) we must convert the state machine to an automaton using state transition elements (STE's), which are the single automaton resource units of the AP.

The **leven** program will accept a string or file of strings as input patterns and create Levenshtein automata with an edit distance chosen by the user. It can also create automatons with random patterns of DNA characters or alpha-numeric characters with a pattern width and edit distance chosen by the user. It will then create an automata network markup language (ANML) file, which is an XML file using the ANML syntax created by Micron.

(*See  <a href="https://jeffudall.github.io/Levenshtein/Code/">README</a> file in the Code folder for more information on input syntax and program behavior.*)

The leven program is dependant on <a href="https://github.com/jackwadden/VASim">VASim</a> by Jack Wadden from University of Virginia. You will need to download VASim, place it in one folder up, and compile it before compiling the **leven** main.cpp (or edit the Make file) C++ code file. 

### **Examples and Images**

#### Levenshtein Example

If a Levenshtein string pattern is *p*="*wahoo*" and Levenshtein edit distance is *d*=*2* then the resulting Levenshtein automaton would look like **Figure 1** below. The first number in each state is the column, from zero to the width of the pattern string - 0-5 in this case. The second number is the row, from 0 to the edit distance - 0-2 here.

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/Levenshtein/master/Images/Levenshtein-automaton-sm.jpg" width="647" height="300" alt="state_wahoo_d2">  
</p>

<p align="center">
<i><b>Figure 1</b> - Levenshtein automaton with string pattern p="wahoo" and edit distance of d=2.**[1]**    
</br>(Starting/always active state is green and reporting states have purple outlines.)</i>
</p>

Starting at the first state, (**0.0**) it examines the first character of an input string. If the first character is "**w**" it would move the next state to the right, (**1.0**), indicating one *match* and zero edits. If it was a blank space it would move to the state above, (**0.1**), indicating one *deletion* edit. For any other character it would move one state up and one to the right, (**1.1**), indicating one *insertion* or *substitution* edit. 

Next it would continue on to examine the second character at the new active state, either (**1.0**), (**0.1**), or (**1.1**), and move on to the next state depending if it gets a *match*(right), *deletion*(up), or *insert/substitution*(up and right). 

If it reaches any of the states to the far right (any 5.X states) this indicates the input string (p) matches the given pattern string within the given edit distance (d). However, if it reaches the top level of the automaton (any of the X.2 states) and encounters a futher edit this will terminate it's movement through the Levenshtein automata, thus preventing a positive match.


#### Automata Processor Levenshtein

STE's only output a logical yes/no match for the character they are looking for. This means that every transition will turn on the attached child STE if it returns a match for the input character. In order to make an Levenshtein automaton extra STE's must be used to recreate the same behavior as the above state Levenshtein automaton(**Figure 1**). These extra STE's will match on any input, and are indicated with the ( **\*** ) chacter. Connecting them as shown below (**Figure 2**) allow us to construct a Levenstein automaton using STE's.
<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/Levenshtein/master/Images/Levenshtein%20graph%20WAHOO%20draft%203%20sm.jpg" width="1000" height="417" alt="state_wahoo_d2_AP">  
</p>

<p align="center">
<i><b>Figure 2</b> - Levenshtein automaton built with STE's for the Automata Processor(AP) 
<br>(Starting/always active STE's are green and reporting STE's are purple.)</i>
</p>


## **Automata**

Automata are constructed using pattern strings. Each pattern string is broken up into constituent characters and emitted as a Levenshtein automaton with a given Levenshtein edit distance.

### **Standard Automata**
The Levenshtein standard automata was constructed by running the leven executable on the `DNA_width20_x10.txt` input file. This takes each twenty character wide DNA patter strings on ten lines and converts it to ten Levenshtein automata which can recognize each of the twenty pattern strings in a given string of DNA nucleotides within Levenshtein edit distance *d*=*3*.

## **Inputs**
Input streams to Levenshtein automata consist of character strings of undetermined length. The Levenshtein automaton will report any matches within the given edit distance in the character string.

### **Standard Inputs**
The `DNA_20x10.input` input file was constructed using the strings contained in the `DNA_width20_x10.txt` input file. Each pattern string is separated by three characters "` | `" to help read the edit distance results easier when viewing in Dan Kramp's <a href="http://automata9.cs.virginia.edu:9090/#">ANML Viewer</a> from the University of Virginia. 


## References

[1] T. Tracy II, M. Stan, N. Brunelle, J. Wadden, K. Wang, K. Skadron, G. Robins, "Nondeterministic Finite Automata in Hardware - the Case of the Levenshtein Automaton" University of Virginia, Charlottesville, VA, Proceedings of the Workshop on Architectures and Systems for Big Data (ASBD), in conjunction with ISCA, June 2015.
