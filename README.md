# FairnessNetworks
## Abstract
We consider the problem of selecting 𝑘 seed nodes in a social network to maximize the minimum probability of activation under an independent cascade beginning at these seeds. The motivation is to promote fairness by ensuring that even the least advantaged members of the network have good access to information. Our problem can be viewed as a variant of the classic influence maximization objective, but it appears somewhat more difficult to solve: only heuristics are known. Moreover, the scalability of these methods is sharply constrained by the need to repeatedly estimate access probabilities. We design and evaluate a suite of 10 new scalable algorithms which crucially do not require probability estimation. To facilitate comparison with the state-of-the-art, we make three more contributions which may be of broader interest. We introduce a principled method of selecting a pairwise information transmission parameter used in experimental evaluations, as well as a new performance metric which allows for comparison of algorithms across a range of values for the parameter 𝑘. Finally, we provide a new benchmark corpus of 174 networks drawn from 6 domains. Our algorithms retain most of the performance of the state-of-the-art while reducing running time by orders of magnitude. Specifically, a meta-learner approach is on average only 20\% less effective than the state-of-theart on held-out data, but about 75 − 130 times faster. Further, the meta-learner’s performance exceeds the state-of-the-art on about 20\% of networks, and the magnitude of its running time advantage is maintained on much larger networks.

## Network Corpus
The most recent network corpus of smaller datasets used in the study is `./datasets/corpus_augmented.pkl`. This file is a `pandas` dataframe, network citations are provided in the file itself.

The recent larger datasets used are `./datasets/email-EuAll.txt` and `./datasets/google+.csv`.

Google+ (2013) Citation:
M. Fire et al. "Computationally efficient link prediction in a variety of social networks." ACM Transactions on Intelligent Systems and Technology 5(1), Article 10 (2013)

Email Network (EU research inst.) Citation:
Leskovec, J. Kleinberg and C. Faloutsos. "Graph Evolution: Densification and Shrinking Diameters." ACM Transactions on Knowledge Discovery from Data 1(1), article 2 (2007).

Additionally, we provide `.gml` files for the networks in the corpus in the `./datasets/gml` directory, alongside a list of citations in `./datasets/gml/_CITATIONS.txt`.

## Codebase
### Data pre-processing
The codebase is designed to work with a pre-processed network corpus. The code for pre-processing the networks for inclusion in the corpus can be found in `./code/runners.py`, mainly the method `run_augment_corpus()`.

### Algorithm Implementations
All algorithm implementations are found in `./code/algorithms.py`.
The codebase includes implementations of the following algorithms from prior literature:
- Random
- Greedy
- Myopic
- Naive Myopic
- Gonzales

Additionally, the codebase includes the following novel algorithms:
- Myopic BFS
- Naive Myopic BFS
- Myopic PPR
- Naive Myopic PPR
- MinDegree_hc
- MinDegree_hcn
- MinDegree_nd
- MinDegree_ndn
- LeastCentral
- LeastCentral_n

### Algorithm Performance Evaluations
To produce algorithm performance evaluations on a given network in the corpus of smaller datasets, run `python main.py corpus_multi [index]`, where index is an integer in [0, 174]. This will also compute independent cascade parameters for three select spreadabilities, and additionally evaluate under several select preset independent cascade parameters. 

To produce performance evaluations for the larger networks, run `python main.py [network_command] [algo_names] [spreadability] [k (number of seeds)]`. Spreadability takes a long time to compute on the larger networks, so a spreadability must be specified to run the evaluations. The network commands are "google" and "email_network" for Google+ (2013) and Email Network (EU research inst.), respectively. 

The output files are stored in `./cache/evaluations/` as both `.npz` and `.txt` files. The `.npz` files are used to produce algorithm runtimes (see paragraph below).

### Algorithm Runtimes

To produce algorithm runtimes for a network in the corpus of smaller datasets, run `python main.py timing [spreadability] [index]`, where index is an integer in [0, 174]. The implementation currently relies on presence of corresponding performance evaluation files in `./cache/evaluations/`, outlined in the previous paragraph. The output files are stored in `./cache/timing_algos/`. All-Pairs-Shortest-Paths (APSP), required for Gonzales; LeastCentral; LeastCentral_n; MinDegree_hc; and MinDegree_hcn, were calculated separately. See "Networkit and All-Pairs-Shortest-Paths" paragraph.

To produce algorithm runtimes for the larger networks, run `python main.py [network_command] [algo_names] [spreadability] [k (number of seeds)]`. The timing data will be saved in `./cache/timing_algos/`. The data is formatted in pairs of numbers, where the first number is the algorithm time (without APSP or evaluation), and the second number is the APSP time (see next paragraph).

### Networkit and All-Pairs-Shortest-Paths

Originally, our implementation used the `networkx` python package to calculate APSP for Gonzales, LeastCentral, LeastCentral_n, MinDegree_hc and MinDegree_hcn. When the algorithms were timed on the corpus of smaller networks, the APSP time was computed separately using the `networkit` python package, computed on a single core, and stored in `./cache/times_apsp.npz`. However, when we added the larger networks to our study, the `networkx` implementation was impractically slow. Thus, we changed our logic to convert the `networkx` graph to a `networkit` graph in order to calculate APSP. 

### Hyperparameter Tuning
Our hyperparameter tuning strategy is included as commented-out code in `./code/runners_figs.py`, lines 2340-2360. The results of this search step were originally cached and analyzed later. Our final selection of hyperparameters reflects a choice of hyperparameters that deliver the highest prediction accuracy on average across the network corpus used in this study, and can be found in `./code/runners_figs/`, line 2362.


## Repository Overview

```
.
├── code
│   ├── cache
│   │   ├── algo_cache // various algorithm seed set caches
│   │   │   └── ...
│   │   ├── evaluations // evaluation results for corpus and large networks
│   │   │   └── ...
│   │   ├── features.npz // corpus network features
│   │   ├── times_apsp.npz // apsp times per-network
│   │   ├── timing_algos // algorithm timing measurements
│   │   │   └── ...
│   │   ├── timing_probest
│   │   |   └── [various ProbEst timing experiments]
│   ├── cpp // fast implementation of ProbEst
│   │   ├── Makefile
│   │   ├── prob_est
│   │   └── prob_est.cpp
│   ├── algorithms.py // algorithm implementations
│   ├── bruteforce.py // ideal combinatoric bruteforce algorithm
|   ├── confirm_alpha.py // confirms activation percent for large networks
│   ├── experiments.py // experimental setups
|   ├── find_variance.py // finds variance in degree distribution of large networks
│   ├── independent_cascade.py // independent cascade helper code for slow implementation of ProbEst
│   ├── main.py // main executable
│   ├── networks.py // various synthetic and corpus networks
│   ├── probability.py // ProbEst implementations
│   ├── runners_figs.py // figure plotting code
│   ├── runners.py // code for running experiments, augmenting network corpus, etc.
│   ├── spreadability.py // spreadability comptutation code
│   └── timing_runner.sh // bash scheduler for timing experiments
├── datasets // various data sets used in the study
│   ├── corpus_augmented.pkl // most recent corpus
│   └── ... // other loose files are a part of the corpus compilation process
└── README.md

```
