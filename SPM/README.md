# Sequential Pattern Mining (SPM)
## Description
Sequential pattern mining (SPM) is a widely used data mining technique for discovering common sequences of events in large databases. It identifies strong and interesting sequential relations among variables in structured databases.

A pretty intuitive description of SPM is that it looks for frequent permutations of frequent itemsets, and the order among itemsets/transactions matters. During the purchase of a laptop among all of his transactions, the customer will usually buy the laptop itself and a harddisk first, then flashdrive, and then software packages. Thus in this example the sequence we are mining is:
> <{*laptop, harddisk*}, {*flashdrive*}, {*software packages*}>.

More formally, define the *set of items* *I* = {*i*<sub>1</sub>, *i*<sub>2</sub>, ... , *i*<sub>m</sub>} , where *i*<sub>k</sub> is usually represented by an integer, call item ID. <br>
Let the *sequential pattern* (or *sequence*) be *s* =<*t*<sub>1</sub> *t*<sub>2</sub> ... *t*<sub>n</sub>> , where *t*<sub>k</sub> is a transaction and also can be called as an *itemset*. <br>
Deﬁne an element of a sequence or the *itemset* by *t*<sub>j</sub> = {*x*<sub>1</sub>, *x*<sub>2</sub>, ... , *x*<sub>m</sub>} where *x*<sub>k</sub> ∈ *I*. In a sequence, one item may occur just once in one transaction but may appear in many transactions. <br>
We also assume that the order within a transaction (itemset) does not matter, so the items within one transaction can be lexicographically ordered in preprocessing stage. We deﬁne the size of a se- quence as the number of items in it. A sequence with a size k is called a k-sequence. Sequence s called to be a subsequence of s are integers 1 −k t ⊆−r a sequential pattern. The support for a sequence is the num- ber of total data sequences that contains this sequence. A sequence is known as frequent iﬀ its support is greater than a given threshold value called minimum support, minsup. The goal of SPM is to ﬁnd out all the sequential patterns whose supports are greater than minsup.

## Inputs
### SPM_1MB.input
### SPM_10MB.input

## References
Ke Wang, Elaheh Sadredini, and Kevin Skadron. 2016. Sequential pattern mining with the Micron automata processor. In Proceedings of the ACM International Conference on Computing Frontiers (CF '16). ACM, New York, NY, USA, 135-144. DOI: http://dx.doi.org/10.1145/2903150.2903172
