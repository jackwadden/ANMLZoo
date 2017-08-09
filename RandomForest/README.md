# RandomForest
## Description

This is an open-source implementation of Decision Tree-based (Random Forest, Boosted Regression Trees, Adaboost) machine learning models as Automata on Micron's Automata Processor (AP). This code trains a Decision Tree-based model with Scikit Learn (on the CPU), and transforms the resulting model into ANML, an XML-like representation of Nondeterministic Finite Automata (NFA) for the Automata Processor.

For more about the Automata Processor, visit CAP's website: http://cap.virginia.edu/

This project is written in Python in the Object-Oriented style.

### Download
Download the RandomForest code from author Tommy Tracy II's repository located <a href="https://github.com/tjt7a/rfautomata">here</a>. You can also clone it to your machine using the following command: 
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
or to install without root access use the following command:
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

## Automata Files

### 300f_15t_from_model_MNIST.anml
A random forest with 15 trees and 300 features per input trained on the MNIST digit recognition library. This ANML file was generated as a part of the original ANMLZoo benchmark suite. It was generated incorrectly and thus should not be considered a "standard candle". However, it is a valid benchmark and is maintained for posterity.

### rf.1chip.anml
A portion of 300f_15t_from_model_MNIST.anml properly pruned to max out the resources of an AP chip.

## Inputs
### mnist_1MB.input

### mnist_10MB.input

# References
Tracy II, T., Fu, Y., Roy, I., Jonas, E., & Glendenning, P. (2016, June). Towards Machine Learning on the Automata Processor. In International Conference on High Performance Computing (pp. 200-218). Springer International Publishing.
