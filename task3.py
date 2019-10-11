#Task 3

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

#Returns a table with the subset of entries to consider for sampling - based on evidence
def getSampleSpace(table, samples, node):

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

    #Iterate through the table values, and take the ones with the correct data
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

# Use a random number to generate a value from the outcomeSpace of var given the Sample Space probabilities
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

#Sample from the graph in topological order
def sample(graph, prob_tables):

    ordering = topologicalSort(graph)
    samples = {}

    for node in ordering:
        sampleSpace, nodeIndex = getSampleSpace(prob_tables[node], samples, node)

        val = sampleValue(sampleSpace, nodeIndex)
        samples[node] = val

    return samples

# ================== Code from wk  3 tutorial ======================
def normalize(f):
    """
    argument
    `f`, factor to be normalized.

    Returns a new factor f' as a copy of f with entries that sum up to 1
    """
    table = list()
    sum = 0
    for k, p in f['table'].items():
        sum = sum + p
    for k, p in f['table'].items():
        table.append((k, p/sum))
    return {'dom': f['dom'], 'table': odict(table)}

def prob(factor, *entry):
    """
    argument
    `factor`, a dictionary of domain and probability values,
    `entry`, a list of values, one for each variable in the same order as specified in the factor domain.

    Returns p(entry)
    """

    return factor['table'][entry]     # insert your code here, 1 line

def join(f1, f2, outcomeSpace):
    """
    argument
    `f1`, first factor to be joined.
    `f2`, second factor to be joined.
    `outcomeSpace`, dictionary with the domain of each variable

    Returns a new factor with a join of f1 and f2
    """

    # First, we need to determine the domain of the new factor. It will be union of the domain in f1 and f2
    # But it is important to eliminate the repetitions
    common_vars = list(f1['dom']) + list(set(f2['dom']) - set(f1['dom']))

    # We will build a table from scratch, starting with an empty list. Later on, we will transform the list into a odict
    table = list()

    # Here is where the magic happens. The product iterator will generate all combinations of varible values
    # as specified in outcomeSpace. Therefore, it will naturally respect observed values
    for entries in product(*[outcomeSpace[node] for node in common_vars]):

        # We need to map the entries to the domain of the factors f1 and f2
        entryDict = dict(zip(common_vars, entries))
        f1_entry = (entryDict[var] for var in f1['dom'])
        f2_entry = (entryDict[var] for var in f2['dom'])

        # Insert your code here
        p1 = prob(f1, *f1_entry)           # Use the fuction prob to calculate the probability in factor f1 for entry f1_entry
        p2 = prob(f2, *f2_entry)           # Use the fuction prob to calculate the probability in factor f2 for entry f2_entry

        # Create a new table entry with the multiplication of p1 and p2
        table.append((entries, p1 * p2))
    return {'dom': tuple(common_vars), 'table': odict(table)}



def p_joint(outcomeSpace, cond_tables, nodeList):


    if len(nodeList) < 2:
        return cond_tables

    """
    argument
    `outcomeSpace`, dictionary with domain of each variable
    `cond_tables`, conditional probability distributions estimated from data

    Returns a new factor with full joint distribution
    """

    p = join(cond_tables[nodeList[0]],  cond_tables[nodeList[1]], outcomeSpace)
    for n in range(2, len(nodeList)):
        p = join(p, cond_tables[nodeList[n]], outcomeSpace)

    return p


def marginalize(f, var, outcomeSpace):
    """
    argument
    `f`, factor to be marginalized.
    `var`, variable to be summed out.
    `outcomeSpace`, dictionary with the domain of each variable

    Returns a new factor f' with dom(f') = dom(f) - {var}
    """

    # Let's make a copy of f domain and convert it to a list. We need a list to be able to modify its elements
    new_dom = list(f['dom'])


    #########################
    # Insert your code here #
    #########################
    new_dom.remove(var)
    # Remove var from the list new_dom by calling the method remove(). 1 line
    table = list()                 # Create an empty list for table. We will fill in table from scratch. 1 line
    for entries in product(*[outcomeSpace[node] for node in new_dom]):
        s = 0;                     # Initialize the summation variable s. 1 line

        # We need to iterate over all possible outcomes of the variable var
        for val in outcomeSpace[var]:
            # To modify the tuple entries, we will need to convert it to a list
            entriesList = list(entries)
            # We need to insert the value of var in the right position in entriesList
            entriesList.insert(f['dom'].index(var), val)


            #########################
            # Insert your code here #
            #########################

            p = prob(f, *tuple(entriesList))     # Calculate the probability of factor f for entriesList. 1 line
            s = s + p                            # Sum over all values of var by accumulating the sum in s. 1 line

        # Create a new table entry with the multiplication of p1 and p2
        table.append((entries, s))
    return {'dom': tuple(new_dom), 'table': odict(table)}


def evidence(var, e, outcomeSpace):
    """
    argument
    `var`, a valid variable identifier.
    `e`, the observed value for var.
    `outcomeSpace`, dictionary with the domain of each variable

    Returns dictionary with a copy of outcomeSpace with var = e
    """
    newOutcomeSpace = outcomeSpace.copy()      # Make a copy of outcomeSpace with a copy to method copy(). 1 line
    newOutcomeSpace[var] = (e,)                # Replace the domain of variable var with a tuple with a single element e. 1 line
    return newOutcomeSpace

def query(p, outcomeSpace, q_vars, q_evi):
    """
    argument
    `p`, probability table to query.
    `outcomeSpace`, dictionary will variable domains
    `q_vars`, list of variables in query head
    `q_evi`, dictionary of evidence in the form of variables names and values

    Returns a new factor NORMALIZED factor will all hidden variables eliminated as evidence set as in q_evi
    """

    # Let's make a copy of these structures, since we will reuse the variable names
    pm = p.copy()
    outSpace = outcomeSpace.copy()

    # First, we set the evidence
    for var_evi, e in q_evi.items():
        outSpace = evidence(var_evi, e, outSpace)

    # Second, we eliminate hidden variables NOT in the query
    for var in outSpace:
        if not var in q_vars:
            pm = marginalize(pm, var, outSpace)

    return normalize(pm)

#=========================================================================

queryNodes = list(outcomeSpace.keys())
p = p_joint(outcomeSpace, prob_tables, queryNodes)
#########################
# Test code
#########################
printFactor(query(p, outcomeSpace,['BC'], {'Age':'50-74', 'Location':'UpInQuad'}))



#Different Queries for the network

#Bayesian Network
printFactor(query(p, outcomeSpace,['LymphNodes', 'BC'], {'Metastasis' : 'no'}))
#more queries....


def querySample(samples, var, var_evi, outcomeSpace):

    if len(samples) == 0:
        return

    #Initalise frequency dictionary
    frequencies = {}
    for k in samples[0]:
        frequencies[k] = {}
        for o in outcomeSpace[k]:
            frequencies[k][o] = 0

    for s in samples:
        discard = False
        for key, it in s.items():
            if key in var_evi:
                if var_evi[key] != it:
                    discard = True
                    break


        #Discard sample if disagrees with evidence
        if discard == True:
            continue

        #Update variable frequencies
        for key in var:
            frequencies[key][s[key]] += 1
    print(frequencies[var[0]])

    return 0


generatedSamples = []

# Generate 1000 Samples from forward sampling on the network
for x in range(1000):
    s = sample(graph, prob_tables)
    generatedSamples.append(s)


#Sample queries (same as bayesian)
querySample(generatedSamples, ['BC'], {'Mass':'No', 'Age':'35-49'}, outcomeSpace)
#more queries...
