# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 11:42:16 2020

@author: coolb
"""

import matplotlib.pyplot as plt
import numpy as np

#%%

def FLOP_PSO(t):
    return 11*t**2

def FLOP_NM(t):
    return 4*t**3

axis = np.linspace(1,5)

plt.plot(axis,FLOP_PSO(axis),label = 'PSO FLOPS')
plt.plot(axis,FLOP_NM(axis),label = 'NM FLOPS')

plt.xlabel('t')
plt.ylabel('FLOPS')
plt.legend()
plt.savefig('FLOPS.eps')