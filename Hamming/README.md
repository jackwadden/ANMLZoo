# Hamming
## Description
Hamming distance is a calculation of how many differences there are between two strings of the same length. The automata-based computation uses a mesh network of [<symbol>]/[^<symbol>] decisions to keep track of how many differences are seen in an input string when compared to an embedded string [1].

## ANML
### 93_20X3.1chip.anml
93 Hamming distance widgets. Each widget calculates all strings within Hamming distance 3 of a randomly embedded string of length 20. This automata was tuned so that it uses the resources of an entire AP chip.

## Inputs
### hamming_1MB.input
1MB of randomly generated alphanumeric characters.

### hamming_10MB.input
10MB of randomly generated alphanumeric characters.

## References
[1] Roy, Indranil, and Srinivas Aluru. "Finding motifs in biological sequences using the micron automata processor." Parallel and Distributed Processing Symposium, 2014 IEEE 28th International. IEEE, 2014.


