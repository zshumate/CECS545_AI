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

import math
import matplotlib.pyplot as plt
import sys, random, time
from math import sqrt


coords = []
LAST_SCORE = -1


def woc_score(coords, tour):
    cities = []
    num_cities = len(tour)
    for i in range(num_cities):
       city_i = tour[i]
       a, b = coords[city_i]
       cities.append({"x":a,"y":b})
    city_0 = tour[0]
    a, b = coords[city_0]
    cities.append({"x":a,"y":b})

    distance = 0
    for i in xrange(len(cities)-1):
        distance += getDistance(cities[i]['x'], cities[i]['y'], cities[i+1]['x'], cities[i+1]['y'], )
    return distance

# Find the distance between two points
def getDistance(x1, y1, x2, y2):
    return math.sqrt(pow(float(x1) - float(x2), 2) + pow(float(y1) - float(y2), 2))

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
   start = time.time()
   global coords
   cm     = []
   cities = []
   crowd = []
   finalRoute = []
   current = 0

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
   ga.setGenerations(10000)
   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.002)                                    # choises are 0.02 (1) or 0.002 (2)
   ga.setPopulationSize(80)

   ga.evolve(freq_stats=500)
   pop = ga.getPopulation()
   best = ga.bestIndividual()

   # graph and print the best route
   write_tour_to_img(coords, best, "tsp_result.png")
   print(best)

   # initialize a matrix to perform a wisom of crowds analysis
   for i in xrange(len(cities)):
       nestedList = []
       for j in xrange(len(cities)):
           nestedList.append(0)
       crowd.append(nestedList)

   # populate matrix with occuences of specific edges
   for i in xrange(20):
       for j in xrange(len(cities)):
           if j+1 == len(cities):
               minimum = min(pop[i][j], pop[i][0])
               maximum = max(pop[i][j], pop[i][0])
               crowd[minimum][maximum] += 1
           else:
               minimum = min(pop[i][j], pop[i][j+1])
               maximum = max(pop[i][j], pop[i][j+1])
               crowd[minimum][maximum] += 1

   # find best path from wisdom of crowds
   finalRoute.append(0)
   while(len(finalRoute) < len(cities)):
       x, wisdom = 0, 0
       for i in xrange(len(cities)):
           minimum = min(current, i)
           maximum = max(current, i)
           if crowd[minimum][maximum] > wisdom and i not in finalRoute:
               wisdom = crowd[minimum][maximum]
               x = i
       current = x
       finalRoute.append(current)

   print finalRoute
   print 'woc Score: %s' % woc_score(coords, finalRoute)
   write_tour_to_img(coords, finalRoute, "woc_result.png")

   # print time for script to run
   print '\nThis script took ', time.time()-start, ' seconds.'


if __name__ == "__main__":
    main(sys.argv)
