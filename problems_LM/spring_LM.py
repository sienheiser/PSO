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


np.random.seed(42)
#pts = [opt.Vec(v) for v in np.random.rand(51,1)]
#klist = [1 for i in range(len(pts)-1)]
#
#o = opt.Optimizer()
#
#for i in range(len(klist)):
#    o.add_residual(opt.partial(residual,klist[1]),pts[i],pts[i+1])
#o.optimize()
#
#print(pts)
#
#for i in range(len(pts)-1):
#    n = i+1
#    length = pts[n]-pts[i]
#    print('The differences are',length)






#%%

numberOfPoints = [11,21,31,41,51]#number of points
data = []#This is where the tuples of (average time,no. of iteration, average time per iteration) will be created


for NumPoints in numberOfPoints: 
    iterations = 1000
    nu = 0
    avg_time = 0
    avg_iter = 0

    lis_time = []
    lis_iter = []


    time1 = time.time()
    while nu < iterations:
        pts = [opt.Vec(v) for v in np.random.rand(NumPoints,1)]
        klist = [1 for i in range(len(pts)-1)]
        o = opt.Optimizer()
        for i in range(len(klist)):
            o.add_residual(opt.partial(residual,klist[1]),pts[i],pts[i+1])
    
        t0 = time.time()
        o.optimize()
        t1 = time.time()
#       print('The point are',pts)
        for i in range(len(pts)-1):
            n = i+1
            length = pts[n]-pts[i]
            if round(length[0]) != 1.0:
                print('not good accuracey')
                break
    
        avg_iter += o.iterations/iterations
        avg_time += (t1-t0)/iterations
    
        lis_time.append(t1-t0)
        lis_iter.append(o.iterations)
    
    
        nu += 1
        if nu % 100 == 0:
            print(nu)

    print('average iterations',avg_iter)
    print('average_time',avg_time)


#%% calculating standard deviation of time and iterations
    va_time = 0
    va_iter = 0

    for ti in lis_time:
        va_time += (ti-avg_time)**2

    for it in lis_iter:
        va_iter += (it-avg_iter)**2
    
    sd_time = opt.np.sqrt(va_time/iterations)
    sd_iter = opt.np.sqrt(va_iter/iterations)

    print('The average time with standard deviation',avg_time,sd_time)
    print('The average iterations with tandard deviation of iterations',avg_iter,sd_iter)
#    
#   
#%% calculating average time per iteration
    timeTot = ufloat(avg_time,sd_time)
    iterTot = ufloat(avg_iter,sd_iter)
    avg_time4 = round(avg_time,4)
    sd_time4 =round(sd_time,4)
    avg_iter4 = round(avg_iter,4)
    sd_iter4 = round(sd_iter,4)
    print('Average time per iteration',timeTot/iterTot) 
    data.append((ufloat(avg_time4,sd_time4),ufloat(avg_iter4,sd_iter4),timeTot/iterTot))
    
    
#%%
for i in data:
    print(i)
    
#%% saving data as csv

datastr = [str(i) for i in data]


with open('listfile.txt', 'w') as filehandle:
    for listitem in data:
        filehandle.write('%s\n' % data)