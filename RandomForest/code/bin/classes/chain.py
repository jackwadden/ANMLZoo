'''
-----                                               -----
=   This objected-oriented module defines a chain class =
=   ----------------------                              =
=   Author: Tom Tracy II                                =
=   email: tjt7a@virginia.edu                           =
=   University of virginia                              =
=   ----------------------                              =
=    12 June 2017
=    Version 0.2                                        =
=                                                       =
=   In the first version, we removed edges              =
-----                                               ------
'''

# Utility Imports
import copy


# Define Node class
class Node(object):

    # Constructor for Node
    def __init__(self, feature, threshold, gt):
        self.feature_ = feature         # Index of the feature
        self.threshold_ = threshold     # Threshold
        self.gt_ = gt                   # greater-than?; else less-than

        # Automata-related stuff
        # We're going to need a character set per STE
        self.character_sets = None      # Start with an empty set

    # Deep copy of the Node
    def copy(self):
        return copy.deepcopy(self)

    # String representation of the node
    def __str__(self):
        string = ""
        string += "[f:%d" % self.feature_
        if self.gt_:
            string += ">"
        else:
            string += "<="
        string += "%s]" % str(self.threshold_)
        string += "CharSet: %s\n" % str(self.character_sets)
        return string

    # Define Node equivalence
    def __eq__(self, other):
        return self.feature_ == other.feature_ and\
            self.threshold_ == other.threshold_ and\
            self.gt_ == other.gt_

    # Define comparison operator for sorting
    def __cmp__(self, other):
        return self.get_key().__cmp__(other.get_key())

    # Define the key used for comparison
    def get_key(self):
        return self.feature_

    # Set the direction (is the direction greater-than?)
    def set_direction(self, gt):
        self.gt_ = gt

    # Set the character sets of the current node
    def set_character_sets(self, character_sets):
        self.character_sets = character_sets
        self.character_sets.sort()


# Define Chain class
class Chain(object):

    # Chain constructor
    def __init__(self, tree_id, tree_weight=None):
        self.nodes_ = []                # List of nodes
        self.tree_id_ = tree_id
        self.chain_id_ = None
        self.value_ = None
        self.chain_ = None

        # This was added for boosted regression trees
        self.tree_weight_ = tree_weight

    # Deep copy of the Chain
    def copy(self):
        return copy.deepcopy(self)

    # String representation of the Chain
    def __str__(self):
        string = "id: " + str(self.chain_id_) + '\n'
        for index, node in enumerate(self.nodes_):
            string += str(node) + "(" + str(index) + ")"
            string += '\n'
        return string

    # Set the chain id
    def set_chain_id(self, chain_id):
        self.chain_id_ = chain_id

    # Set the value of the chain
    def set_value(self, value):
        self.value_ = value

    # Sort the chain by feature value, then update ids and children
    def sort_and_combine(self, verbose=False):

        # Sort the nodes_ in the chain by feature value (increasing)
        self.nodes_.sort()

        # Can't combine with only one node!
        if len(self.nodes_) == 1 or len(self.nodes_) == 0:
            return

        # Let's combine!
        previous_index = 0
        current_index = 1

        while True:

            previous_node = self.nodes_[previous_index]
            current_node = self.nodes_[current_index]

            # If they have the same feature, combine
            if previous_node.feature_ == current_node.feature_:

                new_character_sets = []

                assert len(previous_node.character_sets) ==\
                    len(current_node.character_sets), "|ccs| != |pcs|!"

                for pcs, ccs in zip(previous_node.character_sets,
                                    current_node.character_sets):

                    intersection = list(set(pcs).intersection(set(ccs)))
                    intersection.sort()
                    new_character_sets.append(intersection)

                assert len(new_character_sets) ==\
                    len(previous_node.character_sets) ==\
                    len(current_node.character_sets)

                previous_node.set_character_sets(new_character_sets)
                self.nodes_.remove(current_node)

            else:

                previous_index += 1
                current_index += 1

            # We're done
            if current_index == len(self.nodes_):
                break

    # Add a node to the chain
    def add_node(self, node):

        if node in self.nodes_:
            return -1

        else:
            self.nodes_.append(node)

            return 1
