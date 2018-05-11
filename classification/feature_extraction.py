from sys import argv, stdout
import numpy as np
from heapq import heappush, heappop

def matching(adjMat):
    numNodes = len(adjMat)

    dNodes = [sum(row) for row in adjMat]
    nodes = [(i, dNodes[i]) for i in range(len(adjMat))]
    numExposed = len(adjMat)
    matching = [-1 for i in range(len(adjMat))]

    for i in range(len(adjMat)):
            node, unused = nodes[i]
            neighborColors = set()
            if matching[node] == -1:
                for j in range(len(adjMat)):
                    neighbor, unused = nodes[j]
                    if adjMat[node][neighbor] != 0:
                        if matching[neighbor] == -1:
                            matching[node] = neighbor
                            matching[neighbor] = node
                            numExposed -= 2
                            break

    return(numExposed)

def kruskals(adjMat):
    def same_tree(node, neighbor, trees):
        return trees[node] == trees[neighbor]

    def combine_trees(tree1, tree2, trees):
            trees[tree1] = trees[tree1].union(trees[tree2]) #combine trees
            for node in trees[tree1]:
                    trees[node] = trees[tree1]

    numNodes = len(adjMat)

    treeEdges = []
    treeNodes = {}
    for i in range(numNodes):
            treeNodes[i] = {i}

    edgeHeap = []

    # sort edges
    for node in range(numNodes):
            for neighbor in range(numNodes):
                    if neighbor > node:
                            break; #assume simple, undirected graph
                    edge = adjMat[node][neighbor]
                    if edge > 0: #nonzero weight
                            heappush(edgeHeap, (edge, node, neighbor))

    edge, node, neighbor = heappop(edgeHeap)
    while len(edgeHeap) > 0:
            combine_trees(node, neighbor, treeNodes)
            treeEdges.append((node, neighbor, edge))

            while same_tree(node, neighbor, treeNodes):
                    try:
                            edge, node, neighbor = heappop(edgeHeap)
                    except:
                            break

    treeMatrix = np.zeros((numNodes, numNodes))

    for pair in treeEdges:
            node, neighbor, weight = pair
            treeMatrix[node][neighbor] = weight
            treeMatrix[neighbor][node] = weight

    return(np.sum(treeMatrix))

def dijkstras(adjMat):
    numNodes = len(adjMat)
    root = 0 #defined by problem
    paths = [[] for i in range(numNodes)]
    distances = [-1 for i in range(numNodes)] #-1 signifies infinite distance
    unvisitedNodes = set(i for i in range(numNodes))
    distances[root] = 0

    while (len(unvisitedNodes) > 0):
            unvisitedNodes.remove(root)
            for neighbor in range(numNodes):
                    weight = adjMat[root][neighbor]
                    distance = weight + distances[root]
                    if weight > 0 and (distance < distances[neighbor] or distances[neighbor] == -1):
                            distances[neighbor] = distance
                            paths[neighbor] = paths[root][:]
                            paths[neighbor].append(root + 1) #nodes indexed by 1

            try:
                    root = min(node for node in unvisitedNodes if distances[node] != -1)
            except:
                    break #graph is not connected

    return np.mean(distances) 

#run Tarjan's Algorithm to count strongly connected components
def num_SCCs(adjMat):
    global generateIndex
    dimen = len(adjMat)
    
    SCCs = []
    nodeStack = []
    onStack = np.zeros((dimen), dtype='int32')
    generations = np.zeros((dimen), dtype='int32')
    labels = [i for i in range(dimen)]

    inSCC = np.zeros((dimen), dtype='int32')
    generateIndex = 1 #start from 1 as 0 signifies undefined
    
    def tarjans(currentNode):
        global generateIndex #use same for all function calls

        generations[currentNode] = generateIndex
        labels[currentNode] = generateIndex
        generateIndex += 1

        nodeStack.append(currentNode)
        onStack[currentNode] = True

        #Recurse on neighbors
        for neighbor in range(dimen):
            if adjMat[currentNode][neighbor]:
                if generations[neighbor] == 0:
                    tarjans(neighbor)
                    labels[currentNode] = min(labels[currentNode], generations[neighbor])
                elif onStack[neighbor]:
                    labels[currentNode] = min(labels[currentNode], generations[neighbor])

        if labels[currentNode] == generations[currentNode]: #new SCC found
            SCC = []
            componentNode = nodeStack.pop()
            onStack[componentNode] = False
            SCC.append(componentNode)
            while componentNode != currentNode:
                componentNode = nodeStack.pop()
                onStack[componentNode] = False
                SCC.append(componentNode)
            SCCs.append(SCC)

    for node in range(dimen): #Run tarjans
        if generations[node] == 0:
            tarjans(node)

    largest = max(len(SCC) for SCC in SCCs)

    return len(SCCs), largest

############################### READ GRAPH DATA ################################
label = ''
path  = ''
rawdata = []
training = False
for arg in argv[1:]:
    if arg == '--train':
            training = True
    elif "--label=" not in arg:
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
    features[i][2], features[i][3] = (num_SCCs(adjMatrix))
    features[i][4] = dijkstras(adjMatrix)
    features[i][5] = matching(adjMatrix)

    print(".", end="")
    stdout.flush()
print()

if training:
    outfile = open('data_label_train_' + label + ".csv", 'w')
else:
    outfile = open('data_label_test_' + label + ".csv", 'w')

for row in features:
    for feature in row:
        outfile.write(str(feature))
        outfile.write(',')
    outfile.write(label)
    outfile.write('\n')
outfile.close()
