#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 20:54:11 2023

@author: mritch
"""

import pandas as pd
import numpy as np

v = np.loadtxt('count_2w.txt', dtype=str)[:,:2]
v2 = np.zeros(v.shape[0]).astype(str)
m=[]
for i, x in enumerate(v):
    v2[i] = (x[0]+x[1]).lower()
    m.append(v2[i].isalpha() & len(v2[i])>4)
v = v2[m]

w = np.loadtxt('words.txt', dtype=str)
w2 = np.concatenate((w,v))
np.savetxt('words2.txt', w2, fmt='%s')
