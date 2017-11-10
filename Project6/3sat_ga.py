'''
Authors: Adam Vest, Dane Copple, Zack Shumate
CECS 545 Final Project
'''


import argparse
import time
import random
import numpy as np


#constants
VAR_COUNT_OFFSET = 2
CLAUSE_COUNT_OFFSET = 3


#options for running solver
class GASATOptions():
    def __init__(self):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument('--data_path', default="./sat_data_20_91/uf20-01.cnf", help="data file containing problem to satisfy")
        self.parser.add_argument('--initialization_strategy', default="random", help="initialization strategy for GA population")
        self.parser.add_argument('--population_size', type=int, default=100, help="size of GA population")
        self.parser.add_argument('--selection_strategy', default="bin", help="selection strategy for GA")
        self.parser.add_argument('--number_of_bins', type=int, default=5, help="number of bins for binning selection strategy")
        self.parser.add_argument('--generations_limit', type=int, default=100, help="number of generations to continue w/o improvement")
        self.parser.add_argument('--visualize_results', type=int, default=1, help="whether to visualize results")

    def parse_args(self):
        return self.parser.parse_args()

#solver structure for 3-SAT
class SATSolver():
    def __init__(self, data_path):
        self.variables, self.clauses = [], []
        self.variable_count, self.clause_count = 0, 0

        with open(data_path) as f:
            for line in f:
                words = line.split()

                if words[0] == "c":
                    continue
                elif words[0] == "%":
                    break
                elif words[0] == "p":
                    self.variable_count = int(words[VAR_COUNT_OFFSET])
                    self.clause_count = int(words[CLAUSE_COUNT_OFFSET])
                    self.variables = [False for i in range(self.variable_count)]
                else:
                    clause = []

                    for i in range(len(words[:-1])):
                        clause.append(int(words[i]))

                    self.clauses.append(clause)

    def makes_true(self, clause, variables):
        for var in clause:
            if var > 0 and variables[var-1] == 1:
                return 1
            elif var < 0  and variables[(-1*var)-1] == 0:
                return 1

        return 0

    def test_solution(self, variables):
        true_count = 0

        for clause in self.clauses:
            true_count += self.makes_true(clause, variables)

        return true_count

    def get_num_variables(self):
        return self.variable_count

    def get_num_clauses(self):
        return self.clause_count


# initializes population according to some strategy
def initialize_population(solver, population_size, initialization_strategy):
    if initialization_strategy == "random":
        population = [np.random.choice([0, 1], size=solver.get_num_variables()) for i in range(population_size)]
    else:
        raise NotImplementedError("Invalid choice of initialization strategy!")

    return population

#selects parents to mate based on probabilities assigned by parent individual costs
def select_mating_pairs(solver, population, number_of_bins, selection_strategy):
    parent_pairs = []

    if selection_strategy == "bin":
        individual_costs = [(i, solver.test_solution(population[i])) for i in range(len(population))]
        individual_costs.sort(key=lambda x: x[1])
        n = len(population) / number_of_bins
        bins = [individual_costs[i:i+n] for i in range(0, len(individual_costs), n)]

        for i in range(len(bins)):
            bins[i] = [pair[0] for pair in bins[i]]

        bin_percent = 1.0 / sum(range(1, number_of_bins+1))
        intervals, begin_interval, end_interval = [], 0.0, 0.0

        for i in range(len(bins)):
            interval_value = (i+1) * (bin_percent / len(bins[i]))

            for individual in bins[i]:
                end_interval += interval_value
                intervals.append((individual, begin_interval, end_interval))
                begin_interval = end_interval

        for i in range(len(population)):
            i, j = random.random(), random.random()
            parent1 = [x[0] for x in intervals if x[1] <= i < x[2]][0]
            parent2 = [x[0] for x in intervals if x[1] <= j < x[2]][0]

            if individual_costs[parent1][1] > individual_costs[parent2][1]:
                parent_pairs.append((population[parent1], population[parent2]))
            else:
                parent_pairs.append((population[parent2], population[parent1]))
    else:
        raise NotImplementedError("Invalid choice of selection strategy!")

    return parent_pairs

#combines two parent solutions to produce a child
def crossover():
    print "hi"

#mutates a chromosome within a member of the population
def mutation(variables):
    rand = random.randint(0,VAR_COUNT_OFFSET)
    variables[rand] = !variables[rand]

#combine population solutions via Wisdom of Crowds and find its weight
def combine_via_woc():
    print "hi"

#find the best individual and its cost in the current generation
def get_best_child():
    print "hi"

#solve TSP using a genetic algorithm
def ga_solve(solver, args):
    start_time = time.time()
    population = initialize_population(solver, args.population_size, args.initialization_strategy)
    generation_count, no_improvement_count = 0, 0
    best_cost, best_solution = np.inf, None
    combined_solution_costs, best_child_costs = [], []

    while no_improvement_count < args.generations_limit:
        parents_to_mate = select_mating_pairs(solver, population, args.number_of_bins, args.selection_strategy)
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
        print "hi"


if __name__ == "__main__":
    args = GASATOptions().parse_args()
    sat_solver = SATSolver(args.data_path)
    ga_solve(sat_solver, args)
