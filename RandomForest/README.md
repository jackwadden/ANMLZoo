# RandomForest
## Description

This benchmark is an implementation of decision tree-based (Random Forest, Boosted Regression Trees, AdaBoost) machine learning inference via automata processing. This benchmark provides a series of tools that trains a decision tree-based model with <a href="http://scikit-learn.org/stable/index.html#">scikit-learn</a> (on a CPU), and transforms the resulting model into ANML format, an XML-like representation of Nondeterministic Finite Automata (NFA), for the Automata Processor. It has been extended to work with FPGAS as well with the help of <a href="https://github.com/ted-xie/REAPR">REAPr</a>.

For more about the Automata Processor, visit <a href="http://cap.virginia.edu/">CAP's website</a>.


## Random Forest Algorithm

Random Forest is a supervised machine learning algorithm used for classification. Being an ensemble method, it is composed of a plurality of binary decision trees that each compute a classification separately before being combined by a majority vote function. Each tree is trained on a random subset of a labeled feature training data. By training on a random subset of feature data, the ensemble can avoid overfitting the trees to the training data and decrease the resulting model variance.


The Random Forest algorithm computes a classification, or a mapping from an input feature vector, as shown in (b), to a discrete set of outputs called Classes. A classification is performed by taking a root-to-leaf traversal, as shown in (a), through each decision tree of the ensemble by comparing feature vector values against thresholds. These thresholds are learned during the training process and are shown by black floating point values to the right of the comparison operator in each node of the decision tree (a). If the feature value at the index passes the inequality test, a left branch is taken, otherwise a right branch is taken.


Each path through a decision tree corresponds to a classification for that decision tree. The resulting classification from each tree is then the input to a majority voting function, the result serving as the classification for the whole Forest.

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/classification_decision_tree.jpg" width="820" height="423" alt="Classification decision tree">
</p>
<p align="center">
<b>Figure 1</b><i> - Decision tree (a) with a single feature vector input (b). The feature vector provided corresponds to the computed, highlighted path from the root of the tree (topmost node) to the leaf node, which represents a classification of Class 2. </i><b>[1]</b>
</p>


<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/tree_with_variables.jpg" width="809" height="254" alt="Tree with variables">  
</p>
<p align="center">
<b>Figure 2</b><i> - Same decision tree with values replaced by variables.</i><b>[1]</b>
</p>

## Random Forest on the Automata Processor

In order to take advantage of the high parallelism of the Automata Processor or FPGA, we translate each possible path in the decision tree into a single chain of feature comparisons; one chain per path. Because all automata, in this case represented by chains, evaluate the same input at the same time, it becomes necessary to align the feature evaluations of each chain (ie, first evaluate feature 1, then feature 2, etc.).


If a feature from the feature vector is not present in one of the resulting chains, we represent the node with a **(\*)** (evaluate true to any value) node.

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/complete_chains_a.jpg" width="821" height="358" alt="Reordered and complete tree">  
</p>
<p align="center">
<b>Figure 3</b><i> - Decision tree paths represented as chains of feature values. The chain that matches the provided feature vector from Figure 1 is highlighted. </i><b>[1]</b>
</p>

The Automata Processor can only process 8-bit input symbols and lacks any support for floating point computation. In order to support floating-point feature comparisons, we divided the feature address space of each feature into range intervals between all thresholds per feature. This allows us to now map feature values from floating point into a discrete set of range 'bins', without loss of fidelity.

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/feature_addresses.jpg" width="819" height="243" alt="Feature addresses">  
</p>
<p align="center">
<b>Figure 4</b><i> - Floating-point feature address spaces are broken down into intervals between thresholds.  The intervals that the inputs map to by the feature vector from Figure 1 are highlighted. You'll notice that feature 4's address space does not have a highlighted region; this is because that path does not include feature 4 comparison operations.</i><b>[1]</b>
</p>

