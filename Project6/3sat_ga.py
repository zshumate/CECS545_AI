'''
Authors: Adam Vest, Dane Copple, Zack Shumate
CECS 545 Final Project
'''


import argparse
import time
import os
import random
import numpy as np


#constants



#options for running solver
class GASATOptions():
    def __init__(self):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument('--data_path', required=True, help="data file containing problem to satisfy")

    def parse_args(self):
        return self.parser.parse_args()


#loads given data file and initializes a graph containing the appropriate nodes
def initialize_graph(data_path):
    graph = TSPGraph()

    f = open("./%s" % data_path)
    lines = f.readlines()[DATA_OFFSET:]
    f.close()

    for line in lines:
        x, y = line.strip().split()[COORDINATES_OFFSET:]
        graph.add_vertex(x, y)

    graph.add_edges()

    return graph

#initializes population according to some strategy
def initialize_population():

#selects parents to mate based on probabilities assigned by parent individual costs
def select_mating_pairs():

#combines two parent solutions to produce a child
def crossover():

#combine population solutions via Wisdom of Crowds and find its weight
def combine_via_woc():

#find the best individual and its cost in the current generation
def get_best_child():

#solve TSP using a genetic algorithm
def ga_solve():
    start_time = time.time()
    population = initialize_population()
    generation_count, no_improvement_count = 0, 0
    best_cost, best_solution = np.inf, None
    combined_solution_costs, best_child_costs = [], []

    while no_improvement_count < args.generations_limit:
        parents_to_mate = select_mating_pairs()
        children = [crossover() for parents in parents_to_mate]
        children = [mutate() for child in children]
        combined_soln, combined_soln_cost = combine_via_woc()
        best_child, best_child_cost = get_best_child()
        population = children

        if best_child_cost < ((1-args.improvement_limit) *  best_cost):
            best_solution = best_child
            best_cost = best_child_cost
            no_improvement_count = 0
        else:
            no_improvement_count += 1

        generation_count += 1
        combined_solution_costs.append((generation_count, combined_soln_cost))
        best_child_costs.append((generation_count, best_child_cost))

        print "Overall Best Solution: %s" % best_solution
        print "Overall Best Solution Cost: %g" % best_cost
        print "Generation %d Combined Solution: %s" % (generation_count, combined_soln)
        print "Generation %d Combined Solution Cost: %g" % (generation_count, combined_soln_cost)
        print "Generation %d Best Child: %s" % (generation_count, best_child)
        print "Generation %d Best Child Cost: %g\n" % (generation_count, best_child_cost)

    print "Execution Time: %g seconds" % (time.time() - start_time)

    if args.visualize_results:


if __name__ == "__main__":
    args = GASATOptions().parse_args()
    ga_solve()
