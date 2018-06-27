'''
    The purpose of this program is to extract the pixel feature matrix (X)
    and classification vector (y) from normalized OCR data file.

    X: contains black/white pixels (0, 1) of normalized handwritten characters
        Each handwritten image has dimensions 8 x 16
    y: contains corresponding character labels
        a-z (lowercase)
    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    Data from:
    https://github.com/adiyoss/StructED/tree/master/tutorials-code/ocr/data
    http://ai.stanford.edu/~btaskar/ocr/
    ----------------------
    14 November 2016
    Version 1.0
'''

# Support imports
from optparse import OptionParser
import numpy as np
import logging

# Visualization imports
import matplotlib.pyplot as plt
import random

# Global variables (dimensions of the image data and size of file)
ROWS = 16
COLS = 8
LINES = 52152 # How many lines are in the file?

# Turn on logging.
logging.basicConfig(format='%(asctime)s : %(message)s', level=logging.INFO)

# Visualize the data
def visualize(X, y, rndm=True):
    index = 0
    if rndm:    # Do we wanna see a random sample?
        index = random.randint(0, LINES-1)

    features = X[index]
    character = y[index]

    heatmap = features.reshape((ROWS, COLS))
    plt.matshow(heatmap, cmap=plt.cm.hot, vmin=0, vmax=1)
    plt.title("Visualization of '%s' from index %d" % (character, index))
    plt.xlabel('x-pixels')
    plt.ylabel('y-pixels')
    plt.show()

# Read from the ocr file
def readOCR(filename, verbose):
    y = []#np.empty((0, 1), np.uint)
    X = []#np.empty((0, ROWS * COLS), np.uint)

    with open(filename) as ocrfile:
        i = 1
        for line in ocrfile:
            tokens = line.split('\t')
            #index = int(tokens[0])
            character = tokens[1]
            #next_id = int(tokens[2])
            #word_id = int(tokens[3])
            #position = int(tokens[4])
            #fold = int(tokens[5])
            pixels = tokens[6:]
            pixels.remove('\n') # Cut off the training newline

            y.append(character)
            X.append([int(x) for x in pixels])

            #y = np.vstack((y, np.array([character])))
            #X = np.vstack((X, np.array([int(x) for x in pixels])))

    # Convert lists into arrays
    X = np.array(X)
    y = np.array(y)

    return X, y

if __name__ == '__main__':

    # Parse Command Line Arguments
    usage = 'usage: %prog [options]'
    parser = OptionParser(usage=usage)
    parser.add_option('-i', '--file-in', type='string', dest='infile', help='Input OCR data file')
    parser.add_option('-o', '--file-out', type='string', dest='outfile', help='Save resulting X and y to a file')
    parser.add_option('-v', '--verbose', action='store_true', default=False, dest='verbose', help='Verbose')
    parser.add_option('--visualize', action='store_true', default=False, dest='viz', help='Enable to visualize')
    options, args = parser.parse_args()

    if options.outfile is None:
        print parser.usage
        raise ValueError("No valid OCR output file name specified; provide '-o'")
        exit(-1)

    if options.infile is not None:
        if options.verbose:
            logging.info('Reading from file: %s' % options.infile)

    else:
        raise ValueError("No valid OCR input file name specified; provide '-i")
        exit(-1)

    X, y = readOCR(options.infile, options.verbose)

    if options.verbose:
        logging.info('Done reading file')
        logging.info('X dimensions: (%d, %d), y dimensions: (%d, %d)' % (X.shape[0], X.shape[1], y.shape[0], y.shape[1]))

    if options.viz:
        logging.info('Visualizing a random handwritten image')
        visualize(X, y)

    if options.verbose:
        logging.info("Writing to file: %s" % options.outfile)

    np.savez(options.outfile, X=X, y=y)
