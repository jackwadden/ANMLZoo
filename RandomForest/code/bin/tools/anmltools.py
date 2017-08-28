'''
    This module is meant for interfacing with the ANML API

    This module contains two functions:
    1. generate_anmL(): Generate ANML from the chains

    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    12 June 2017
    Version 0.2
'''
from classes.Anml import *


# Generate ANML code for the provided chains
def generate_anml(chains, feature_table, value_map, anml_filename,
                  reverse_value_map=None, unrolled=False):

    anml_net = Anml()

    # This code is used to start and report
    report_symbol = r"[\x%02X]" % 255

    # Iterate through all chains
    for chain in chains:

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

        # stes for the current chain
        stes = []

        # Start the chain with an id that ends in _s (for start)
        ste_id = "%dt_%dl_s" % (chain.tree_id_, chain.chain_id_)

        # Have a start ste that matches on 255
        start_ste = anml_net.AddSTE(report_symbol, AnmlDefs.ALL_INPUT,
                                    anmlId=ste_id, match=False)

        # stes[0] is the start ste that only accepts \xff = 255 in base 10
        stes.append(start_ste)

        # Now go through each of the remaining STEs
        for ste_i in range(feature_table.ste_count_):

            # Give them identifiers based on tree id, chain id, and ste id
            ste_id = "%dt_%dl_%d" % (chain.tree_id_, chain.chain_id_, ste_i)

            # Add to the list
            ste = anml_net.AddSTE(character_classes[ste_i], AnmlDefs.NO_START,
                                  anmlId=ste_id, match=False)

            # Connect them forward (this is where the loop is made)
            anml_net.AddAnmlEdge(stes[-1], ste, 0)

            stes.append(ste)

        # If we are looping
        if not unrolled:
            # Our cycle; mapping from end of the chain to the start of the loop
            anml_net.AddAnmlEdge(stes[-1], stes[feature_table.start_loop_ + 1], 0)

        # For quickrank
        if value_map is not None:

            # Look up the index assigned ot the value
            report_code = value_map[chain.value_]

            # Reporting STE ID
            ste_id = "%dt_%dl_%dr" %\
                (chain.tree_id_, chain.chain_id_, report_code)

        else:

            # 1 offset needed because the AP can't handle '0' report codes
            report_code = chain.value_ + 1

            # Reporting STE ID
            ste_id = "%dt_%dl_%dr" %\
                (chain.tree_id_, chain.chain_id_, report_code)

        ste = anml_net.AddSTE(report_symbol, AnmlDefs.NO_START,
                              anmlId=ste_id, reportCode=report_code)

        # If we're doing chains, we know the last ste will go to the reporting state
        if unrolled:
            anml_net.AddAnmlEdge(stes[-1], ste, 0)
        else:
            # Need to add 1 to the index, because the first STE is the starting STE
            anml_net.AddAnmlEdge(stes[feature_table.end_loop_ + 1], ste, 0)

        del stes

    anml_net.ExportAnml(anml_filename)
