import unittest
from chain import *
from random import *

'''
    This unit test file tests various aspects of the Chain and Node class

    ----------------------
    Author: Tom Tracy II
    email: tjt7a@virginia.edu
    University of Virginia
    ----------------------
    18 November 2016
    Version 1.0
'''

# Test the Node class with a few unit tests
class TestNode(unittest.TestCase):

	# Build an arbitrary node; we'll use this for testing
	def setUp(self):
		feature = 12
		threshold = 0.12
		gt = False
		self.node = Node(feature, threshold, gt)

	def test_constructor(self):
		self.assertEqual(self.node.feature_, 12)
		self.assertEqual(self.node.threshold_, 0.12)
		self.assertEqual(self.node.gt_, False)

	def test_equivalence(self):
		node = Node(12, 0.12, False)
		self.assertTrue(node == self.node)

	def test_sorting(self):
		unsorted_nodes = []
		for f in range(10, -1, -1):
			unsorted_nodes.append(Node(f, 0, False))

		sorted_nodes = sorted(unsorted_nodes)
		unsorted_nodes.sort()
		self.assertEqual(sorted_nodes, unsorted_nodes)


	def test_set_character_set(self):
		character_set = []

		for i in range(10):
			character = randint(1, 254)

			if character not in character_set:
				character_set.append(character)

		self.node.set_character_set(character_set)
		character_set.sort()

		self.assertEqual(len(character_set), len(self.node.character_set))

		for i, j in zip(character_set, self.node.character_set):
			self.assertEqual(i, j)


	def test_set_character_set_continuous(self):

		character_set = range(0, 101)
		self.node.set_character_set(0, 100)
		self.assertEqual(character_set, self.node.character_set)


	# Sort the chain by feature value, then update ids and children
	def sort_and_combine(self):

		# Sort the nodes_ in the chain by feature value (increasing)
		self.nodes_ = sorted(self.nodes_)

		# Can't combine with only one node!
		if len(self.nodes_) == 1 or len(self.nodes_) == 0:
			return

		# Let's combine!
		previous_index = 0
		current_index = 1

		assert len(self.nodes_[0].character_set) > 0, "Character sets not set!"

		while True:
			previous_node = self.nodes_[previous_index]
			current_node = self.nodes_[current_index]

			# If they have the same feature, combine
			if previous_node.feature_ == current_node.feature_:
				previous_node.character_set += current_node.character_set
				self.nodes_.remove(current_node)
			else:
				previous_index += 1
				current_index += 1

			# We're done
			if current_index == len(self.nodes_):
				break


class TestChain(unittest.TestCase):

	def setUp(self):

		self.C = Chain(0)

	def test_constructor(self):

		chain = self.C

		self.assertEqual(len(chain.nodes_), 0)
		self.assertEqual(chain.uid_, 0)
		self.assertEqual(chain.tree_id_, 0)
		self.assertEqual(chain.chain_id_, None)
		self.assertEqual(chain.value_, None)

	def test_add_node(self):

		chain = self.C
		features = []

		for _i in range(10):
			f = _i * 10

			features.append(f)

			node = Node(f, 0.1*f, False)
			chain.add_node(node)

		self.assertEqual(len(chain.nodes_), 10)
		self.assertEqual(chain.uid_, len(chain.nodes_))

	def test_set_value(self):

		chain = self.C
		chain.set_value(101)
		self.assertEqual(chain.value_, 101)

	def test_set_chain_id(self):

		chain = self.C
		chain.set_chain_id(999)
		self.assertEqual(chain.chain_id_, 999)

	def test_sort_and_combine(self):

		chain = self.C
		features = []

		for _i in range(10):
			f = randint(1, 5)
			features.append(f)

			node = Node(f, random()*f, False)

			character_set = []

			for _i in range(10):
				character_set.append(randint(1, 100))

			node.set_character_set(character_set)
			chain.add_node(node)

		chain2 = chain.copy()
		chain2.sort_and_combine()

		# First check to make sure we don't have duplicates
		features_seen = []
		for node in chain2.nodes_:
			self.assertFalse(node.feature_ in features_seen)
			features_seen.append(node.feature_)

		# Check that they're sorted
		previous_feature = -1
		for feature in features_seen:
			self.assertTrue(previous_feature < feature)
			previous_feature = feature

		# Check that the thresholds have been combined
		#chain.nodes_.sort()
		combined_thresholds = {}

		for node in chain.nodes_:
			if node.feature_ not in combined_thresholds:
				combined_thresholds[node.feature_] = node.character_set
			else:
				for c_s in node.character_set:
					if c_s not in combined_thresholds[node.feature_]:
						combined_thresholds[node.feature_].append(c_s)

		for feature, thresholds in combined_thresholds.items():
			thresholds.sort()

		for node in chain2.nodes_:
			self.assertTrue(node.feature_ in combined_thresholds.keys())
			self.assertEqual(node.character_set, combined_thresholds[node.feature_])



if __name__ == '__main__':
	unittest.main()