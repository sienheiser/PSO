# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 12:10:41 2020

@author: coolb
"""

import PSO_algorithm as pt
import matplotlib.pyplot as plt
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
    if round(optimizedPts[0][0],significantFigures) != round(gradient,significantFigures):
        print('Gradient of built-in python method and PSO do not match')
        return False
    if round(optimizedPts[1][0],significantFigures) != round(yIntercept,significantFigures):
        print('Y-intercept of built-in python method and PSO do not match')
        return False



#%% The script for gathering data
def script(pts,costfunction,numIterations):
    i = 0#for while loop
    iterations = numIterations#condition for while loop

    lis_iter = []#appends the iterations for every run
    lis_time = []#appends the time take to solve for every run
    
    dataPSO = []#appends list of tuples with format (avg_time,average_iter,average time per iteration)
    
    while i<iterations:
#        print('value i',i)
        t0 = time.time()
        po = pt.PSO(pts,costfunction,20,1e-12)
        t1 = time.time()
#        print('The points are',pts)
    
        lis_iter.append(po.iteration)
        lis_time.append(t1-t0)
        
        if conditionLines(po.best_position,X,Y)==False:#looks if best position satifies the condition
            return 'Solution does not satisfy condition, will not gather data.'

#            print('length',round(length[0],2))
        
        if i%10 == 0:
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

#%% initilizing problem
pt.np.random.seed(42)
pts = pt.np.random.rand(40,2)
X = [x for x,y in pts]
Y = [y for x,y in pts]

def residuals(x,y,a,b):
    return y-a[0]*x-b[0]

def costfunc(pts,pos):#defining the cost function
    cost = 0
    for x,y in pts:
        cost += residuals(x,y,pos[0],pos[1])*residuals(x,y,pos[0],pos[1])
    return cost

position = [pt.ma.Vec(2),pt.ma.Vec(2)]#[a,b]
#print(costfunc(pts,position))
f = pt.partial(costfunc,pts)
po = pt.PSO(position,f,20,1e-12)
print('The number of iterations is',po.iteration)
#print('The best cost is',po.best_cost)
#print('The best position is',po.best_position)
#%%
m,b = pt.np.polyfit(X,Y,1)
def line(x,a,b):
    return x*a+b
x = pt.np.linspace(0,1)
print('m,b',m,b)
print('gradient, slope',po.best_position)
plt.plot(x,line(x,m,b),label = 'inbuilt method')
plt.plot(x,line(x,po.best_position[0],po.best_position[1]),label='PSO')
plt.plot(X,Y,'o')
plt.legend()
plt.show()


#%%  running the script


numPoints = [10]# The number of points
data = []
for points in numPoints:
    pts = pt.np.random.rand(points,2)#poitns 
    X = [x for x,y in pts]# x coordinates of points
    Y = [y for x,y in pts]# y coordinates of points
    position = pt.np.random.rand(2,1)# random guess for gradient and yIntercept
    costfunction = pt.partial(costfunc,pts)
    
    data.append(script(pts,costfunction,100))
    print(data)
    



    

