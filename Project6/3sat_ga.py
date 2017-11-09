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
variables = []
clauses = []
count = 0


#options for running solver
class GASATOptions():
    def __init__(self):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument('--data_path', required=True, help="data file containing problem to satisfy")
        self.parser.add_argument('--visualize_results', type=int, default=1, help="whether to visualize results")

    def parse_args(self):
        return self.parser.parse_args()


#reads in data from a provided file
def read_file(data_path):
    f = open("%s" % data_path)
    with open('./%s' % data_path) as f:
        for line in f:
            words = line.strip('\n').split(' ')
            if words[0] == 'c':
                continue
            elif words[0] == 'p':
                variableCount = int(words[2])
                clauseCount = int(words[4])
                for i in xrange(variableCount):
                    variables.append(False)
                for i in xrange(clauseCount):
                    clauses.append('')
            else:
                for x in words:
                    if x == '0' or x == '%':
                        break
                    elif x == '':
                        continue
                    else:
                        if int(x) > 0:
                            x = str(int(x) - 1)
                        else:
                            x = str(int(x) + 1)
                        clauses[count] += (x + ' ')
                count += 1

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
