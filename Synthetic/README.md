# Synthetic Automata
## Description
In general, it can be difficult or impossible to guarantee certain properties of automata for controlled experiments. It is therefore important to have a set of automata benchmarks (or generation tools) in the benchmark suite that can precisely vary metrics such as the visited set (the set of states consistently visited during computation) and the active set (the number of active states which need to perform memory accesses per cycle). These synthetic automata and synthetic automata generation tools allow for controlled experiments measuring the specific impact of memory hierarchy latency or throughput on total performance.

We present a parametric synthetic automata design to control for the ratio of active set to visited set. Each automaton is organized as a ring of stages. Each stage in the ring has a fixed number of states that is always activated Fig. 2. Parameterizable synthetic automata design. Each ring is guaranteed to have a constant active set and visited set, and is driven by an easy-togenerate input string. This instance has width 3, thus active set 3. Each stage is fully connected with its succeeding stage to form a continuous ring. The circumference, n, is derived using the equation n = d visited width e. by the previous stage. This property guarantees that at any one cycle, the active set in any one ring is equal to the width of the stage. Each ring is also of a fixed circumference (i.e. the number of stages in the ring). Therefore, the total visited set of the automaton is the width of the stage times the number of stages in the ring. This design allows us to individually control for both active set and visited set, and isolate the impact of each on performance of different automata-processing engines.

## Inputs
### 1000_1MB.input
### 1000_10MB.input

## References
Wadden, J., Dang, V., Brunelle, N., Tracy II, T., Guo, D., Sadredini, E., Wang, K., Bo, C., Robins, G., Stan, M., and Skadron, S. "ANMLZoo: A Benchmark Suite for Exploring Bottlenecks in Automata Processing Engines and Architectures." 2016 IEEE International Symposium on Workload Characterization (IISWC'16). IEEE, 2016.

