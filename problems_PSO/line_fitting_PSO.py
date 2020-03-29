# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 12:10:41 2020

@author: coolb
"""

import PSO_algorithm as pt
import matplotlib.pyplot as plt



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


po = pt.PSO(position,f,20,40)

m,b = pt.np.polyfit(X,Y,1)
#
def line(x,a,b):
    return x*a+b
x = pt.np.linspace(0,1)

print('m,b',m,b)
print('PSO gradient, slope',po.best_position)
#%%
plt.plot(x,line(x,m,b),label = 'inbuilt method')
plt.plot(x,line(x,po.best_position[0],po.best_position[1]),label='PSO')
plt.plot(X,Y,'o')
plt.legend()
plt.show()