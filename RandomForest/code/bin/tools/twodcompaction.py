'''
    This module is intended for 2d compaction
    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    18 December 2017
    Version 0.2
'''

# Imports
import logging

logging.basicConfig(format='%(asctime)s : %(message)s', level=logging.INFO)


'''
    Combine the feature address spaces to best utilize STEs

        threshold_map contains mapping from feature index to thresholds
'''

def twodcompact(threshold_map, priority='runtime', unrolled=False, verbose=True):

    if verbose:
        logging.info("Running 2d-compact() on %d unique features; each with min=%d to max=%d unique threshold counts" %
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

    else:
        start_loop, end_loop = None, None

    # Verification to make sure resulting feature pointer and stes are right
    verification(threshold_map, feature_pointer, stes, verbose)

    return feature_pointer, stes, start_loop, end_loop
