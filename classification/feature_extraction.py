from sys import argv
import numpy as np

label = ''
path  = ''
rawdata = []
for arg in argv[1:]:
    if "--label=" not in arg:
        rawdata.append(open(arg).read().split('\n'))
    elif "--label=" in arg:
        if label == '':
            label = arg.replace('--label=', '')
        else:
            print("Err: label already specified")
            quit()
    else: #should not happen right now
        print('Unexpected argument: ' + arg)
        print('Expecting .grph file, --label= or --path=')

if label == '':
    print("Err: label not specified")
    quit()

features = np.zeros((len(rawdata), 10), dtype='int32')
for i, graph in enumerate(rawdata):
    adjMatrix = np.zeros((len(graph),len(graph)), dtype='int32')
    for r, row in enumerate(graph):
        row = row.split(' ')
        for pair in row:
            split = pair.split(',')
            if len(split) < 2:
                break #done reading row
            adjMatrix[r][int(split[0])] = int(float(split[1]))

    features[i][0] = len(graph) #Number of nodes
    features[i][1] = np.sum(adjMatrix) #Number of edges

outfile = open('data_label=' + label + ".csv", 'w')
for row in features:
    for feature in row:
        outfile.write(str(feature))
        outfile.write(',')
    outfile.write(label)
    outfile.write('\n')
outfile.close()
