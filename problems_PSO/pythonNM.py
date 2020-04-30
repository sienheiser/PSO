# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 14:06:22 2020

@author: coolb
"""

import numpy as np
from scipy.optimize import minimize
from functools import partial

#%%

#%% residual of springs
def residual(k, v1, v2):
    return v2 - v1 - k

#%% cost function

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


#%%
    
pts = np.random.rand(1,21)[0]
klist = [1 for i in range(len(pts)-1)]

costfunction = partial(costfun,klist)

res = minimize(costfunction,pts,method = 'nelder-mead', options={'xatol': 1e-8, 'disp': True})
#%%
for i in range(len(res.x)-1):
    length = res.x[i+1]-res.x[i]
    print(length)
    