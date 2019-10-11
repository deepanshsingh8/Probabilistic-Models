# Make division default to floating-point, saving confusion
from __future__ import division
from __future__ import print_function

# Necessary libraries
import numpy as np
import pandas as pd
import task2

# combinatorics
from itertools import product, combinations
# ordered dictionaries are useful for keeping ordered sets of varibles
from collections import OrderedDict as odict
# visualise our graph
from graphviz import Digraph

# table formating for screen output
from tabulate import tabulate

# easier debugging display
pd.set_option('display.multi_sparse', False)
from pprint import pprint


def prob(factor, *entry):
    """
    argument
    `factor`, a dictionary of domain and probability values,
    `entry`, a list of values, one for each variable in the same order as specified in the factor domain.

    Returns p(entry)
    """

    return factor['table'][entry]

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
        p1 = prob(f1, *f1_entry)  # Use the fuction prob to calculate the probability in factor f1 for entry f1_entry
        p2 = prob(f2, *f2_entry)  # Use the fuction prob to calculate the probability in factor f2 for entry f2_entry

        # Create a new table entry with the multiplication of p1 and p2
        table.append((entries, p1 * p2))
    return {'dom': tuple(common_vars), 'table': odict(table)}


def p_joint(outcomeSpace, cond_tables):
    """
    argument
    `outcomeSpace`, dictionary with domain of each variable
    `cond_tables`, conditional probability distributions estimated from data

    Returns a new factor with full joint distribution
    """
    p = join(cond_tables['BC'], cond_tables['Mass'], outcomeSpace)
    p = join(p, cond_tables['AD'], outcomeSpace)
    p = join(p, cond_tables['MC'], outcomeSpace)
    p = join(p, cond_tables['S'], outcomeSpace)
    p = join(p, cond_tables['V'], outcomeSpace)
    p = join(p, cond_tables['H'], outcomeSpace)
    p = join(p, cond_tables['L'], outcomeSpace)
    p = join(p, cond_tables['A'], outcomeSpace)  # Complete the code for the remaining tables. 6 lines
    return p


#########################
# Test code
#########################
outcomeSpace, prob_tables = task2.learn_bayes_net(task2.graphT, 'resources/bc_2.csv')
p = p_joint(outcomeSpace, prob_tables)
task2.printFactor(p)


# def evidence(var, e, outcomeSpace):
#     """
#     argument
#     `var`, a valid variable identifier.
#     `e`, the observed value for var.
#     `outcomeSpace`, dictionary with the domain of each variable
#
#     Returns dictionary with a copy of outcomeSpace with var = e
#     """
#     newOutcomeSpace = outcomeSpace.copy()  # Make a copy of outcomeSpace with a copy to method copy(). 1 line
#     newOutcomeSpace[var] = (e,)  # Replace the domain of variable var with a tuple with a single element e. 1 line
#     return newOutcomeSpace
#
#
# def marginalize(f, var, outcomeSpace):
#     """
#     argument
#     `f`, factor to be marginalized.
#     `var`, variable to be summed out.
#     `outcomeSpace`, dictionary with the domain of each variable
#
#     Returns a new factor f' with dom(f') = dom(f) - {var}
#     """
#
#     # Let's make a copy of f domain and convert it to a list. We need a list to be able to modify its elements
#     new_dom = list(f['dom'])
#
#     #########################
#     # Insert your code here #
#     #########################
#     new_dom.remove(var)  # Remove var from the list new_dom by calling the method remove(). 1 line
#     table = list()  # Create an empty list for table. We will fill in table from scratch. 1 line
#     for entries in product(*[outcomeSpace[node] for node in new_dom]):
#         s = 0  # Initialize the summation variable s. 1 line
#
#         # We need to iterate over all possible outcomes of the variable var
#         for val in outcomeSpace[var]:
#             # To modify the tuple entries, we will need to convert it to a list
#             entriesList = list(entries)
#             # We need to insert the value of var in the right position in entriesList
#             entriesList.insert(f['dom'].index(var), val)
#
#             #########################
#             # Insert your code here #
#             #########################
#
#             p = prob(f, *tuple(entriesList))  # Calculate the probability of factor f for entriesList. 1 line
#             s = s + p  # Sum over all values of var by accumulating the sum in s. 1 line
#
#         # Create a new table entry with the multiplication of p1 and p2
#         table.append((entries, s))
#     return {'dom': tuple(new_dom), 'table': odict(table)}
#
#
# def normalize(f):
#     """
#     argument
#     `f`, factor to be normalized.
#
#     Returns a new factor f' as a copy of f with entries that summation up to 1
#     """
#     table = list()
#     summation = 0
#     for k, p in f['table'].items():
#         summation = summation + p
#     for k, p in f['table'].items():
#         table.append((k, p / summation))
#     return {'dom': f['dom'], 'table': odict(table)}
#
#
# def query(p, outcomeSpace, q_vars, **q_evi):
#     """
#     argument
#     `p`, probability table to query.
#     `outcomeSpace`, dictionary will variable domains
#     `q_vars`, list of variables in query head
#     `q_evi`, dictionary of evidence in the form of variables names and values
#
#     Returns a new factor NORMALIZED factor will all hidden variables eliminated as evidence set as in q_evi
#     """
#
#     # Let's make a copy of these structures, since we will reuse the variable names
#     pm = p.copy()
#     outSpace = outcomeSpace.copy()
#
#     # First, we set the evidence
#     for var_evi, e in q_evi.items():
#         outSpace = evidence(var_evi, e, outSpace)
#
#     # Second, we eliminate hidden variables NOT in the query
#     for var in outSpace:
#         if not var in q_vars:
#             pm = marginalize(pm, var, outSpace)
#     return normalize(pm)
#
#
# #########################
# # Test code
# #########################
# input_file = 'resources/bc_2.csv'
#
# with open(input_file) as f:
#     data = pd.read_csv(f)
#
# print(data.head())
#
# Y = data["BC"]
# X = data.drop(["BC"], axis=1)
# print(X.shape)
#
# seed = 10
# X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=0.2, random_state=seed)
# task2.printFactor(query(p, outcomeSpace, 'L', C=2))

# task2.printFactor(join(query(p, outcomeSpace, 'H'),query(p, outcomeSpace, 'L'), outcomeSpace))
# print()
# task2.printFactor(query(p, outcomeSpace, ('H', 'L')))

