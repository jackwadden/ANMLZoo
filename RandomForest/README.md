# RandomForest
## Description

This benchmark is an open-source implementation of decision tree-based (Random Forest, Boosted Regression Trees, Adaboost) machine learning models as automata on Micron's Automata Processor (AP) and is written in Python in the Object-Oriented style. This code trains a decision tree-based model with <a href="http://scikit-learn.org/stable/index.html#">scikit-learn</a> (on a CPU), and transforms the resulting model into the ANML format, an XML-like representation of nondeterministic finite automata (NFA) for the Automata Processor. 

For more about the Automata Processor, visit <a href="http://cap.virginia.edu/">CAP's website</a>. 


## Random Forest Algorithm

Random Forest is an ensemble technique supervised classification algorithm. It is made of many binary decision trees, each trained by a random subset of sample data. We can 

A feature

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/classification_decision_tree.jpg" width="820" height="423" alt="Classification decision tree"> 
</p>
<p align="center">
<b>Figure 1</b> - Decision tree with a single feature vector <b>[1]</b>
</p>


<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/tree_w_values.jpg" width="614" height="194" alt="Tree with values">  
</p>
<p align="center">
<b>Figure 2</b> - The  <b>[1]</b>
</p>


<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/complete_chains_a.jpg" width="821" height="358" alt="Reordered and complete tree">  
</p>
<p align="center">
<b>Figure 3</b> - The  <b>[1]</b>
</p>


<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/feature_addresses.jpg" width="819" height="243" alt="Feature addresses">  
</p>
<p align="center">
<b>Figure 4</b> - The  <b>[1]</b>
</p>

<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/chains_as_automata.jpg" width="711" height="460" alt="Chains as automata">  
</p>
<p align="center">
<b>Figure 5</b> - The  <b>[1]</b>
</p>


<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/combined_features.jpg" width="816" height="274" alt="Combined features automata">  
</p>
<p align="center">
<b>Figure 6</b> - The  <b>[1]</b>
</p>



### Execution Pipeline

First a feature vector values are turned into 8-bit label values and added to a lavel vector. Next the AP processes these vectors in parallel to identify tree classifications.
<p align="center">
<img src="https://raw.githubusercontent.com/jeffudall/ANMLZooCopy/master/RandomForest/images/execution_pipeline.jpg" width="711" height="578" alt="Execution pipeline"> 
</p>
<p align="center">
<b>Figure 7</b> - The  <b>[1]</b>
</p>
Currently the final voting stage, of combining the classifications from all trees, must be done on a CPU.



### Download
Download the RF Automata code, by author Tommy Tracy II, from the repository located <a href="https://github.com/tjt7a/rfautomata">here</a>. You can also clone it to your machine using the following command: 
`git clone git@github.com:tjt7a/rfautomata.git`

## Dependancies
Make sure that you have the following dependencies installed. If missing, **use pip to install**. (If this doesn't work you will need to download and run python setup file or download the source code and add to PYTHONPATH.)
- <a href="https://github.com/python/cpython/blob/2.7/Lib/optparse.py">optparse</a>
- <a href="https://pypi.python.org/pypi/logging/0.4.9.6">logging</a>
- <a href="https://github.com/python/cpython/blob/3.6/Lib/pickle.py">pickle</a>
- <a href="https://pypi.python.org/pypi/numpy/1.13.1">NumPy</a>
- <a href="https://pypi.python.org/pypi/scipy/0.19.1">SciPy</a>
- <a href="https://pypi.python.org/pypi/scikit-learn">scikit-learn</a>
- <a href="https://pypi.python.org/pypi/termcolor/1.1.0">termcolor</a>
- <a href="https://pypi.python.org/pypi/xmltodict/0.11.0">xmltodict</a>
- <a href="https://pypi.python.org/pypi/enum/0.4.6">enum</a>
- <a href="https://pypi.python.org/pypi/jsonschema#downloads">jsonschema</a>

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
$ export PYTHONPATH = [filepath]/mnrl/python
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
