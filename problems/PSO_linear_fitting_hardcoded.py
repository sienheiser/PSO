# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 11:35:56 2020

@author: coolb
"""
#%%

from __future__ import division
import random

from functools import partial
import matplotlib.pyplot as plt
import numpy as np



#%%
class Particle:
    '''
    func: Is the cost function
    x is position of particle in arrays
    
    
    '''
    
    def __init__(self,x):
        self.position_i = x #particle position
        self.velocity_i = None #particle velocity
        self.best_position_i = None #best 
        self.err_best_i=-1        # best individual cost
        self.err_i=-1            # individual cost
        self.length_i = len(x)
        
        self.velocity_i = np.ndarray(len(x),dtype=np.float64)
        for i in range(self.length_i):
            self.velocity_i[i] = random.uniform(-1,1)#initilaizing correct length of velocity
    
#        print('*position_i',*self.position_i)   
    def evaluate(self,func):
        
        self.err_i = func(*self.position_i)#evaluating the cost at particle position and recording individual cost 
#        print('This is err_i',self.err_i)
        if self.err_i<self.err_best_i or self.err_best_i == -1:#arguement for recording best indiviual cost
#            print('in if loop')
#            print('position_i',self.position_i)
            self.best_position_i = self.position_i#setting the best individual cost
            self.err_best_i = self.err_i#setting the best individual position
            
   
    u = np.linspace(-5,5)
            
    def update_velocity(self,pos_best_g):
        w=0.5       # constant inertia weight (how much to weigh the previous velocity)
        c1=1        # cognative constant
        c2=2        # social constant
        for i in range(self.length_i):
            r1 = random.random()#random numbers
            r2 = random.random()#random number
        
            vel_cognitive=c1*r1*(self.best_position_i[i]-self.position_i[i])#defining the cognitive velocity
            vel_social=c2*r2*(pos_best_g[i]-self.position_i[i])#defining the social velocity
            self.velocity_i[i]=w*self.velocity_i[i]+vel_cognitive+vel_social#updating the velocity component-wise
        
    def update_position(self,bounds):
        self.position_i=self.position_i+self.velocity_i#updating position
        for i in range(0,self.length_i):
            # adjust maximum position if necessary
            if self.position_i[i]>bounds[1]:#checking if updated position is out of bounds
                self.position_i[i]=bounds[1]

            # adjust minimum position if neseccary
            if self.position_i[i] < bounds[0]:#checking if updated position is out of bounds
                self.position_i[i]=bounds[0]

    
#%%
class PSO():
    def __init__(self,costFunc,x0,bounds,num_particles,maxiter):
        
        '''
        costFunc: The cost function 
        x0: Inpute that can be placed in the costFunc, it is an array.
        bounds: Search a specific reigon
        num_particles: Amount of particles
        maxiter: Number of iterations 
        '''
        global num_dimensions
        num_dimensions = len(x0)
        err_best_g=-1                   # best error for group
        self.pos_best_g=None               # best position for group

        # establish the swarm
        swarm=[]
        for i in range(0,num_particles):
            array = np.ndarray(num_dimensions,dtype = np.float64)#creating array of correct dimensions
#            print('The array is',array)
            for j in range(num_dimensions):
                array[j] = random.uniform(-5,5)#setting random values to elements of array
#            print('Then array is',array)
            swarm.append(Particle(array))#Placing particles at random positions
        
        i=0
        while i < maxiter:
            #print i,err_best_g
            # cycle through particles in swarm and evaluate fitness
            for j in range(0,num_particles):
                swarm[j].evaluate(costFunc)#evaluating step funciton
                
                if swarm[j].err_i < err_best_g or err_best_g == -1:#finding the best position out of all particles
                    self.pos_best_g=swarm[j].position_i#setting the found best position to best group position
                    err_best_g=float(swarm[j].err_i)#setting the best cost to best group cost
            
            for j in range(0,num_particles):
                swarm[j].update_velocity(self.pos_best_g)#updating individual velocity
                swarm[j].update_position(bounds)#updating individual position
            i+=1
            
#        print('History',swarm[0].history)  
        print ('FINAL:')
        print ('Best position',self.pos_best_g)
        print ('Cost is',err_best_g)
#            




#%%

#pts = [(1,1),(2,3),(3,2),(4,5)]
pts = np.random.rand(10,2)
X = [x for x,y in pts]
Y = [y for x,y in pts]

def residuals(x,y,a,b):
    return y-a*x-b

def costfunc(pts,a,b):#defining the cost function
    cost = 0
    for x,y in pts:
        cost += residuals(x,y,a,b)*residuals(x,y,a,b)
    return cost

position = np.array([2,2])#[a,b]

par = Particle(position)
f = partial(costfunc,pts)

print('position',par.position_i)
print('velocity',par.velocity_i)
par.evaluate(f)
print('err_i,err_best_i,best_position_i',par.err_i,par.err_best_i,par.best_position_i)
par.update_velocity(position)
par.update_position([-5,5])
print('updated,velocity,position',par.velocity_i,par.position_i)



        
#%%

po = PSO(partial(costfunc,pts),np.array([1,1]),[-5,5],10,100)


#%%

m,b = np.polyfit(X,Y,1)#using numpy linear fitting to compare to PSO

print('m,b',m,b)


#%%
def line(x,a,b):
    return x*a+b

x = np.linspace(0,1)
plt.plot(X,Y,'o')
plt.plot(x,line(x,m,b),label = 'in-built pyhton method')
plt.plot(x,line(x,po.pos_best_g[0],po.pos_best_g[1]),label = 'PSO')
plt.legend()
plt.xlabel('[arbitrary units]')
plt.ylabel('[arbitrary units]')







        
    