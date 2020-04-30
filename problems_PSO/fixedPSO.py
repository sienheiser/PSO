# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 14:21:38 2020

@author: coolb
"""


import PSO_algorithm as pt
import numpy as np
from functools import partial


#%%


def residual(k, v1, v2):
    return v2[0] - v1[0] - k

def costfun2(klist,firstPoint,pts):
    '''
    klist: list of k values
    firstPoint: first point of pts so pts[0]
    pts: point
    '''
    cost = 0
    cost += residual(klist[0],firstPoint,pts[0])**2
    for i in range(0,len(klist)-1):
#        print('i',i)
        n = i+1
        cost += residual(klist[i],pts[i],pts[n])**2
    return cost



#%%
np.random.seed(42)
pts = [pt.ma.Vec(x) for x in np.random.rand(10,1)]
print('The points are',pts)
klist = [1 for i in range(len(pts))]
#%%
firstPoint = pt.ma.Vec(0.0)
costfun2(klist,firstPoint,pts)

#%%
firstPoint = pt.ma.Vec(0.0)
costfunction = partial(costfun2,klist,firstPoint)#costfunction with first point fixed


#%%

po = pt.PSO(pts,costfunction,200,1e-12)

print('The best cost is',po.best_cost)
#print('The best position is',po.best_position)
print('The number of iterations are',po.iteration)
print(po.best_position[0])
for i in range(len(po.best_position)-1):
    length = po.best_position[i+1]-po.best_position[i]
    print(length)
    
#