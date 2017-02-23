# Brill
## Description
Brill is short for Brill rule tag updates in the Brill part-of-speech tagging application. The first stage of Brill tagging tags words with a naive tag from a database, that is not context sensitive. The second stage uses learned rules to update tags depending on local words. Identifying where to apply rules in the tagged corpus is the non-trivial task that automata are meant to accelerate.

## Inputs
### brill_1MB.input
A 1MB snippet of the Brown Tagged Corpus.

### vasim_10MB.input
A 10MB snippet of the Brown Tagged Corpus.

## References

[1] K. Zhou, J. Wadden, J. J. Fox, K. Wang, D. E. Brown and K. Skadron, "Regular expression acceleration on the micron automata processor: Brill tagging as a case study," 2015 IEEE International Conference on Big Data (Big Data), Santa Clara, CA, 2015, pp. 355-360.


