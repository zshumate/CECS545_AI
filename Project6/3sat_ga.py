'''
Authors: Adam Vest, Dane Copple, Zack Shumate
CECS 545 Final Project
'''


import argparse
import time
import random
import os
import numpy as np
import matplotlib.pyplot as plt


#constants
VAR_COUNT_OFFSET = 2
CLAUSE_COUNT_OFFSET = 3


#options for running solver
class GASATOptions():
    def __init__(self):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument('--data_path', required=True, help="data file containing problem to satisfy")
        self.parser.add_argument('--initialization_strategy', default="random", help="initialization strategy for GA population")
        self.parser.add_argument('--population_size', type=int, default=100, help="size of GA population")
        self.parser.add_argument('--selection_strategy', default="bin", help="selection strategy for GA")
        self.parser.add_argument('--number_of_bins', type=int, default=5, help="number of bins for binning selection strategy")
        self.parser.add_argument('--crossover_strategy', default="random", help="crossover strategy for GA")
        self.parser.add_argument('--mutation_strategy', default="point", help="mutation strategy for GA")
        self.parser.add_argument('--mutation_prob', type=float, default=.2, help="mutation probability")
        self.parser.add_argument('--generations_limit', type=int, default=500, help="number of generations to continue w/o improvement")
        self.parser.add_argument('--improvement_limit', type=int, default=1, help="min number of constraints to satisfy to continue training")
        self.parser.add_argument('--visualize_results', type=int, default=1, help="whether to visualize results")
        self.parser.add_argument('--save_results', type=int, default=0, help="whether to save result images")

    def parse_args(self):
        return self.parser.parse_args()

#solver structure for 3-SAT
class SATSolver():
    def __init__(self, data_path):
        self.clauses = []
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
                else:
                    self.clauses.append([int(words[i]) for i in range(len(words[:-1]))])

    def makes_true(self, clause, variables):
        for var in clause:
            if (var > 0 and variables[var-1] == 1) or (var < 0 and variables[(-1*var)-1] == 0):
                return 1

        return 0

    def test_solution(self, variables):
        true_count = 0

        for clause in self.clauses:
            true_count += self.makes_true(clause, variables)

        return true_count

    def test_variable(self, variables, i):
        true_count = 0

        if variables[i]:
            for clause in self.clauses:
                if (i+1) in clause:
                    true_count += 1
        else:
            for clause in self.clauses:
                if -1*(i+1) in clause:
                    true_count += 1

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
    # elif selection_strategy == "ordered":
    #
    else:
        raise NotImplementedError("Invalid choice of selection strategy!")

    return parent_pairs

#combines two parent solutions to produce a child
def crossover(solver, parents, crossover_strategy):
    child = []

    if crossover_strategy == "random":
        for i in range(len(parents[0])):
            if(np.random.rand() > .5):
                child.append(parents[0][i])
            else:
                child.append(parents[1][i])
    elif crossover_strategy == "standard":
        idx = np.random.randint(len(parents[0]))
        child1, child2 = np.concatenate((parents[0][:idx], parents[1][idx:])), np.concatenate((parents[1][:idx], parents[0][idx:]))
        child = child1 if solver.test_solution(child1) >= solver.test_solution(child2) else child2
    elif crossover_strategy == "greedy":
        for i in range(len(parents[0])):
            if parents[0][i] == parents[1][i]:
                child.append(parents[0][i])
            else:
                if solver.test_variable(parents[0], i) >= solver.test_variable(parents[1], i):
                    child.append(parents[0][i])
                else:
                    child.append(parents[1][i])
    else:
        raise NotImplementedError("Invalid choice of crossover strategy!")

    return child

#mutates a chromosome within a member of the population
def mutate(child, mutation_prob, mutation_strategy):
    if np.random.rand() < mutation_prob:
        if mutation_strategy == "point":
            rand_idx = np.random.randint(len(child))
            child[rand_idx] = 0 if child[rand_idx] == 1 else 1
	elif mutation_strategy == "pairswap":
	    randomNumber = np.random.randint(len(child))
	    while randomNumber != 0:
		switch1 = np.random.randint(len(child))
		switch2 = np.random.randint(len(child))
		child[switch1], child[switch2] = child[switch2], child[switch1]
		randomNumber -= 1
        else:
            raise NotImplementedError("Invalid choice of mutation strategy!")

    return child

