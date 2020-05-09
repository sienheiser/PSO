# -*- coding: utf-8 -*-
"""
Created on Sat May  9 07:47:02 2020

@author: coolb
"""

import numpy as np
import matplotlib.pyplot as plt

def exponential(x,a,b,c):
    return a+b*np.e**(x*c)

def powerlaw(x,a,b,c):
    return a +b*x**c

def log(x,a,b,c):
    return a+b*np.log(c*x)

def polynomial(x,*coefficients):
    poly = 0
    for i in range(len(coefficients)):
        poly += coefficients[i]*x**(len(coefficients)-1-i)
    return poly

