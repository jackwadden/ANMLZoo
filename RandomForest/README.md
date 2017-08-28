# RandomForest
## Description

This benchmark is an open-source implementation of decision tree-based (Random Forest, Boosted Regression Trees, AdaBoost) machine learning models as automata on Micron's Automata Processor (AP) written in Python in Object-Oriented style. This code trains a decision tree-based model with <a href="http://scikit-learn.org/stable/index.html#">scikit-learn</a> (on a CPU), and transforms the resulting model into the ANML format, an XML-like representation of nondeterministic finite automata (NFA) for the Automata Processor. 

For more about the Automata Processor, visit <a href="http://cap.virginia.edu/">CAP's website</a>. 


## Random Forest Algorithm

Random Forest is an ensemble method supervised learning classification algorithm. It is made of many binary decision trees, each trained by a random subset of labled feature sample data. By taking random subset of feature data Random Forest can avoid overfitting the trees to the data and decrease model variance without increasing bias. 

The final leaf node in a decion tree can be grouped into a class. Each path through a decision tree corrisponds to one of the available classes. We can then match each feature vector to a specific path and class. 

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/classification_decision_tree.jpg" width="820" height="423" alt="Classification decision tree"> 
</p>
<p align="center">
<b>Figure 1</b><i> - Decision tree with a single feature vector. The feature vector provided corrisponds to the highlighted path from the root of the tree to the classified leaf node. </i><b>[1]</b>
</p>


<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/tree_with_variables.jpg" width="809" height="254" alt="Tree with variables">  
</p>
<p align="center">
<b>Figure 2</b><i> - Same decision tree with values replaced by variables.</i><b>[1]</b>
</p>

## Random Forest on the Automata Processor

In order to take advantage of the non-linear features of the AP we translate each possible path in the decision tree as a single chain of features. If the feature is not a part of the original tree we represent the node with a **(\*)** (take anything) node. 

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/complete_chains_a.jpg" width="821" height="358" alt="Reordered and complete tree">  
</p>
<p align="center">
<b>Figure 3</b><i> - Decision tree paths represented as chains of feature values. The chain that matches the provided feature vector from Figure 1 is highlighted. </i><b>[1]</b>
</p>

The lack of support in the AP for floating point input means that in order to support features with floating point values in the 8-bit memory of an STE it is nessicary to divide the feature address space into interval thresholds which represent each feature of the feature vector space.

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/feature_addresses.jpg" width="819" height="243" alt="Feature addresses">  
</p>
<p align="center">
<b>Figure 4</b><i> - Floating-point feature vectors must be broken down into intervals in order to represent each chain of the decision tree.  The intervals represented by the feature vector from Figure 1 are highlighted.</i><b>[1]</b>
</p>

These decision path chains can then be represented by STE's in the AP, however this is not an efficient use of the memory space available in each STE.

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/chains_as_automata.jpg" width="711" height="460" alt="Chains as automata">  
</p>
<p align="center">
<b>Figure 5</b><i> - Decision tree paths as chains using STEs in the AP. The chain that would report on finding the feature vector from Figure 1 is highlighted.</i><b>[1]</b>
</p>

Finally in order to take full advantage of the space available in each STE of the AP we turn the chains into cycles with the members of the chains. As each chain is unique we can use repeating loops to check that each feature value of the chain is true before returning a match for the leaf node's class. If the tested value is not a member of the cycle it will no longer activate itself on the next value. If all values in the cycle return true it will report the class as true.

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/combined_features.jpg" width="816" height="274" alt="Combined features automata">  
</p>
<p align="center">
<b>Figure 6</b><i> - Decision tree paths represented as single cycles using STEs of the AP. The cycle that would report on finding the feature vector from Figure 1 is highlighted.</i><b>[1]</b>
</p>



### Execution Pipeline

The execution pipeline of the Random Forest algorithm has three steps. First a feature vector values are turned into 8-bit label values and added to a label vector. Next the AP processes these vectors in parallel to identify tree classifications. This is where the speed advantages of using the AP become apparent. 

Currently the final voting stage of the Random Foreset algorithm, combining the classes from all trees, must be done on a CPU. This is a simple average of the reported classes.

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/execution_pipeline.jpg" width="711" height="578" alt="Execution pipeline"> 
</p>
<p align="center">
<b>Figure 7</b><i> - The three stages of the execution pipeline -First, feature value ranges are calculated, then feature vectors are translated into lable vectors (based on the floating-point value intervals calculated by the FPGA on the AP card), and finally the AP uses the decision tree paths (translated into STE cycles) to process the data and return classifications.</i><b>[1]</b>
</p>

## Dependancies
Make sure that you have the following dependencies installed. If missing, **use pip to install**. (If this doesn't work you will need to download and run python setup file or download the source code and add to PYTHONPATH.)


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
To use pip to install in BASH, type the following command: 
```
$ pip install <package name>
```  
To install without root access use the following command:
```
$ pip install -- user <package name>
```    
#### Python setup file
To run the python setup file simply download the dependancy, go to the directory in BASH, and type the following to run the python setup file:
```
$ python setup.py install
```

### MNRL
You also need to add the MNRL dependancy:
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

In order to use this code to train ensemble modes from your own data, it is necessary to write an extractor for your raw data. This script processes your raw data and converts it into Numpy X and y matrices. These are then stored in a Numpy Zip file (.npz). Please see the following examples found in the <a href="https://github.com/tjt7a/rfautomata/tree/master/data">data</a> folder of RF Automata.

### ocrExtractor

The ocrExtractor program extracts the pixel feature matrix (X) and classification vector (y) from normalized handwritten letter data based on Rob Kassel's OCR work. The data can be obtained from the following locations:  
https://github.com/adiyoss/StructED/tree/master/tutorials-code/ocr/data  
http://ai.stanford.edu/~btaskar/ocr/  
-i: Input OCR data file derived from Rob Kassel's MIT work  
-o: The output .npz filename that will contain X and y  
-v: Verbosity flag  
--visualize: This flag will open a gui and show a random handwritten character for reference.

### mslrExtractor

The mslrExtractor program extracts the learn-to-rank feature matrix (X) and resulting rank score vector (y) from the MSLR LETOR data. The data can be obtained from Microsoft's website.  
-i: Input MSLR data file  
-o: The output .npz filename that will contain X and y  
-v: Verbosity flag  


## Automata Files

### 300f_15t_from_model_MNIST.anml
A random forest with 15 trees and 300 features per input trained on the MNIST digit recognition library. This ANML file was generated as a part of the original ANMLZoo benchmark suite. It was generated incorrectly and thus should not be considered a "standard candle". However, it is a valid benchmark and is maintained for posterity.

### rf.1chip.anml
A portion of 300f_15t_from_model_MNIST.anml properly pruned to max out the resources of an AP chip.

## Inputs
### mnist_1MB.input

### mnist_10MB.input

# References
**[1]** Tracy II, T., Fu, Y., Roy, I., Jonas, E., & Glendenning, P. (2016, June). Towards Machine Learning on the Automata Processor. In International Conference on High Performance Computing (pp. 200-218). Springer International Publishing, 2016.
