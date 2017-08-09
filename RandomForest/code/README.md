# automatize - RF Automata Generator

The Random Forest automata generator, **automatize.py**, is an Object-Oriented style Python script which will generate an ANML file compatible with the Micron Automata Processor(AP).

For program dependancies see main <a href="https://github.com/jeffudall/ANMLZooCopy/blob/master/RandomForest/README.md">RandomForest README</a>.

## Inputs
The **automatize.py** script will create an ANML file when given a model pickle file, *m*.

The command line parameters are in this format:  
`automatize.py -m <model file> - a <output ANML name> [OPTIONS]`


## Usage Parameter Descriptions

### -m \<model file>
This parameter specifies the name of the the Scikit Learn model use by **automatize.py** to create the ANML file. 

### - a \<output ANML name>
This parameter specifies name of the output ANML file (default: **model.anml**).

### [OPTIONS]
These parameters specify the following options:
- **--unrolled**: Don't compress the chains into loops; this generates one STE per feature per chains (default: false)
- **--mnrl**: Generate MNRL chains with floating point inequalities (default: false)
- **--short**: Make a short version of the input file to the AP (default: false)
- **--longer**: Make a 1000x larger input file to the AP (default: false)

## Example
```
$ automatize.py -m model.pickle -a mymodel.anml --short
```
This will use a short version of the model.pickle file to make an ANML file named *mymodel.anml*.

<p align="center">
<img src="" width="" height="" alt="">  
</p>

## Outputs
The **automatize.py** script creates the follwing files:  
- **model.anml**: This is the ANML-formatted automata file
- **input_file.bin**: A transformed input file for testing. It was generated from the testing_data.pickle file.

The resulting Levenshtein automata ANML file can be viewed in Dan Kramp's <a href="http://automata9.cs.virginia.edu:9090/#">ANML Viewer</a> from the University of Virginia.

---

# Input File Generator - trainEnsemble.py 

## Inputs
The Random Forest decision tree ensemble data training script, **trainEnsemble.py**, will train a Random Forest decision tree ensemble model when given a canned dataset, *c*, a model type, *m*, a depth of decision trees, *d*, and a number of trees, *n*.

The command line parameters are in this format:  
`trainEnsemble.py -c <canned dataset> -m <model type> -d <depth of decision trees> -n <number of trees in ensemble>`

## Usage Parameter Descriptions

### -c \<canned dataset>
This parameter specifies the name of the canned dataset used by **trainEnsemble.py** to create the Random Forest. 

MNIST, a canned dataset included in SciKit LEARN, is provided as an example.

### -m \<model type>
This parameter specifies model type
- **rf** = **Random Forest** 
- brt = Gradient Boosting
- ada = Ada Boost

### -d \<depth of decision trees>
This parameter specifies the maximum depth of the decision tree learners. 

### -n \<number of trees in ensemble>
This parameter specifies the number of decision trees in the ensemble. 

## Example
```
$ trainEnsemble.py -c mnist -m rf -d 8 -n 10
```
This will make an Random Forest using the MNIST canned dataset with a maximum depth of 8 tree learners and 10 trees in the ensemble. 

## Outputs
The **trainEnsemble.py** script creates the follwing files:  
**model.pickle**: a serialized Scikit Learn Random Forest model  
**report.txt**: a file that contains the parameters used for training the model  
**testing_data.pickle**: a serialized file containing the training data for testing the mod

---

## Other Inputs
If you do not need customized inputs, the "inputs" folder contains a number of standardized input files.

---

# Optional - Test the CPU throughput of the model

In order to get an approximation of the performance of the same Random Forest on a standard CPU processor you can use the **test_cpu.py** script to calculate the average throughput of your model on your CPU.

Simply run **test_cpu.py** in the same directory as your generated model files
```
$ test_cpu.py
```
You can also provide other options in this format:
```
$ test_cpu.py -n <test iterations> -j <threads> -m <model file> -t <testing data>
```

## Usage Parameters

### -n \<test iterations>
The number of test iterations (defaults to 1000)

### -j \<threads>
The number of threads to be used for running the model

### -m \<model file>
The serialized model file (defaults to **model.pickle**)

### -t \<testing data>
The testing data (defaults to **testing_data.pickle**)


## Output

The resulting throughput is a measurment in kilo samples classified per wall-clock second.
