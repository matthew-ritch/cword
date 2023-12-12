#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 16:42:55 2023

@author: mritch
"""

import pandas as pd
import numpy as np

class vertex:
    def __init__(self, identifier, rows, cols, edges, possible_words):
        self.identifier = identifier
        self.rows = rows
        self.cols = cols
        self.edges = [] #these will be tuples (pointer, [this_posn, that_posn])
        self.possible_words = possible_words
        self.used = False

def find_spaces(st, ws):
    #identify word locations and indices
    amask = ~pd.isna(st)
    dmask = amask.copy()
    spaces=[]
    for i in range(st.shape[0]):
        for j in range(st.shape[1]):
            if amask[i,j]: #check if is already in an across word
                v = np.append(st[i,j:], np.nan)
                end = j + np.argmax(pd.isna(v))
                if end>j+1:
                    spaces.append([(end-j)*[i],np.arange(j, end)])
                    amask[i,j:end] = False
            if dmask[i,j]: #check if is already in a down word
                v = np.append(st[i:,j], np.nan)
                end = i + np.argmax(pd.isna(v))
                if end>i+1:
                    spaces.append([np.arange(i, end), (end-i)*[j]])
                    dmask[i:end,j] = False
    return spaces

def make_edges(graph):
    '''
    make array of indices of letters which overlap for given work intersect
    '''
    n = len(graph)
    edges = np.full([n, n, 2], 100)
    for v in graph:
        i = v.identifier
        for e in v.edges:
            j = e[0].identifier
            edges[i,j,:]=np.array(e[1]).astype(int)
    return edges
    

def make_graph(st, ws, spaces):
    #initialize graph
    graph = []
    for i, indices in enumerate(spaces):
        w = st[indices[0], indices[1]]
        if any(w=='.'):
            candidates = ws[ws.str.fullmatch(''.join(w))]
        else:
            candidates=np.array([''.join(w)])
        word = vertex(i, indices[0], indices[1], [], candidates)
        graph.append(word)
                
    #add edges to graph
    for i, v1 in enumerate(graph):
        for j, v2 in enumerate(graph[i:]):
            if j == 0: continue
            #check for intersection
            c = False
            v1where = np.nan
            v2where = np.nan
            for ii, coord1 in enumerate(zip(v1.rows, v1.cols)):
                for jj, coord2 in enumerate(zip(v2.rows, v2.cols)):
                    if (coord1[0] == coord2[0]):
                        if (coord1[1] == coord2[1]):
                            c = True
                            v1where = int(ii)
                            v2where = int(jj)
            if c:
                v1.edges.append([v2,[v1where, v2where]])
                v2.edges.append([v1,[v2where, v1where]])
    edges = make_edges(graph)
    
    return graph, edges
        
def setup(st, ws):
    st[pd.isna(st)]='.'
    st[st=='/']=np.nan
    
    spaces = find_spaces(st, ws)
    graph, edges = make_graph(st, ws, spaces)   
    
    return graph, edges

def coolprint(arr):   
    arr = arr.copy()
    arr[pd.isna(arr)] = '■'
    arr[arr=='.']='_'
    for i in range(arr.shape[0]):
        #print(''.join(['_']*arr.shape[1]))
        s=''
        for j in range(arr.shape[1]):
            s+=arr[i,j]+' '
        print(s)
    print('\n')   