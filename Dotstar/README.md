# Dotstar
## Description
Backdoor is a set of synthetic automata generated from regular expressions created with Michela Becchi's synthetic regular expression generation tool [1]. These exact rules were the ones used to evaluate the GPU automata processing engine presented in [2]. To form these rules, we combined the 5% 10% and 20% dotstar probability regular expression rulesets. The regular expressions used to generate this file is located in the regex directory. Input stimulus was created using Michela Becchi's input trace generation tools. We constructed a trace with 75% probability of state match for evaluation.

## Inputs
### backdoor_1MB.input
Derived from a trace generated with a 75% match probability.

### backdoor_10MB.input
Derived from a trace generated with a 75% match probability. Concatenated to reach 10MB.

## References

[1] Becchi, Michela, Mark Franklin, and Patrick Crowley. "A workload for evaluating deep packet inspection architectures." Workload Characterization, 2008. IISWC 2008. IEEE International Symposium on. IEEE, 2008.

[2] Yu, Xiaodong, and Michela Becchi. "GPU acceleration of regular expression matching for large datasets: exploring the implementation space." Proceedings of the ACM International Conference on Computing Frontiers. ACM, 2013.

## License
See license file.
