# Leven - Levenshtein Automaton ANML Creation Program

The Levenshtein Automaton ANML Creation Program, *leven*, is a C++ progam that can generate Levenshtein automata giving a pattern string, *p*, and Levenshtein edit distance, *d*. The leven program is dependent on <a href="https://github.com/jackwadden/VASim">VASim</a> by Jack Wadden from University of Virginia. You will need to download VASim and place it in one folder up when compiling **main.cpp** (or edit the make file). 

The *leven* executable creates a customized ANML file, named *leven_[input info].anml*, and a MNRL file, named *leven_[input info].mnrl*,containing Levenshtein automata based on the command-line parameters in this format:  
`leven <MODE> <string/file name/rand width> <edit dist> <random type> <random iterations> [--reduce]`

## Usage Parameter Descriptions

### \<MODE>
This parameter specifies what mode you would like to use, '`s`' for **String**, '`f`' for **File**, or '`r`' for **Random**.  
>**String mode** - accepts a string, directly in the command line, and creates a Levenshtein automaton using that pattern string and using a given edit distance.  
>**File mode** - accepts a text file, with each line in the file being implemented as a separate Levenshtein automaton iteration, using a given edit distance. **NOTE:** *Do not include empty lines or spaces. Any empty line in the file will abort importing pattern strings. A space will cause an error.*  
>**Random mode** - accepts a character width and edit distance and creates Levenshtein automata using either DNA or alpha-numeric character sets.  
(See below for more detailed examples of the different modes.)

### \<string/file name/rand width>
This parameter specifies either the string characters in **String mode**, the file name in **File mode**, or the width of the random string(s) to generate in **Random mode**.

### \<edit dist>
This parameter specifies the Levenshtein distance used when making the Levenshtein automata. The edit distance is the number of edits a matching string can have and still count as a match. An **_edit_** is either an *insertion*, *substitution*, or *deletion*. **NOTE:** *This number **MUST** be smaller than the pattern string width. (If the pattern string width is equal to or smaller than the edit distance the resulting Levenshtein automaton will match **EVERY** input string, thus making the automaton completely useless.)*

**Example:** If the pattern string is "`wahoo`" and the edit distance is *d=2* then input strings such as "*wah*" "*wahooes* "*hoos*" "*wallhoo*" etc would all report a match because they are each only two edits away from "`wahoo`". Other strings like "*wa*" "*oohs*" "*ah*" "oops" will not report a match. Neither will any string report a match that doesn't contain at least three characters from "*wahoo*" in the same order. For instance "*oohaw*" will not report as a match, but "*hoo*" will.

### \<random type>
This parameter specifies which random type to use - either '`DNA`' or '`alphanum`'. **Only applies to Random mode**

>#### DNA type
>This will make random pattern string(s) using the the four DNA nucleobases '`A`'(adenine), '`T`'(thymine), '`G`'(guanine), or '`C`'(cytosine).

>#### alphanum type
>This type will make random pattern string(s) using alpha-numeric characters consisting of 0-9 and A-Z (upper case and lower case) characters. 

### \<random iterations>
This parameter specifies how many iterations of Levenshtein automata the resulting ANML file will contain. **Only applies to Random mode**

### --reduce
If the program sees the --reduce flag in the input arguments, it will emit a levenshtein automata that only reports whether or not an input string is exactly the edit distance away from the encoded string. Levenshtein automata tend to generate lots of redundant matches for strings that are highly similar. This methodology is meant to reduce state requirements in the case that the minimum edit distance for a matching string is not required.

---

## Examples and Detailed MODE Usage

The program has three modes - **String**, **File**, and **Random**. 

### **String mode**  
This mode allows you directly enter a pattern string to be made into a Levenshtein automaton with a given edit distance.  
The arguments are in this format:
```
leven s <pattern string> <edit dist> 
```

Example:
```
leven s wahoo 2
```

>This will make a Levenshtein automaton with *p="wahoo"* with an edit distance of *d=2*.  
>This uses 5 STEs, one for each character, like this:    
>>**[(w)(a)(h)(o)(o)]**


<p align="center">
<img src="https://raw.githubusercontent.com/jackwadden/ANMLZoo/master/Levenshtein/images/string%20wahoo%20d2%20test%20edit.png" width="605" height="130" alt="string_example_wahoo_d2">  
</p>

The resulting Levenshtein automata ANML file can be viewed in Dan Kramp's <a href="http://automata9.cs.virginia.edu:9090/#">ANML Viewer</a> from the University of Virginia (**Figure 1**).

<p align="center">
<img src="https://raw.githubusercontent.com/jackwadden/ANMLZoo/master/Levenshtein/images/ANMLviewer_wahoo_d2.png" width="833" height="391" alt="ANMLviewer_wahoo_d2">  
</p>
<p align="center">
<i>Figure 1 - In the image above the green STE's are showing a match with the yellow "`w`" character in the input string. (They are three (`*`) STE's and one (`w`) STE). The yellow STE's are the children STE's activated that will examine the next character, "`a`". The orange STE's are the reporting STE's that are activated when reaching the pink characters, "`h`", "`o`", "`o`", "` `", "`W`", ect that are two, or less, edits away from "`wahoo`".
</i></p>


