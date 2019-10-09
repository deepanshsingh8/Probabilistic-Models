"""
Task 3 - Sampling the Bayesian Network - Forward Sampling
"""

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


def getSampleSpace(table, node):

    lst = list(table.items())

    space = list(lst[1])
    space = list(space[1].items())


    return space


def sampleValue(sampleSpace):

    rnd = random.random()

    lst = [0]

    for row in sampleSpace:
        lst.append(row[1])

    lst.append(1)
    lst.sort()

    prob = 0
    # sampling correctly ?????
    for index in range(1, len(lst)):

        if rnd >= lst[index-1] and rnd < lst[index]:
            prob = lst[index]
            if prob == 1:
                prob = lst[index- 1]
            break

    chosenVal = ''

    for val in sampleSpace:
        if val[1] == prob:
            chosenVal = val[0]


    return chosenVal



def sample(graph, prob_tables):

    ordering = topologicalSort(graph)
    samples = {}

    for node in ordering:
        sampleSpace = getSampleSpace(prob_tables[node], node)

        val = sampleValue(sampleSpace)
        samples[node] = val

    return samples

#for x in range(1000):
s = sample(graph, prob_tables)
    #print(s)
