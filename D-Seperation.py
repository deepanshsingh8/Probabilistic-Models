# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 14:56:47 2019

@author: Deepansh
"""

from __future__ import division
from __future__ import print_function
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from itertools import product, combinations
from collections import OrderedDict as odict
from graphviz import Digraph
from tabulate import tabulate
pd.set_option('display.multi_sparse', False)
from pprint import pprint
from copy import deepcopy


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

#quiz Question
g= {
    'A':['C'],
    'B':['C','D'],
    'C':['F','E'],
    'D':['E'],
    'E':[],
    'F':[]
    }

#question from slides
g__ = {
      'A':['T'],
      'T':['P'],
      'P':['X','D'],
      'C':['P'],
      'S':['B','C'],
      'B':['D'],
      'X':[],
      'D':[]
      }

#random question
g_ = {
      'U': ['W'],
      'V':['W','X','T'],
      'W':['Y'],
      'X':['Y'],
      'T':['Z'],
      'Z':[],
      'Y':[]
      }

def d_seperation(G,X,Y,Z):
    #using refine graph to apply the algorithm required by the assignment to get a refined graph
    temp_dict=refine_graph(G,X,Y,Z) #this is a recursive function which removes all the leaf nodes and the node that is not required.
    #creating a undirected graph after removing the nodes and the branches..
    new_dict = {}
    for key,value in temp_dict.items(): 
        for val in value: 
            if key in new_dict: #if key is there in  the dictionary, append the value, i.e. add an edge
                new_dict[key].append(val)
            else:
                new_dict[key] = [val] #create a new key and add the vale, i.e. edge
            
            if val in new_dict:              
                new_dict[val].append(key) #create the edge back so that its an undirected graph
            else:
                new_dict[val] = [key] #create the new key and add the edge.

    #new_dict is an undirect graph in place of the original graph
    x_list = X.split(',')
    y_list = Y.split(',')
    path = []
    #print(x_list,y_list)
    for x in x_list:
        for y in y_list:
            path += find_connection(new_dict,x,y) #recursive path finding algorithm
    
    #print(path)
    if path==[]: #if no paths are found then that means that X and Y are d-seperated
        print(f"{X} and {Y} are d-seperated given {Z}")
    else: #otherwise not
        print(f"{X} and {Y} are not d-seperated given {Z}")



def refine_graph(temp_dict,X,Y,Z):
    union = str(X)+'-'+str(Y)+'-'+str(Z) #create a single string for better searching, typically X U Y U Z
    G=deepcopy(temp_dict) #copy the dictionary as the key values are being changed at each iteration
    for key in G.keys():
        if len(G[key])==0:
            if key not in union: # this means node is not in X U Y U Z
                temp_dict.pop(key,None) #remove key as it is a leaf nodek
                for node in temp_dict.keys():
                    try:
                        temp_dict[node].remove(key) #remove the existence of the leaf node from the graph
                    except ValueError:
                        pass     
    G=deepcopy(temp_dict)    #copy the dictionary again
    for key in G.keys(): 
        if len(G[key])==0: #check and see if there are any new leaf nodes created due to removal of leaf nodes
            if key not in union: #there are new leaf nodes and the node is not in X U Y U Z
                temp_dict=refine_graph(temp_dict,X,Y,Z) #recursive call 
        else:
            continue
        
    #now the second step of the algorithm, remove the outgoing branches of node that is in Z. 
    for key in temp_dict.keys():
        if key in Z: #if the node is in Z, remove the branches
            temp_dict[key] = [] #replace the list with empty list to remove any outgoing branches from the key
    return temp_dict

def find_connection(g, X, Y, path=[]):
        path = path + [X] #add the paths together
        if X == Y: #base function that if start node==end node
            return path
        if X not in g: #if Start node is not in the graph
            return [] #return empty list
        for node in g[X]: #for all nodes in the values
            if node not in path:
                newpath = find_connection(g, node, Y, path)
                if newpath: return newpath
        return [] #return empty list

d_seperation(g_, 'U', 'V', 'Z')