### **File mode**  
This mode allows you to import a file with multiple pattern strings to be made into Levenshtein automata.  
**Note:** The new line character serves as a delimiter separating each pattern string/Levenshtein automata iteration. Also   **empty lines are NOT allowed** in string text file.  

The arguments for **File mode** are in this format:
```
leven f <pattern file name> <edit dist>  
```

**Example**:  
```
leven f pattern.txt 2 
```

This will make a Levenshtein automaton for each line of chars in file, each with edit distance d=3.  
>If your `pattern.txt` file is:  
>>Bob  
>>Jones  
>>Karen  
>>Mary

You will get four Levenshtein automata of various sizes, one for each line of text, like this:  
>**(B)(o)(b)  
>(J)(o)(n)(e)(s)  
>(K)(a)(r)(e)(n)  
>(M)(a)(r)(y)**

<p align="center">
<img src="https://raw.githubusercontent.com/jackwadden/ANMLZoo/master/Levenshtein/images/file%20input%20test%20edit.png" width="605" height="180" alt="file_example">  
</p>

You can see these Levenshtein automata in the ANML Viewer below (**Figure 2**).

<p align="center">
<img src="https://raw.githubusercontent.com/jackwadden/ANMLZoo/master/Levenshtein/images/pattern_Lev_ANML.png" width="833" height="391" alt="pattern_Lev_ANML">  
</p>
<p align="center">
<i>Figure 2 - In the image above the green STE's are showing a match with the yellow "`B`" character in the input string. The yellow STE's are the children STE's activated that will examine the next character, "`o`". 
</br><b>Note:</b> The `Bob` Levenshtein automata is reporting (purple STE) at the first B because "B" is two edits away from `Bob`.
</i></p>

### **Random mode**  
The arguments for random mode are in this format:
```
leven r <width> <edit dist> <DNA or alphanum> <iterations>
```

**DNA Example**:  
```
leven r 5 2 DNA 5 
```

This will make five random Levenshtein automata, each five DNA chars long, with a edit distance of d=2 like this:  
>**(G)(G)(A)(G)(A)   
>(T)(C)(A)(G)(G)  
>(C)(G)(A)(A)(C)  
>(A)(G)(A)(A)(C)  
>(G)(G)(C)(G)(G)**

<p align="center">
<img src="https://raw.githubusercontent.com/jackwadden/ANMLZoo/master/Levenshtein/images/rand%20DNA%20test%20edit.png" width="605" height="170" alt="rand_dna">  
</p>

**Alpha-num Example**:
```
leven r 5 2 alphanum 5 
```

This will make five random Levenshtein automata, each five alpha-numeric chars long, with a edit distance of d=2  
>**(5)(j)(p)(t)(N)  
>(l)(b)(W)(e)(r)  
>(9)(n)(V)(w)(5)  
>(4)(d)(B)(q)(q)  
>(0)(j)(g)(t)(e)**

<p align="center">
<img src="https://raw.githubusercontent.com/jackwadden/ANMLZoo/master/Levenshtein/images/rand%20alphanum%20test%20edit.png" width="605" height="175" alt="rand_alphanum">  
</p>

### --reduce Option

**DNA Example**:  
```
leven r 5 2 DNA 5 --reduce
```
This will generate an automata that will only report strings when it encounters strings with exactly an edit distance of two away from the encoded string.

### Output ANML and MNRL file names
After the program concludes, an ANML and MNRL files will be generated in the same folder as the **leven** executable is run from. The name of the ANML and MNRL file will begin with "*leven_*" then contain info based on the string/file name/random type and edit distance (in addition to the width and iterations for the random mode), and end with the "*.anml*" or "*.mnrl*" file extensions. 

**Examples:**  
`leven_wahoo_d2.anml`  
`leven_wahoo_d2.mnrl` 

`leven_test.txt_d2.anml`  
`leven_test.txt_d2.mnrl`  

`leven_DNA_w5_d3_x20.anml`  
`leven_DNA_w5_d3_x20.mnrl`  

---


## Input File Generators

These input file generators were created for use with the <a href="https://github.com/jackwadden/ANMLZoo/tree/master/Hamming">Hamming distance</a> automata but input can be used for Levenshtein automata as well.

## DNA Input - dnaGen.sh
dnaGen.sh randomly generates a number of randomized DNA characters, which are by default outputted to standard out but can be piped to a text file if desired.

### Default Example Use 
 ```
 $ ./dnaGen.sh 10
```
The above line generates 10 random DNA characters to the console.
    echo

### Piping Output Example Use
```
$ ./dnaGen.sh 10 > output.txt
```
The above line saves the output to a file named output.txt.

---

## Alpha-numeric Input - inputGen.sh
inputGen.sh randomly generates a number of randomized alphanumeric characters, which are by default outputted to standard out but can be piped to a text file if desired.

### Default Example Use 
 ```
 $ ./inputGen.sh 8
```
The above line generates 8 random alphanumeric characters to the console.

### Piping Output Example Use
```
$ ./dnaGen.sh 8 > output.txt
```
The above line saves the output to a file named output.txt.

---

## **Other Inputs**
If you do not need customized inputs, the "inputs" folder contains a number of standardized input files.
