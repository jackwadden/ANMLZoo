'''
    The purpose of this program is to extract the X feature vector and y
    results from MSLR data.
    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    12 November 2016
    Version 1.0
'''

import sys, json
from optparse import OptionParser
import numpy as np
import logging

# Turn on logging.
logging.basicConfig(format='%(asctime)s : %(message)s', level=logging.INFO)

# Read the MSLR file and stack X and y
def readmslr(filename):

    # Populate lists and then convert to NUMPY arrays; faster then stacking
    y = []
    X = []

    # This assumes that they're in the correct order
    with open(filename) as mslrfile:
        for line in mslrfile:
            tokens = line.split()
            score = int(tokens[0])
            features = [float(x.split(':')[1]) for x in tokens[2:]]

            if '\n' in features:
                features.remove('\n')

            assert len(features) == 136, "Don't have the right number of features"

            y.append(score)
            X.append(features)

    # Convert lists into arrays
    X = np.array(X)
    y = np.array(y)

    return X, y

if __name__ == '__main__':

    # Parse Command Line Arguments
    usage = '%prog [options][text]'
    parser = OptionParser(usage)
    parser.add_option('-i', '--file-in', type='string', dest='infile', help='Input MSLR data file')
    parser.add_option('-o', '--file-out', type='string', dest='outfile', help='Save resulting X and y to a file')
    parser.add_option('-v', '--verbose', action='store_true', default=False, dest='verbose', help='Verbose')
    options, args = parser.parse_args()

    if options.outfile is None:
        raise ValueError("No valid mslr output file name specified; provide '-o'")
        exit(-1)

    if options.infile is not None:
        if options.verbose:
            logging.info('Reading from file: %s' % options.infile)

        X, y = readmslr(options.infile)

        if options.verbose:
            logging.info('Done reading file')

    else:
        raise ValueError("No valid mslr input file name specified; provide '-i")
        exit(-1)

    if options.verbose:
        logging.info("Writing to file: %s" % options.outfile)

    np.savez(options.outfile, X=X, y=y)
