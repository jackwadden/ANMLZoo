# RandomForest
## Description

This is an open-source implementation of Decision Tree-based (Random Forest, Boosted Regression Trees, Adaboost) machine learning models as Automata on Micron's Automata Processor (AP). This code trains a Decision Tree-based model with Scikit Learn (on the CPU), and transforms the resulting model into ANML, an XML-like representation of Nondeterministic Finite Automata (NFA) for the Automata Processor. 

While the first, labeling, stage occurs on the FPGA on the AP card and the second, model execution, stage occures on the AP; currently the final voting stage of classification must be done on a CPU.

For more about the Automata Processor, visit CAP's website: http://cap.virginia.edu/

This project is written in Python in the Object-Oriented style.

### Download
Download the RF Automata code from author Tommy Tracy II's repository located <a href="https://github.com/tjt7a/rfautomata">here</a>. You can also clone it to your machine using the following command: 
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

In order to use this code to train ensemble modes from your own data, it is necessary to write an extractor for your raw data. This script processes your raw data and converts it into Numpy X and y matrices. These are then stored in a Numpy Zip file (.npz). Please see the following examples found in <a href="https://github.com/tjt7a/rfautomata/tree/master/data">data</a> folder of RF Automata:

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
Tracy II, T., Fu, Y., Roy, I., Jonas, E., & Glendenning, P. (2016, June). Towards Machine Learning on the Automata Processor. In International Conference on High Performance Computing (pp. 200-218). Springer International Publishing, 2016.