Now that we have a method to map floating point features to discrete ranges, we use a Finite State Automata state per feature to recognize a set of ranges. These decision path chains are then represented by states on the AP/FPGA that are connected with activation edges.

This is not an efficient use of the memory space available in each state, as only a few bits in each state are required to represent the subset of ranges accepted by that state. In other words, each of the circles below is only mapping to a small set of bits from a much larger set (256 in the case of the AP), resulting in an under-utilization of the hardware resources.

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/chains_as_automata.jpg" width="711" height="460" alt="Chains as automata">  
</p>
<p align="center">
<b>Figure 5</b><i> - Decision tree paths as chains using STEs on the AP. The chain that would report on computing the feature vector from Figure 1 is highlighted. </i><b>[1]</b>
</p>

Finally in order to take full advantage of the space available in each STE of the AP, or per FPGA state, we turn the chain automata from <b>Figure 5</b> into loops, as shown in <b>Figure 6</b>. Because we use non-overlapping address spaces per feature (as shown in <b>Figure 4</b>), we can combine these states and repeatedly access the same combined state, effectively looping to evaluate each feature value before returning a match for the leaf node's class. If a feature value is not evaluated to true during any of the loops, the loop will no longer activate itself on the next feature value, ending its computation. Only if all values in the loop return true, will the report state of the loop be reached, indicating a valid traversal.

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/combined_features.jpg" width="816" height="274" alt="Combined features automata">  
</p>
<p align="center">
<b>Figure 6</b><i> - Decision tree paths represented as single-state loops using STEs of the AP. The loop that would report on finding the feature vector from Figure 1 is highlighted.</i><b>[1]</b>
</p>



### Execution Pipeline

The execution pipeline of the Random Forest algorithm has three steps. First a feature vector's values are turned into 8-bit label values and added to a label vector. Next, the AP or FPGA processes these vectors in parallel to identify tree classifications, one per tree. This is where the speed advantages of using the AP/FPGA become apparent.

Currently the final voting stage of the Random Foreset algorithm, combining the classes from all trees, must be done on a CPU. This is a simple average of the reported classes. Reapr does this voting step on the FPGA, itself.

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/execution_pipeline.jpg" width="711" height="578" alt="Execution pipeline">
</p>
<p align="center">
<b>Figure 7</b><i> - The three stages of the execution pipeline: First, feature value ranges are calculated, then feature vectors are translated into label vectors (based on the floating-point value intervals calculated by the FPGA on the AP/FPGA), and finally the AP uses the decision tree paths (translated into loop automata) to process the data and return classifications.</i><b>[1]</b>
</p>

## Dependancies
Make sure that you have the following dependencies installed. If missing, **use pip to install**. If this doesn't work you will need to download and run the python setup file or download the source code and add to PYTHONPATH.


<table align="center" border="0">
  <tr>
    <td><a href="https://github.com/python/cpython/blob/2.7/Lib/optparse.py">optparse</a></td>
    <td><a href="https://pypi.python.org/pypi/logging/0.4.9.6">logging</a></td>
    <td><a href="https://github.com/python/cpython/blob/3.6/Lib/pickle.py">pickle</a></td>
    <td><a href="https://pypi.python.org/pypi/numpy/1.13.1">NumPy</a></td>
    <td><a href="https://pypi.python.org/pypi/scikit-learn">scikit-learn</a></td>
  </tr>
  <tr>
    <td><a href="https://pypi.python.org/pypi/termcolor/1.1.0">termcolor</a></td>
    <td><a href="https://pypi.python.org/pypi/xmltodict/0.11.0">xmltodict</a></td>
    <td><a href="https://pypi.python.org/pypi/enum/0.4.6">enum</a></td>
    <td><a href="https://pypi.python.org/pypi/scipy/0.19.1">SciPy</a></td>
    <td><a href="https://pypi.python.org/pypi/jsonschema#downloads">jsonschema</a></td>
  </tr>
</table>
</p>

