# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 14:43:07 2020

@author: coolb
"""
#%%

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

#%%

avgTime = [0.0941,0.2546,0.7558,1.4299,2.3035,3.3424]
numSprings = [5,10,20,30,40,50]


plt.plot(numSprings,avgTime,'o')
plt.xlabel('number of springs')
plt.ylabel('average time')


def power(x,a,b,c):
    return a*x**b+c

popt,pcov = curve_fit(power,numSprings,avgTime)

#%%

xaxis = np.linspace(0,50)
f = power(xaxis,*popt)

plt.plot(xaxis,f)

plt.xlabel('Number of springs')
plt.ylabel('Averave time')

