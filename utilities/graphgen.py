from graphviz import Digraph
from sys import argv

graphdata = open(argv[1]).read().split('\n')

dot = Digraph()
for i, row in enumerate(graphdata):
    pairs = row.split(' ')
    for pair in pairs:
        if pair != '':
            neighbor, weight = pair.split(',')
            dot.edge(str(i), str(neighbor), label=str(int(float(weight))))

dot.render('digraph.gv')
