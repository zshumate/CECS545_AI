# Zachary Shumate
# CECS 545 - AI
# Project 1

#!/usr/bin/env python

import sys
import time
import math
from itertools import *
import matplotlib.pyplot as plt

def main(argv):
    start = time.time()
    cities = []
    output = {"path":{}, "distance":99999999999999}
    num = 0
    x, y = [], []

    # read cities from file given as a argument into a list of dictionaries
    with open(argv[1]) as f:
        for i in xrange(7):
            f.next()
        for line in f:
            words = line.split(" ")
            cities.append({"num":words[0],"x":words[1],"y":words[2].strip()})
            num += 1

    for c in cities:
        if c["num"] == 1:
            c["next"] = [2,3,4]
        if c["num"] == 2:
            c["next"] = [3]
        if c["num"] == 3:
            c["next"] = [4,5]
        if c["num"] == 4:
            c["next"] = [5,6,7]
        if c["num"] == 5:
            c["next"] = [7,8]
        if c["num"] == 6:
            c["next"] = [8]
        if c["num"] == 7:
            c["next"] = [9,10]
        if c["num"] == 8:
            c["next"] = [9,10,11]
        if c["num"] == 9:
            c["next"] = [11]
        if c["num"] == 10:
            c["next"] = [11]



    sys.exit() # temp, for testing

    # remove starting ciri from list to cut down on the permutations need to generate
    # first = cities.pop(0)
    # num -= 1
    # generate and loop through each permutation
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
    for c in output["path"]:
        x.append(c["x"])
        y.append(c["y"])
    x.append(output["path"][0]["x"])
    y.append(output["path"][0]["y"])
    plt.plot(x,y)
    plt.show()

if __name__ == "__main__":
    main(sys.argv)