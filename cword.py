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
    #st = st[np.arange(st.shape[0])[np.any(~pd.isna(st), axis=1)], :]
    #st = st[:,np.arange(st.shape[1])[np.any(~pd.isna(st), axis=0)]]
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
                    dmask[i:end,j] = False
    #add any words used in the start file        
    for sp in spaces:
        word = st[sp[0],sp[1]]
        if ~(word=='#').any():
            w = ''.join(word)
            if ws.str.fullmatch(w).sum()==0:
                ws[len(ws)]=w
    #change to periods
    st[st=='#'] = '.'
    #mix up words
    #ws = ws.reset_index(drop=True).sample(frac=1)
    #sort words by letter frequencies
    letters=[]
    for w in ws:
        for l in w:
            letters.append(l)
    letters,counts = np.unique(letters, return_counts=True)
    counts = counts / sum(counts)
    
    scores = []
    for w in ws:
        scores.append(0)
        for l in w:
            scores[-1] += counts[letters==l][0]
    order = np.argsort(scores)
    ws = ws[order].reset_index(drop=True)
    
    return st, spaces, ws

def find_next_loc(arr, spaces, wd):
    x = np.array([]).astype(int)
    inds=[]
    
    for i, sp in enumerate(spaces):
        s = arr[sp[0],sp[1]]
        s = ''.join(s)
        if '.' not in s: #handle an existing full word
            if wd[len(s)].str.fullmatch(s).sum()>0: 
                x = np.append(x, 1) #if this is in our dictionary
            else:
                #return -2
                x = np.append(x, 0) #if this is not in our dictionary
        else:
            inds.append(i) #this is a space we need to add letters to
            c = wd[len(s)].str.fullmatch(s).sum()
            x = np.append(x, c) #append how many possible words fit here (only considering letters in this word)
    #stop conditions
    if (x==0).any(): #puzzle not possible
        return -2
    if ~(len(inds)>0) & (~(arr == '.').any()): #puzzle full
        return -1
    #return most constrained space
    options = np.array(x[inds])
    if any(options==0):
        return -2
    m = np.min(options[options>=1])
    ind = inds[np.argwhere(options == m)[0][0]]

    return ind

def propose_words(arr, spaces, ind, wd):
    a = arr.copy()
    sp = spaces[ind]
    s = ''.join(a[sp[0],sp[1]])
    candidates = wd[len(s)][wd[len(s)].str.fullmatch(s)]#.reset_index(drop=True).sample(frac=1)
    #TODO add bit which order candidates by number of options they allow. currently selects randomly
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
    ws = pd.Series(np.loadtxt('dict/words2.txt', dtype=str)).str.lower() #this allows ws.str. regex
    ws = ws.reset_index(drop=True)
        
    #st = pd.read_csv('starts/ballstart.csv', header=None).values       
    st = pd.read_excel('starts/weather5.xlsx', header=None).values  
    extra = pd.Series(st[:12,21].astype(str))
    st = st[2:17, 2:17]
    st[pd.isna(st)] = '#'
    st[st == '.'] = '#'
    st[(st == '?') | (st == '/')] = np.nan
    
    st, spaces, ws = setup(st, ws)
    
    w_ls = np.array([len(x) for x in ws.values])
    space_ls = np.unique([len(x[0]) for x in spaces])
    m = np.zeros_like(ws.values)==1
    for s in space_ls:
        m = m | (w_ls == s)
    ws = ws[m]
    ws = pd.concat([extra,ws], ignore_index=True)
    
    l = np.array([len(y) for y in ws])
    ls = np.unique(l)
    wd ={}
    for ll in ls:
        wd[ll] = ws[l == ll]
    
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
        
        ind = find_next_loc(arr, spaces, wd)
        if ind == -1:
            completes.append(arr)
            np.save('c2.npy', completes)
            continue
        if ind == -2:
            continue
        cs = propose_words(arr, spaces, ind, wd)
        for c in cs:
            sp = spaces[ind]
            arr[sp[0], sp[1]]=[*c]
            state.append(arr.copy())
            
    for c in completes:
        coolprint(arr)
        
if __name__ == '__main__':
    # a = np.zeros((100,100))
    # for i in range(a.shape[1]):
    #    a[i,:]=np.arange(100)
    # b = a.copy().transpose()
    # c = (1*(np.sqrt((a-20)**2 + (b-20)**2) < 6)).astype(str)
    # c[c=='0']=''
    # c[c=='1']='#'
    # pd.DataFrame(c).to_csv('c.csv')
    
       
    main()

        
        
