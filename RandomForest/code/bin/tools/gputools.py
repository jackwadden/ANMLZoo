'''
    This module is meant for generating GPU chains

    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    10 April 2016
    Version 1.0
'''

# Generate GPU chains

def gpu_chains(chains, feature_table, value_map, gpu_chains_filename):

    gpu_file = open(gpu_chains_filename, 'w')

    # Write the number of chains, and the bin count per chain
    # The number of chains in this gpu chains file
    gpu_file.write(str(len(chains)) + "\n")

    # The number of stes per chain
    gpu_file.write(str(feature_table.ste_count_) + "\n")

    # The ste at which the loop starts
    gpu_file.write(str(feature_table.start_loop_) + "\n")

    # The number of features per sample
    gpu_file.write(str(len(feature_table.features_)) + "\n")

    # Iterate through all chains
    for chain in chains:

        # For quickrank
        if value_map is not None:

            # Look up the index assigned ot the value
            report_code = value_map[chain.value_]

        else:

            # 1 offset needed because the AP can't handle '0' report codes
            report_code = chain.value_ + 1

        chain_id = "%dt_%dl_%dr" %\
            (chain.tree_id_, chain.chain_id_, report_code)

        gpu_file.write(str(chain_id) + '\n')

        # character class assignments for STEs start with '[' and end with ']'
        character_classes = ['[' for _ste in range(feature_table.ste_count_)]

        next_node_index = 0

        # Iterate through all features in the feature_table
        for _f in feature_table.features_:

            # If we're still pointing to a valid node ...
            if next_node_index < len(chain.nodes_):

                # Grab that next node
                next_node = chain.nodes_[next_node_index]

                # If that node has the feature we're looking at...
                if next_node.feature_ == _f:

                    # If we have multiple STEs assigned to this feature...
                    ste_index = 0

                    for _ste, _start, _end in feature_table.get_ranges(_f):

                        for c in next_node.character_sets[ste_index]:

                            character_classes[_ste] += r"\x%02X" % c

                    next_node_index += 1

                # If the node does not have the feature we're looking for
                else:

                    for _ste, _start, _end in feature_table.get_ranges(_f):

                        # Feature is not part of chain, accept full range
                        character_classes[_ste] += r"\x%02X-\x%02X" %\
                            (_start, _end - 1)

            # We're done with the available features in our chain
            else:

                for _ste, _start, _end in feature_table.get_ranges(_f):

                    # Because feature not part of chain, accept full range
                    character_classes[_ste] += r"\x%02X-\x%02X" %\
                        (_start, _end - 1)

        # End character classes with ']'
        for i in range(len(character_classes)):
            character_classes[i] += "]"

        for character_class in character_classes:
            gpu_file.write(character_class + '\n')

    gpu_file.close()
