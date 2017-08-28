#!/usr/bin/env python

import sys
import time
import math
from itertools import *

def main(argv):
    start = time.time()
    cities = []
    output = {"path":{}, "distance":99999999999999}
    num = 0

    with open(argv[1]) as f:
        for i in xrange(7):
            f.next()
        for line in f:
            words = line.split(" ")
            cities.append({"num":words[0],"x":words[1],"y":words[2].strip()})
            num += 1

    first = cities.pop(0)
    num -= 1
    for p in permutations(cities):
        count = 0
        distance = 0
        while count <= num:
            if(count == 0):
                distance += math.sqrt(pow(float(first['x']) - float(p[count]['x']), 2) + pow(float(first['y']) - float(p[count]['y']), 2))
            elif(count == num):
                distance += math.sqrt(pow(float(first['x']) - float(p[count-1]['x']), 2) + pow(float(first['y']) - float(p[count-1]['y']), 2))
            else:
                distance += math.sqrt(pow(float(p[count-1]['x']) - float(p[count]['x']), 2) + pow(float(p[count-1]['y']) - float(p[count]['y']), 2))
            count += 1
        if(min(output['distance'], distance) == distance):
            path = list(p)
            path.insert(0,first)
            output = {"path":path, "distance":distance}
    print(output)

    print '\nThis script took ', time.time()-start, ' seconds.'

if __name__ == "__main__":
    main(sys.argv)
