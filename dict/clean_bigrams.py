#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 20:54:11 2023

@author: mritch
"""

import pandas as pd
import numpy as np


w = pd.Series(np.loadtxt('words.txt', dtype=str)).str.lower()
l = np.array([len(y) for y in w])

ls = np.unique(l)
wd ={}
for ll in ls:
    wd[ll] = w[l == ll]


v = np.loadtxt('count_2w.txt', dtype=str)[:,:2]
v2 = np.zeros(v.shape[0]).astype(str)
m=np.zeros(v.shape[0]) == 1
o = []
for i, x in enumerate(v):
    if i%2000 == 0:
        print(i/len(v))
    v2[i] = (x[0]+x[1]).lower()
    c1 = v2[i].isalpha() & (len(v2[i])>4)
    if not c1:
        continue
    c1 = False
    c2 = False
    
    if len(x[0])>15:
        o.append(x[0])
    elif len(x[0])>1 :
        c1 = any(wd[len(x[0])].str.fullmatch(x[0])) 
    else:
        c1 = True
        
    if not c1:
        continue
    
    if len(x[1])>15:
        o.append(x[1])   
    elif len(x[1])>1:
        c2 = any(wd[len(x[1])].str.fullmatch(x[1]))
    else:
        c2 = True
        
    m[i] = (c1 & c2)
    
    
v = v2[m]

w2 = np.concatenate((w,v, np.unique(o)))
np.savetxt('words2.txt', w2, fmt='%s')
