# Zachary Shumate
# CECS 545 - AI
# Project 4

#!/usr/bin/env python

from pyevolve import G1DList, GAllele
from pyevolve import GSimpleGA
from pyevolve import Mutators
from pyevolve import Crossovers
from pyevolve import Consts
from pyevolve import DBAdapters

import matplotlib.pyplot as plt
import sys, random
from math import sqrt


coords = []
LAST_SCORE = -1


def cartesian_matrix(coords):
   """ A distance matrix """
   matrix = {}
   for i,(x1,y1) in enumerate(coords):
      for j,(x2,y2) in enumerate(coords):
         dx, dy = x1-x2, y1-y2
         dist = sqrt(dx*dx + dy*dy)
         matrix[i,j] = dist
   return matrix

def tour_length(matrix, tour, num):
   """ Returns the total length of the tour """
   total = 0
   t = tour.getInternalList()
   for i in range(num):
      j      = (i+1)%num
      total += matrix[t[i], t[j]]
   return total

def write_tour_to_img(coords, tour, img_file):
   """ The function to plot the graph """
   x, y = [], []
   num_cities = len(tour)
   for i in range(num_cities):
      city_i = tour[i]
      a, b = coords[city_i]
      x.append(a)
      y.append(b)
   city_0 = tour[0]
   a, b = coords[city_0]
   x.append(a)
   y.append(b)

   plt.clf()
   plt.plot(x,y)
   plt.savefig(img_file)
   print "The plot was saved into the %s file." % (img_file,)

def G1DListTSPInitializator(genome, **args):
   """ The initializator for the TSP """
   lst = [i for i in xrange(genome.getListSize())]
   random.shuffle(lst)
   genome.setInternalList(lst)

def evolve_callback(ga_engine):
   global LAST_SCORE
   if ga_engine.getCurrentGeneration() % 100 == 0:
      best = ga_engine.bestIndividual()
      if LAST_SCORE != best.getRawScore():
         write_tour_to_img( coords, best, "tspimg/tsp_result_%d.png" % ga_engine.getCurrentGeneration())
         LAST_SCORE = best.getRawScore()
   return False

def main(argv):
   global coords
   cm     = []
   cities = []

   # read cities from file given as a argument into a list of dictionaries
   with open(argv[1]) as f:
       for i in xrange(7):
           f.next()
       for line in f:
           words = line.split(" ")
           cities.append({"num":words[0],"x":words[1],"y":words[2].strip()})

   # put coordinates into a form best suited for the funtion to parse
   coords = [(float(c['x']), float(c['y']))
                 for c in cities]
   cm     = cartesian_matrix(coords)
   genome = G1DList.G1DList(len(coords))

   # initialize evaluation function and crossover function
   genome.evaluator.set(lambda chromosome: tour_length(cm, chromosome, len(cities)))
   genome.crossover.set(Crossovers.G1DListCrossoverEdge)        # choices are G1DListCrossoverEdge (A) or G1DListCrossoverCutCrossfill (B)
   genome.initializator.set(G1DListTSPInitializator)

   ga = GSimpleGA.GSimpleGA(genome)
   # set up database to generate improvment curve graph after genetic algorithm
   sqlite_adapter = DBAdapters.DBSQLite(identify="ex1")
   ga.setDBAdapter(sqlite_adapter)
   # initialized genetic algorithm variables (generations, crossover rate, mutation rate, and population size)
   ga.setGenerations(100000)
   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.002)                                    # choises are 0.02 (1) or 0.002 (2)
   ga.setPopulationSize(80)

   ga.evolve(freq_stats=500)
   best = ga.bestIndividual()

   # graph and print the best route
   write_tour_to_img(coords, best, "tsp_result.png")
   print(best)

   pop = ga.getPopulation().sort()



if __name__ == "__main__":
    main(sys.argv)
