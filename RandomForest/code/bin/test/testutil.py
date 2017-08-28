'''
    This unit test file tests various aspects of the util module

    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    28 February 2017
    Version 1.0
'''

import unittest
import util
from random import *


# Test the Node class with a few unit tests
class TestNode(unittest.TestCase):

	# Build an arbitrary node; we'll use this for testing
	def setUp(self):

		# Use the big threshold map to test around the 254 edge case
		self.big_threshold_map = {}

		for f in range(randint(1, 100)):

			self.big_threshold_map[f] = []

			for t in range(randint(1,1000)):

				self.big_threshold_map[f].append(t)

		# Use the small threshold map to test smaller features


	def test_big_threshold(self):

		for i in range(10000):
			util.compact(self.big_threshold_map, verbose=False)

if __name__ == '__main__':
	unittest.main()