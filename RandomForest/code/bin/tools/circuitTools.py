'''
    This module is meant for circuit implementations of the RF

    This module contains one function:
    1. generate_circuits(): Generate circuits from the chains
    2. export_circuit(): Write the circuits out to a file
    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    13 November 2017
    Version 0.2
'''

# Write the circuit out to a file
def export_circuit(filename, circuit, feature_table):

    with open(filename, 'w') as f:

        # Write Header
        f.write('# Feature_i -> \tthresholds\n')
        for _f in feature_table.permutation_:
            f.write("# "+str(_f)+" (" + str(len(feature_table.threshold_map_[_f])) + ") -> \t")
            for _t in feature_table.threshold_map_[_f]:
                f.write(str(_t)+",")
            f.write("\n")
        f.write("#----------\n")
        f.write("# chain id\n")
        f.write("# [state_0-state_n labels]\n")
        f.write("# result value\n")
        f.write("#----------\n")

        for i, line in enumerate(circuit):
            if i%3 == 0:
                f.write("\n")
            f.write(str(line)+'\n')

    return None

# Generate circuit file from the chains
def generate_circuits(chains, feature_table, value_map, filename,
                      reverse_value_map=None, unrolled=False):

    circuit = []

    for chain in chains:

        circuit.append(chain.chain_id_)

        character_classes = ["" for _ste in range(feature_table.ste_count_)]
        next_node_index = 0

        for _f in feature_table.features_:

            if next_node_index < len(chain.nodes_):

                next_node = chain.nodes_[next_node_index]

                if next_node.feature_ == _f:

                    ste_index = 0

                    for _ste, _start, _end in feature_table.get_ranges(_f):

                        temp_set = next_node.character_sets[ste_index]

                        if len(temp_set) > 1:
                            character_classes[_ste] += r"%s-%s" % \
                                                    (str(min(temp_set)), str(max(temp_set)))
                        else:
                            character_classes[_ste] += "%s" % temp_set[0]

                        ste_index += 1

                    next_node_index += 1

                else:

                    for _ste, _start, _end in feature_table.get_ranges(_f):

                        # Feature is not part of chain, accept full range
                        character_classes[_ste] += r"%s-%s" %\
                            (_start, _end - 1)

            # We're done with the available features in our chain
            else:

                for _ste, _start, _end in feature_table.get_ranges(_f):

                    # Because feature not part of chain, accept full range
                    character_classes[_ste] += "%s-%s" %\
                        (_start, _end - 1)

        circuit.append(character_classes)
        circuit.append(chain.value_)

    export_circuit(filename, circuit, feature_table)

    return circuit