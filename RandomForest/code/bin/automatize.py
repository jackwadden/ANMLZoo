#!/usr/bin/env python

"""
    The purpose of this program is to convert
    Scikit Learn (RF, BRT) and Quick Rank models into an
    automata representation.
    * http://scikit-learn.org/stable/
    * https://github.com/hpclab/quickrank

    For the time being let's only support Random Forests,
    BRTs, ADABOOST, and QuickRank Models.
    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    15 January 2018
    Version 0.3

    *Definitions*
    ----------------------
    features: a LIST containing all of the features

    threshold_map: a Python Dictionary that maps features to a list of
    all thresholds used for that feature in the entire ensemble model
        ie if feature 0 is split on 1.2, 3, 4.5 and 6, the entry in the
        threshold map would look like this:
            threshold_map[0] = [1.2, 3, 4.5, 6]

"""

# Utility Imports
from optparse import OptionParser
import numpy as np
import os.path

# Automata Imports
from classes.featureTable import *

# Import tools
import tools.charactersets as cs
import tools.quickrank as qr
import tools.sklearn as skl
from tools.anmltools import *
import tools.gputools as gputools
from tools.io import *

# WARNING: EXPERIMENTAL
from tools.circuitTools import generate_circuits

# MNRL Tools
from tools.mnrltools import *

# Turn on logging; let's see what all is going on
logging.basicConfig(format='%(asctime)s : %(message)s', level=logging.INFO)

