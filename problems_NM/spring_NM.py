# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 12:20:52 2020

@author: coolb
"""

import NM
from functools import partial
import numpy as np
import time
from uncertainties import ufloat
from uncertainties.umath import *

#%% points of ends of springs
np.random.seed(42)




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




#%% defining some functions to help with timing the algorithm and gathering data

def script(transformations,pts,costfunction,tolerance,iterations):
    i = 0 #index used for while loop
    
    avg_time = 0 #used for summing time taken for NM to reacha solution
    avg_iter = 0 #used for summing the no. of iterations taken for nm to reach a solution

    lis_time = []#used for appending the iterations taken each loop for calculating the standard deviation later
    lis_iter = []#same as lis_time but for iterations
    
    

    while i < iterations:
        simplex = NM.Simplex(pts)#initializing simplex
#        for j in simplex.vertices:
#            print(j)
#        print('---------------------')
        
        t0 = time.time()
        NMalgo = NM.NMalgorithm(transformations,simplex,costfunction,tolerance)#running the algorithm
        t1 = time.time()
    
        avg_time += (t1-t0)/iterations#adding time per run
        avg_iter += NMalgo.iterations/iterations#adding the iterations per run
        
        lis_time.append(t1-t0)#appending the time
        lis_iter.append(NMalgo.iterations)#appending the iterations
        
        if i%10 == 0:#used to check progress
            print(i)
        
        for k in range(len(NMalgo.best_vertex)-1):
            length = NMalgo.best_vertex[k+1] - NMalgo.best_vertex[k]
#            print(length)
            if round(length,2) != 1.0:
                return False
#        print('--------------------')
        
        i += 1#adding one to the index
        
        
    
    print('Average time',avg_time)
    print('Average iterations',avg_iter)
    
    va_time = 0#variance of time
    va_iter = 0#variance of iterations

    for ti in lis_time:
        va_time += (ti-avg_time)**2#calculating the variance for time

    for it in lis_iter:
        va_iter += (it-avg_iter)**2#calculating the variance for iterations
    
    sd_time = np.sqrt(va_time/iterations)#calculating the standard deviations
    sd_iter = np.sqrt(va_iter/iterations)

    print('Standard deviation of time',sd_time)
    print('Standard deviation of iterations',sd_iter)
    
    TimePerIter = ufloat(avg_time,sd_time)/ufloat(avg_iter,sd_iter)
    
    return (ufloat(round(avg_time,4),round(sd_time,4)),ufloat(round(avg_iter,4),round(sd_iter,4)),TimePerIter)
    
    
    
    
    
#%%
numOfPoints = [31,41]
dataNM = []

#pts = np.random.rand(1,31)[0]
#klist = [1 for i in range(len(pts)-1)]

#script(NM.SimpTransform,pts,f,1e-12,1)

for NumPoints in numOfPoints:
    pts = np.random.rand(1,NumPoints)[0]
    klist = [1 for i in range(len(pts)-1)]
    f = partial(costfun,klist)
    result = script(NM.SimpTransform,pts,f,1e-12,1000)
    print(result)
    if result == False:
        break
    dataNM.append(result)
    
#%%
for data in dataNM:
    print(data)


#%% running NM

#simplex = NM.Simplex(pts)
#print(simplex.vertices)
#transformation = NM.SimpTransform
#tolerance = 1e-12
#
#
#NMalgo = NM.NMalgorithm(transformation,simplex,f,tolerance)
#print('The number of iterations are',NMalgo.iterations)
#
#for i in range(len(NMalgo.best_vertex)-1):
#    length = NMalgo.best_vertex[i+1]-NMalgo.best_vertex[i]
#    print(length)
#print('The initial points were',pts)
#print('The final points are',NMalgo.best_vertex)
    


