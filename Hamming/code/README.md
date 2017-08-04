# **Inputs**

## **hamming_generator.py**
hamming_generator.py generates a customized input .anml file based on a number of command-line arguments provided. More specifically,
hamming_generator.py takes in 4 command line arguments in the following order:
<input_type>, <num_nodes>, <input_length>, <input_hamming_distance>.

**Parameter Use Explanations**
### <input_type>
This parameter specifies what type of input you want the script to generate. Currently, there are two options. Enter 'h' if you want the generated input file to contain randomized DNA strings. Enter 'h' is you want the generated input file to contain randomized alphabetical and numeric strings.

### <num_nodes>
This parameter specifies how many nodes of input will be in the generated input file.

### <input_length>
This parameter specifies how long each node of input will be in the generated input file.

### <input_hamming_distance>
This parameter specifies how many hamming errors you want in a given input node.

### Example Use
```
$ python hamming_generator.py h 1000 5 4
```
The above command will generate an input file of 1000 nodes, each with a length of 5 and a hamming distance of 4. Each node will be a randomized alphanumeric string.

### Input file name
After the script concludes, an input file will be generated with a customized name based on the command-line arguments provided.

---

## **dnaGen.sh**
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

## **inputGen.sh**
inputGen.sh randomly generates a number of randomized alphanumeric characters, which are by default outputted to standard out but can be piped to a text file if desired.

### Default Example Use 
 ```
 $ ./inputGen.sh 8
```
The above line generates 8 random alpha-numeric characters to the console.

### Piping Output Example Use
```
$ ./dnaGen.sh 8 > output.txt
```
The above line saves the output to a file named output.txt.

---

## **Other inputs**
If you do not need customized inputs, the "inputs" folder contains a number of standardized input files.
