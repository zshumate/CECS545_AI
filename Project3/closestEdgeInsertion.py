# Zachary Shumate
# CECS 545 - AI
# Project 3

#!/usr/bin/env python

import sys
import time
import math
import matplotlib.pyplot as plt

# Graph each iteration
def graph(output, cities):
    x, y = [], []
    for c in output:
        x.append(c["x"])
        y.append(c["y"])
    plt.plot(x,y)
    plt.pause(.5)

# Find the distance between two points
def getDistance(x1, y1, x2, y2):
    return math.sqrt(pow(float(x1) - float(x2), 2) + pow(float(y1) - float(y2), 2))

def main(argv):
    start = time.time()
    cities = []
    output = {"path":[], "distance":0}
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

    # start with three cities, since it is trivial
    edges.append({'xFrom':cities[0]['x'], 'yFrom':cities[0]['y'], 'xTo':cities[1]['x'], 'yTo':cities[1]['y'], 'from':cities[0]['num'], 'to':cities[1]['num']})
    edges.append({'xFrom':cities[1]['x'], 'yFrom':cities[1]['y'], 'xTo':cities[2]['x'], 'yTo':cities[2]['y'], 'from':cities[1]['num'], 'to':cities[2]['num']})
    edges.append({'xFrom':cities[2]['x'], 'yFrom':cities[2]['y'], 'xTo':cities[0]['x'], 'yTo':cities[0]['y'], 'from':cities[2]['num'], 'to':cities[0]['num']})

    # iterate through the remaining cities
    for c in cities[3:]:
        output['path'] = []
        count = 0
        distance = 999999999
        n = 0
        # find the closest edge
        for e in edges:
            d = getDistance(c['x'], c['y'], e['xFrom'], e['yFrom']) + getDistance(c['x'], c['y'], e['xTo'], e['yTo']) - getDistance(e['xFrom'], e['yFrom'], e['xTo'], e['yTo'])
            if d < distance:
                distance = d
                n = count
            count += 1
        # replace the closest edge with two new edges
        edges.insert(n,{'xFrom':edges[n]['xFrom'], 'yFrom':edges[n]['yFrom'], 'xTo':c['x'], 'yTo':c['y'], 'from':edges[n]['from'], 'to':c['num']})
        edges[n+1] = {'xFrom':c['x'], 'yFrom':c['y'], 'xTo':edges[n+1]['xTo'], 'yTo':edges[n+1]['yTo'], 'from':c['num'], 'to':edges[n+1]['to']}
        output['path'].append(cities[0])
        for e in edges:
            output['path'].append(cities[int(e['to'])-1])
        plt.clf()
        # fig = plt.figure()                    # This has been commented out to reduce memory usage if you run this
        # ax = fig.add_subplot(111)             # This code provides the annotations for the city numbers
        # for c in cities:
        #     ax.annotate('%s' % c['num'], xy=(c['x'], c['y']), textcoords='data')
        graph(output['path'], cities)
    time.sleep(2)

    count = 0
    while count < len(output['path'])-1:
        output['distance'] += getDistance(output['path'][count]['x'], output['path'][count]['y'], output['path'][count+1]['x'], output['path'][count+1]['y'])
        count += 1

    # print outout
    print(output)

    # print time for script to run
    print '\nThis script took ', time.time()-start, ' seconds.'

if __name__ == "__main__":
    main(sys.argv)
