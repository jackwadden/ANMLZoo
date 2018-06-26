'''
    The purpose of this program is to visualize the contents
    of the OCR dataset.

    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    Data from:
    https://github.com/adiyoss/StructED/tree/master/tutorials-code/ocr/data
    http://ai.stanford.edu/~btaskar/ocr/
    ----------------------
    28 November 2016
    Version 1.0
'''

# Support imports
from optparse import OptionParser
import numpy as np
import logging

# Visualization imports
import matplotlib.pyplot as plt
import random

# ocrExtractor imports
from ocrExtractor import readOCR

ROWS = 16
COLS = 8

# Read the npz file in and suck out the X and y
def readOCR(filename):

    # Load the training files
    npzfile = np.load(filename)
    X = npzfile['X']
    y = npzfile['y']
    return X, y

def writeSymbolFile(X, count, outfilename):

    f = open(outfilename, 'wb')
    f.write(chr(255))
    for i in range(count):
        for symbol in X[i]:
            value = chr(int(symbol))
            f.write(value)
            print value,
        f.write(chr(255))
        print ""
    f.close()


# Visualize the data
'''
    This is probably not the best / fastest way to visualize
    the OCR images.
    * Room for improvement *
'''
def visualize(X, y, index):

    features = X[index]
    character = y[index]

    heatmap = features.reshape((ROWS, COLS))
    plt.matshow(heatmap, cmap=plt.cm.hot, vmin=0, vmax=1)
    plt.title("Visualization of '%s' from index %d" % (character, index))
    plt.xlabel('x-pixels')
    plt.ylabel('y-pixels')
    plt.show()

# Main()
if __name__ == '__main__':
    datafilename = "ocr/letter.npz"

    X, y = readOCR(datafilename)  # Read the OCR data, verbosely

    print "X.shape: ", X.shape
    print "y.shape: ", y.shape

    writeSymbolFile(X, 10, "10_symbols_ocr.bin")
    # Just for kicks, display the first 100 images
    for i in range(100):
        visualize(X, y, i)