# Automatize - Random Forest Automata Generator

The Random Forest automata generator, **bin/automatize.py**, is an Object-Oriented style Python script that will generate an ANML file compatible with the Micron Automata Processor(AP) as well as REAPR for FPGA.

For program dependancies see main <a href="https://github.com/jeffudall/ANMLZooCopy/blob/master/RandomForest/README.md">RandomForest README</a>.

## Inputs

The **bin/automatize.py** script will create an ANML file when given a model pickle file.

The command line parameters are in this format:  
`automatize.py <model pickle file> [OPTIONS]`

## Usage Parameter Descriptions

### [OPTIONS]
You can also specifiy these optional parameters:
- **`-a <name of output ANML file>`**: Name of output ANML file (default: model.anml)
- **`--short`**: Make an input file with the first 100 inputs for testing (default: false)
- **`--longer`**: Make a 1000x larger input file to the AP (default: false)
- **`--unrolled`**: Skip compressing the chains into loops. This generates one STE per feature per chains. (This will create a very big output file.) (default: false)
- **`-p`**: Generate a plot of the threshold count distribution of the features (default: false)
- **`-v`**: Print verbose descriptions of each step in program's progress. (default: false)
- **`--circuit`**: Generate circuit-compatible chains and output files (default: false) **EXPERIMENTAL**
- **`--gpu`**: Generate GPU-compatible chains and output files (default: false) **EXPERIMENTAL**


## Example
```
$ bin/automatize.py model.pickle -a mymodel.anml --short -v
```

## Outputs
The **automatize.py** script creates the follwing files:  
- **model.anml**: This is the ANML-formatted automata file
- **input_file.bin**: A transformed input file for testing (in this case short). It was generated from the testing_data.pickle file.

The resulting Levenshtein automata ANML file can be viewed in Dan Kramp's <a href="https://github.com/dankramp/AutomataLab">AutomataLab</a> viewer from the University of Virginia.

---

# Obtain Final Results with VASim

To get the final outcome from your date you must bring the ANML file and input data into <a href="https://github.com/jackwadden/VASim">VASim</a>. You can then output a report showing the final output from each of the trees in the forest. To obtain a final result you would simply need to take the most popular answer from the trees.

The command line parameters are in this format:  
`vasim <ANML file> <input file> --report`

For more information on VASim see the VASim page <a href="http://www.cs.virginia.edu/~jpw8bd/vasim_docs/">here</a>.

## Example
```
$ vasim mymodel.anml input_file.bin --report
```
This will import your ANML file and input and make you a report .txt file with the results.

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/VASim_output_report.png" width="912" height="639" alt="VASim example">  
</p>

You can then open up the <a href="https://github.com/jeffudall/ANMLZooCopy/blob/master/RandomForest/code/output/reports_0tid_0packet.txt">txt file</a> that is created and see the results for each input file.

In the below example using MNIST canned data (see **Input File Generator - trainEnsemble.py** below) you can see that the 7259 sample was unanimously chosen as option 1 (zero), while sample 7686 thought was mostly recognized as option 6 (five) but a few thought it was option 4 (three) or option 7 (six). For sample 8113 it was almost unanimously recognized as option 4 (three) but one tree thought it was option 6 (five).

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/VASim_results.png" width="250" height="511" alt="VASim output">  
</p>


---

# Input File Generator - bin/trainEnsemble.py

## Inputs
The decision tree ensemble data training script, **trainEnsemble.py**, will train a decision tree ensemble model when given a canned dataset, *c*, OR training and testing data (*t*, *x*), a model type, *m*, a depth of decision trees, *d* OR number of leaf nodes per tree, *l*, and a number of trees, *n*.

The command line parameters are in this format:

`trainEnsemble.py -c <canned dataset> -m <model type> -d <depth of decision trees> -n <number of trees in ensemble>`

## Usage Parameter Descriptions

