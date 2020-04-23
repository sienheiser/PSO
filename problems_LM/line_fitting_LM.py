# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 16:32:05 2020

@author: coolb
"""
import optimizer as opt
import time
import numpy as np
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
        variance += (da-average)**2
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
    optGradient = round(optimizedPts[0][0],significantFigures)
    optYintercept = round(optimizedPts[1][0],significantFigures)
#    print('The optimized gradient is',optGradient)
#    print('The gradient is',gradient)
    
    if optGradient != round(gradient,significantFigures):
        print('Gradient of built-in python method and LM do not match')
        return False
    if optYintercept != round(yIntercept,significantFigures):
        print('Y-intercept of built-in python method and LM do not match')
        return False


def vert_dist(x,y,a,b):
    '''
    pt: point (x,y)
    a: slope of line
    b: y-intercept
    '''
    return y-a[0]*x-b[0]
#%% 
def script(numIterations,numberOfPoints):
    i = 0#for while loop
    iterations = numIterations#condition for while loop

    lis_iter = []#appends the iterations for every run
    lis_time = []#appends the time take to solve for every run
    
    dataPSO = []#appends list of tuples with format (avg_time,average_iter,average time per iteration)
    
    while i<iterations:
        np.random.seed(42)
        pts = np.random.rand(numberOfPoints,2)
        X = [x for x,y in pts]# x coordinates of points
        Y = [y for x,y in pts]# y coordinates of points
        li = [opt.Vec(1),opt.Vec(1)]
        u = opt.Optimizer()
        
        for x,y in pts:
            u.add_residual(opt.partial(vert_dist,x,y),li[0],li[1])
        
#        print('value i',i)
        t0 = time.time()
        u.optimize()
        t1 = time.time()
#        print('The points are',pts)
    
        lis_time.append(t1-t0)
        lis_iter.append(u.iterations)
        
        if conditionLines(li,X,Y)==False:#looks if best position satifies the condition
            return 'Solution does not satisfy condition, will not gather data.'

#            print('length',round(length[0],2))
        
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


#%% running the scripts
numPoints = [20]#Number of points
data = []#appends the data

for points in numPoints:
    data.append(script(numIterations = 100,numberOfPoints = 10))
    

#%%
#np.random.seed(42)
#
#pts = np.random.rand(10,2)
#X = [x for x,y in pts]
#Y = [y for x,y in pts]
#li = [opt.Vec(1),opt.Vec(1)]
#u = opt.Optimizer()
#for x,y in pts:
#    u.add_residual(opt.partial(vert_dist,x,y),li[0],li[1])
#u.optimize()
#
#gradient,yintercept = np.polyfit(X,Y,1)
