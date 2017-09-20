# Zachary Shumate
# CECS 545 - AI
# Project 3

#!/usr/bin/env python

import sys
import time
import math
import sympy
from sympy import Point
from sympy.geometry import Segment
import matplotlib.pyplot as plt

def graph(output):
    x, y = [], []
    for c in output:
        x.append(c["x"])
        y.append(c["y"])
    # x.append(output[0]["x"])
    # y.append(output[0]["y"])
    plt.plot(x,y)
    plt.pause(.5)
    # plt.show()

def main(argv):
    start = time.time()
    cities = []
    output = {"path":[], "distance":99999999999999}
    num = 0
    edges = []
    plt.ion()

    # read cities from file given as a argument into a list of dictionaries
    with open(argv[1]) as f:
        for i in xrange(7):
            f.next()
        for line in f:
            words = line.split(" ")
            cities.append({"num":words[0],"x":words[1],"y":words[2].strip()})
            num += 1

    edges.append({'edge':Segment((cities[0]['x'],cities[0]['y']),(cities[1]['x'],cities[1]['y'])), 'from':cities[0]['num'], 'to':cities[1]['num']})
    edges.append({'edge':Segment((cities[1]['x'],cities[1]['y']),(cities[2]['x'],cities[2]['y'])), 'from':cities[1]['num'], 'to':cities[2]['num']})
    edges.append({'edge':Segment((cities[2]['x'],cities[2]['y']),(cities[0]['x'],cities[0]['y'])), 'from':cities[2]['num'], 'to':cities[0]['num']})

    for c in cities[3:]:
        output['path'] = []
        count = 0
        distance = 999999999
        n = 0
        for e in edges:
            d = e['edge'].distance((c['x'],c['y']))
            if d < distance:
                distance = d
                n = count
            count += 1
        edges.insert(n,{'edge':Segment((c['x'],c['y']),(cities[int(edges[n]['from'])-1]['x'],cities[int(edges[n]['from'])-1]['y'])), 'from':edges[n]['from'], 'to':c['num']})
        edges[n+1] = {'edge':Segment((c['x'],c['y']),(cities[int(edges[n]['to'])-1]['x'],cities[int(edges[n+1]['to'])-1]['y'])), 'from':c['num'], 'to':edges[n+1]['to']}
        output['path'].append(cities[0])
        for e in edges:
            output['path'].append(cities[int(e['to'])-1])
            plt.clf()
        graph(output['path'])

    sys.exit()

    # # remove starting ciri from list to cut down on the permutations need to generate
    # first = cities.pop(0)
    # num -= 1
    # # generate and loop through each permutation
    # for p in permutations(cities):
    #     count = 0
    #     distance = 0
    #     # calculate the distance between two cities and add to total distance
    #     while count <= num:
    #         if(count == 0):
    #             distance += math.sqrt(pow(float(first['x']) - float(p[count]['x']), 2) + pow(float(first['y']) - float(p[count]['y']), 2))
    #         elif(count == num):
    #             distance += math.sqrt(pow(float(first['x']) - float(p[count-1]['x']), 2) + pow(float(first['y']) - float(p[count-1]['y']), 2))
    #         else:
    #             distance += math.sqrt(pow(float(p[count-1]['x']) - float(p[count]['x']), 2) + pow(float(p[count-1]['y']) - float(p[count]['y']), 2))
    #         count += 1
    #     # overwrite the output if new cycle has shorter distance
    #     if(min(output['distance'], distance) == distance):
    #         path = list(p)
    #         path.insert(0,first)
    #         output = {"path":path, "distance":distance}

    # print outout
    print(output)

    # print time for script to run
    print '\nThis script took ', time.time()-start, ' seconds.'

    # graph output
    graph(output["path"])
    # for c in output["path"]:
    #     x.append(c["x"])
    #     y.append(c["y"])
    # x.append(output["path"][0]["x"])
    # y.append(output["path"][0]["y"])
    # plt.plot(x,y)
    # plt.show()

if __name__ == "__main__":
    main(sys.argv)
