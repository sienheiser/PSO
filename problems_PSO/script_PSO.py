# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 14:39:27 2020

@author: coolb
"""

from uncertainties import ufloat
from uncertainties.umath import *
import time
import PSO_algorithm as pt
import numpy as np
from functools import partial





#%% Methods that will be used in script for gathering data

def conditionSprings(optimizedPts):
    '''
    optimizedPts: The optimized parameters
    Function checks the distance between the adjacent points and sees if
    they satisfy the condition that the distance is equal to rest lenght within 
    two significant figures.
    '''
    for j in range(len(pts)-1):
        length = optimizedPts[j+1]-optimizedPts[j]
        if round(length[0],2) != 1.0:
            return False
        else:
            pass
        
def Average(data):
    '''
    data: list of data
    This method calculates the average of the data, then uses the data to 
    calculate the standard deviation of the data.
    '''
    average = sum(data)/len(data)#calculating the average
    
    variance = 0#used for calculating the variance
    
    for da in data:
        variance += (da-average)**2
    standardDeviation = np.sqrt(variance)
    return(average,standardDeviation)
    
#%% The script
def script(pts,costfunction,numIterations):
    i = 0#for while loop

    lis_iter = []#appends the iterations for every run
    lis_time = []#appends the time take to solve for every run
    dataPSO = []#appends list of tuples with format (avg_time,average_iter,average time per iteration)
    
    while i<numIterations:
        t0 = time.time()
        algorithm = pt.PSO(pts,costfunction,20,1e-12)
        t1 = time.time()
        lis_time.append(t1-t0)#appends time taken to list
        lis_iter.append(algorithm.iteration)#appends iteratins take to list
        
        if conditionSprings(algorithm.best_position)==False:#looks if best position satifies the condition
            return 'Solution does not satisfy condition, will not gather data.'
        
        if i%10 == 0:# used for keeping track of where the loop is
            print('iterations are',i)
        i += 1
        
    avg_time,sd_time = Average(lis_time)#calulates average and standard deviation of time
    avg_iter,sd_iter = Average(lis_iter)#calculates average and standat deviation of iterations
        
    avg_time4,sd_time4 = round(avg_time,4),round(sd_time,4)#rounds to 4 s.f.
    avg_iter4,sd_iter4 = round(avg_iter,4),round(sd_iter,4)#rounds to 4 s.f.
        
    avgTimePerIter = ufloat(avg_time,sd_time)/ufloat(avg_iter,sd_iter)#calculates the average time per iteration
        
    dataPSO.append((avg_time4,sd_time4,avg_iter4,sd_iter4,avgTimePerIter))
    return dataPSO
        
        
    
#%% defining residuals and costfunction

def residual(k, v1, v2):#The residuals for springs
    return v2[0] - v1[0] - k

def costfun(klist,pts):#The cost funciton for springs
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
numPoints = 6#corresponds to 6 points

pts =  [pt.ma.Vec(v) for v in np.random.rand(numPoints,1)]#The parameters for springs
klist = [1 for i in range(len(pts)-1)]#The rest length for springs


#%% The cost fucntion
costfunction = partial(costfun,klist)#Cost function the PSO takes in

#%%
data = script(pts,costfunction,100)



#%%


