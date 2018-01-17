#!/usr/bin/env python
"""
    The purpose of this program is to train a decision-tree based learning
    algorithm using Scitkit-Learn and to write the resulting model and testing
    data to their respective files for automatization.
    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    16 January 2018
    Version 0.3
"""

# Support Imports
import pickle
from optparse import OptionParser
import numpy as np
import logging
import time

# Model Imports
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier

# Feature selection imports
from sklearn.feature_selection import SelectKBest, chi2

# Dataset Imports
from sklearn.datasets import fetch_mldata

# Metrics Import
from sklearn import metrics

# Global dictionaries
model_names = {'rf': 'Random Forest',
               'brt': 'Boosted Regression Trees',
               'ada': 'Adaboost Classifier',
               'xgb': 'XGboost'
               }

metric_names = {'acc': 'accuracy',
                'f1': 'f1-score',
                'mse': 'Mean Squared Error',
                'auc': 'Area Under the Curve'
                }

datasets = {'mnist': 'MNIST original'}

# Turn on logging.
logging.basicConfig(format='%(asctime)s : %(message)s', level=logging.INFO)


# Train the model on the given training data
def train_model(model_, x_train_, y_train_):

    model_.fit(x_train_, y_train_.ravel())


# Test the model on the given testing data
def test_model(model_, x_test_, y_test_, metric_):

    if metric_ == 'acc':

        return metrics.accuracy_score(y_test_, model_.predict(x_test_))

    elif metric_ == 'f1':

        return metrics.f1_score(y_test_, model_.predict(x_test_))

    elif metric_ == 'mse':

        return metrics.mean_squared_error(y_test_, model_.predict(x_test_))

    else:

        raise ValueError("Invalid metric %s provided" % metric_)


# Dump the model to a file
def dump_model(model_, modelfile):

    with open(modelfile, 'wb') as f:

        pickle.dump(model_, f)


# Dump test data
def dump_test(x_test_, y_test_, testfile_):

    with open(testfile_, 'wb') as f:

        pickle.dump((x_test_, y_test_), f)


# Write report out to file
def write_report(report_name_, report_dict_):

    with open(report_name_, 'w') as f:

        for key, value in report_dict_.items():

            f.write(str(key) + ":" + str(value))


# Calculate the average throughput of the model on the CPU
def print_throughput(model_, x_test_, iters_):

    logging.info("Model: %s" % str(model_))
    logging.info("Test Data: %d samples x %d features" % x_test_.shape)

    # Grab the start time
    start_time = time.time()

    # Do a bunch of predictions
    for i in range(iters_):
        model_.predict(x_test_)

    # Grab the end time
    end_time = time.time()

    # Grab average time per iterations
    avg_time = (end_time - start_time) / float(iters_)

    logging.info("Average Time: %f" % avg_time)

    # Throughput = num_feature_vectors / average time per iteration
    throughput = float(x_test_.shape[0]) / avg_time

    # Metric becomes kilo-samples / sec
    kthroughput = throughput / 1000.0

    logging.info("Throughput: %f ksamples / second" % kthroughput)

# Dump the predictions made by the model to a file for testing
def dump_predictions(model_, x_test_, filename_):

    predictions = model_.predict(x_test_)

    with open(filename_, 'w') as f:

        for prediction in predictions:

            f.write(str(int(prediction)) + '\n')


