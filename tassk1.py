# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 14:56:47 2019

@author: Deepansh
"""

# Make division default to floating-point, saving confusion
from __future__ import division
from __future__ import print_function

# Necessary libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
# combinatorics
from itertools import product, combinations
# ordered dictionaries are useful for keeping ordered sets of varibles
from collections import OrderedDict as odict
#visualise our graph
from graphviz import Digraph
# table formating for screen output
from tabulate import tabulate
# easier debugging display
pd.set_option('display.multi_sparse', False)
from pprint import pprint
from copy import deepcopy
'''
'Age' : A
'Location' : B
'BC': C
'Metastasis': D
'Lymphnodes':E
'Mass': F
'BreastDensity': G
'Size': H
'Shape': I
'Margin': J
'Spiculation': K
'AD': L
'MC': M
'SkinRetract': N
'NippleDischare': O
'FibrTissueDev': P

graph = {
    'L': ['S', 'V'],
    'H': ['S', 'V'],
    'S': ['O'],
    'V': ['C', 'O'],
    'O': ['B'],
    'A': ['T'],
    'T': ['B']
}
'''
with open('bc 2.csv') as h:
    df = pd.read_csv(h)

#for col in df.columns:
    #print(df[col].value_counts())
    
#print(df.dtypes)

lable_make = LabelEncoder()
for col in df.columns:    
    df[col] = lable_make.fit_transform(df[col])
#the catagorical columns have been converted into numerical values for calculation of probability tables.
#print(df.head(10))

'''


outcome_space = dict(
        Age=(0,1,2,3),
        Location=(0,1,2,3),
        Metastasis=(0,1),
        Lymphnodes=(0,1),
        Mass=(0,1,2),
        BreastDensity=(0,1,2),
        Size=(0,1,2),
        Shape=(0,1,2,3),
        Margin(0,1),
        Spiculation=(0,1),
        AD=(0,1),
        MC=(0,1),
        SkinRetract=(0,1),
        NippleDischarge=(0,1),
        FibrTissueDev=(0,1),
        BC=(0,1,2))


dot = Digraph(comment='ICU Graph')

for v in graph:
    dot.node(str(v))

for v in graph:
    for w in graph[v]:
        dot.edge(str(v), str(w))
#print(dot)

#deseperation(graph,BC,Mass,Margin)  A|B,C

def find_path_recursive(G,X,Y): 
    if X==Y:
        return True
    list_values = G[X]
    for val in list_values:
        find_path(G,val,Y)


'''
graph = { 
        'BC':['Mass','AD','MC','SkinRetract','Nippledischarge','Metastasis'],
        'Mass':['Size','Shape','Margin'],
        'AD':['Fibrtissuedev'],
        'MC':[],
        'SkinRetract':[],
        'Nippledischarge':[],
        'Metastasis':['Lymphnodes'],
        'Size':[],
        'Shape':[],
        'Margin':[],
        'Fibrtissuedev':['Skinretract','Nippledischarge','Spiculation'],
        'Lymphnodes':[],
        'Breastdensity':['Mass'],
        'Age':['BC'],
        'Location':['BC'],
        'Spiculation':['Margin']
        }   



g = {
    'L': ['R'],
    'R': ['D','T'],
    'B': ['T'],
    'D': [],
    'T': ['Z'],
    'Z': [],
}
 
def d_seperation(G,X,Y,Z):
    union = X+Y+Z
    temp_dict = deepcopy(G)
    for key in G.keys():
        if len(G[key])==0:
            if key not in union:
                #remove key as it is a leaf node.
                temp_dict.pop(key,None)
                for node in temp_dict.keys():
                    try:
                        temp_dict[node].remove(key)
                    except ValueError:
                        pass                    
        if key in Z:
            temp_dict[key] = [] #replace the list with empty list to remove any outgoing branches from the key
    
    
    #creating a undirected graph after removing the nodes and the branches..
    #print(temp_dict)
    new_dict = {}
    for key,value in temp_dict.items():
        for val in value:
            if key in new_dict:
                new_dict[key].append(val)
            else:
                new_dict[key] = [val]
            #print(val)
            if val in new_dict:              
                new_dict[val].append(key)
            else:
                new_dict[val] = [key]

    #new_dict is an undirect graph in place of the original graph
    #print(new_dict)
    
    path = find_path(new_dict,X,Y)
    print(path)
    if path==None:
        print("X and Y are deseperated given Z")
    else:
        print("X and Y are not deseperated given Z")


'''
def find_path(graph, start_vertex, end_vertex, path=None):
        """ find a path from start_vertex to end_vertex 
            in graph """
        if path == None:
            path = []
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return path
        if start_vertex not in graph:
            return None
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_path = find_path(vertex, end_vertex, path)
                if extended_path: 
                    return extended_path
        return None
'''
def find_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if start not in graph:
            return None
        for node in graph[start]:
            if node not in path:
                newpath = find_path(graph, node, end, path)
                if newpath: return newpath
        return None
'''
g__ = {'A': ['B', 'C'],
             'B': ['C', 'D'],
             'C': ['D'],
             'D': ['C'],
             'E': ['F'],
             'F': ['C']}

path = find_path(g__,'A','D')   
print(path)
'''
d_seperation(g, 'L', 'B', 'T,R')

#def estimate_probability():
