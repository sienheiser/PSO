# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 12:10:31 2020

@author: coolb
"""

import NM
import numpy as np
from functools import partial
import time
from uncertainties import ufloat
from uncertainties.umath import *

#%%


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
    
def conditionLines(optimizedPts,X,Y):
    '''
    optimizedPts: The optimized parameters
    X: list of x coordinates of points
    Y: list of y coordinates of points
    
    Methods uses built-in python methods to check whether PSO finds
    good gradient and y-intercept
    '''
    gradient,yIntercept = np.polyfit(X,Y,1)#finding the best gradient and y-intercept
    significantFigures = 3
    if round(optimizedPts[0],significantFigures) != round(gradient,significantFigures):
        print('Gradient of built-in python method and PSO do not match')
        return False
    if round(optimizedPts[1],significantFigures) != round(yIntercept,significantFigures):
        print('Y-intercept of built-in python method and PSO do not match')
        return False
    
#%%
def script(guess,pts,costfunction,numIterations):
    i = 0#for while loop
    iterations = numIterations#condition for while loop

    lis_iter = []#appends the iterations for every run
    lis_time = []#appends the time take to solve for every run
    
    dataPSO = []#appends list of tuples with format (avg_time,average_iter,average time per iteration)
    transformations = NM.SimpTransform
    
    X = [x for x,y in pts]
    Y = [y for x,y in pts]
    
    while i<iterations:
        simplex = NM.Simplex(guess)
#        print('value i',i)
        t0 = time.time()
        po = NM.NMalgorithm(transformations,simplex,costfunction,1e-12)
        t1 = time.time()
#        print('The points are',pts)
    
        lis_iter.append(po.iterations)
        lis_time.append(t1-t0)
        
        if conditionLines(po.best_vertex,X,Y)==False:#looks if best position satifies the condition
            return 'Solution does not satisfy condition, will not gather data.'

#            print('length',round(length[0],2))
        
        if i%100 == 0:
            print('iterations are',i)
        
        i += 1
#    
#    
    avg_time,sd_time = Average(lis_time)#calculates average time and standard deviation
    avg_iter,sd_iter = Average(lis_iter)#calculates average iterations and standard devitation
    
    avg_time4,sd_time4 = round(avg_time,3),round(sd_time,3)#roudning to 4 s.f.
    avg_iter4, sd_iter4  = round(avg_iter,3),round(sd_iter,3)#rounding to 4s.f

    
    dataPSO.append((ufloat(avg_time4,sd_time4),ufloat(avg_iter4,sd_iter4),ufloat(avg_time,sd_time)/ufloat(avg_iter,sd_iter)))
    
    
    return dataPSO

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
#f = partial(costfunc,pts)#creating the cost function
#guess = np.array([1,2])# a guess
#simplex = NM.Simplex(guess) #creating a simplex
#tolerance = 1e-12
#
#NMalgo = NM.NMalgorithm(NM.SimpTransform,simplex,f,tolerance)
#print('The best position',NMalgo.best_vertex)
#print('The cost',NMalgo.best_cost)
#print('The iterations',NMalgo.iterations)

#%%

numOfPoints = [10,20,30,40,50]
guess = np.array([1,2])# a guess
data = []
for points in numOfPoints:
    pts = np.random.rand(points,2)
    f = partial(costfunc,pts)#creating the cost function
    data.append(script(guess,pts,f,1000))
    print(data)
    
#%%
for i in data:
    print(i)