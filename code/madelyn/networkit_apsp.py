import numpy as np
import time
import networkit as nk
import pandas as pd

with open("networkit_times_compare.txt", "w") as output_file:
    output_file.write("hash\t\t\t\t\tindex\tnodes\tedges\ttheir_time(s)\tmy_time(s)\n")
    times_dict = dict(np.load("cache/times_apsp.npz", allow_pickle=True))
    df = np.load("../datasets/corpus_augmented.pkl", allow_pickle=True)
    print("data loaded", flush=True)
    for net_hash, their_time in times_dict.items():
        index = df.index[df['hashed_network_name'] == net_hash]
        nodes = df.iloc[index]['nodes_id'].to_list()[0]
        edges = df.iloc[index]['edges_id'].to_list()[0]
       
        graph = nk.Graph()
        for edge in edges:
            graph.addEdge(edge[0], edge[1], addMissing=True)
        assert(graph.numberOfNodes() == len(nodes))
        assert(graph.numberOfEdges() == len(edges))

        start = time.time()
        apsp = nk.distance.APSP(graph)
        apsp.run()
        distances = apsp.getDistances()
        assert(len(distances) == len(nodes))
        end = time.time()
        output_file.write(f"{net_hash}\t{index.tolist()}\t{len(nodes)}\t{len(edges)}\t{np.round(their_time, 3)}\t\t{round(end-start, 3)}\n")


