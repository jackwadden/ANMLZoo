'''
    The purpose of this module is to set character sets.

    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    19 October 2017
    Version 1.0
'''

# Set the character sets of each node in the chains
def set_character_sets(chain, ft):

    # Iterate through all nodes
    for node in chain.nodes_:

        # Build character set list for this node
        # one character set per STE assigned to node
        character_sets = []

        # Grab STE labels associated with feature; make a copy
        # [(ste, start, end)]
        ranges = list(ft.get_ranges(node.feature_))

        # Haven't found our 'range' yet
        found = False

        # If this STE accepts <= the threshold
        if not node.gt_:

            # Go through each STE from the smallest to largest features
            for ste, start, end in ranges:

                # Each STE assigned to this feature needs its own character set
                character_set = []

                # Grab labels assigned to range for this feature in this STE
                labels = range(start, end)

                # Also grab the thresholds assigned to the feature at this ste
                thresholds = ft.stes_[ste][start:end]

                assert len(labels) == len(thresholds),\
                    "Zipping labels and thresholds is gonna fail :("

                # If range was discovered in a previous bin, -2
                if found:

                    # Only accept '-2' flag; not in any ranges (for this STE))
                    character_set.append(labels[-1])

                    assert thresholds[-1] == -2,\
                        "The last label for this bin is not -2, it's %d" %\
                        (labels[-1])
                    assert character_set == [labels[-1]]

                else:

                    # Go from  first (smallest) to the last (largest) label
                    for label, threshold_limit in zip(labels, thresholds):

                        # We accept this label, because its <= threshold
                        if threshold_limit < node.threshold_:
                            character_set.append(label)

                        # We accept this label, and we're done
                        elif threshold_limit == node.threshold_:
                            character_set.append(label)
                            found = True
                            break

                        # We should never have made it here!
                        else:
                            print "We should not be here!"
                            exit()

                # Append the character set for this ste
                character_sets.append(character_set)

        # If this STE accepts >
        else:

            # Invert the ranges, to start from the largest features
            # Means we'll need to reverse our character sets at the end
            ranges.reverse()

            # Go through each STE from the larges to the smallest feature
            for ste, start, end in ranges:

                character_set = []

                # Reversed labels
                labels = range(end - 1, start - 1, -1)

                # We're going throught the thresholds from back to front
                thresholds = ft.stes_[ste][start:end]
                thresholds.reverse()

                # print "> Threshold: ", node.threshold_
                # print "Thresholds: ", thresholds
                # print "Labels: ", labels

                assert len(labels) == len(thresholds),\
                    "Zipping labels and thresholds is gonna fail :("

                # If range was discovered in a previous bin, -2
                if found:

                    # We'll only accept the '-2' flag
                    character_set.append(labels[0])

                    assert thresholds[0] == -2,\
                        "The last label for this bin is not -2"

                else:

                    # Go from last (largest) to first (smallest) label
                    for label, threshold_limit in zip(labels, thresholds):

                        # Expect -2 before outside of our range; ignore it
                        if threshold_limit == -2:
                            continue

                        # -1 will always be accepts (for >)
                        elif threshold_limit == -1:
                            character_set.append(label)

                        # If our threshold > threshold_limit, we'll accept
                        elif threshold_limit > node.threshold_:
                            character_set.append(label)

                        # Don't accept and break
                        elif threshold_limit == node.threshold_:
                            found = True
                            break

                        else:
                            print "We shouldn't be here"
                            exit()

                # Append the character set for this ste
                character_sets.append(character_set)

            character_sets.reverse()

        assert len(ft.feature_pointer_[node.feature_]) == len(character_sets),\
            "character sets aren't the right length"

        for c_s in character_sets:
            c_s.sort()

        # Set the node's character sets
        node.set_character_sets(character_sets)
