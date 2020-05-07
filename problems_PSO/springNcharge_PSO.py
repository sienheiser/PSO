# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 11:45:25 2020

@author: coolb
"""

import PSO_algorithm as pt
from functools import partial
import numpy as np

#%% Initializing the problem


pts = [pt.ma.Vec(v) for v in [0,1,2]]#position of charged particles
springConst = [1,1]#spring constants
springLen = [1,1]#spring rest lengths
culoumbCont = 1

#%% building the spring potential
def V_spring(springConst,springLen,pts):
    '''
    pts: list points where the end of the springs meet
    springConst: list of spring constants
    springLen : list of spring rest lengths
    '''
    totalsum = 0
    for i in range(len(springConst)):
        totalsum += springConst[i]*(pts[i+1][0]-pts[i][0]-springLen[i])**2
        
    return totalsum

#%% checking if the spring potential returns the correct value
#f = partial(V_spring,springConst,springLen)
#po = pt.PSO(pts,f,20,1e-12)
#print('best cost',po.best_cost)
#print('best position',po.best_position)
#
#for i in range(len(po.best_position)-1):
#    n = i+1
#    length = po.best_position[n]-po.best_position[i]
#    print(length)
    

#%% building the coloumb potential
    
def V_coloumb(charges,pts):
    '''
    charges: list of charges for different particles
    pts: position of the charges
    '''
    constant = 1#1/4*pi*epsilon_0
    totalsum = 0
    for i in range(len(pts)):
        for j in range(len(pts)):
            if i == j:
                pass
            else:
                totalsum += constant *charges[i]/abs((pts[j][0]-pts[i][0]))
    return totalsum
charges = [10,20,30]#charges of the particles
#print('The value of the coloumb potential is',V_coloumb(charges,pts))

#%% Running PSO on v_coloumb
#po1 = pt.PSO(pts,partial(V_coloumb,charges),10,1e-5)
#print('best cost',po.best_cost)
#print('best position',po.best_position)


#%% building the total potential

def V(springConst,springLen,charges,pts):
    return V_spring(springConst,springLen,pts)+V_coloumb(charges,pts)

g = partial(V,springConst,springLen,charges)#the cost function of the problem


po2 = pt.PSO(pts,g,50,1e-12)

print('best cost',po2.best_cost)
print('best position',po2.best_position)



#%% New trial

#pts = [pt.ma.Vec(2),pt.ma.Vec(1)]
#klist = [1]
#charges = [1,1]
#
#def v_spring(pts,klist):
#    su = 0
#    for i in range(len(klist)):
#        su += (pts[i+1][0]-pts[i][0]-klist[i])
#    return su
#
#def v_coloumb(pts,charges):
#    return charges[0]*charges[1]*1/np.sqrt((pts[0][0]-pts[1][0])**2)
#
#print(v_coloumb(pts,charges))
#        
#def v(klist,charges,pts):
#    return v_spring(pts,klist)+v_coloumb(pts,charges)
#
#cost = partial(v,klist,charges)
#
#po3 = pt.PSO(pts,cost,50,1e-12)
#
#print('best cost',po3.best_cost)
#print('best position',po3.best_position)
