import random

# Recursively find child nodes such that nodes first in the ordering have no more unvisited children.
def topologicalSortRec(G, v, ordering, visited):

    visited.append(v)
    for child in G[v]:
        if child not in visited:
            topologicalSortRec(G, child, ordering, visited)

    ordering.insert(0, v)

#Find a topological ordering on the graph
def topologicalSort(graph):

    ordering = []
    visited = []

    for node in graph:
        if node not in visited:
            topologicalSortRec(graph, node, ordering, visited)


    return ordering  # return the stack - ordering on the graph


def getSampleSpace(table, samples, node):

   # print(table)

    keys = list(table['dom'])

    nodeIndex = keys.index(node)

    observed = []
    indexes = {}

    for i in samples:
        if i in keys:
            observed.append(i)
            indexes[keys.index(i)] = i


    space = []

    listTable = list(table['table'].items())

    for example in listTable:
        nodes = list(example[0])
        add = True
        for i in indexes.keys():
            if nodes[i] != samples[indexes[i]]:
                add = False
                break
        #Add the row from the table with the correctly observed data
        if add == True:
            space.append(example)


    return space, nodeIndex


def sampleValue(sampleSpace, nodeIndex):


    rnd = random.random()

    lst = []
    names = {}
    for row in sampleSpace:
        lst.append(row[1])
        names[str(row[1])] = list(row[0])[nodeIndex]

    lst.sort()

    lst.insert(0, 0)

    #Split up the probabilities into 'regions' for the rnd to fall into
    regions = []
    sumVal = 0
    for i in range(1, len(lst)):
        sumVal += lst[i - 1]
        regions.append(lst[i] + sumVal)


    lst.pop(0)



    for indx in range(len(regions)):
        if rnd < regions[indx]:
            chosen = indx
            break

    chosenVal = names[str(lst[chosen])]



    return chosenVal



def sample(graph, prob_tables): #, queryNode, numObserved):

    ordering = topologicalSort(graph)
    samples = {}
    #samples = {'Age' : '50-74', 'Location':'LowInQuad'} #for testing

    for node in ordering:
        sampleSpace, nodeIndex = getSampleSpace(prob_tables[node], samples, node)

        val = sampleValue(sampleSpace, nodeIndex)
        samples[node] = val

    return samples

#for x in range(1000):
s = sample(graph, prob_tables)
print(s)
