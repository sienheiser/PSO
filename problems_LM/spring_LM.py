# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 14:28:43 2020

@author: coolb
"""

import optimizer as opt
import time
import numpy as np
from uncertainties import ufloat
from uncertainties.umath import *
#%%

def residual(k, v1, v2):
    return v2[0] - v1[0] - k

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
    
def conditionSprings(optimizedPts):
    '''
    optimizedPts: The optimized parameters
    Methods looks at the optimzed parameters and sees the difference between
    adjacent points, if the differences are equal.
   
    '''
    for i in range(len(optimizedPts)-1):
        length = optimizedPts[i+1]-optimizedPts[i]
        if round(length[0],2) != 1.0:
            print('Does not satisfy the condition')
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
#        print('i',i)
        u = opt.Optimizer()
        pts = [opt.Vec(x) for x in np.random.rand(numberOfPoints,1)]
        for j in range(len(pts)-1):
            u.add_residual(opt.partial(residual,1),pts[j],pts[j+1])        
#        print('value i',i)
        t0 = time.time()
        u.optimize()
        t1 = time.time()
#        print('The points are',pts)
    
        lis_time.append(t1-t0)
        lis_iter.append(u.iterations)
        
        if conditionSprings(pts)==False:#looks if best position satifies the condition
            return 'Solution does not satisfy condition, will not gather data.'

#            print('length',round(length[0],2))
        
        if i%100 == 0:
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
np.random.seed(42)


#%%
numPoints = [6,41]#number of points
data = []
for points in numPoints:
    data.append(script(1000,points))
    print(data)
    
#%%
for i in data:
    print(i)

 



    
