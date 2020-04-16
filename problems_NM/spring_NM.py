# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 12:20:52 2020

@author: coolb
"""

import NM
from functools import partial
import numpy as np

#%% points of ends of springs
pts =   np.random.rand(1,31)[0]

klist = [1 for i in range(len(pts)-1)]


#%% residual of springs
def residual(k, v1, v2):
    return v2 - v1 -k

#%% cost funtion

def costfun(klist,pts):
    '''
    klist: list of k values
    pts: point
    '''
    cost = 0
    for i in range(len(klist)):
        n = i+1
        cost += residual(klist[i],pts[i],pts[n])**2
    return cost


f = partial(costfun,klist)


#%% running NM

simplex = NM.Simplex(pts)
#print(simplex.vertices)
transformation = NM.SimpTransform
tolerance = 1e-12


NMalgo = NM.NMalgorithm(transformation,simplex,f,tolerance)

#%%
for i in range(len(NMalgo.best_vertex)-1):
    length = NMalgo.best_vertex[i+1]-NMalgo.best_vertex[i]
    print(length)