# Main()
if __name__ == '__main__':

    quickrank = False

    # Parse Command Line Arguments
    usage = '%prog [options][model filename]'

    parser = OptionParser(usage)

    parser.add_option('-a', '--anml', type='string', dest='anml',
                      default='model.anml', help='ANML output filename')

    parser.add_option('--gpu', action='store_true', default=False, dest='gpu',
                      help='Generate GPU compatible chains and output files **EXPERIMENTAL**')

    parser.add_option('--circuit', action='store_true', default=False, dest='circuit',
                      help='Generate circuit compatible chains and output files **EXPERIMENTAL**')

    parser.add_option('--unrolled', action='store_true', default=False, dest='unrolled',
                      help='Set to get unrolled chains (no loops)')

    parser.add_option('--mnrl', action='store_true', default=False, dest='mnrl',
                      help='Generate MNRL chains (with floating point thresholds \
                      and one STE per feature)')

    parser.add_option('--short', action='store_true', default=False, dest='short',
                      help='Make a short version of the input (100 samples)')

    parser.add_option('--longer', action='store_true', default=False,
                      dest='longer',
                      help='Make a 1000x longer input (23,100,000)')

    parser.add_option('-p', '--thresholds', action='store_true', default=False,
                      dest='plot_thresholds',
                      help='Generate a plot of the distribution of threshold counts')

    parser.add_option('-v', '--verbose', action='store_true', default=False,
                      dest='verbose', help='Verbose')

    options, args = parser.parse_args()

    model_filename = None

    # Verify model filename parameter
    if len(args) == 1:

        model_filename = args[0]

        # Verify that the file exists
        if not os.path.isfile(model_filename):
            parser.error("No valid model file; provide <model filename>")

        if options.verbose:
            logging.info("Loading model file from %s" % model_filename)

    else:
        parser.error("No valid model; provide <model filename>")

    # Grab the model
    model = None

    # Simple check if quickrank model (might wanna improve this later)
    if '.xml' in model_filename:

        quickrank = True

        model = qr.load_qr(model_filename)

        # Grab the constituent trees
        trees = qr.grab_data(model)

    # Else, its a scikit learn-type model
    else:
        model = load_model(model_filename)

        # Grab the constituent trees
        trees = [dtc.tree_ for dtc in model.estimators_]

    if options.verbose:
        logging.info("Grabbed %d constituent trees to be 'chained'" %
                     len(trees))

    # Convert all trees to chains
    # Each chain represents a root->leaf path
    chains = []

    # Keep track of map from unique
    # feature -> thresholds used for branch comparisons
    threshold_map = {}

    # Keep track of unique class values (unique(Y))
    values = []

    # We're going to use these to index leaf values (classes)
    value_map = {}
    reverse_value_map = {}

    # To deal with quickrank, we need to parse the trees differently
    if quickrank:

        if options.verbose:
            logging.info("Converting QuickRank trees to chains")

        # Here is where we generate the chains from the trees
        for tree_id, tree_weight, tree_split in trees:

            qr.tree_to_chains(tree_id, tree_weight, tree_split,
                              chains, threshold_map, values)

        # Sort the classification values
        values.sort()

        # Create a map from value to index (starting from 1 -- imposed by AP)
        for _i, _value in enumerate(values):

            value_map[_value] = _i + 1
            reverse_value_map[_i + 1] = _value

    # Else, we're dealing with an SKLEARN model
    else:

        if options.verbose:
            logging.info("Converting SKLEARN trees to chains")

        # Grab the classification values
        classes = model.classes_

        if options.verbose:
            logging.info("%d unique classifications available: %s" %
                         (len(classes), str(model.classes_)))

        # For each tree, chain-ify
        for tree_id, tree in enumerate(trees):

            skl.tree_to_chains(tree, tree_id, chains, threshold_map, values)

        if options.verbose:
            logging.info("There are %d chains" % len(chains))

        for _i in values:
            # value_map[classes[_i]] = _i + 1

            # We don't need a value map (this might not be true)
            value_map = None
            reverse_value_map[_i + 1] = classes[_i]

    if options.verbose:
        logging.info("Done converting trees to chains; now sorting")

    # Because we built the chains from the left-most to the right-most leaf
    # We can simply assign chain ids sequentially over our list
    for chain_id, chain in enumerate(chains):
        chain.set_chain_id(chain_id)

    # Now, once we have our chains, we can make our mnrl chains (which contain thresholds)
    if options.mnrl:
        mnrl_network = make_mnrl_chains(chains)

        mnrl_network.exportToFile("chains.mnrl")

        X_test, y_test = load_test("testing_data.pickle")

        # Catch
        if not X_test or not y_test:
            raise ValueError

        np.savetxt("testing.csv", X_test, delimiter=',', fmt='%1.4e')

        if options.verbose:
            logging.info("Done generating MNRL and testing output files")

        # We stop here with MNRL
        exit(0)

    # Sort the thresholds for all features
    for f, t in threshold_map.items():
        t.sort()

    if options.verbose:
        logging.info("There are %d features in the threshold map [%d-%d]" %
                     (len(threshold_map.keys()), min(threshold_map.keys()),
                      max(threshold_map.keys())))

    # Let's look at the threshold distribution
    if options.plot_thresholds:
        from tools.plot import plot_thresholds
        plot_thresholds(threshold_map)

    if options.verbose:
        logging.info("Building the Feature Table")

    # Create ideal address spacing for all features and thresholds
    ft = FeatureTable(threshold_map, unrolled=options.unrolled)

    if options.verbose:
        logging.info("Sorting and combining the chains")

    # Set the character sets for each node in the chains
    # Then sort and combine the states in the chains
    for chain in chains:
        cs.set_character_sets(chain, ft)
        chain.sort_and_combine()

    if options.verbose:
        logging.info("Dumping Chains, Feature Table,\
            Value Map and Reverse Value Map to pickle")

    # Generate output for GPU implementation
    if options.gpu:

        if options.verbose:
            logging.info("Generating %d GPU chains" % (len(chains)))

        gputools.gpu_chains(chains, ft, value_map, options.anml)

    # Generate output for circuit implementation
    elif options.circuit:

        if options.verbose:
            logging.info("Generating circuit file with %d chains" % (len(chains)))

        generate_circuits(chains, ft, value_map, "circuits.txt", unrolled=options.unrolled)

    # Else, we're dealing with a spatial architecture; generate ANML
    else:

        if options.verbose:
            logging.info("Generating ANML file with %d chains" % (len(chains)))

        generate_anml(chains, ft, value_map, options.anml, unrolled=options.unrolled)

    if options.verbose:
        logging.info("Dumping test file")

    X_test, y_test = load_test("testing_data.pickle")

    # If using quickrank, our features are based at index = 1, instead of 0
    ft.input_file(X_test, "input_file.bin", onebased=quickrank,
                  short=options.short, delimited=True)

    logging.info("Done!")
