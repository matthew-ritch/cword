#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 09:12:03 2023

@author: matthew.drummond.ritch@gmail.com

"""

import pandas as pd
import numpy as np
import copy
import time
from setup import setup
    
    
def find_paths(graph, n):
    '''
    n is number of vertices per path in the paths to find
    
    could make faster by removing already used possibilities earlier
    '''
    
    n_paths = []
    #have_started = []
    
    #each vertex v is a starting point
    for v in graph:
        #start with this v
        vid = v.identifier
        in_progress = [[vid]]
        
        #find all n-clusters with this vertex
        while in_progress:
            path = in_progress.pop(-1)
            possible_next_vertices = [x[0].identifier for x in graph[path[-1]].edges]
            #don't revisit the last tile
            if len(path)>1:
                possible_next_vertices.remove(path[-2])
            for p in possible_next_vertices:
                if len(path) == n-1:
                    if p >= vid:#not in have_started:
                        n_paths.append(path + [p])
                elif p not in path:
                    in_progress.append(path + [p])
        #have_started.append(v.identifier)
    return n_paths

def prune_path(graph, edges, n, p):
    words = [graph[x].possible_words for x in p]
    #masks = [np.zeros(len(w)) for w in words]
    
    chains = [[x] for x in words[0]]
    finished = []
    
    while chains:
        this = chains.pop()
        posn_to_add = len(this)
        intersection = edges[p[posn_to_add-1],p[posn_to_add],:]
        letter_to_match = this[-1][intersection[0]]
        possible_next_words = [x for x in words[posn_to_add] if x[intersection[1]]==letter_to_match]
        
        if posn_to_add == n-1:
            for next_word in possible_next_words:
                finished.append(this + [next_word])
        else:
            #check for cycle
            if p[posn_to_add+1] in p[:posn_to_add+1]:
                w = np.where(p[posn_to_add+1] == np.array(p[:posn_to_add+1]))
                #then the word we are adding must be compliant with the next word
                intersection = edges[p[posn_to_add],p[posn_to_add+1],:]
                for pnw in possible_next_words:
                    actual = []
                    if (pnw[intersection[0]] == this[w][intersection[1]]):
                        actual.append(pnw)
                possible_next_words = actual
                        
            for next_word in possible_next_words:
                chains.append(this + [next_word])
    graph[p[0]].possible_words = np.unique([x[0] for x in finished])

def prune(graph, edges, n):
    paths = find_paths(graph, n)
    for p in paths:
        print(p)
        prune_path(graph, edges, n, p)
        prune_path(graph, edges, n, p[::-1])
        
        
        
        


ws = pd.Series(np.loadtxt('dict/words2.txt', dtype=str)).str.lower().reset_index(drop=True) #this allows ws.str. regex
    
st = pd.read_excel('starts/weather4.xlsx', header=None).values  
extra = pd.Series(st[:12,21].astype(str))
st = st[2:17, 2:17]

graph, edges = setup(st, ws)

flag = False
n = 1
while not flag:
    n += 1
    print(n)
    t0 = time.time()
    paths = prune(graph, edges, n)
    print(time.time() - t0)
    if n ==2: break
    
        
# if __name__ == '__main__':
#     main()

        
        
