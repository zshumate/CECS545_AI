from cuber import *

c = Cube()

for edges in xrange(0, 14, 2):
    print "Bad edges: {}".format(edges)
    for count in xrange(10):
        print gen_known_scramble(edges)
        
c.display()
print c.bad_edge_count()
print ""
c.execute(gen_scramble(),reset=True,display=True)
print c.bad_edge_count()
