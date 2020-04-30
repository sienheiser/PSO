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
    


#%% method for average and standard deviation
def Average(data):
    '''
    data: list of data
    This method calculates the average of the data, then uses the data to 
    calculate the standard deviation of the data.
    '''
    average = sum(data)/len(data)#calculating the average
    
    variance = 0#used for calculating the variance
    
    for da in data:
        variance += (da-average)**2/len(data)
    standardDeviation = np.sqrt(variance)
    return(average,standardDeviation)
    
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
#%% Script for getting average time and iterations
def script(pts,costfunction,numIterations):
    i = 0#for while loop
    iterations = numIterations#condition for while loop

    lis_iter = []#appends the iterations for every run
    lis_time = []#appends the time take to solve for every run
    
    dataPSO = []#appends list of tuples with format (avg_time,average_iter,average time per iteration)

    while i<iterations:
#        print('value i',i)
        t0 = time.time()
        po = pt.PSO(pts,costfunction,int(20*(len(pts)-1)),1e-12)
        t1 = time.time()
    
    
        lis_iter.append(po.iteration)
        lis_time.append(t1-t0)
        
        if conditionSprings(po.best_position)==False:#looks if best position satifies the condition
            return 'Solution does not satisfy condition, will not gather data.'

#            print('length',round(length[0],2))
#        print(po.best_cost)
        if i%10 == 0:
            print('iterations are',i)
        
        i += 1
#    
#    
    avg_time,sd_time = Average(lis_time)#calculates average time and standard deviation
    avg_iter,sd_iter = Average(lis_iter)#calculates average iterations and standard devitation
    
    avg_time4,sd_time4 = round(avg_time,4),round(sd_time,4)#roudning to 4 s.f.
    avg_iter4, sd_iter4  = round(avg_iter,4),round(sd_iter,4)#rounding to 4s.f

    
    dataPSO.append((ufloat(avg_time4,sd_time4),ufloat(avg_iter4,sd_iter4),ufloat(avg_time,sd_time)/ufloat(avg_iter,sd_iter)))
    
    
    return dataPSO
#%%

#%% points of ends of springs
np.random.seed(42)
pts =  [pt.ma.Vec(v) for v in np.random.rand(6,1)]
klist = [1 for i in range(len(pts)-1)]
costfunction = pt.partial(costfun,klist)
#%% running PSO algorithm
po = pt.PSO(pts,costfunction,23,1e-12)

print('best position',po.best_position)
print('best cost',po.best_cost)
print('number of iterations',po.iteration)


for i in range(len(po.best_position)-1):
    n = i+1
    length = po.best_position[n]-po.best_position[i]
    print(length)
#%%

#%% Running the script
NumPoints = [11]
data = []
j = 0 
for points in NumPoints:
    print('select {} position from NumPoints'.format(j))
    pts =  [pt.ma.Vec(v) for v in np.random.rand(points,1)]
    klist = [1 for i in range(len(pts)-1)]
    costfunction = pt.partial(costfun,klist)
    data.append(script(pts,costfunction,numIterations = 1000))
    j += 1
#    print(script(pts,costfunction,numIterations = 20))

    


#%%
