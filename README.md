# ANMLZoo Automata Processing Benchmark Suite

IMPORTANT: if using ANMLZoo for experiments, please see ERRATA below...

## Description
High-performance automata-processing engines are traditionally evaluated using a limited set of regular expressionrulesets. While regular expression rulesets are valid real-world examples of use cases for automata processing, they represent a small proportion of all use cases for automata-based computing. With the recent availability of architectures and software frameworks for automata processing, many new applications have been found to benefit from automata processing. These show a wide variety of characteristics that differ from prior, popular regular-expression benchmarks, and these should be considered when designing new systems for automata processing.
This paper presents ANMLZoo, a benchmark repository for automata-based applications as well as automata engines for both von-Neumann and reconfigurable dataflow architectures.

## Errata
Since the publication of ANMLZoo, we have found a few issues with the construction of the benchmarks. We've listed the main issues below that may impact your experimentation with suggested ways to get around this. We will be updated the benchmark suite with a Version 1.1 Summer 2017 that addresses most of these issues.

1. **The prefix merging algorithm in VASim had a bug that missed some minimization opportunities:** We have since fixed this bug and are now able to properly minimize applications like SPM. SPM even in the ANMLZoo paper had a node count of over 100,000! We originally included the application because the Micron compiler was able to identify these optimization opportunities.

2. **RandomForest was incorrectly generated:** RandomForest was originally incorrectly generated for the ANMLZoo paper. We recognized this very early on and we have already generated a new application that fits within a single chip. I have noted this in the README for that application. The new application is rf.1chip.anml, while the old application used for the paper remains in the repo. This is discussed in the RandomForest README.

3. **Some ANMLZoo benchmarks were improperly labeled as compiling to 1 chip:** To generate ANMLZoo "standard candle" automata, we increased the widget count until the number of "rectangular blocks" used by the Micron compiler violated the number of available rectangular blocks on the Micron D480 chip. Unfortunately, this was not the correct way to identify if an automata used more than 1 chip's worth of resources. Consequently, we now know that applications such as Levenshtein, EntityResolution, Snort, and ClamAV actually require 1.5 chips (or 3 half cores). We are looking to remedy this in Version 1.1.

## TODO
The benchmark suite has known mistakes outlined int the Errata. However, there are features that many users have requested that we plan to add in future versions. They are outlined below. If you would like a feature or application added to ANMLZoo, please create an issue ticket with a full description and use case of your feature.

- Fix Erratum #3.
- Add code for ANML emission.
- Support [MNRL](https://github.com/kevinaangstadt/mnrl) file format.
- Add more inputs for training and testing of automata optimization algorithms and automata processing engines and architecture development.
- Add more automata within each "benchmark" label. Applications like Hamming and Levenshtein have huge amount of play in how they are generated. They were originally generated with semi-arbitrary parameters and so other applications with other dimensions could be added.

## Benchmark Contributors

Jack Wadden<br>
Vinh Dang<br>
Deyuan Guo<br>
Elaheh Sadredini<br>
Ke Wang<br>
Chunkun Bo<br>
Nathan Brunelle<br>
Tom Tracy II<br>
Matt Grimm<br>

This suite was originally compiled by Jack Wadden (jackwadden@gmail.com). 
 
If you use this benchmark suite in a publication, please use the following citation:

Wadden, J., Dang, V., Brunelle, N., Tracy II, T., Guo, D., Sadredini, E., Wang, K., Bo, C., Robins, G., Stan, M., and Skadron, S. "ANMLZoo: A Benchmark Suite for Exploring Bottlenecks in Automata Processing Engines and Architectures." 2016 IEEE International Symposium on Workload Characterization (IISWC'16). IEEE, 2016.

```
@inproceedings{ANMLZoo,  
    title={{ANMLZoo: A Benchmark Suite for Exploring Bottlenecks in Automata Processing Engines and Architectures}},  
    author={Wadden, Jack and Dang, Vinh and Brunelle, Nathan and Tracy II, Tom and Guo, Deyuan and Sadredini, Elaheh and Wang, Ke and Bo, Chunkun and Robins, Gabriel and Stan, Mircea and Skadron, Kevin},
    booktitle={Proceedings of the IEEE International Symposium on Workload Characterization (IISWC)},  
    year={2017},  
}
```

## License
Each benchmark and automata processing engine in ANMLZoo is individually licensed. Please refer to the benchmark directories for individual license files.
