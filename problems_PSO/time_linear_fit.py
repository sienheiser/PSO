# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:27:40 2020

@author: coolb
"""

import timeit as tt


mysetup = '''
import PSO_algorithm as pt
import matplotlib.pyplot as plt'''
            
mycode = ''' 
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
po = pt.PSO(position,f,21,27)
'''
print('This time is',tt.timeit(setup = mysetup,stmt = mycode, number = 100)/100)

