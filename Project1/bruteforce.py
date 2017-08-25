#!/usr/bin/env python

import sys
from itertools import *

def main(argv):
    cities = []

    with open(argv[1]) as f:
        for i in xrange(7):
            f.next()
        for line in f:
            words = line.split(" ")
            cities.append({"num":words[0],"x":words[1],"y":words[2].strip()})

    

if __name__ == "__main__":
    main(sys.argv)
