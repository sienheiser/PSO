# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 11:15:29 2020

@author: coolb
"""
#%%
import PSO_algorithm as pt
import time
import numpy as np
from uncertainties import ufloat
from uncertainties.umath import *

#%% points of ends of springs
#pts =  [pt.ma.Vec(v) for v in [-2, -1, 0, 0.5, 1.5, 2.5]]
#
#klist = [1,1,1,1,1]

#%% Increasing the number of spings
np.random.seed(42)
pts = [pt.ma.Vec(v) for v in np.random.rand(1,1)]
klist = [1 for i in range(len(pts)-1)]

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
    

#costfun(klist,pts)
    
#%% initilizing cost function for springs

costfunction = pt.partial(costfun,klist)

#%% running PSO algorithm
po = pt.PSO(pts,costfunction,20,1e-12)

print('best position',po.best_position)
print('best cost',po.best_cost)
print('iterations',po.iteration)

for i in range(len(po.best_position)-1):
    n = i+1
    length = po.best_position[n]-po.best_position[i]
    print(round(length[0]))


#%% Script for getting average time and iterations
#numberOfPoints = [11,21,31,41,51]#number of points
#dataPSO = []#This is where the tuples of (average time,no. of iteration, average time per iteration) will be created
#
#i = 0
#iterations = 5
#avg_iter = 0
#avg_cost = 0
#avg_time = 0
#    
#lis_iter = []
#lis_time = []
#
#while i<iterations:
#    lengths = []
#    t0 = time.time()
#    po = pt.PSO(pts,costfunction,20,1e-12)
#    t1 = time.time()
#
#    avg_iter += po.iteration/iterations
#    avg_time += (t1-t0)/iterations
#        
#    lis_iter.append(po.iteration)
#    lis_time.append(t1-t0)
#        
#    for j in range(len(po.best_position)-1):
#        n = j+1
#        length = po.best_position[n]-po.best_position[i]
#        print(length)
#        
#    i += 1
#    
#    
#print('average iterations',avg_iter)
#print('avg_time',avg_time)

#%% calculating standard deviation of time and iterations
#va_time = 0
#va_iter = 0
#
#for ti in lis_time:
#    va_time += (ti-avg_time)**2
#
#for it in lis_iter:
#    va_iter += (it-avg_iter)**2
#    
#sd_time = pt.np.sqrt(va_time/iterations)
#sd_iter = pt.np.sqrt(va_iter/iterations)
#
#print('Standard deviation of time',avg_time,sd_time)
#print('Standard deviation of iterations',avg_iter,sd_iter)
   
#%% calculating average time per iteration
#timeTot = ufloat(avg_time,sd_time)
#iterTot = ufloat(avg_iter,sd_iter)
#avg_time4 = round(avg_time,4)
#sd_time4 =round(sd_time,4)
#avg_iter4 = round(avg_iter,4)
#sd_iter4 = round(sd_iter,4)
#print('Average time per iteration',timeTot/iterTot) 
#dataPSO.append((ufloat(avg_time4,sd_time4),ufloat(avg_iter4,sd_iter4),timeTot/iterTot))


#%% Testing loops
    
#li = [1,2,3,4,5,6]
#
#for i in li:
#    for j in li:
#        print('i j',i,j)
#        if j == 3:
#            break
#

