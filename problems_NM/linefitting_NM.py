# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 12:10:31 2020

@author: coolb
"""

import NM
import numpy as np
from functools import partial

#%% initilizing the problem
np.random.seed(42)
pts = np.random.rand(10,2)
X = [x for x,y in pts]
Y = [y for x,y in pts]

def residuals(x,y,a,b):
    return y-a*x-b

def costfunc(pts,pos):#defining the cost function
    cost = 0
    for x,y in pts:
        cost += residuals(x,y,pos[0],pos[1])*residuals(x,y,pos[0],pos[1])
    return cost

#%%
f = partial(costfunc,pts)#creating the cost function
guess = np.array([1,2])# a guess
simplex = NM.Simplex(guess) #creating a simplex
tolerance = 1e-12

NMalgo = NM.NMalgorithm(NM.SimpTransform,simplex,f,tolerance)
print('The best position',NMalgo.best_vertex)
print('The cost',NMalgo.best_cost)
