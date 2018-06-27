import logging
import pickle

# Turn on logging; let's see what all is going on
logging.basicConfig(format='%(asctime)s : %(message)s', level=logging.INFO)


# Load a sklearn model from a file
def load_model(modelfile):

    # Read the modelfile pickle
    with open(modelfile, 'rb') as f:
        model = pickle.load(f)

    return model


# Load testing data
def load_test(testfile):

    # Read the testing data in to be used to generate a symbol file
    with open(testfile, 'rb') as f:
        x_test, y_test = pickle.load(f)

    return x_test, y_test

# Dump feature table
def dump_feature_table(ft, ft_filename):

    # Dump the feature table to a file for labeling
    with open(ft_filename, 'wb') as f:
        pickle.dump(ft, f)


# Load feature table
def load_feature_table(ft_filename):

    # Dump the feature table to a file for labeling
    with open(ft_filename, 'rb') as f:
        ft = pickle.load(f)

    return ft
