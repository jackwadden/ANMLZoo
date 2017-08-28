'''
    This module is intended for utilities purposes
    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    12 June 2017
    Version 0.2
'''

import math
from heapq import *
import logging

logging.basicConfig(format='%(asctime)s : %(message)s', level=logging.INFO)

# Get valid ordering of features
# this is the order in which the input is streamed
def getordering(ft):

    # Keep track of the features assigned to each STE
    stes = [[] for x in xrange(ft.ste_count_)]

    # Let's figure out which bins the features are assigned to
    for _f in ft.features_:

        for _i in ft.get_stes(_f):

            stes[_i].append(_f)

    print "STES: ", stes

    '''
        Some Comments

        A loop is a series of contiguous STEs that are connected in a cycle,
        where the end of the series is connected to the start of the
        series; this allows for combining multiple features into fewer STEs
        by temporally representing them (in space and time).
    '''

    # This is the permutation of features
    permutation = []

    if ft.unrolled:

        for _i in range(0, ft.ste_count_):

            assert len(stes[_i]) == 1, "Bad assumption about size of STE allocation"

            permutation.append(stes[_i].pop())


    else:
        print "Start loop: ", 0, ft.start_loop_

        # All STEs with a single feature (not part of the loop)
        for _i in range(0, ft.start_loop_):

            print "Size of ste ", _i, ": ", len(stes[_i])

            assert len(stes[_i]) == 1,\
                "Bad assumption about size of STE allocations"

            permutation.append(stes[_i].pop())

        index = ft.start_loop_

        while len(stes[index]) > 0:
            permutation.append(stes[index].pop(0))

            if index == len(stes) - 1:

                index = ft.start_loop_

            else:

                index += 1

    for ste in stes:

        assert len(ste) == 0, "Permutation generator failed"

    # Return the permutation
    return permutation


'''
    Combine the feature address spaces to best utilize STEs
    
        threshold_map contains mapping from feature index to thresholds
'''

def compact(threshold_map, priority='runtime', unrolled=False, verbose=True):

    if verbose:
        logging.info("Running compact() on %d unique features; each with min=%d to max=%d unique threshold counts" %
                     (len(threshold_map.keys()),
                     min([len(thresholds) for _,thresholds in threshold_map.iteritems()]),
                     max([len(thresholds) for _,thresholds in threshold_map.iteritems()])))

    # Set maximum bin size (in the case of an STE its 2^8 - 1)
    # [0 - 254] are allowed (which counts the extra -1)
    # [0-253] are for thresholds [254] is for the -1
    # [255] is meant for the escape character (0xff)
    BINSIZE = 254

    # STEs with full addressing
    stes = []

    # Keep track of the [[ste, start, end]] of each feature for quick lookups
    feature_pointer = {}

    # Make (feature, len(thresholds)) tuples to be ordered by len(thresholds)
    # Sort tuples (feature, threshold_count)
    #   by threshold_count from largest -> smallest
    threshold_counts = [(f, len(thresholds)) for
                        f, thresholds in threshold_map.iteritems()]

    # Sorted tuples of (feature, number of thresholds) from most to least
    threshold_counts.sort(key=lambda x: x[1], reverse=True)

    if verbose:
        logging.info("Maximum Binsize set to %d thresholds" % BINSIZE)
        logging.info("Initialized stes[] and feature_pointer{}")
        logging.info("Created sorted threshold_counts containing (feature, len(thresholds))")

    # This function grabs all 'large' features that take
    # one full STE or more, updating the threshold_counts by
    # removing those features and stes variable with the address table

    if unrolled:
        logging.info("Attempting to pack all features into their own (1 or more) bins")
    else:
        if verbose:
            logging.info("Attempting to pack 'large' features into 1 or more bins")

    # Grab the big features
    stes, feature_pointer, threshold_counts = big_features(stes, feature_pointer, threshold_map, threshold_counts,
                BINSIZE, verbose, unrolled=unrolled)

    print "STEs post big_features"
    for ste in stes:
        print ste

    # This means we have remaining small features
    if len(threshold_counts) > 0:

        assert not unrolled, "It appears that something went wrong with generating long chains";

        if verbose:
            logging.info("We still have %d features left to put into bins: \n%s" %
                         (len(threshold_counts), str([(_f, _t) for
                          _f, _t in threshold_counts])))

        start_loop, end_loop = small_features(stes, feature_pointer,
                                             threshold_map, threshold_counts,
                                             BINSIZE, verbose,
                                             priority=priority)

    # Verification to make sure resulting feature pointer and stes are right
    verification(threshold_map, feature_pointer, stes, verbose)

    return feature_pointer, stes, start_loop, end_loop