### -c \<canned dataset>
This parameter specifies the name of the canned dataset used by **trainEnsemble.py** from SKLEARN.

MNIST, a canned dataset included in SciKit LEARN, is provided as an example.

### -m \<model type>
This parameter specifies model type
- **`rf`** = **Random Forest**
- **`brt`** = **Boosted Regression Trees**
- **`ada`** = **Adaboost Classifier**

### -d \<depth of decision trees>
This parameter specifies the maximum depth of the decision tree learners.

### -n \<number of trees in ensemble>
This parameter specifies the number of decision trees in the ensemble.

### [OPTIONS]
You can also specifiy these optional parameters:
- **`-l <number of leaves>`**: Instead of depth you can specify number of leaves for decision trees.  
- **`-j <number of jobs>`**: You can specify the number of jobs to run in parallel for fit/predict.
- **`-t <training npz file name>`**: Name of training data .npz file.   
- **`-x <testing data npz file name>`**: Name of testing data .npz file.
- **`-f <number of features>`**: The number of features to use for training.
- **`--report`**: You can specify the name of the report file that contains infromation about the trained model. (default is *"report.txt"*)
- **`--metric`**: Choose the metric used for evaluation.  
    - **`acc`**: Accuracy score (default)  
    - `f1` : F1 score   
    - `mse`: Mean Squared Error  
- **`--feature_importance`**: Dump the feature importance values of the trained ensemble.
- **`-p <Name of predictions file>`**: Name of the file containing model predictions for testing (default: predictions.txt)
- **`-v`**: Print verbose descriptions of each step in program's progress (default: false)


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
- **model.pickle**: a serialized Scikit Learn decision tree ensemble model  
- **report.txt**: a file that contains the parameters used for training the model  
- **testing_data.pickle**: a serialized file containing the testing data

---

## Other Inputs
If you do not need customized inputs, the *inputs* folder contains a number of standardized input files.

---

# Majority Voter - bin/classify.py

## Inputs
The Random Forest classify script, **classify.py**, reads a reports file generated by VASIM, and generates a file containing the resulting classifications.

The command line parameters are in this format:

`classify.py reports_0tid_0packet.txt`

## Usage Parameter Descriptions

### reports file
This file is generated by VASIM with the **-r** flag, and contains one line per report.


### [OPTIONS]
You can also specifiy these optional parameters:
- **`-o <classification output filename>`**: You can specify the classification filename. (default: classifications.txt)


## Outputs
The resulting output file contains one line per classification in the following format:

*input index:classification*

---

# Optional - Test the CPU throughput of the model
In order to get an approximation of the performance of the same Random Forest on a standard CPU processor you can use the **bin/test_cpu.py** script to calculate the average throughput of your model on your CPU. Simply run **test_cpu.py** in the same directory as your generated model files

## Usage Parameters
All parameters are optional parameters:

- **`-n <test iterations>`**: Number of test iterations (defaults to 1000)
- **`-j <threads>`**: Number of threads used to run the model
- **`-m <model file>`**: The serialized model file name (defaults to *model.pickle*)
- **`-t <testing data>`**: The testing data output file name (defaults to *testing_data.pickle*)
- **`-v`**: Print verbose descriptions of each step in program's progress.

## Example
If you are using the default settings you can simply run it via this command:
```
$ test_cpu.py
```
<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/test_cpu_run_1.png" width="631" height="90" alt="test_cpu screen shot">  
</p>

If using custom settings you can provide other options in this format:
```
$ test_cpu.py -m <model file> -t <testing data> -n <test iterations> -j <threads>
```

## Output
The resulting throughput is a measurment in kilo samples classified per wall-clock second.

# Citing This Code

If you use this code for research purposes, please cite the below paper which introduces the contained algorithms.
Citation:

Tracy II, Tommy & Fu, Al, et al. "Towards machine learning on the Automata Processor." International Conference on High Performance Computing. Springer International Publishing, 2016.