# Main()
if __name__ == '__main__':

    # Parse Command Line Arguments
    usage = '%prog [options][text]'
    parser = OptionParser(usage)

    parser.add_option('-c', '--canned', type='string', dest='canned',
                      help='A canned dataset included in SKLEARN (mnist)')

    parser.add_option('-t', '--train', type='string', dest='trainfile',
                      help='Training Data File (.npz file)')

    parser.add_option('-x', '--test', type='string', dest='testfile',
                      help='Testing Data File (.npz file)')

    parser.add_option('--metric', type='string', default='acc',
                      dest='metric',
                      help='Provide the training metric to be displayed')

    parser.add_option('-m', '--model', type='string', dest='model',
                      help='Choose the model')

    parser.add_option('--model-out', type='string', dest='modelout',
                      default='model.pickle', help='Output model file')

    parser.add_option('-d', '--depth', type='int', dest='depth',
                      help='Max depth of the decision tree learners')

    parser.add_option('-l', '--leaves', type='int', dest='leaves',
                      help='Max number leaves of the decision tree learners')

    parser.add_option('-n', '--tree_n', type='int', dest='tree_n',
                      help='Number of decision trees')

    parser.add_option('-f', '--n_features', type='int', dest='n_features',
                      help='The number of features when fit is performed.')

    parser.add_option('-j', '--njobs', type='int', dest='njobs',
                      help='Number jobs to run in parallel for fit/predict')

    parser.add_option('--feature_importance', action='store_true', default=False,
                      dest='feature_importance',
                      help='Dump the feature importance values of the trained forest')

    parser.add_option('-v', '--verbose', action='store_true', default=False,
                      dest='verbose', help='Verbose')

    parser.add_option('-r', '--report', type='string', dest='report',
                      default='report.txt', help='Name of the report file')

    parser.add_option('-p', '--predictions', type='string', dest='predictions',
                      default='predictions.txt', help='Predictions made by model')

    options, args = parser.parse_args()

    params = {}
    report_dict = {}
    canned = False
    X = None
    y = None

    # Validate command line arguments
    if options.trainfile is None:
        if options.canned not in datasets.keys():
            raise ValueError("No valid training data filename specified; \
                              provide -t or a valid canned dataset")
        else:
            canned = True

    if options.model is None:
        raise ValueError("No valid model specified;\
                         provide {'rf', 'brt', 'ada'}")
    else:
        options.model = options.model.lower()

    if options.model not in model_names.keys():
        raise ValueError("No valid model specified;\
                         provide {'rf', 'brt', 'ada'}")

    if options.depth is None:

        if options.leaves is None:
            raise ValueError("No valid tree depth or leaves specified;\
                             provide -d <max depth> or -l <max leaves>")
        else:
            params['max_leaf_nodes'] = options.leaves
            report_dict['max_leaf_nodes'] = options.leaves
    else:
        params['max_depth'] = options.depth
        report_dict['max_depth'] = options.depth

    if options.tree_n is None:
        raise ValueError("No tree count specified; provide -n <num trees>")

    params['n_estimators'] = options.tree_n
    report_dict['n_estimators'] = options.tree_n

    if options.njobs is not None:
        params['n_jobs'] = options.njobs
        report_dict['n_jobs'] = options.njobs

    if options.verbose:
        logging.info("Loading training file from %s" % options.trainfile)

    if canned:
        canned_dataset = fetch_mldata(datasets[options.canned])
        X = canned_dataset.data
        y = canned_dataset.target

    else:
        # Load the training files
        npzfile = np.load(options.trainfile)
        X = npzfile['X']
        y = npzfile['y']

    if options.verbose:
        logging.info("Shape of the loaded training data. X:(%d,%d), y:(%d)" %
                     (X.shape[0], X.shape[1], y.shape[0]))

    X_test = None
    y_test = None

    if options.testfile is None:
        logging.info("No included test file, so going to split training data")
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            test_size=0.33,
                                                            random_state=42)

    else:
        # Use train file for training
        X_train = X
        y_train = y

        # Load the testing files
        npzfile = np.load(options.testfile)
        X_test = npzfile['X']
        y_test = npzfile['y']

    if options.verbose:
        logging.info("Shape of the loaded testing data. X:(%d,%d), y:(%d)" %
                     (X_test.shape[0], X_test.shape[1], y_test.shape[0]))

    if options.verbose:
        logging.info("Setting the model to be learned to: %s" % options.model)
        logging.info("With parameters: %s" % str(params))

    model = None

    if options.model == 'rf':
        model = RandomForestClassifier(**params)

    elif options.model == 'brt':
        model = GradientBoostingClassifier(**params)

    elif options.model == 'ada':
        del params['max_depth']
        del report_dict['max_depth']
        model = AdaBoostClassifier(**params)

    else:
        raise ValueError("No valid model specified")

    report_dict['model'] = model

    # Transform X to n_features
    if options.n_features is not None:

        # For simplicity, we're going to use the CHI-squared test to choose the
        # n_features least correlated features to train our model
        ch2 = SelectKBest(chi2, k=int(options.n_features))
        X_train = ch2.fit_transform(X_train, y_train)
        X_test = ch2.transform(X_test)

    if options.verbose:
        logging.info("Training the %s model" % model_names[options.model])

    # Train the model
    train_model(model, X_train, y_train)

    if options.verbose:
        logging.info("Testing the %s model" % model_names[options.model])

    metric = options.metric
    if options.metric not in metric_names.keys():
        logging.info("No metric defined; defaulting to accuracy")
        metric = 'acc'

    result = test_model(model, X_test, y_test, metric)

    logging.info(metric_names[metric] + ":" + str(result))
    report_dict[metric_names[metric]] = str(result)

    if options.verbose:
        logging.info("Writing model out to %s" % options.modelout)

    # Write the model out to a file
    dump_model(model, options.modelout)

    if options.verbose:
        logging.info("Writing testing data out to testing_data.pickle")

    # Dump the feature importance values
    if options.feature_importance:
        print "Feature Importance: "
        print model.feature_importances_

    # Write out the test data for testing with the automata
    dump_test(X_test, y_test, "testing_data.pickle")

    # Print throughput results for the CPU after 100 testing loops
    print_throughput(model, X_test, 100)

    # Write out the predictions made by the model (for testing)
    dump_predictions(model, X_test, options.predictions)

    # Write out the report
    if options.report is not None:
        write_report(options.report, report_dict)