#combine population solutions via Wisdom of Crowds and find its weight
def combine_via_woc(population, woc_strategy):
    if woc_strategy == "weighted":
        
    else

#find the best individual and its cost in the current generation
def get_best_child(solver, children):
    best_individual_cost = (None, 0)
    individual_costs = [(child, solver.test_solution(child)) for child in children]

    for i in range(len(individual_costs)):
        if individual_costs[i][1] > best_individual_cost[1]:
            best_individual_cost = individual_costs[i]

    return best_individual_cost

#visualize GA results
def visualize_generation_costs(num_variables, num_clauses, best_child_costs, save_results):
    generations, child_costs = [], []

    # for generation_data in combined_solution_costs:
    #     generations.append(generation_data[0])
    #     combined_costs.append(generation_data[1])

    for generation_data in best_child_costs:
        generations.append(generation_data[0])
        child_costs.append(generation_data[1])

    # plt.plot(generations, combined_costs, label="Combined Solution Costs", color="navy")
    plt.plot(generations, child_costs, label="Best Child Costs", color="darkorange")
    plt.xlabel("Generation")
    plt.ylabel("Number of Unsatified Constraints")
    plt.title("Generation vs. Cost (%d, %d)" % (num_variables, num_clauses))
    plt.legend(loc="upper right")

    if save_results:
        file_count = len([name for name in os.listdir("./images") if os.path.isfile("./images/" + name)])
        plt.savefig("./images/Result%s.png" % (file_count+1))

    plt.show()

#solve TSP using a genetic algorithm
def ga_solve(solver, args):
    start_time = time.time()
    population = initialize_population(solver, args.population_size, args.initialization_strategy)
    generation_count, no_improvement_count = 0, 0
    best_cost, best_solution, num_clauses = 0, None, solver.get_num_clauses()
    combined_solution_costs, best_child_costs = [], []

    while no_improvement_count < args.generations_limit:
        parents_to_mate = select_mating_pairs(solver, population, args.number_of_bins, args.selection_strategy)
        children = [crossover(solver, parents, args.crossover_strategy) for parents in parents_to_mate]
        children = [mutate(child, args.mutation_prob, args.mutation_strategy) for child in children]
        # combined_soln, combined_soln_cost = combine_via_woc()
        best_child, best_child_cost = get_best_child(solver, children)
        population = children

        if best_child_cost >= (args.improvement_limit + best_cost):
            best_solution = best_child
            best_cost = best_child_cost
            no_improvement_count = 0
        else:
            no_improvement_count += 1

        generation_count += 1
        # combined_solution_costs.append((generation_count, num_clauses-combined_soln_cost))
        best_child_costs.append((generation_count, num_clauses-best_child_cost))

        print "Overall Best Solution: %s" % best_solution
        print "Overall Best Solution Cost: %g" % (num_clauses-best_cost)
        # print "Generation %d Combined Solution: %s" % (generation_count, combined_soln)
        # print "Generation %d Combined Solution Cost: %g" % (generation_count, num_clauses-combined_soln_cost)
        print "Generation %d Best Child: %s" % (generation_count, best_child)
        print "Generation %d Best Child Cost: %g\n" % (generation_count, num_clauses-best_child_cost)

        if num_clauses-best_cost == 0:
            print "* 3SAT INSTANCE SOLVED *\n"
            break

    print "Execution Time: %g seconds" % (time.time() - start_time)

    if args.visualize_results:
        visualize_generation_costs(solver.get_num_variables(), num_clauses, best_child_costs, args.save_results)


if __name__ == "__main__":
    args = GASATOptions().parse_args()
    sat_solver = SATSolver(args.data_path)
    ga_solve(sat_solver, args)
