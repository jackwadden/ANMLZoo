# ClamAV
## Description
ClamAV is an open source repository of virus signatures available at https://www.clamav.net/downloads. The ANML file for ClamAV is a subset of the full signature database. In particular, many signatures with large quantifiers (>64) are ignored and instead are treated as chains of STEs (no counter) by the Micron PCRE compiler.

## Inputs
### vasim_1MB.input
A 1MB snippet of the UVA Virtual Automata Simulator (VASim) binary, assumed to be a representative executable.

### vasim_10MB.input
A 10MB snippet of the UVA Virtual Automata Simulator (VASim) binary, assumed to be a representative executable. A concatenation of the smaller VASim binary.

## References

[1] Kojm, T., M. Cathey, and C. Cordes. "ClamAV." https://www.clamav.net/downloads. (2004).


