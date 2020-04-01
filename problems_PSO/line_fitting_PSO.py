# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 12:10:41 2020

@author: coolb
"""

import PSO_algorithm as pt
import matplotlib.pyplot as plt
import time



#%% initilizing problem
pt.np.random.seed(42)
pts = pt.np.random.rand(10,2)
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
#
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


#%%  script for getting average time and average number of iterations

i = 0
iterations = 10000
avg_iter = 0
avg_cost = 0
avg_time = 0

lis_iter = []
lis_time = []

while i<iterations:
    t0 = time.time()
    po = pt.PSO(position,f,20,1e-12)
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

print('Standard deviation of time',sd_time)
print('Standard deviation of iterations',sd_iter)


    