'''
    The purpose of this function is to strip out the features
    that require one or more full STEs
'''


def big_features(stes, feature_pointer, threshold_map, threshold_counts,
                 BINSIZE, verbose, unrolled=False):

    # As we assign big features to STEs, we need to keep track to remove them
    counts_to_remove = []

    # Start from largest feature threshold count to smallest
    for _f, _t in threshold_counts:

        if unrolled and _t <= BINSIZE:

            if verbose:
                logging.info("UNROLLING: Found feature %d to fit in exactly one bin!" % _f)

            counts_to_remove.append((_f, _t))

            stes, feature_pointer = update_stes(stes, feature_pointer, threshold_map, [_f])

        # If the feature is an exact fit, shove it in
        elif _t == BINSIZE:

            if verbose:
                logging.info("Found feature %d to use exactly one bin!" % _f)

            counts_to_remove.append((_f, _t))

            stes, feature_pointer = update_stes(stes, feature_pointer, threshold_map,
                        [_f])

        # If this is a LARGE feature (many thresholds), split 'er up
        # For the time being, assign each of these sub-thresholds to
        # its own STE ( *This is not ideal )
        elif _t > BINSIZE:

            if verbose:
                logging.info("Found feature %d to have %d thresholds! (>=BINSIZE))" % (_f, _t))

            # We're going to have to remove this feature from the list
            counts_to_remove.append((_f, _t))

            # New list of STEs for the feature
            feature_pointer[_f] = []

            # Index into threshold_map
            i = 0

            while _t > BINSIZE:

                sub_thresholds = threshold_map[_f][i:i + BINSIZE]

                # If, however, the feature is bigger, we're going to need one
                # 'don't care' per STE; only one STE will have the range
                sub_thresholds.append(-2)

                # Assign the full STE address space to the feature
                ste = len(stes)
                start = 0
                end = len(sub_thresholds)

                # Make sure we did this right
                assert end <= BINSIZE + 1,\
                    "Start:%d, End:%d, |STE| > %d!" % (start, end, BINSIZE)
                assert sub_thresholds[-1] == -2,\
                    "The end of the sub_threshold is not -2!"

                # Update feature_pointer to include STE and start,end addresses
                feature_pointer[_f].append((ste, start, end))

                assert len(sub_thresholds) > 0

                stes.append(sub_thresholds)

                # Update pointers
                i += BINSIZE
                _t -= BINSIZE

            # If we have exactly BINSIZE thresholds left to pack...
            if _t == BINSIZE:

                # Awkward; we're only going to fit BINSIZE - 1 into next bin
                sub_thresholds = threshold_map[_f][i:(i + BINSIZE - 1)]
                sub_thresholds.append(-2)

                ste = len(stes)
                start = 0
                end = len(sub_thresholds)

                # Sanity check
                assert end <= BINSIZE + 1,\
                    "Start:%d, End:%d, |STE| > %d!" % (start, end, BINSIZE)

                feature_pointer[_f].append((ste, start, end))

                assert len(sub_thresholds) > 0

                stes.append(sub_thresholds)

                # Update pointers
                i += (BINSIZE - 1)
                _t -= (BINSIZE - 1)

            # If there's anything left,...
            if _t > 0:

                # We have less than BINSIZE thresholds left, so pack em up!
                sub_thresholds = threshold_map[_f][i:]
                sub_thresholds.append(-1)
                sub_thresholds.append(-2)

                ste = len(stes)
                start = 0
                end = len(sub_thresholds)

                # Last sanity check
                assert end <= BINSIZE + 1,\
                    "Start:%d, End:%d, |STE| > %d!" % (start, end, BINSIZE)

                feature_pointer[_f].append((ste, start, end))

                assert len(sub_thresholds) > 0

                stes.append(sub_thresholds)

        # Break; we're now working with the 'smaller features'
        else:
            break

    if verbose:
        logging.info("Found %d features that take 1 or more full bins" %
                     len(counts_to_remove))

    for removable in counts_to_remove:
        threshold_counts.remove(removable)

    if verbose:
        if len(counts_to_remove) > 0:
            logging.info("Resulting feature pointer: \n\n%s\n" %
                         str(feature_pointer))
            logging.info("Resulting bin address spacing (%d bins): \n\n%s\n" %
                         (len(stes), str(stes)))

    return (stes, feature_pointer, threshold_counts)

'''
    Pack the thresholds into STEs
'''

