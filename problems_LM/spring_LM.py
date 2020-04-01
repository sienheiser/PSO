# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 14:28:43 2020

@author: coolb
"""

import optimizer as opt
import time
#%%

def residual(k, v1, v2):
    return v2[0] - v1[0] - k



 


iterations = 10000
i = 0
avg_time = 0
avg_iter = 0

lis_time = []
lis_iter = []

time1 = time.time()
while i < iterations:
    pts = [opt.Vec(x) for x in [-2, -1, 0, 0.5, 1.5, 2.5]]
    o = opt.Optimizer()
    o.add_residual(opt.partial(residual, 1), pts[0], pts[1])
    o.add_residual(opt.partial(residual, -1), pts[2], pts[1])
    o.add_residual(opt.partial(residual, 1), pts[2], pts[3])
    o.add_residual(opt.partial(residual, -1), pts[4], pts[3])
    o.add_residual(opt.partial(residual, 1), pts[4], pts[5])
    
    
    
    
    t0 = time.time()
    o.optimize()
    t1 = time.time()
    
    avg_iter += o.iterations/iterations
    avg_time += (t1-t0)/iterations
    
    lis_time.append(t1-t0)
    lis_iter.append(o.iterations)
    
    i += 1

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
    
    
