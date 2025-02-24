import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import experiments as exp
import algorithms as alg
import time

class Experiment:
    '''
    Runs an experiment on a given graph G, with a given algorithm, for given parameters
    '''

    def __init__(self, G, initial_seeds = [], k=100, p=0.5, ic_trials=10000, iterations=20, use_cache=False, algorithm=None, name=None, perform_eval=True, threads=0):
        self.G = G
        self.initial_seeds = initial_seeds
        self.p = p
        self.k = k
        self.ic_trials = ic_trials
        self.iterations = iterations
        self.algorithm = algorithm
        self.start_time = None
        self.end_time = None
        self.name = name
        self.use_cache = use_cache
        self.perform_eval = perform_eval
        #algorithm time summed over all iterations
        self.delta_time = None
        self.threads = threads
        #summed over all iterations
        self.precompute_total_time = 0
        #summed over all iterations
        self.eval_time = 0

    def run(self):
        '''
        Runs the experiment and returns the average evaluation.
        '''

        # start the timer
        self.start_time = time.time()

        # run the algorithm for the specified number of iterations
        evaluations = []
        for i in range(self.iterations):
            print(f"[{self.name}] Iteration {i+1}/{self.iterations}")

            algo = self.algorithm(
                self.G, k=self.k, seeds=[self.initial_seeds[i]], p=self.p, ic_trials=self.ic_trials, use_cache=self.use_cache, threads=self.threads)
            
            if self.perform_eval:
                evaluations.append(algo.evaluate())
                print(f"[{self.name}] Evaluation: {evaluations[-1]}")
                self.precompute_total_time += algo.precompute_time
                self.eval_time += algo.eval_time
            else:
                algo.predict()
                self.precompute_total_time += algo.precompute_time

        # end the timer
        self.end_time = time.time()

        self.delta_time = self.end_time - self.start_time - self.precompute_total_time - self.eval_time

        print(f"[{self.name}] Time taken: {self.delta_time} seconds. Algorithm Precompute Time: {algo.precompute_time}. Eval time: {self.eval_time}")
        
        return evaluations
    
def run_specified_experiments(G, k, p, iterations, init_seeds=None, use_cache=False, algo_dict=None, draw_fig=False, save_evals=True, p_tag=None, save_timing=True):
    evaluations = {}
    times = {}

    if p_tag == None:
        p_tag = str(p).replace('.', '')

    if draw_fig:
        # reset plt
        plt.clf()

    # roll a random seed from G for each iteration
    if init_seeds==None:
        initial_seeds = np.random.choice(G.nodes, size=iterations, replace=False)
    else:
        initial_seeds = init_seeds

    print(f'Running experiments on {G.name} with p = {p}, k = {k} for {iterations} iterations. Initial seeds: {initial_seeds}')

    # iterate over algorithms set to True
    for key, val in algo_dict.items():
        if val:
            print(f'Running {key}', flush=True)

            # initialize specified experimental environments and evaluate
            experiment = Experiment(G=G, k=k, initial_seeds=initial_seeds, p=p, iterations=iterations, use_cache=use_cache, algorithm=alg.get_algorithm(key), name=key)
            print(f"IC trials: {experiment.ic_trials}", flush=True) 
            evaluations[key] = [i for lst in experiment.run() for i in lst] #flatten eval list and put in dict
            times[key] = (experiment.delta_time, experiment.precompute_total_time)
            if draw_fig:
                plt.plot(range(1, len(evaluations[key])+1), evaluations[key], label=key)

    if draw_fig:
        plt.legend()
        plt.title(f'p = {p}')
        plt.xlabel('k')
        plt.ylabel('min access probability')

        # integer ticks
        plt.xticks(np.arange(0, k+1, 10))
        plt.yticks(np.arange(0, 1.1, 0.1))

        plt.grid(True, which='both', axis='both', linestyle='--')

        # save figure with tight layout
        plt.savefig(f'../figures/{G.name}_{p}.png', bbox_inches='tight')

    if save_evals:
        # save evaluations
        np.save(f'./cache/evaluations/{G.name}_{p_tag}_{round(p, 3)}.npy', evaluations)
        path = f'./cache/evaluations/{G.name}_{round(p, 3)}_IC{experiment.ic_trials}_eval.txt'
        with open(path, "a") as eval_file:
            for algo, evals in evaluations.items():
                eval_file.write(f"{algo}\n")
                for min_broad in evals:
                    eval_file.write(f"{(round(float(min_broad), 3))} ")
                eval_file.write("\n")

    if save_timing:
        #save times to file. Note that they are formatted (algo_time, precompute_time)
        #Note that the times are saved as the sum over all iterations
        path=f'./cache/timing_algos/{G.name}_{round(p, 3)}_IC{experiment.ic_trials}_times.txt'
        with open(path, "a") as time_file:
            for algo, time in times.items():
                time_file.write(f"{algo}\n")
                for num in time:
                    time_file.write(f"{(round(num, 3))} ")
                time_file.write("\n")
            

    return evaluations

def run_timing_experiment(G, algo_dict, p, p_tag, iterations=10, k=1):
    # roll a random seed from G for each iteration
    initial_seeds = np.random.choice(G.nodes, size=iterations, replace=False)

    k = 10

    print(f'Running timing experiments on {G.name} with p = {p}, k = {k} for {iterations} iterations. Initial seeds: {initial_seeds}')

    times = {}
    for a in algo_dict.keys():
        if algo_dict[a]:
            times[a] = []

    # iterate over algorithms set to True
    for key, val in algo_dict.items():
        if val:
            # initialize specified experimental environments and evaluate
            experiment = Experiment(G=G, k=k, initial_seeds=initial_seeds, p=p, iterations=iterations, use_cache=False, algorithm=alg.get_algorithm(key), name=key, perform_eval=False, threads=1)
            experiment.run()

            # get the time
            delta_time = experiment.delta_time
            avg_time = delta_time / iterations

            times[key].append(avg_time)

            print(f'Average time taken for {key}: {avg_time}')
    return times
