# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 14:28:43 2020

@author: coolb
"""

import optimizer as opt
import time
import numpy as np
#%%

def residual(k, v1, v2):
    return v2[0] - v1[0] - k



#pts = [opt.Vec(v) for v in np.random.rand(20,1)]
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


iterations = 30
nu = 0
avg_time = 0
avg_iter = 0

lis_time = []
lis_iter = []


time1 = time.time()
while nu < iterations:
    print(nu)
    pts = [opt.Vec(v) for v in np.random.rand(10,1)]
    klist = [1 for i in range(len(pts)-1)]
    o = opt.Optimizer()
    for i in range(len(klist)):
        o.add_residual(opt.partial(residual,klist[1]),pts[i],pts[i+1])
    
    t0 = time.time()
    o.optimize()
    t1 = time.time()
#    print('The point are',pts)
#    for i in range(len(pts)-1):
#        n = i+1
#        length = pts[n]-pts[i]
#        print('The differences are',length)
    
    avg_iter += o.iterations/iterations
    avg_time += (t1-t0)/iterations
    
    lis_time.append(t1-t0)
    lis_iter.append(o.iterations)
    
    
    nu += 1

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

print('Standard deviation of time',sd_time)
print('Standard deviation of iterations',sd_iter)
    
    
