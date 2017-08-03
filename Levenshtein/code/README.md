# Leven - Levenshtein Automaton ANML Creation Program

The Levenshtein Automaton ANML Creation Program, *leven*, is a C++ progam that can generate Levenshtein automata giving a pattern string, *p*, and Levenshtein edit distance, *d*.

The leven program is dependant on <a href="https://github.com/jackwadden/VASim">VASim</a> by Jack Wadden from University of Virginia. You will need to download VASim and place it in one folder up when compiling main.cpp (or edit the make file). 

The *leven* executable creates a customized ANML file, named *leven.anml*, containing Levenshtein automata based on the command-line parameters in this format:  
`leven <MODE> <string/file name/rand width> <edit dist> <random type> <random iterations>`

## Parameter Descriptions

### \<MODE>
This parameter specifies what mode you would like to use, '`s`' for **String**, '`f`' for **File**, or '`r`' for **Random**.  
>**String mode** - accepts a string, directly in the command line, and creates a Levenshtein automaton using that pattern string and using a given edit distance.  
>**File mode** - accepts a text file, with each line in the file being implimented as a separate Levenshtein automaton iteration, using a given edit distance.  **NOTE:** *Any empty line in the file will abort importing pattern strings.*  
>**Random mode** - accepts a character width and edit distance and creates Levenshtein automata using either DNA or alpha-numeric character sets.  
(See below for more detailed examples of the different modes.)

### \<string/file name/rand width>
This parameter specifies either the string characters in **String mode**, the file name in **File mode**, or the width of the random string(s) to generate in **Random mode**.

### \<edit dist>
This parameter specifies the Levenshtein distance used when making the Levenshtein automata. The edit distance is the number of edits a matching string can have and still count as a match. An **_edit_** is either an *insertion*, *substitution*, or *deletion*. **NOTE:** *This number **MUST** be smaller than the pattern string width. (If the pattern string width is equal to or smaller than the edit distance the resulting Levenshtein automaton will match **EVERY** input string, thus making the automaton completely useless.)*

**Example:** If the pattern string is "*wahoo*" and the edit distance is *d=2* then words such as "*wah*" "*wahooes* "*hoos*" "*wallhoo*" etc would all match because they are each only two edits away from "*wahoo*". Other strings like "*wa*" "*oohs*" "*ah*" "oops" will not report a match. Neither will any string report a match that doesn't contain at least three characters from "*wahoo*" in the same order. For instance "*oohaw*" will not report as a match, but "*hoo*" will.

### \<random type>
This parameter specifies which random type to use - either '`DNA`' or '`alphanum`'. **Only applies to Random mode**

>#### DNA type
>This will make random pattern string(s) using the the four DNA nucleobases '`A`'(adenine), '`T`'(thymine), '`G`'(guanine), or '`C`'(cytosine).

>#### alphanum type
>This type will make random pattern string(s) using alpha-numeric characters consisting of 0-9 and A-Z (upper case and lower case) characters. 

### \<random iterations>
This parameter specifies how many iterations of Levenshtein automata the resulting ANML file will contain. **Only applies to Random mode**


## **Detailed MODE Usage**

The program has three modes - **String**, **File**, and **Random**. 

### **String mode**  
This mode allows you directly enter a pattern string to be made into a Levenshtein automaton with a given edit distance.  
The arguments are in this format:  
`leven s <pattern string> <edit dist>` 

Example:  
>**leven s wahoo 2**

>This will make a Levenshtein automaton with *p="wahoo"* with an edit distance of *d=2*.  
>This uses 5 STEs, one for each character, like this:    
>>**[(w)(a)(h)(o)(o)]**


<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/Levenshtein/master/Images/string%20wahoo%20d2%20test%20edit.png" width="605" height="130" alt="string_example_wahoo_d2">  
</p>

The resulting Levenshtein automata ANML file can be viewed in Dan Kramp's <a href="http://automata9.cs.virginia.edu:9090/#">ANML Viewer</a> from the University of Virginia:

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/Levenshtein/master/Images/viewer_wahoo_d2.png" width="966" height="422" alt="ANML_viewer_wahoo_d2">  
</p>
In the image above the green STE's are showing a match with the yellow "`w`" chacter in the input string. (They are three (`*`) STE's and one (`w`) STE). The yellow STE's are the children STE's activated that will examine the next character, "`a`". The orange STE's are the reporting STE's that are activated when reaching the pink characters, "`h`", "`o`", "`o`", "` `", "`W`", ect that are two, or less, edits away from "`wahoo`".


### **File mode**  
This mode allows you to import a file with multiple pattern strings to be made into Levenshtein automata.  
**Note:** The new line character serves as a delimiter separating each pattern string/Levenshtein automata interation. Also  **emply lines are allowed** in text file.  
The arguments for **File mode** are in this format:  
`leven f <pattern file name> <edit dist>`  

**Example**:  
>**leven f pattern.txt 2**  

>This will make a Levenshtein automaton for each line of chars in file, each with edit distance d=3.  
>If your `pattern.txt` file is:  
>>Bob  
>>Jones  
>>Karen  
>>Mary

>You will get four Levenshtein automata of various sizes, one for each line of text, like this:  
>>**(B)(o)(b)  
>>(J)(o)(n)(e)(s)  
>>(K)(a)(r)(e)(n)  
>>(M)(a)(r)(y)**

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/Levenshtein/master/Images/file%20input%20test%20edit.png" width="605" height="180" alt="file_example">  
</p>

### **Random mode**  
The arguments for random mode are in this format:  
`leven r <width> <edit dist> <DNA or alphanum> <iterations>`  

**DNA Example**:  
>**leven r 5 2 DNA 5** 

>This will make five random Levenshtein automata, each five DNA chars long, with a edit distance of d=2 like this:  
>>**(G)(G)(A)(G)(A)   
>>(T)(C)(A)(G)(G)  
>>(C)(G)(A)(A)(C)  
>>(A)(G)(A)(A)(C)  
>>(G)(G)(C)(G)(G)**

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/Levenshtein/master/Images/rand%20DNA%20test%20edit.png" width="605" height="170" alt="rand_dna">  
</p>

**Alpha-num Example**:
>**leven r 5 2 alphanum 5**  

>This will make five random Levenshtein automata, each five alpha-numeric chars long, with a edit distance of d=2  
>>**(5)(j)(p)(t)(N)  
>>(l)(b)(W)(e)(r)  
>>(9)(n)(V)(w)(5)  
>>(4)(d)(B)(q)(q)  
>>(0)(j)(g)(t)(e)**

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/Levenshtein/master/Images/rand%20alphanum%20test%20edit.png" width="605" height="175" alt="rand_alphanum">  
</p>
