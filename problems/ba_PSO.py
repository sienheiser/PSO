# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 10:34:40 2020

@author: coolb
"""

#%%

import numpy as np
from functools import partial
import random
import math_utils as ma
import test_state as state

#%% Buidling Particle class

class Particle:
    def __init__(self,noisy_points):
        self.position_i = []
        self.best_pos_i = None
        
        self.velocity_i = []
        
        self.cost_i = -1
        self.best_cost_i = -1
        
        for i in noisy_points:
            self.position_i.append(ma.Vec(np.random.uniform(-2,2,len(i))))
            
        for i in self.position_i:
            self.velocity_i.append(ma.Vec(np.random.uniform(-1,1,len(i))))
        
        

#%%

class Swarm:
    def __init__(self,noisy_points,num_particles:int):
        self.best_pos_g = None
        
        self.best_cost_g = -1
        
        self.swarm = []
        
        for i in range(num_particles):
            self.swarm.append(Particle(noisy_points))
        
    def evaluate(self,costfunc):
        
        for particle in self.swarm:
            particle.cost_i = ba(particle.position_i)
            print('cost_i',particle.cost_i)
            if particle.best_cost_i>particle.cost_i or particle.best_cost_i == -1:
                particle.best_cost_i = particle.cost_i
                particle.best_pos_i = particle.position_i
            
            if self.best_cost_g > particle.best_cost_i or self.best_cost_g == -1:
                self.best_cost_g = particle.best_cost_i
                self.best_pos_g = particle.best_pos_i
                
    def update_velocity(self):
            w=0.5       # constant inertia weight (how much to weigh the previous velocity)
            c1=1        # cognative constant
            c2=2        # social constant
            for particle in self.swarm:
                for vel_i in particle.velocity_i:
                    print('this is vel_i',vel_i)
                    for index in range(len(vel_i)):
                        r1 = random.random()
                        r2 = random.random()
                        vel_cognitive=c1*r1*(particle.best_pos_i[index]-particle.position_i[index])
                        vel_social=c2*r2*(self.best_pos_g[index]-particle.position_i[index])
                        vel = w*vel_i[index]+vel_cognitive+vel_social
                        print('======================',vel)
                        vel_i[index] = w*vel_i[index]+vel_cognitive+vel_social
                    print('this is vel_i updated',vel_i)
                    

              
            
            
            
#%% initializing the problem
observations = state.observations
cameras = state.cameras
noisy_points = state.noisy_points


#%% testing particles
par = Particle(noisy_points)
print('position_i',par.position_i)
print('velocity_i',par.velocity_i[0])
print(len(par.velocity_i[0]))


#%% defining the cost function

ba = partial(state.bundle_adjust,observations,cameras)

#%% initilizing the swarm

s = Swarm(noisy_points,2)

#%% testing swarm evaluate
s.evaluate(ba)

print('best_pos_g',s.best_pos_g)
print('best_cost_g',s.best_cost_g)

#%% testing swarm velocity_update
s.update_velocity()

#%% testing if __setitem__ works