def pack(threshold_counts, ste_count, verbose):

    # Use a min heap to keep track of bins and always add the next
    # largest to the smallest available bin...
    heap = []

    if verbose:
        logging.info("Initializing %d empty bin(s) to be filled" %
                     ste_count)

    # Add <ste_count> empty 'bins' to our priority queue
    for i in range(ste_count):
        heappush(heap, (0, []))

    if verbose:
        logging.info("Filling bins by putting largest available item in \
                     most empty bin")

    # Iterate through all features in threshold_counts, and update bins
    # We're updating the bins such that the emptiest is filled first (with thresholds)
    for _f, _t in threshold_counts:

        # Pull off the most empty bin (the top of the heap)
        size, features = heappop(heap)

        # Add the next largest feature
        features.append(_f)
        size += (_t + 1) # Add the number of thresholds + the needed -1 label
        heappush(heap, (size, features))

    feature_list = []
    sizes = []

    # Now let's pop off the bins
    for i in range(ste_count):

        # Returns (size, features)
        size, features = heappop(heap)
        features.sort() # Sort the features by index (not strictly necessary)
        feature_list.append(features)   # Add our list of features for the given STE to our list
        sizes.append(size)  # Have a list of sizes

        if verbose:
            logging.info("STE %d stats: size=%d, %d features=%s" %
                         (i, size, len(features), str(features)))

    single_ste_features = []

    # This is kind of a neat idea; if some features
    # require a full STE with our best packing
    # strategy, remove them and try packing again!
    for _f in feature_list:

        print _f, len(_f)
        # Check if one of the STEs only has a single feature in it
        if len(_f) == 1:

            # Remove it from the feature_list and from the list of sizes
            single_ste_features.append(_f)

            assert _f in feature_list

            # Grab the index of the feature to be removed
            f_index = feature_list.index(_f)

            print "Feature to remove: ", _f
            print "From feature_list: ", feature_list[f_index]

            print (feature_list[f_index][0], sizes[f_index]-1)

            # ... also remove this feature from the threshold_counts
            assert (feature_list[f_index][0], sizes[f_index]-1) in threshold_counts

            # Remove from threshold counts
            threshold_counts.remove((feature_list[f_index][0], sizes[f_index]-1))

            # Remove the feature from the feature list
            feature_list.pop(f_index)

            # .. and the relevant size from the size list
            sizes.pop(f_index)


            assert len(feature_list) == len(sizes)

        assert len(_f) > 0

    print "--------------------Pack-----------------"
    print "Feature List: ", feature_list
    print "Sizes: ", sizes
    print "Single STE Features: ", single_ste_features
    print "-------------------------------------------"

    return feature_list, sizes, single_ste_features


'''
    The goal is to cram the remaining thresholds into as few bins as possible
    Such that there are an equal number of features per bin
    and that the address space is efficiently used.
        priority={'runtime', 'capacity'}
'''


