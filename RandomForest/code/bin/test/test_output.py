# Utility Imports
import sys
from optparse import OptionParser
import logging
import pickle
import numpy as np
from collections import Counter
import itertools

# Load the chains, FT and value map from a file
def load_cftvm(cftFile):

    with open(cftFile, 'rb') as f:
        chains, ft, value_map, reverse_value_map = pickle.load(f)

    return chains, ft, value_map, reverse_value_map

# Load test data
def load_test(testfile):

  with open(testfile, 'rb') as f:

    X_test, y_test = pickle.load(f)

  return X_test, y_test

# Load a sklearn model from a file
def load_model(modelfile):

    # Read the modelfile pickle
    with open(modelfile, 'rb') as f:
        model = pickle.load(f)

    return model

def run_model(model, X):
    return model.predict(X)

if __name__ == "__main__":

    # Parse Command Line Arguments
    usage = '%prog [options][text]'
    parser = OptionParser(usage)
    parser.add_option('-c', '--cftvm', type='string', dest='cftvm', help='Filename of chains and feature table pickle')
    parser.add_option('-r', '--report', type='string', dest='report', help='Report file from VAsim')
    parser.add_option('-m', '--model', type='string', dest='model', help='The model to be used for comparison')
    parser.add_option('-t', '--test', type='string', dest='test', help='The test data')
    parser.add_option('-v', '--verbose', action='store_true', default=False, dest='verbose', help='Verbose')
    options, args = parser.parse_args()

    # This allows us to test the ANML code faster by loading our converted data structures
    if options.cftvm is not None:
        chains, ft, value_map, reverse_value_map = load_cftvm(options.cftvm)

    if options.model is None:
        raise ValueError("No valid model specified")

    # Load the cftvm file
    chains, ft, value_map, reverse_value_map = load_cftvm(options.cftvm)

    X, y = load_test(options.test)

    model = load_model(options.model)
    model_results = run_model(model, X)

    automata_results = []

    previous_cycle_count = None
    class_list = []

    with open(options.report, 'r') as f:

        for line in f:

            report_components = line.split(':')
            cycle_count = int(report_components[0].strip())
            reporting_ste = report_components[1].strip()
            classification = int(report_components[2].strip())

            if previous_cycle_count is None:
                previous_cycle_count = cycle_count

            if cycle_count != previous_cycle_count:
                automata_results.append(max(set(class_list), key=class_list.count))
                class_list = []
                previous_cycle_count = cycle_count

            else:
                class_list.append(classification)

        automata_results.append(max(set(class_list), key=class_list.count))

    for i, j in zip(model_results, automata_results):

        print i, ' : ', reverse_value_map[j]