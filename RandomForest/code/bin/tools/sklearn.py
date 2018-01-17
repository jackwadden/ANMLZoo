'''
    The purpose of this module is to convert Scikit Learn models into
    an automata representation.

    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    19 October 2017
    Version 1.0
'''

# Utility Imports
import sys
import numpy as np

# RF Automata Imports
from classes.chain import *
from classes.featureTable import *
from classes.chain import *

# Convert tree to chains (for scikit-learn models)
def tree_to_chains(tree, tree_id, chains, threshold_map, values):

    # Root node attributes
    feature = tree.feature[0]
    threshold = tree.threshold[0]

    # Keeping track of features and associated thresholds for all trees
    if feature not in threshold_map:
        threshold_map[feature] = [threshold]

    # If feature already seen, check to see if this is a unique threshold
    elif threshold not in threshold_map[feature]:
        threshold_map[feature].append(threshold)

    # Let's grab references to our children nodes
    left = tree.children_left[0]
    right = tree.children_right[0]

    # Let's create a 'left' chain from the root
    left_chain = Chain(tree_id)

    # This is the root node -> left decision
    root_node = Node(feature, threshold, False)
    left_chain.add_node(root_node)

    # Let's create a 'right' chain from the root
    right_chain = Chain(tree_id)

    # This is the root node -> right decision
    root_node = Node(feature, threshold, True)
    right_chain.add_node(root_node)

    # We have our left chain; let's recurse!
    chains += recurse(tree, left, left_chain, threshold_map, values)

    # We have our right chain; let's recurse!
    chains += recurse(tree, right, right_chain, threshold_map, values)

    # Ok we're done here
    return


# Recursive function to convert trees into chains
def recurse(tree, index, temp_chain, threshold_map, values):

    feature = tree.feature[index]
    threshold = tree.threshold[index]

    # We're a leaf; we're done here
    if feature == -2:

        # Take the most observed class index
        value = np.argmax(tree.value[index])

        # Have we seen this leaf node value before?
        if value not in values:
            # We have a new leaf up in here!
            values.append(value)

        # Set the value of the chain
        temp_chain.set_value(value)

        # This returns the chain as a single value list
        return [temp_chain]

    # If we're not a leaf, we must have children!
    else:

        # Because we're a binary decision tree, we must have both a left and right child
        left = tree.children_left[index]
        right = tree.children_right[index]

        # Keeping track of features and associated thresholds
        if feature not in threshold_map:
            threshold_map[feature] = [threshold]

        elif threshold not in threshold_map[feature]:
            threshold_map[feature].append(threshold)

        # Let's go left, then right
        left_chain = temp_chain
        right_chain = left_chain.copy()

        # feature, threshold, gt
        node_l = Node(feature, threshold, False)
        left_chain.add_node(node_l)

        # Let's do the same for the right and recurse
        node_r = Node(feature, threshold, True)
        right_chain.add_node(node_r)

        return recurse(tree, left, left_chain, threshold_map, values) + \
            recurse(tree, right, right_chain, threshold_map, values)