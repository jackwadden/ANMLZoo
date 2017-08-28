'''
    The purpose of this program is to test the result
    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    1 December 2016
    Version 1.0
'''

# Support Imports
import sys, pickle
from optparse import OptionParser
import numpy as np
import logging
import array

# Model Imports
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier

# Metrics Import
from sklearn import metrics

# Turn on logging.
logging.basicConfig(format='%(asctime)s : %(message)s', level=logging.INFO)

# Load the chains, FT and value map from a file
def load_cft_vm(cftFile):

    logging.info("Loading Chains, FT, ValueMap file from %s" % cftFile)

    f = open(cftFile, 'rb')
    chains, ft, value_map = pickle.load(f)
    f.close()

    return chains, ft, value_map

# Main()
if __name__ == '__main__':

    # Parse Command Line Arguments
    usage = '%prog [options][text]'
    parser = OptionParser(usage)
    parser.add_option('-t', '--test', type='string', dest='testfile', help='Testing Data File (.npz file)')
    parser.add_option('--metric', type='string', default='acc', dest='metric', help='Provide the training metric to be displayed')
    parser.add_option('-m', '--model', type='string', dest='model', help='Choose the model')
    #parser.add_option('-o', '--file-out', type='string', dest='outfile', help='Save resulting X and y to a file')
    parser.add_option('--chain-ft-vm', type='string', dest='cftvm', help="Filename of chains and feature table pickle")
    parser.add_option('-v', '--verbose', action='store_true', default=False, dest='verbose', help='Verbose')
    parser.add_option('-r', '--report', type='string', dest='report', help='Name of the report file')
    options, args = parser.parse_args()

    params = {}
    report_dict = {}

    # Validate command line arguments
    if options.testfile is None:
        raise ValueError("No valid training data filename specified; provide -t")
        exit(-1)

    if options.cftvm is None:
        raise ValueError("No valid chain-ft-vm filename specified; provide --chain-ft-vm")
        exit(-1)

    # Load the training files
    npzfile = np.load(options.testfile)
    X = npzfile['X']
    y = npzfile['y']

    logging.info("Shape of the loaded testing data. X:(%d,%d), y:(%d,%d)" %(X.shape[0], X.shape[1], y.shape[0], y.shape[1]))

    # We're gonna write out the first 10
    X_test = X[:10]
    y_test = y[:10]

    chains, ft, value_map = load_cft_vm(options.cftvm)

    print ft.features_
    print ft.feature_pointer_

    inputfile = file('input.bin', 'wb')
    inputstring = array.array('B')
    inputstring.append(255)

    for row in X_test:
        for f_i, f_v in enumerate(row):
            if f_i in ft.features_:
                ste, symbol = ft.get_symbol(f_i, f_v)
                inputstring.append(symbol)
                #print "Feature: ", f_i,
                #print "Symbol: ", symbol,
        inputstring.append(255)

inputfile.write(inputstring.tostring())
inputfile.close()

