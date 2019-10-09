"""
Task 2 - Generating Probability Tables From Data
"""

# Get data from file, learn parameters
from collections import OrderedDict as odict
import pandas as pd
from itertools import product, combinations
import numpy as np
from tabulate import tabulate


# ================= Code from Week 3 Tutorial ====================================


def allEqualThisIndex(dict_of_arrays, **fixed_vars):
    """
    Helper function to create a boolean index vector into a tabular data structure,
    such that we return True only for rows of the table where, e.g.
    column_a=fixed_vars['column_a'] and column_b=fixed_vars['column_b'].

    This is a simple task, but it's not *quite* obvious
    for various obscure technical reasons.

    It is perhaps best explained by an example.

    >>> all_equal_this_index(
    ...    {'X': [1, 1, 0], Y: [1, 0, 1]},
    ...    X=1,
    ...    Y=1
    ... )
    [True, False, False]
    """
    # base index is a boolean vector, everywhere true
    first_array = dict_of_arrays[list(dict_of_arrays.keys())[0]]
    index = np.ones_like(first_array, dtype=np.bool_)
    for var_name, var_val in fixed_vars.items():
        index = index & (np.asarray(dict_of_arrays[var_name]) == var_val)
    return index


def printFactor(f):
    """
    argument
    `f`, a factor to print on screen
    """
    # Create a empty list that we will fill in with the probability table entries
    table = list()

    # Iterate over all keys and probability values in the table
    for key, item in f['table'].items():
        # Convert the tuple to a list to be able to manipulate it
        k = list(key)
        # Append the probability value to the list with key values
        k.append(item)
        # Append an entire row to the table
        table.append(k)
    # dom is used as table header. We need it converted to list
    dom = list(f['dom'])
    # Append a 'Pr' to indicate the probabity column
    dom.append('Pr')
    print(tabulate(table, headers=dom, tablefmt='orgtbl'))


def transposeGraph(G):
    GT = dict((v, []) for v in G)
    for v in G:
        for w in G[v]:
            if w in GT:
                GT[w].append(v)
            else:
                GT[w] = [v]
    return GT


# From Week 2 Tutorial
def estProbTable(data, var_name, parent_names, outcomeSpace):
    """
    Calculate a dictionary probability table by ML given
    `data`, a dictionary or dataframe of observations
    `var_name`, the column of the data to be used for the conditioned variable and
    `var_outcomes`, a tuple of possible outcomes for the conditiona varible and
    `parent_names`, a tuple of columns to be used for the parents and
    `parent_outcomes` a tuple of all possible parent outcomes
    Return a dictionary containing an estimated conditional probability table.
    """
    var_outcomes = outcomeSpace[var_name]
    parent_outcomes = [outcomeSpace[var] for var in (parent_names)]
    # cartesian product to generate a table of all possible outcomes
    all_parent_combinations = product(*parent_outcomes)

    prob_table = odict()

    for i, parent_combination in enumerate(all_parent_combinations):
        cond_array = []
        parent_vars = dict(zip(parent_names, parent_combination))
        parent_index = allEqualThisIndex(data, **parent_vars)
        for var_outcome in var_outcomes:
            var_index = (np.asarray(data[var_name]) == var_outcome)
            prob_table[tuple(list(parent_combination) + [var_outcome])] = (
                                                                                  var_index & parent_index).sum() / parent_index.sum()

    return {'dom': tuple(list(parent_names) + [var_name]), 'table': prob_table}


# ==========================================================


graph = {
    'LymphNodes': [],
    'Metastasis': ['LymphNodes'],
    'BC': ['Metastasis', 'MC', 'SkinRetract', 'NippleDischarge', 'AD'],
    'MC': [],
    'Age': ['BC'],
    'Location': ['BC'],
    'BreastDensity': ['Mass'],
    'Mass': ['Size', 'Shape', 'Margin'],
    'Size': [],
    'Shape': [],
    'Margin': [],
    'Spiculation': ['Margin'],
    'FibrTissueDev': ['Spiculation', 'NippleDischarge', 'SkinRetract'],
    'NippleDischarge': [],
    'SkinRetract': [],
    'AD': ['FibrTissueDev'],
}

graphT = transposeGraph(graph)

"""
Read the data, and return an outcomeSpace dictionary with
all of the different nodes, and their domains
"""


def getOutcomeSpace(data):
    nodes = []
    outcomes = []

    for x in data:
        nodes.append(x)
        count = 0
        diffList = []
        for val in data[x]:
            if val not in diffList:
                count += 1
                diffList.append(val)
        outcomes.append(diffList)

    outcomeSpace = {}
    for i in range(len(nodes)):
        outcomeSpace[nodes[i]] = tuple(outcomes[i])

    return dict(outcomeSpace)


def learn_bayes_net(graph, file, outcomeSpace, prob_tables):
    with open(file) as h:
        data = pd.read_csv(h)

    # possible outcomes, by variable
    outcomeSpace = getOutcomeSpace(data)

    prob_tables = odict()
    for node, parents in graphT.items():
        prob_tables[node] = estProbTable(  # Estimate the probability for a single table. 1 line
            data,
            node,
            parents,
            outcomeSpace)

    ##############################
    # Test code
    ##############################
    print('estimated P(Location)=')
    printFactor(prob_tables['Shape'])
    print()

    return outcomeSpace, prob_tables


prob_tables = []
outcomeSpace = []

outcomeSpace, prob_tables = learn_bayes_net(graph, 'bc 2.csv', outcomeSpace, prob_tables)
