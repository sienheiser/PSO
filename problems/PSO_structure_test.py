# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 14:37:46 2020

@author: coolb
"""

#%%
import numpy as np
import random 
from functools import partial
import matplotlib.pyplot as plt
#%%


class Particle:
    '''
    func: Is the cost function
    x is position of particle in arrays
    
    
    '''
    
    def __init__(self,x):
        self.position_i = [] #particle position
        self.velocity_i = [] #particle velocity
        self.best_position_i = None #best 
        self.err_best_i=-1        # best individual cost
        self.err_i=-1            # individual cost
        self.length_i = len(x)
        
        for i in x:
            self.position_i.append(np.random.uniform(-5,5,len(i)))
        
        for i in x:
            self.velocity_i.append(np.random.uniform(-1,1,len(i)))
            
        
#%%
            
class Swarm:
    def __init__(self,x,num_particles:int):
        self.best_pos_g = None
        self.best_cost_g = -1
        
        
        self.swarm = []
        
        for i in range(num_particles):
    
    def evaluate(self,func):
        for particle in self.swarm:
            particle.err_i = func(particle.position_i)#evaluating the cost at particle position and recording individual cost
            if particle.err_i<particle.err_best_i or particle.err_best_i == -1:#arguement for recording best indiviual cost
#            print('in if loop')
#            print('position_i',self.position_i)
                particle.best_position_i = particle.position_i#setting the best individual cost
                particle.err_best_i = particle.err_i#setting the best individual position
            
            
            if self.best_cost_g > particle.err_best_i or self.best_cost_g == -1:
                self.best_cost_g = particle.err_best_i
                self.best_pos_g = particle.best_position_i
    
    def update_velocity(self):
        w=0.5       # constant inertia weight (how much to weigh the previous velocity)
        c1=1        # cognative constant
        c2=2        # social constant
        for particle in self.swarm:
            for i in range(len(particle.position_i)):
                for j in range(len(particle.position_i[i])):
                    r1 = random.random()#random numbers
                    r2 = random.random()#random number
                    vel_cognitive=c1*r1*(particle.best_position_i[i][j]-particle.position_i[i][j])#defining the cognitive velocity
                    vel_social=c2*r2*(self.best_pos_g[i][j]-particle.position_i[i][j])#defining the social velocity
                    particle.velocity_i[i][j]=w*particle.velocity_i[i][j]+vel_cognitive+vel_social#updating the velocity component-wise
#            print('particle velocity after update',particle.velocity_i)
    
    def update_position(self):
        for particle in self.swarm:
            particle.position_i=particle.position_i+particle.velocity_i
            
#%%
class PSO:
    def __init__(self,noisy_points,costfunc,num_particles:int,num_iterations:int):
        self.best_cost = None
        self.best_position = None
        
        sw = Swarm(noisy_points,num_particles)
        i = 0
        while i<num_iterations:
            sw.evaluate(costfunc)
            sw.update_velocity()
            sw.update_position()
            i += 1
        
        self.best_cost = sw.best_cost_g
        self.best_position = sw.best_pos_g
        print('The best cost is',self.best_cost)
        print('The best position is',self.best_position)
        
    
#%%
            
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
f = partial(costfunc,pts)

#%%
#sw = Swarm(position,1)
#sw.evaluate(f)
#sw.update_velocity()
#sw.update_position()

#%%

po = PSO(position,f,20,25)

m,b = np.polyfit(X,Y,1)

def line(x,a,b):
    return x*a+b
x = np.linspace(0,1)

plt.plot(x,line(x,m,b),label = 'inbuilt method')
plt.plot(x,line(x,po.best_position[0],po.best_position[1]),label='PSO')
plt.plot(X,Y,'o')
