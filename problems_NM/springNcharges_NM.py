# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:19:55 2020

@author: coolb
"""
import NM 
from functools import partial
import numpy as np

#%%
pts = np.array([0.0,1.0,2.0])#position of charged particles
springConst = [1,1]#spring constants
springLen = [1,1]#spring rest lengths
charges = [1,2,3]#charges of the particles
culoumbCont = 1


#%%

def V_spring(springConst,springLen,pts):
    '''
    pts: list points where the end of the springs meet
    springConst: list of spring constants
    springLen : list of spring rest lengths
    '''
    totalsum = 0
    for i in range(len(springConst)):
        totalsum += springConst[i]*(pts[i+1]-pts[i]-springLen[i])**2
        
    return totalsum


def V_coloumb(charges,pts):
    '''
    charges: list of charges for different particles
    pts: position of the charges
    '''
    constant = 1#1/4*pi*epsilon_0
    totalsum = 0
    for i in range(len(pts)):
        for j in range(len(pts)):
            if i == j:
                pass
            else:
                totalsum += (constant *charges[i]/(pts[j]-pts[i]))
    return totalsum

#%% Testing NM on V_coloumb
    
f = partial(V_coloumb,charges)
simplex = NM.Simplex(pts)
transformations = NM.SimpTransform
tolerance = 1e-12
NMalgo = NM.NMalgorithm(transformations,simplex,f,tolerance)
print('The best vertex is',NMalgo.best_vertex)


