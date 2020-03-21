# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 11:15:29 2020

@author: coolb
"""
#%%
import PSO_algorithm as pt
#%%



#%% points of ends of springs
pts =  [pt.ma.Vec(v) for v in [-2, -1, 0, 0.5, 1.5, 2.5]]

klist = [1,-1,1,-1,1]

#%% residual of springs
def residual(k, v1, v2):
    return v2[0] - v1[0] - k

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
    

costfun(klist,pts)
    
#%% initilizing cost function for springs

costfunction = pt.partial(costfun,klist)

#%% running PSO algorithm
po = pt.PSO(pts,costfunction,50,100)






