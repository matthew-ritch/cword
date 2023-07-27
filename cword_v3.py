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
    
def crawl_graph_old(graph, path, n_to_add, possible_edges, added_node):
    '''
    recursive pathfinding, starting with the path given as an argument
    adds nodes until n_to_add = 0
    
    TODO why are we still getting repeats?
    '''
    if path == [0,1,2]:
        print([x[1].identifier for x in possible_edges])
        print('\n')
    #g = copy.deepcopy(graph)
    possible_edges = possible_edges.copy()
    results = []
    if n_to_add > 0:
        if added_node:
            most_recent = graph[path[-1]]
            new_possibles = [[most_recent, x[0]] for x in most_recent.edges]
            possible_edges += new_possibles
            if len(path) > 1: #remove previous node
                previous_node = graph[path[-2]]
                for e in possible_edges:
                    if (e[0].identifier == previous_node.identifier):
                        if (e[1].identifier == most_recent.identifier):
                            possible_edges.remove(e)
                            continue
                    if e[1].used:
                        possible_edges.remove(e)
        #end case 1: not enough nodes remaining to fill n_to_add
        if len(possible_edges) == 0:
            return []
        
        #for each one of these either we add it or not
        for e in possible_edges:
            possible_edges.remove(e)
            #either add the edge/neighbor:
            #decrement n_to_add and pass path with this dst appended
            n = n_to_add - 1
            results = results + crawl_graph(graph, path+[e[1].identifier], n, possible_edges, True)
            #or don't add the neighbor
            #don't decrement n_to_add or add dst to path
            n = n_to_add - 0
            results = results + crawl_graph(graph, path, n, possible_edges, False)
            return results
    else:
        return [path]   

def crawl_graph(graph, path, n_to_add, possible_edges=None):
    '''
    recursive pathfinding, starting with the path given as an argument
    adds nodes until n_to_add = 0
    
    TODO why are we still getting repeats?
    '''
    print(path)
    results = []
    if n_to_add > 0:
        most_recent = graph[path[-1]]
        if not possible_edges:
            possible_edges = [[most_recent, x[0]] for x in most_recent.edges]
            if len(path) > 1: #remove previous node
                previous_node = graph[path[-2]]
                for e in possible_edges:
                    if (e[0].identifier == previous_node.identifier):
                        possible_edges.remove(e)
                    elif e[1].used:
                        possible_edges.remove(e)
        #end case 1: not enough nodes remaining to fill n_to_add
        if len(possible_edges) == 0:
            return []
        
        #for each one of these either we add it or not
        for e in possible_edges:
            possible_edges.remove(e)
            #either add the edge/neighbor:
            #decrement n_to_add and pass path with this dst appended
            results = results + crawl_graph(graph, path+[e[1].identifier], n_to_add-1)
            #or don't add the neighbor
            #don't decrement n_to_add or add dst to path
            results = results + crawl_graph(graph, path, n_to_add, possible_edges.copy())
            return results
    else:
        return [path]  
    
def find_clusters(graph, n):
    '''
    n is number of vertices per cluster in the clusters to find
    '''
    clusters = []
    n_neighbors = []
    for vert in graph:
        n_neighbors.append(len(vert.edges))
    
    for i in np.argsort(n_neighbors):
        #take vertex
        vertex = graph[i]
        #find all n-clusters with this vertex
        path = [vertex.identifier]
        clusters = clusters + crawl_graph(graph, path, n-1)
        #remove this vertex from consideration on the next loop
        #this prevents repeat collections
        vertex.used = True
    
    #reset used status
    for vertex in graph:
        vertex.used =  False
        
    return clusters
      

    

ws = pd.Series(np.loadtxt('dict/words2.txt', dtype=str)).str.lower().reset_index(drop=True) #this allows ws.str. regex
    
st = pd.read_excel('starts/weather4.xlsx', header=None).values  
extra = pd.Series(st[:12,21].astype(str))
st = st[2:17, 2:17]

graph, edges = setup(st, ws)

flag = False
n = 2
while not flag:
    n += 1
    t0 = time.time()
    print(n)
    clusters = find_clusters(graph, n)
    if True:
        x = ['-'.join(np.array(c).astype(str)) for c in clusters]
        l, counts = np.unique(x, return_counts=True)
        clusters2 = [np.array(x.split('-')).astype(int) for x in l]
        repeats = np.array(clusters2)[counts>1]
    print(time.time() - t0)
    if n ==4: break
    
    #reduce word possibilities using each cluster here
    
    
        
# if __name__ == '__main__':
#     main()

        
        