def small_features(stes, feature_pointer, threshold_map, threshold_counts,
                   BINSIZE, verbose, priority='runtime'):

    # In the future we will support 'runtime' and 'capacity' optimization
    if priority != 'runtime':
        print "Sorry, but we only have 'runtime' support at this time"
        q = input("Continue binpacking with priority set to runtime?: y/n")
        if q != 'y' and q != 'Y':
            print "Quiting prematurely"
            exit()

    # We'll start at the minimum possible number of STEs that could work out
    min_ste_count = int(math.ceil(float(reduce(lambda x, y: x + y, [x[1] for
                                           x in threshold_counts])) / float(BINSIZE)))

    assert min_ste_count > 0

    if verbose:
        logging.info("Found that %d is the min number of STEs to fit all remaining features" % min_ste_count)

    iteration_counter = 0
    ste_count = min_ste_count

    # Iterate through all of the threshold tuples
    while True:

        if verbose:
            logging.info("Iteration %d: attempting %d bins with %d features" %
                         (iteration_counter, ste_count, len(threshold_counts)))

        iteration_counter += 1

        feature_list, sizes, single_ste_features = pack(threshold_counts, ste_count, verbose)

        # This is kind of a neat idea; if some features
        # require a full STE with our best packing
        # strategy, remove them and try packing again!
        for _f in single_ste_features:

            if verbose:
                logging.info("Found feature %d needed a full bin!" % _f[0])

            # New list of STEs for the feature
            stes, feature_pointer = update_stes(stes, feature_pointer, threshold_map,
                        _f)

            # Because we removed a full-STE feature, reduce the STE count
            ste_count -= 1

        # Verify that there are no single-feature STEs left (should have been removed by pack
        for _f in feature_list:
            print _f, len(_f)
            assert len(_f) > 1
            assert len(feature_list) == len(sizes)

        # We're done
        if len(feature_list) == 0:

            if verbose:
                logging.info("All features required one bin each; \
                             we're done here")
            return (None, None)

        # If the most full STE is not over-full...
        if max(sizes) <= BINSIZE:

            if verbose:
                logging.info("Binsize: %d" % BINSIZE)
                logging.info("We managed to fit all features into %d bins" %
                             ste_count)

            num_features_per_ste = [len(x) for x in feature_list]

            print "Sizes: ", sizes
            print "num_features_per_ste: ", num_features_per_ste

            if verbose:
                logging.info("Checking to see if the bins are balanced")

            # If imbalanced by the number of features assigned to the STEs...
            if max(num_features_per_ste) - min(num_features_per_ste) > 1:

                if verbose:
                    logging.info("The bins are not balanced! (min=%d,max=%d) features in a bin" % (min(num_features_per_ste), max(num_features_per_ste)))

                if balance(feature_list, sizes, threshold_map,
                           threshold_counts, BINSIZE, verbose):

                    feature_list.sort(key=lambda x: len(x), reverse=True)

                    start_loop = len(stes)
                    end_loop = None

                    for _f in feature_list:
                        if len(_f) < len(feature_list[0]) and end_loop is None:
                            end_loop = len(stes)

                        stes, feature_pointer = update_stes(stes, feature_pointer, threshold_map,_f)

                    if end_loop is None:
                        end_loop = len(stes) - 1

                    return (start_loop, end_loop)

                else:
                    # Try with another STE
                    ste_count += 1
                    logging.info("Balancing failed :/; incremeneting ste_count to: " + str(ste_count))

            else:

                if verbose:
                    logging.info("The bins are balanced; we're done here")
                    logging.info("The largest STE is: %d" % max(num_features_per_ste))
                    logging.info("The smallest STE is: %d" % min(num_features_per_ste))

                feature_list.sort(key=lambda x: len(x), reverse=True)

                # We're going to start the loop
                start_loop = len(stes)
                end_loop = None

                for _f in feature_list:

                    # If current feature has fewer features than previous,
                    # last STE must serve as the end of the loop
                    if len(_f) < len(feature_list[0]) and end_loop is None:
                        end_loop = len(stes) - 1

                    stes, feature_pointer = update_stes(stes, feature_pointer, threshold_map,
                                _f)

                if end_loop is None:
                    end_loop = len(stes) - 1

                return (start_loop, end_loop)

        else:

            if verbose:
                logging.info("Couldn't fit them in %d bins" % ste_count)
                logging.info("One STE is too full with %d thresholds!" % max(sizes))

            # Continue to increment the STE counter
            ste_count += 1

# Try to balance the STEs so that there are an equal number of features
# per STE (+/- 1)


def balance(feature_list, sizes, threshold_map, threshold_counts,
            BINSIZE, verbose):

    if verbose:
        logging.info("Unbalanced feature list: %s" % str(feature_list))
        logging.info("Min features in an STE: %d" % min([len(x) for x in feature_list]))
        logging.info("Max features in an STE: %d" % max([len(x) for x in feature_list]))

    # Find the min number of features in any of the STEs
    min_features = min([len(x) for x in feature_list])

    # Use a min heap to keep track of bins and always add the next
    # largest to the smallest available bin...
    current_heap = []
    next_heap = []

    # The list of extra features that we will distribute among the STEs
    extra_features = []

    # Iterate through the current STE feature assignments
    for i, ste in enumerate(feature_list):

        num_features = len(ste)

        if verbose:
            print("We're going to remove %d features from ste %d" %
                  ((num_features - min_features), i))

        # Remove the extra features from each STE
        for _ in range(num_features - min_features):

            # We know the features at the end of the ste are the smallest
            feature_to_be_removed = ste.pop()
            extra_features.append(feature_to_be_removed)

            # Update the size of the current STE
            sizes[i] -= (len(threshold_map[feature_to_be_removed]) + 1)

        # Once extra features removed, push updated STEs to the heap
        heappush(current_heap, (sizes[i], ste))


    # These should stay ordered; we're simply filtering the ones we care about
    extra_threshold_counts = [x for x in threshold_counts if
                              x[0] in extra_features]

    # Iterate through all extra features and add them to the STEs
    for _f, _t in extra_threshold_counts:

        # Our heap is empty; time to refill
        if not current_heap:

            # Swap the empty heap with the one with stuff in it
            temp = next_heap
            next_heap = current_heap
            current_heap = temp

        # Pull off the most empty bin
        size, features = heappop(current_heap)

        # Add the next largest feature
        features.append(_f)
        size += (_t + 1)

        # If we bust the size limit, we're done here. oh well
        if size > BINSIZE:
            logging.info("Size (" + str(size) + ") > BINSIZE (" + str(BINSIZE) + ") this doesn't work. Try again")
            return False

        heappush(next_heap, (size, features))

    if verbose:
        logging.info("Balanced feature list: %s" % str(feature_list))

    print "next_heap: ", next_heap
    print "current_heap: ", current_heap

    temp_features = []
    temp_sizes = []
    temp_ = []
    while next_heap:
        size, features = heappop(next_heap)
        temp_.append(features)
        temp_sizes.append(size)

    print "next_heap: ", next_heap
    print "current_heap: ", current_heap

    while current_heap:
        size, features = heappop(current_heap)
        temp_.append(features)
        temp_sizes.append(size)

    print "Temp: ", temp_
    print "Temp Sizes: ", temp_sizes

    # If we got here without issues, we balanced!
    print "Current Heap: "
    for size, features in current_heap:
        print size, features, len(features)
    print "Next Heap:"
    for size, features in next_heap:
        print size, features, len(features)

    return True