#### PIP install
To install all of the dependencies, install from the requirements document:
```
$ pip install -r requirements.txt
```
To use pip to install individual packages in BASH, type the following command:
```
$ pip install <package name>
```  
To install without root access use the following command:
```
$ pip install -- user <package name>
```    
#### Python setup file
To run the python setup file, download the dependency, go to the directory in the terminal, and type the following to run the python setup file:
```
$ python setup.py install
```

### MNRL
You also need to add the MNRL dependency for MNRL support:
- <a href="https://github.com/kevinaangstadt/mnrl/tree/master/python">mnrl</a>

#### Install by Adding to PYTHONPATH
To add MNRL you must add the source code to *PYTHONPATH* in BASH with this command:
```
$ export PYTHONPATH=[filepath]/mnrl/python
```
To check if MNRL is installed properly open python and type
```
>>> import mnrl
```
If nothing happens you are all set. However, if it is not installed properly you will get an error message like:  
```
ImportError: No module named mnrl
```

## Data Input

The canned MNIST data set can be used when running the Random Forest benchmark (see <a href="https://github.com/jackwadden/ANMLZoo/tree/master/RandomForest/code"> README in code folder</a>); however, if you would like to use this code to train ensemble modes from your own data, it is necessary to write an extractor for your raw data. This script processes your raw data and converts it into Numpy X and y matrices. These are then stored in a Numpy Zip file (.npz). The extractors shown below can be found in the code/data directory.

### ocrExtractor

The ocrExtractor program extracts the pixel feature matrix (X) and classification vector (y) from normalized handwritten letter data based on Rob Kassel's OCR work. The data can be obtained from the following locations:  
https://github.com/adiyoss/StructED/tree/master/tutorials-code/ocr/data  
http://ai.stanford.edu/~btaskar/ocr/  

-i: Input OCR data file derived from Rob Kassel's MIT work  
-o: The output .npz filename that will contain X and y  
-v: Verbosity flag  
--visualize: This flag will open a gui and show a random handwritten character for reference.

### mslrExtractor

The mslrExtractor program extracts the learn-to-rank feature matrix (X) and resulting rank score vector (y) from the MSLR LETOR data. The data can be obtained from Microsoft's website:
https://www.microsoft.com/en-us/research/project/mslr/

-i: Input MSLR data file  
-o: The output .npz filename that will contain X and y  
-v: Verbosity flag  


## Automata Files

Below are pre-computed benchmark automata (.anml files) and example input streams generated by the tools found in the <b>code</b> directory. These atomata and input files were used to evaluate Random Forest automata in ANMLZoo.

### <a href="https://github.com/jackwadden/ANMLZoo/raw/master/RandomForest/anml/300f_15t_tree_from_model_MNIST.anml">300f_15t_from_model_MNIST.anml</a>
A random forest with 15 trees and 300 features per input trained on the MNIST digit recognition library. This ANML file was generated as a part of the original ANMLZoo benchmark suite. It was generated incorrectly and thus should not be considered a "standard candle". However, it is a valid benchmark and is maintained for posterity.

### <a href="https://github.com/jackwadden/ANMLZoo/raw/master/RandomForest/anml/rf.1chip.anml">rf.1chip.anml</a>
This ANML file is a portion of 300f_15t_from_model_MNIST.anml properly pruned to max out the resources of an AP chip.

## Inputs
### <a href="https://github.com/jackwadden/ANMLZoo/raw/master/RandomForest/inputs/mnist_1MB.input">mnist_1MB.input</a>
This is an example input for the MNIST automata that contains 1MB of input data.

### <a href="https://github.com/jackwadden/ANMLZoo/raw/master/RandomForest/inputs/mnist_10MB.input">mnist_10MB.input</a>
This is an example input for the MNIST automata that contains 10MB of input data.


# References
**[1]** Tracy II, T., Fu, Y., Roy, I., Jonas, E., & Glendenning, P. (2016, June). Towards Machine Learning on the Automata Processor. In International Conference on High Performance Computing (pp. 200-218). Springer International Publishing, 2016.
