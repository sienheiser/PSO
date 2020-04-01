# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 11:15:29 2020

@author: coolb
"""
#%%
import PSO_algorithm as pt
import time


#%% points of ends of springs
pts =  [pt.ma.Vec(v) for v in [-2, -1, 0, 0.5, 1.5, 2.5]]

klist = [1,-1,1,-1,1]

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
po = pt.PSO(pts,costfunction,50,1e-12)

print('best position',po.best_position)
print('best cost',po.best_cost)


#%% Script for getting average time and iterations

i = 0
iterations = 10000
avg_iter = 0
avg_cost = 0
avg_time = 0

lis_iter = []
lis_time = []

while i<iterations:
    t0 = time.time()
    po = pt.PSO(pts,costfunction,20,1e-12)
    t1 = time.time()
    
    avg_iter += po.iteration/iterations
    avg_time += (t1-t0)/iterations
    
    lis_iter.append(po.iteration)
    lis_time.append(t1-t0)
    
    i += 1
    
    
print('average iterations',avg_iter)
print('avg_time',avg_time)

#%% calculating standard deviation of time and iterations
va_time = 0
va_iter = 0

for ti in lis_time:
    va_time += (ti-avg_time)**2

for it in lis_iter:
    va_iter += (it-avg_iter)**2
    
sd_time = pt.np.sqrt(va_time/iterations)
sd_iter = pt.np.sqrt(va_iter/iterations)

print('Standard deviation of time',avg_time,sd_time)
print('Standard deviation of iterations',avg_iter,sd_iter)





