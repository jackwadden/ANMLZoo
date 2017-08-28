#!/usr/bin/env python
'''
    The purpose of this program is to test the Scikit-Learn model
    on your CPU to get throughput results.
    
    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    12 June 2017
    Version 0.2
'''

# Utility Imports
from optparse import OptionParser
import logging
import pickle
import time

# Turn on logging; let's see what all is going on
logging.basicConfig(format='%(asctime)s : %(message)s', level=logging.INFO)


# Load a sklearn model from a file
def load_model(modelfile):

    # Read the modelfile pickle
    try:
        with open(modelfile, 'rb') as f:
            model = pickle.load(f)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        exit(-1)

    return model


# Load testing data
def load_test(testfile):

    # Read the testing data in to be used to generate a symbol file
    try:
        with open(testfile, 'rb') as f:
            X_test, y_test = pickle.load(f)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        exit(-1)

    return X_test, y_test


if __name__ == '__main__':

    # Parse Command Line Arguments
    usage = '%prog [options][text]'
    parser = OptionParser(usage)
    parser.add_option('-m', '--model', type='string', dest='model',
                      default='model.pickle',
                      help='Input SKLEARN model pickle file')
    parser.add_option('-t', '--test', type='string', dest='test',
                      default='testing_data.pickle', help='The testing data')
    parser.add_option('-n', '--numiter', type='float', dest='iters',
                      default=1000,
                      help='The number of times the test is run to get data')
    parser.add_option('-j', '--njobs', type='int', dest='njobs',
                      help='The number of threads to execute the model')
    parser.add_option('-v', '--verbose', action='store_true', default=False,
                      dest='verbose', help='Verbose')
    options, args = parser.parse_args()

    logging.info("Running CPU throughput test %d times with model %s" %
                 (options.iters, options.model))

    if options.model is None:
        print(usage)
        exit(-1)
    else:
        model = load_model(options.model)

    if model.max_leaf_nodes is not None:
    	logging.info("Model: nTrees: %d, nLeaves:%d, nJobs: %d" %
        	     (model.n_estimators, model.max_leaf_nodes, model.n_jobs))
    else:
        logging.info("Model: nTrees: %d, maxDepth:%d, nJobs: %d" %
		     (model.n_estimators, model.max_depth, model.n_jobs))

    X_test, y_test = load_test(options.test)
    logging.info("Test Data: %d samples x %d features" % (X_test.shape))

    # Grab the constituent estimators
    trees = model.estimators_

    # If we only have one, let's do a test on of the trees
    if len(trees) == 1:
        logging.info("Only one tree in the Forest; running seperate test")

        if options.njobs is None:
            logging.info("Because there is only one tree, we cannot parallelize")

        start_time = time.time()

        for i in range(int(options.iters)):
            trees[0].predict(X_test)

        end_time = time.time()

        avg_time = (end_time - start_time) / options.iters
        print("Avg Time for D-Tree: ", avg_time)

        throughput = float(X_test.shape[0]) / avg_time
        kthroughput = throughput / 1000.0

        logging.info("D-Tree Throughput: %d kSamples / second" % (kthroughput))
    else:

        if options.njobs is not None:
            model.n_jobs = options.njobs

        start_time = time.time()

        for i in range(int(options.iters)):
            model.predict(X_test)

        end_time = time.time()

        avg_time = (end_time - start_time) / options.iters
        print("Avg Time: ", avg_time)

        throughput = float(X_test.shape[0]) / avg_time
        kthroughput = throughput / 1000.0

        logging.info("RF Throughput: %f ksamples / second" % (kthroughput))