'''
    This function updates stes and feature_pointer variables
    to include the ste assignments made in the features list
'''


def update_stes(stes, feature_pointer, threshold_map, features):

    # Let us use the next STE
    ste = len(stes)

    # Start a new address map for the current feature
    sub_thresholds = []

    # Iterate through all of the features assigned to this STE
    for feature in features:

        # This current feature starts at the next available spot
        start = len(sub_thresholds)

        # Update the address map and end it with a -1
        sub_thresholds.extend(threshold_map[feature][0:])
        sub_thresholds.append(-1)

        # It ends at the end of the map
        end = len(sub_thresholds)

        # So now we know where this feature belongs
        feature_pointer[feature] = [(ste, start, end)]

    assert len(sub_thresholds) > 0
    assert len(sub_thresholds) < 255

    stes.append(sub_thresholds)

    return (stes, feature_pointer)


def verification(threshold_map, feature_pointer, stes, verbose):

    if verbose:
        logging.info("Time to run sanity check on the stes address allocation")

    for f, thresholds in threshold_map.iteritems():

        combined_thresholds = []

        bins = feature_pointer[f]

        if len(bins) == 1:
            ste_index = bins[0][0]
            start = bins[0][1]
            end = bins[0][2]
            combined_thresholds = stes[ste_index][start:(end - 1)]

            assert combined_thresholds == thresholds, \
                "\nCombined Thresholds: %s\n Threshold Map: %s\n" %\
                (str(combined_thresholds), str(thresholds))

        # If this feature is mapped to multiple bins...
        else:
            for i, b in enumerate(bins):
                ste_index = b[0]
                start = b[1]
                end = b[2]

                if i == len(bins) - 1:
                    # For the last STE, the last two labels assigned are -1, -2
                    combined_thresholds.extend(
                        stes[ste_index][start:(end - 2)])
                else:
                    # For all other STEs, the last label is assigned -1
                    combined_thresholds.extend(
                        stes[ste_index][start:(end - 1)])

            assert combined_thresholds == thresholds, \
                "\nCombined Thresholds: %s\n Threshold Map: %s\n" %\
                (str(combined_thresholds), str(thresholds))

    if verbose:
        logging.info("Time to run a sanity check on feature_pointer")

    # Verify that the results make sense
    for f, thresholds in threshold_map.iteritems():

        # Make sure we have the feature in feature_pointer
        assert f in feature_pointer.keys()

        total_address_space = 0

        bins = feature_pointer[f]

        if len(bins) == 1:
            bin_0 = bins[0]
            start_0 = bin_0[1]
            end_0 = bin_0[2]

            total_address_space = (end_0 - start_0 - 1)

            assert len(thresholds) == total_address_space, \
                "|Thresholds|=%d, |total address space|=%d" %\
                (len(thresholds), total_address_space)
        else:
            for i, b in enumerate(bins):

                if i == (len(bins) - 1):
                    total_address_space += (b[2] - b[1] - 2)
                else:
                    total_address_space += (b[2] - b[1] - 1)

            assert len(thresholds) == total_address_space, \
                "|Thresholds|=%d, |total address space|=%d \n%s\n%s" %\
                (len(thresholds), total_address_space, len(thresholds), bins)
    if verbose:
        logging.info("Feature Pointer looks right!")
        logging.info("All Sanity Checks Passed")

    return True
