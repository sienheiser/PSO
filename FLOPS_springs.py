# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:19:49 2020

@author: coolb
"""

import numpy as np
import matplotlib.pyplot as plt

#%%





def FLOP_PSO(m):
    '''
    m: number of parameters
    '''
    return 20*(11*m**2-3*m)

def FLOP_LM(m):
    return 3*m**3-5*m**2+m+2

def FLOP_NM(m):
    return 4*m**2+13*m-7


#%%
m = np.linspace(1,51,100)

plt.plot(m,FLOP_PSO(m),'r',label = 'PSO')
plt.plot(m,FLOP_LM(m),'g',label = 'LM')
plt.plot(m,FLOP_NM(m),'b',label = 'NM')

#plt.ylim(0,10000)
#plt.xlim(0,50)

size = 15
plt.xlabel('Number of parameters',size = size)
plt.ylabel('FLOPS',size = size)
plt.xticks(size = size)
plt.yticks(size = size)
plt.legend()
