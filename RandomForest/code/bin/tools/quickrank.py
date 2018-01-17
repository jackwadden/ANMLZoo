'''
    The purpose of this module is to convert QuickLearn models into
    an automata representation.

    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    27 January 2017
    Version 1.0
'''

# Utility Imports
import sys
import xmltodict
import logging

# RF Automata Imports
from classes.chain import *
from classes.featureTable import *
import tools.charactersets as cs


# Turn on logging.
logging.basicConfig(format='%(asctime)s : %(message)s', level=logging.INFO)

# Load the quickrank xml file
def load_qr(modelfile):

    # Read the modelfile xml file
    with open(modelfile, 'r') as f:
        xml = f.read()

    parsed = xmltodict.parse(xml)

    return parsed


# Grab ensemble and tree data from parsed XML
def grab_data(xml, verbose=False):

    # First layer
    ranker = xml['ranker']

    # 2nd Layer
    info = ranker['info']
    ensemble = ranker['ensemble']

    # Info
    num_trees = int(info['trees'])
    leaves = int(info['leaves'])

    # ensemble
    trees = ensemble['tree']

    if verbose:
        logging.info("Trees:%d, Leaves:%d" % (num_trees, leaves))

    tree_list = []

    for t_ in trees:

        tree_id = int(t_['@id'])
        tree_weight = float(t_['@weight'])
        tree_split = t_['split']

        tree_list.append((tree_id, tree_weight, tree_split))

        if verbose:
            logging.info("ID:%d, WEIGHT:%f" % (tree_id, tree_weight))

    return tree_list


# Convert tree to chains
def tree_to_chains(tree_id, tree_weight, tree_split, chains,
                   threshold_map, values):

    # Root node attributes
    feature = int(tree_split['feature'])
    threshold = float(tree_split['threshold'])
    split = tree_split['split']

    # Keeping track of features and associated thresholds for all trees
    if feature not in threshold_map:
        threshold_map[feature] = [threshold]

    # If the feature has already been seen,
    # check to see if this is a unique threshold
    elif threshold not in threshold_map[feature]:
        threshold_map[feature].append(threshold)

    # Let's grab references to our children nodes
    left = split[0]
    right = split[1]

    # Create chain to be populated with nodes; add root node
    left_chain = Chain(tree_id, tree_weight=tree_weight)
    root_node = Node(feature, threshold, False)
    left_chain.add_node(root_node)

    # Make two copies of our chain
    right_chain = Chain(tree_id, tree_weight=tree_weight)
    root_node = Node(feature, threshold, True)
    right_chain.add_node(root_node)

    # Recursively add chains to the list as we iterate left
    chains += recurse(left, left_chain, threshold_map, values)

    # Recursively add chains to the list as we iterate left
    chains += recurse(right, right_chain, threshold_map, values)

    # Ok, we're done here
    return


# Recursive function to convert trees into chains
def recurse(split, temp_chain, threshold_map, values):

    # We're at a leaf!
    if 'output' in split:
        value = float(split['output'])

        if value not in values:
            values.append(value)

        temp_chain.set_value(value)

        return [temp_chain]

    else:

        feature = int(split['feature'])
        threshold = float(split['threshold'])
        next_split = split['split']

        # Keep track of features and associated thresholds
        if feature not in threshold_map:
            threshold_map[feature] = [threshold]

        elif threshold not in threshold_map[feature]:
            threshold_map[feature].append(threshold)

        # Let's go left, then right
        left_chain = temp_chain
        right_chain = temp_chain.copy()

        # feature, threshold, gt
        node_l = Node(feature, threshold, False)
        left_chain.add_node(node_l)

        # Let's do the same for the right and recurse
        node_r = Node(feature, threshold, True)
        right_chain.add_node(node_r)

        return recurse(next_split[0], left_chain, threshold_map, values) +\
            recurse(next_split[1], right_chain, threshold_map, values)


# Test the module by converting a quickrank xml file into a set of chains
if __name__ == '__main__':
    if len(sys.argv) == 2:
        xml_filename = sys.argv[1]
    else:
        print "Missing xml filename argument"
        exit(0)

    logging.info("Loading quickrank xml file from %s" % xml_filename)
    parsed_xml = load_qr(xml_filename)

    logging.info("Grabbing data from the parsed XML")
    trees = grab_data(parsed_xml)

    # trees contains (tree_id, tree_weight, tree_split)
    for tree_id, tree_weight, tree_split in trees:
        print "Tree ID: %d, Tree Weight: %f" % (tree_id, tree_weight)

    # Convert all trees to chains
    chains = []

    # Keep track of all features used in the ensemble
    features = []

    # Keep track of features -> thresholds
    threshold_map = {}

    # Keep track of unique values
    values = []

    # Iterate through all trees in the ensemble and
    # keep track of chains, features, and thresholds
    logging.info("Converting trees to chains")

    for tree_id, tree_weight, tree_split in trees:

        tree_to_chains(tree_id, tree_weight, tree_split, chains,
                       features, threshold_map, values)

    # Assign chain ids sequentially over list
    for chain_id, chain in enumerate(chains):
        chain.set_chain_id(chain_id)

    # Sort the features
    features.sort()

    # Sort the thresholds for all features
    for f, t in threshold_map.items():
        t.sort()

    # The value_map is used to give unique value ids to each value
    values.sort()

    value_map = {}

    # We're going to map chain values to classes with an offset of 1, because
    # we can't have a report code of 0 (workaround)
    for _i, _value in enumerate(values):
        value_map[_i + 1] = _value

    logging.info("Building the Feature Table")

    # Create ideal address spacing for all features and thresholds
    ft = FeatureTable(threshold_map)

    print "I'm here!"

    logging.info("Compacting the Feature Table")

    ft.compact()    # Run the compactor (NOT IDEAL, but good enough)

    logging.info("Sorting and combining the chains")

    # Set the character sets for each node in the chains
    # Then sort and combine the states in the chains
    for chain in chains:
        cs.set_character_sets(chain, ft)
        chain.sort_and_combine()

    logging.info("Dumping Chains, Feature Table, and Value Map to pickle")

    logging.info("Done!")

    # Create a reverse value map to use index of float value
    reverse_value_map = {value: key for key, value in value_map.iteritems()}
