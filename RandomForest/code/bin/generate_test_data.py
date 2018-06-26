#!/usr/bin/env python

from tools.io import *
from optparse import OptionParser


if __name__ == '__main__':

    # Parse Command Line Arguments
    usage = '%prog [options]'

    parser = OptionParser(usage)

    parser.add_option('--short', action='store_true', default=False, dest='short',
                      help='Make a short version of the input (100 samples)')

    parser.add_option('--input_format', type='string', dest='input_format',
                      default='BIN',
                      help=
                      'Input file format types:\n\
                      \n\
                      SIMPLE: Space-delimited feature values with newlines between vectors (circuit)\n\
                      \n\
                      BIN: Binary feature values with \\xff delimiters (VASIM)\n\
                      \n\
                      CSV: Comma-separated ASCII features with newlines between vectors')

    parser.add_option('-v', '--verbose', action='store_true', default=False,
                      dest='verbose', help='Verbose')

    options, args = parser.parse_args()

    X_test, y_test = load_test("testing_data.pickle")
    ft = load_feature_table("feature_table.pickle")

    ft.input_file(X_test, "input_file", onebased=False,
                  short=options.short, delimited=True)

    #np.savetxt("testing.bin", X_test[:size], delimiter=',', fmt='%d')
    #np.savetxt("predictions.csv", y_test[:size], delimiter=',', fmt='%d')
