#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 09:12:03 2023

@author: matthew.drummond.ritch@gmail.com

"""

import pandas as pd
import numpy as np
import copy
from setup import setup

def prune(graph, edges):
    #checks edgewise associations 
    for e in edges:
        v1 = e[0]
        edge = v1.edges[e[1]]
        v2 = edge[0]
        ind1 = edge[1][0]
        ind2 = edge[1][1]
        letters1 = np.array([x[ind1] for x in v1.possible_words])
        letters2 = np.array([x[ind2] for x in v2.possible_words])
        mask1 = np.zeros_like(letters1, dtype=int)==1
        mask2 = np.zeros_like(letters2, dtype=int)==1
        for l in np.unique(letters1):
            check = letters2 == l
            if any(check):
                mask1[letters1 == l] = True
            mask2[check] = True
            
        if (not any(mask1)) | (not any(mask2)):
            return False
        
        if len(mask1) > 1:
            v1.possible_words = v1.possible_words[mask1]
        elif not mask1[0]:
            v1.possible_words = np.array([])
        
        if len(mask2) > 1:
            v2.possible_words = v2.possible_words[mask2]
        elif not mask2[0]:
            v2.possible_words = np.array([])
        
    return True


def pruneloop(graph, edges):
    start = np.array([len(x.possible_words) for x in graph])
    x1 = start.copy()
    while True:
        x0 = x1.copy()
        check = prune(graph, edges)
        if not check:
            print('No solution.')
            return False
        
        x1 = np.array([len(x.possible_words) for x in graph])
        
        if all(x1 == x0):
            return True



#def main():
ws = pd.Series(np.loadtxt('dict/words2.txt', dtype=str)).str.lower().reset_index(drop=True) #this allows ws.str. regex
    
st = pd.read_excel('starts/weather4.xlsx', header=None).values  
extra = pd.Series(st[:12,21].astype(str))
st = st[2:17, 2:17]

graph, edges = setup(st, ws)
start = np.array([len(x.possible_words) for x in graph])
check = pruneloop(graph, edges)
x1 = np.array([len(x.possible_words) for x in graph])

#find the vertex with smallest number of possibilities and try them all
minim = np.min(x1[start>1])
where = np.where((x1 == minim) & (start>1))[0][1]
possibles = graph[where].possible_words

for i, possible in enumerate(possibles):
    graph1 = copy.deepcopy(graph)
    graph1[where].possible_words = np.array([possible])
    check = pruneloop(graph1, edges)
    x2 = np.array([len(x.possible_words) for x in graph1])
    if check:
        break
    
    
        
    
    
        
#if __name__ == '__main__':
    # a = np.zeros((100,100))
    # for i in range(a.shape[1]):
    #    a[i,:]=np.arange(100)
    # b = a.copy().transpose()
    # c = (1*(np.sqrt((a-20)**2 + (b-20)**2) < 6)).astype(str)
    # c[c=='0']=''
    # c[c=='1']='#'
    # pd.DataFrame(c).to_csv('c.csv')
    
       
    #main()

        
        
