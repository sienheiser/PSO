# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 10:34:40 2020

@author: coolb
"""

#%%
from functools import partial

import PSO_structure_test as pt

import test_state as state

            
#%% initializing the problem
observations = state.observations
#print(observations)
cameras = state.cameras
noisy_points = state.noisy_points

#%% defining the cost function

ba = partial(state.bundle_adjust,observations,cameras)
#%% testing PSO class

po = pt.PSO(noisy_points,ba,50,500)


#%%
