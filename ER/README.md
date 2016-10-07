# Entity Resolution Acceleration using Micron's Automata Processor
## Description
Entity Resolution (ER), the process of finding identical entities across different databases, is critical to many information integration applications. As sizes of databases explode in the big-data era, it becomes computationally expensive to recognize identical entities for all records with variations allowed across multiple databases. Profiling results show that approximate matching is the primary bottleneck. Micron's Automata Processor (AP), an efficient and scalable semiconductor architecture for parallel automata processing, provides a new opportunity for hardware acceleration for ER. We propose an AP-accelerated ER solution [1], which accelerates the performance bottleneck of fuzzy matching for similar but potentially inexactly-matched names, and use a real-world application to illustrate its effectiveness. We compared the proposed method with serveral CPU methods and achieved both promising speedup and better accuracy.

## Inputs
### 1000_1MB.input
### 1000_10MB.input

## References
[1] Chunkun Bo, Ke Wang, Jeffrey J. Fox, and Kevin Skadron. “Entity Resolution Acceleration using Micron’s Automata Processor.”  In Proceedings of the Workshop on Architectures and Systems for Big Data (ASBD), in conjunction with ISCA, June 2015.
