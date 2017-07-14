# **Hamming**

## **Description**
Hamming distance is a calculation of how many differences there are between two strings of the same length. Each character difference adds 1 to the total Hamming distance. For instance, if the strings “Hello” and “Helpp” are being considered, the Hamming distance would be 2. On the Automata Processor, a positional encoding algorithm is used to calculate Hamming distance. Though the Automata Processor does not inherently support arithmetic operations, various positional encodings can be employed in order to represent the outcome of such operations[1]. The two sectionw within the subheader below explain a number of positional encoding algorithms as they are used in the Hamming distance application. 


### **Positional Encoding Algorithms **
I. **Bounded Mismatch Count Automaton (BMCA)**
-This automaton is designed for a sequence of continuous characters and will calculate a Hamming distance, d, for a given input

-In the Bounded Mismatch Count Automaton, the number of columns is equal to the number of characters in the input stream

-The automaton generated with this method will have 2*d + 1 rows of cells arranged in length d, where d is the number of Hamming mistakes the automaton recognizes

-The construction of this type of automaton is dependent of the number of mistakes it is supposed to recognize. In other words, there must always be 2*d+1 rows in every bounded mismatch automaton, where d = the number of Hamming distance mistakes the automaton can recognize.

-Additional automation bounds:  C <= R, where R = number of rows and C = number of columns

-For every correct character, a given bounded mismatch automaton will transition to the next node on its row. When a mismatch occurs, a transition is made from an even numbered row to an odd-numbered row. 

-The total number of STE’s, or cells, this type of automaton requires is (2d+1)L - d^2, where L = length and d = Hamming distance 


![](images/hamming1.png?raw=true)

- The image above, for example, is used to calculate a Hamming distance of 3. Note that a transition is made from an even-numbered row to an odd-numbered row for every mismatch made. Additionally, the end states on the far-right of the graph are used to verify how many mismatches occurred during the input process. This is an example of positional encoding being used to simulate a form of addition (adding up Hamming distances here)

II. **Bounded Mismatch Idenfitication Automaton (BMIA)**
-The bounded mismatch identification automaton is used when the number of Hamming mismatches is not necessary for the given task

-This automaton has d^2 fewer STEs when compared to the BMCA and is composed of 2d+1 rows, with L - d STEs in odd-numbered rows and L-d+1 STEs in even-numbered rows

-In this automaton, the only accept states are in the last two rows 

-This automaton requires L - d^2 STEs

![](images/hamming2.png?raw=true)

-An example of a bounded mismatch identification automaton for length L = 8 and de = 3 is shown above.


## **Hamming Distance Uses**
Hamming distance is currently very applicable in bioinformatics, machine learning, and data mining, among other topics.

## ANML
### 93_20X3.1chip.anml
93 Hamming distance widgets. Each widget calculates all strings within Hamming distance 3 of a randomly embedded string of length 20. This automata was tuned so that it uses the resources of an entire AP chip.

## Inputs
Both included input files employ the full resources of the AP chip by using what we refer to, in the context of the ANML Zoo suite, as the standard candle. This is done in order to create a process by which to judge the AP architecture’s response to a given standardized input set. The standard candle setup allows for easier comparisons with different architectures and increased effectiveness in determining performance and evaluation of different tasks, while maintaining a certain standard of comparability.

### hamming_1MB.input
1MB of randomly generated alphanumeric characters.

### hamming_10MB.input
10MB of randomly generated alphanumeric characters.

## References
[1] Roy, Indranil, and Srinivas Aluru. "Finding motifs in biological sequences using the micron automata processor." Parallel and Distributed Processing Symposium, 2014 IEEE 28th International. IEEE, 2014.


