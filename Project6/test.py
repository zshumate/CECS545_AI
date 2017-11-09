import sys, random, time

variables = []
clauses = []
count = 0

with open('./sat_data_20_91/uf20-01.cnf') as f:
    for line in f:
        words = line.strip('\n').split(' ')
        if words[0] == 'c':
            continue
        elif words[0] == 'p':
            variableCount = int(words[2])
            clauseCount = int(words[4])
            for i in xrange(variableCount):
                variables.append(False)
            for i in xrange(clauseCount):
                clauses.append('')
        else:
            for x in words:
                if x == '0' or x == '%':
                    break
                elif x == '':
                    continue
                else:
                    if int(x) > 0:
                        x = str(int(x) - 1)
                    else:
                        x = str(int(x) + 1)
                    clauses[count] += (x + ' ')
            count += 1

print variables
print ''
print clauses
