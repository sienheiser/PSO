# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 14:52:57 2020

@author: coolb
"""



import numpy as np




#%%




#%% initilizing problem
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


position = [2,2]#[a,b]
print(costfunc(pts,position))

#%%

