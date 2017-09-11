# Zachary Shumate
# CECS 545 - AI
# Project 1

#!/usr/bin/env python

import sys
import time
import math
from itertools import *
import matplotlib.pyplot as plt

# need to pass distances for comparison
def depthSearch(cityList, city, distance, prev):
    if 'distance' not in city or distance < city['distance']:
        city['distance'] = distance
        city['prev'] = prev
    if city['next']:
        for n in city['next']:
            nextDistance = distance + math.sqrt(pow(float(city['x']) - float(cityList[n-1]['x']), 2) + pow(float(city['y']) - float(cityList[n-1]['y']), 2))
            depthSearch(cityList, cityList[n-1], nextDistance, city['num'])

def main(argv):
    start = time.time()
    cities = []
    output = {'path':[], 'distance':0}
    num = 0
    x, y = [], []
    count = 10

    # read cities from file given as a argument into a list of dictionaries
    with open(argv[1]) as f:
        for i in xrange(7):
            f.next()
        for line in f:
            words = line.split(' ')
            cities.append({'num':words[0],'x':words[1],'y':words[2].strip()})
            num += 1

    # hardcode the next possible cities
    for c in cities:
        if c['num'] == '1':
            c['next'] = [2,3,4]
        if c['num'] == '2':
            c['next'] = [3]
        if c['num'] == '3':
            c['next'] = [4,5]
        if c['num'] == '4':
            c['next'] = [5,6,7]
        if c['num'] == '5':
            c['next'] = [7,8]
        if c['num'] == '6':
            c['next'] = [8]
        if c['num'] == '7':
            c['next'] = [9,10]
        if c['num'] == '8':
            c['next'] = [9,10,11]
        if c['num'] == '9':
            c['next'] = [11]
        if c['num'] == '10':
            c['next'] = [11]
        if c['num'] == '11':
            c['next'] = []

    # finds the shortest path via depth first search
    depthSearch(cities,cities[0], 0, '0')

    # retrace recorded path and put into output
    output['distance'] = cities[count]
    while count != -1:
        output['path'].insert(0,cities[count])
        count = int(cities[count]['prev']) - 1

    # print outout
    print(output)

    # print time for script to run
    print '\nThis script took ', time.time()-start, ' seconds.'

    # graph output
    for c in output['path']:
        x.append(c['x'])
        y.append(c['y'])
    x.append(output['path'][0]['x'])
    y.append(output['path'][0]['y'])
    plt.plot(x,y)
    plt.show()

if __name__ == '__main__':
    main(sys.argv)
