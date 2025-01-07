import time
import sys
import networks as networks
import numpy as np
import networkx as nx

corpus_df = np.load("../datasets/corpus_augmented.pkl", allow_pickle=True)
their_times = dict(np.load("cache/times_apsp.npz", allow_pickle=True))
my_file = open("times_comparison.txt", "w")
my_file.write("hash\t\t\t\t\tindex\tnodes\tedges\ttheir_time(s)\tmy_time(s)\n")

for net_hash in their_times.keys():
    #get index of the network whose time we are looking at
    index = corpus_df[corpus_df['hashed_network_name'] == net_hash].index[0]
    n = corpus_df['number_nodes'][index]
    m = corpus_df['number_edges'][index]
    their_time = np.round(their_times[net_hash], decimals=3)

    G = networks.get_corpus_graph(index)
    
    #check that it is the same network
    assert(G.number_of_nodes() == n)
    assert(G.number_of_edges() == m)

    start_time = time.time()
    dict(nx.all_pairs_shortest_path_length(G))
    end_time = time.time()

    my_time = round(end_time-start_time, 3)

    my_file.write(f"{net_hash}\t{index}\t{int(n)}\t{int(m)}\t{their_time}\t\t{my_time}\n")
    print("finished one iter", flush=True)
    

my_file.close()
