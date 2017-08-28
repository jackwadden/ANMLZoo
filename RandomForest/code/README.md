# Automatize - Random Forest Automata Generator

The Random Forest automata generator, **automatize.py**, is an Object-Oriented style Python script which will generate an ANML file compatible with the Micron Automata Processor(AP).

For program dependancies see main <a href="https://github.com/jeffudall/ANMLZooCopy/blob/master/RandomForest/README.md">RandomForest README</a>.

## Inputs
The **automatize.py** script will create an ANML file when given a model pickle file, *m*. We have provided the <a href="https://github.com/jeffudall/ANMLZooCopy/raw/master/RandomForest/code/models/randomforest/model.pickle">model.pickle</a> example file in the models folder. 

The command line parameters are in this format:  
`automatize.py -m <model file> - a <output ANML name> [OPTIONS]`


## Usage Parameter Descriptions

### -m \<model file>
This parameter specifies the name of the the Scikit Learn model use by **automatize.py** to create the ANML file. 

### - a \<output ANML name>
This parameter specifies name of the output ANML file (default: **model.anml**).

### [OPTIONS]
You can also specifiy these optional parameters:
- **`-v`**: Print verbose descriptions of each step in program's progress.
- **`--short`**: Make a short version of the input file to the AP (default: false)
- **`--longer`**: Make a 1000x larger input file to the AP (default: false)
- **`--unrolled`**: Skip compressing the chains into loops. This generates one STE per feature per chains. (This will create a very big output file.)


## Example
```
$ automatize.py -m model.pickle -a mymodel.anml --short -v
```
This will use a short version of the model.pickle file to make an ANML file named *mymodel.anml*.

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/test%20run%201a.png" width="1086" height="315" alt="">  
</p>
<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/test%20run%202.png" width="1087" height="555" alt="">  
</p>

## Outputs
The **automatize.py** script creates the follwing files:  
- **model.anml**: This is the ANML-formatted automata file
- **input_file.bin**: A transformed input file for testing. It was generated from the testing_data.pickle file.

The resulting Levenshtein automata ANML file can be viewed in Dan Kramp's <a href="https://github.com/dankramp/AutomataLab">AutomataLab</a> viewer from the University of Virginia.

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
- **`rf`** = **Random Forest** - Right now this is the only model type available

### -d \<depth of decision trees>
This parameter specifies the maximum depth of the decision tree learners. 

### -n \<number of trees in ensemble>
This parameter specifies the number of decision trees in the ensemble. 

### [OPTIONS]
You can also specifiy these optional parameters:
- **`-l <number of leaves>`**: Instead of depth you can specify number of leaves for decision trees.  
- **`-n <number of jobs>`**: You can specify the number ofjobs to run in parallel for fit/predict  
- **`-t <training npz file name>`**: Name of training data .npz file.   
- **`-x <testing data npz file name>`**: Name of testing data .npz file.  
- **`-v`**: Print verbose descriptions of each step in program's progress.  
- **`--report`**: You can specify the name of the report (default is *"report.txt"*)  
- **`--metric`**: Choose the success metric type  
    - **`acc`**: Accuracy score (default)  
    - `f1` : F1 score   
    - `mse`: Mean Squared Error   

## Example
```
$ trainEnsemble.py -c mnist -m rf -d 8 -n 10
```
This will make an Random Forest using the MNIST canned dataset with a maximum depth of 8 tree learners and 10 trees in the ensemble. 

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/test_run_train.png" width="700" height="167" alt="trainEnsemble screen shot">  
</p>

## Outputs
The **trainEnsemble.py** script creates the follwing files:  
**model.pickle**: a serialized Scikit Learn Random Forest model  
**report.txt**: a file that contains the parameters used for training the model  
**testing_data.pickle**: a serialized file containing the training data for testing the model

---

## Other Inputs
If you do not need customized inputs, the "inputs" folder contains a number of standardized input files.

---

# Optional - Test the CPU throughput of the model
In order to get an approximation of the performance of the same Random Forest on a standard CPU processor you can use the **test_cpu.py** script to calculate the average throughput of your model on your CPU. Simply run **test_cpu.py** in the same directory as your generated model files

## Usage Parameters
All parameters are optional parameters:
- **`-n \<test iterations>`**: Number of test iterations (defaults to 1000)
- **`-j \<threads>`**: Number of threads used to run the model
- **`-m \<model file>`**: The serialized model file name (defaults to *model.pickle*)
- **`-t \<testing data>`**: The testing data output file name (defaults to *testing_data.pickle*)
- **`-v`**: Print verbose descriptions of each step in program's progress.

## Example
If you are using the default settings you can simply run it via this command:
```
$ test_cpu.py
```

If using custom settings you can provide other options in this format:
```
$ test_cpu.py -n <test iterations> -j <threads> -m <model file> -t <testing data>
```

## Output
The resulting throughput is a measurment in kilo samples classified per wall-clock second.
