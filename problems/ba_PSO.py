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
            self.position_i.append(ma.Vec(np.random.uniform(-5,5,len(i))))
            
        for i in self.position_i:
            self.velocity_i.append(ma.Vec(np.random.uniform(-1,1,len(i))))
#        
        

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
#            print('cost_i',particle.cost_i)
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
                for vel_i in range(len(particle.velocity_i)):
#                    print('velocity_i',particle.velocity_i[vel_i])
                    r1 = random.random()
                    r2 = random.random()
                    vel_cognitive=c1*r1*(particle.best_pos_i[vel_i]-particle.position_i[vel_i])
                    vel_social=c2*r2*(self.best_pos_g[vel_i]-particle.position_i[vel_i])
                    particle.velocity_i[vel_i] = w*particle.velocity_i[vel_i]+vel_cognitive+vel_social
#                    print('this is velocity_i updated',particle.velocity_i[vel_i])
                    
    def update_position(self):
        for particle in self.swarm:
            for pos_i in range(len(particle.position_i)):
#                print('pos_i before update',particle.position_i[pos_i])
                particle.position_i[pos_i] = particle.position_i[pos_i]+particle.velocity_i[pos_i]
#                
#                for i in range(len(particle.position_i[pos_i])):
#                    if particle.position_i[pos_i][i] < bounds[0]:
#                        particle.position_i[pos_i][i] = bounds[0]
#                    if particle.position_i[pos_i][i] > bounds[1]:
#                        particle.position_i[pos_i][i] = bounds[1]
                    
#                print('pos_i after update',particle.position_i[pos_i]) 

              
            
#%% creating PSO class which has algorithm

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
        
                     

            
#%% initializing the problem
observations = state.observations
#print(observations)
cameras = state.cameras
noisy_points = state.noisy_points


#%% testing particles
#
#par = Particle(noisy_points)
#print('position_i',par.position_i[0])
#print('velocity_i',par.velocity_i[0])
#print(len(par.velocity_i))


#%% defining the cost function

ba = partial(state.bundle_adjust,observations,cameras)

#%% initilizing the swarm

#s = Swarm(noisy_points,2)

#%% testing swarm evaluate
#s.evaluate(ba)
#
#print('best_pos_g',s.best_pos_g)
#print('best_cost_g',s.best_cost_g)

#%% testing swarm velocity_update
#print('velocity_i before update',s.swarm[1].velocity_i[0],s.swarm[0].velocity_i[2])
#s.update_velocity()
#print('velocity_i before update',s.swarm[1].velocity_i[0],s.swarm[0].velocity_i[2])

#%% testing swarm position_update
#s.update_position([-0.5,0.5])

#%% testing PSO class

po = PSO(noisy_points,ba,500,20)


#%%
