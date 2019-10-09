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

 
def d_seperation(G,X,Y,Z):
    union = X+Y+Z
    for key in G.keys():
        if len(G[key])==0:
            if key not in union: #key!=X && key!=Y && key not in Z
                #remove key as it is a leaf node.
                G.pop(key,None)
            
        if key==Z:
            G[key] = [] #replace the list with empty list to remove any outgoing branches from the key
    if find_path(G,X,Y)==None:
        print("X and Y are deseperated given Z")
    else:
        print("X and Y are not deseperated given Z")



def find_path(G, start_vertex, end_vertex, path=None):
        """ find a path from start_vertex to end_vertex 
            in graph """
        if path == None:
            path = []
        graph = G
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
    
    
d_seperation(graph, 'BC', 'Shape', 'Mass')

#def estimate_probability():
