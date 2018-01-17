'''
    This objected-oriented module defines a Feature Lookup Table class

    This lookup table has three main purposes:
    1. We use the address spaces to efficiently fit all features into
        as few STEs as possible.
    2. We use the resulting lookup table to map feature values to feature
        labels.
    3. We use the lookup table to generate input files for the AP.
    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    12 June 2017
    Version 0.2
'''

# Utility imports
from termcolor import colored
from random import *
from array import *
import tools.util as util
from collections import OrderedDict

# Define FeatureTable class
class FeatureTable(object):

    # Constructor creates one contiguous feature address space
    def __init__(self, threshold_map, unrolled=False, verbose=True):

        # set unrolled for the feature table
        self.unrolled = unrolled

        ordered_threshold_map = OrderedDict(sorted(threshold_map.items(),
                                                   key=lambda x: int(x[0])))

        self.features_ = ordered_threshold_map.keys()

        # A dictionary from features -> list of thresholds
        self.threshold_map_ = ordered_threshold_map

        # Find the minimum number of stes required to handle the features
        feature_pointer, stes, start_loop, end_loop =\
            util.compact(self.threshold_map_, unrolled=self.unrolled, verbose=True)

        # Assign feature_pointer and stes
        # feature -> [(STE, start, end)]
        self.feature_pointer_ = feature_pointer

        # List of address spaces by STE
        self.stes_ = stes

        # Set the number of stes
        self.ste_count_ = len(stes)

        self.start_loop_ = start_loop
        self.end_loop_ = end_loop

        # print "Start, End: ", self.start_loop_, self.end_loop_
        # print(self)

        # Get loopy information (permutation of features)
        self.permutation_ = util.getordering(self)

    # String representation of the STEs
    def __str__(self):
        string = "STE Count: %d\n" % self.ste_count_

        # Enumerate all features and which STE its mapped to / what range
        for i, feature in enumerate(self.features_):
            string += colored("F:%d", 'magenta') % feature

            for ste, start, end in self.feature_pointer_[feature]:

                string += "STE:%d,S:%d,E:%d" % (ste, start, end)
                string += (";") if i != (len(self.features_) - 1) else ("\n\n")

        # Enumerate all stes
        for i, ste in enumerate(self.stes_):
            string += colored("STE:%d", 'blue') % i
            string += "["

            # Enumerate all ranges
            for j, r in enumerate(ste):
                string += (colored(str(r), 'green') if r != -1 else
                           colored(str(r), 'red'))
                string += "]"
                string += ("[") if j != len(ste) - 1 else "]"

        return string

    # Return ranges in address space that corresponds to start/end of feature
    def get_ranges(self, feature):

        return self.feature_pointer_[feature]

    # Return the STEs that this feature is mapped to
    def get_stes(self, feature):

        return [ste for ste, start, end in self.get_ranges(feature)]

    # Ret tuples [(ste, index)] that represent ranges where value is found
    # This is currently implemented with a linear-time algorithm, but can be
    # improved in the future
    def get_symbols(self, feature, value):

        # This gives us stes and pointers into stes
        ranges = self.get_ranges(feature)
        found_symbol = False
        return_list = []

        # Go from start to the end of the ste and check for a matching range
        for ste, start, end in ranges:

            labels = range(start, end)
            thresholds = self.stes_[ste][start:end]

            assert len(labels) == len(thresholds),\
                "Zipping labels and thresholds is gonna fail :("

            # If we've already found our range.. tack on a -2
            if found_symbol:

                return_list.append((ste, end - 1))

                assert thresholds[-1] == -2

            else:

                for label, threshold_limit in zip(labels, thresholds):

                    # We haven't found our range yet
                    if threshold_limit == -2:
                        return_list.append((ste, label))

                    elif threshold_limit == -1:

                        found_symbol = True
                        return_list.append((ste, label))
                        break

                    elif threshold_limit == value:

                        return_list.append((ste, label))
                        found_symbol = True
                        break

                    elif threshold_limit < value:
                        continue

                    elif threshold_limit > value:
                        return_list.append((ste, label))
                        found_symbol = True
                        break

        # Make sure that we return one symbol per STE assigned to feature
        assert len(return_list) == len(ranges)

        return return_list

    # This function generates an input file from an input X
    def input_file(self, X, filename, onebased=False,
                   short=False, delimited=True):

        if short:
            X = X[:10]

        print "Writing %d samples to input file" % X.shape[0]

        if delimited:
            print "Delimited"
        else:
            print "Not Delimited"

        num_bytes_per_class = 0

        # Open up the output file
        with open(filename, 'wb') as f:

            inputstring = array('B')

            if delimited:
                inputstring.append(255)

            print "%d features in each row of X" % len(X[0])
            print "%d unique features in this permutation" %\
                len(set(self.permutation_))
            print "%d cycles per classification" % len(self.permutation_)
            # For each input row...
            for row in X:

                # Use feature indexes as added to feature_pointer ordered dict
                for f_i in self.permutation_:

                    # Get the corresponding feature value
                    if onebased:
                        f_v = row[f_i - 1]
                    else:
                        f_v = row[f_i]

                    for ste, symbol in self.get_symbols(f_i, f_v):

                        inputstring.append(symbol)
                        num_bytes_per_class += 1

                # We always finish each feature with a 255 (if delimited)
                if delimited:
                    inputstring.append(255)

                num_bytes_per_class = 0

            f.write(inputstring.tostring())

        # Return the number of bytes written to the input file
        return len(inputstring.tostring())
