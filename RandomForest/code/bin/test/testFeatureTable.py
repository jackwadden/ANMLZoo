import unittest
from featureTable import *
from random import *

'''
    This unit test file tests various aspects of the featureTable class

    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    8 February 2017
    Version 1.1

    Updated with new FT features including:
    - Supporting multiple STEs per feature
    - Generating an input file for the AP

'''

# Test the FeatureTable class with a few unit tests
class TestFeatureTable(unittest.TestCase):

	# Build an arbitrary node; we'll use this for testing
	def setUp(self):

		self.features = []
		self.threshold_map = {}

		for _f in range(100):

			self.features.append(_f)

			thresholds = []

			for _j in range(randint(50, 999)):

				t = randint(1, 999)

				if t in thresholds:
					continue
				else:
					thresholds.append(t)

			self.threshold_map[_f] = thresholds

		self.features.sort()

		for k, val in self.threshold_map.items():
			val.sort()

		self.ft = FeatureTable(self.features, self.threshold_map)

	# Make sure the constructor was built correctly
	def test_constructor(self):
		self.assertEqual(self.ft.features_, self.features)
		self.assertEqual(self.ft.threshold_map_, self.threshold_map)

		# Grab the number of thresholds used in total
		total_address_space = sum([len(val) for key, val in self.ft.threshold_map_.items()])

		# Then add the number of -1s added (one per feature)
		total_address_space += len(self.features)

		# Check to make sure the address spaces have the same size
		self.assertEqual(len(self.ft.stes_[0]), total_address_space)

		# Now let us test each feature!
		for feature in self.ft.features_:

			for ste, start, end in self.ft.feature_pointer_[feature]:

				thresholds = self.ft.threshold_map_[feature]

				self.assertEqual(ste, 0)

				for i,j in enumerate(range(start, end)):

					self.assertEqual(thresholds[i], self.ft.stes_[ste][j])

	def test_get_ranges(self):

		for ste, start, end in self.ft.get_ranges(self.ft.features_[-1]):
			self.assertEqual(ste, 0)
			self.assertTrue(start < end)

	def test_get_stes(self):

		for f in self.ft.features_:

			self.assertEqual(len(self.ft.get_stes(f)), 1)

	def test_get_symbols(self):

		# Choose a random feature
		for feature in self.ft.features_:

			for ste, start, end in self.ft.get_ranges(feature):

				# Check smallest range
				thresholds = self.ft.threshold_map_[feature]
				small_value = thresholds[0] - 1
				small_labels = self.ft.get_symbols(feature, small_value)[0]

				self.assertEqual(small_labels[0], 0) # STE = 0
				self.assertEqual(small_labels[1], start) # Label = start label

				# Check largest range
				large_value = thresholds[-1] + 1
				large_labels = self.ft.get_symbols(feature, large_value)[0]

				self.assertEqual(large_labels[0], 0)
				self.assertEqual(large_labels[1], end)

	def test_compact(self):

		self.ft.compact(naive=True)

	def test_input_file(self):

		self.ft.compact(naive=True)

		filename = "testfile"

		X = []

		for i in range(100):

			temp = []

			for f in range(100):

				random_value = randint(0, 100)
				temp.append(random_value)

			X.append(temp)

		# Make sure the input looks right
		self.assertEqual(len(X), 100)
		self.assertEqual(len(X[0]), 100)

		# Generate an input file
		bytes_written = self.ft.input_file(X, filename)

		# Verify file is correct
		with open(filename, 'rb') as f:
			data =  f.read()

			#self.assertEqual(bytes_written, len(data), )

			# Convert hex into decimal values
			ord_data = [ord(d) for d in data]

			self.assertEqual(bytes_written, len(ord_data), "Something went wrong; |written data|=%d, |read data|=%d" % (bytes_written, len(ord_data)))


if __name__ == '__main__':
	unittest.main()
