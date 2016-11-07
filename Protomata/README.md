# Protomata
## Description
Protomata[1] converts the 1307 prosite protein motif patterns into regular expression patterns. Once converted to regular expression patterns, each motif pattern can be compiled to form an automata. Because the prosite patterns do not fill an AP chip, prosite patterns were randomly generated and added to the regular expression database until the chip resources were maxed out to create the benchmark standard candle automata. Inputs are formed from sections of the UniProt Consortium database [2].

Special thanks to Matt Grimm (mgrimm@micron.com) for allowing us to use his random protein motif generation tool to build out this benchmark.

## Inputs
### uniprot_fasta_1MB.input
### uniprot_fasta_10MB.input

## References

[1] Roy, Indranil. "Algorithmic techniques for the micron automata processor." (2015).
[2] UniProt Consortium. "UniProt: a hub for protein information." Nucleic acids research (2014)
