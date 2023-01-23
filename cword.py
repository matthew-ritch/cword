#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 09:12:03 2023

@author: matthew.drummond.ritch@gmail.com

"""

import pandas as pd
import numpy as np

def setup(st, ws):
    #take minimal grid
    st = st[np.arange(st.shape[0])[np.any(~pd.isna(st), axis=1)], :]
    st = st[:,np.arange(st.shape[1])[np.any(~pd.isna(st), axis=0)]]
    #identify word locations
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
                    dmask[i:,j] = False
    #add any words used in the start file        
    for sp in spaces:
        word = st[sp[0],sp[1]]
        if ~(word=='#').any():
            ws[len(ws)]=''.join(word)
    #change to periods
    st[st=='#'] = '.'
    return st, spaces, ws

def find_next_loc(arr, spaces, ws):
    x = np.array([]).astype(int)
    for sp in spaces:
        s = arr[sp[0],sp[1]]
        if ~(s=='.').any(): 
            x = np.append(x, -1)
        else:
            s = ''.join(s)
            c = ws.str.fullmatch(s).sum()
            x = np.append(x, c)
    #stop conditions
    if (x==0).any(): #puzzle not possible
        return -2
    if ~(x>=1).any(): #puzzle full
        return -1
    #return most constrained space
    m = np.min(x[x>=1])
    ind = np.argwhere(x == m)[0][0]

    return ind

def propose_words(arr, spaces, ind, ws):
    a = arr.copy()
    sp = spaces[ind]
    s = ''.join(a[sp[0],sp[1]])
    candidates = ws[ws.str.fullmatch(s)].reset_index(drop=True).sample(frac=1)
    #TODO add bit which order candidates by number of options they allow
    return candidates
    
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

def main():
    ws = pd.Series(np.loadtxt('words.txt', dtype=str)).str.lower() #this allows ws.str. regex
    ws = ws.reset_index(drop=True)
    st = pd.read_csv('start.csv', header=None).values        
    st, spaces, ws = setup(st, ws)
    state = []
    completes=[]
    state.append(st.copy())
    
    while state:
        arr = state.pop(-1)
        print('\n'*100)
        if len(completes) > 0:
            print('Completed:\n')
            coolprint(completes[-1])
        print('In Progress:\n')
        coolprint(arr)
        print(len(state), 'solutions in progress,', len(completes),'solutions found.\n')
        
        ind = find_next_loc(arr, spaces, ws)
        if ind == -1:
            
            completes.append(arr)
            continue
        if ind == -2:
            continue
        cs = propose_words(arr, spaces, ind, ws)
        for c in cs:
            sp = spaces[ind]
            arr[sp[0], sp[1]]=[*c]
            state.append(arr.copy())
            
    for c in completes:
        coolprint(arr)
        
if __name__ == '__main__':
    main()

        
        