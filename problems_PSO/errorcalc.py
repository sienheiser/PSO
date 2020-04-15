# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 11:15:51 2020

@author: coolb
"""
from uncertainties import ufloat
from uncertainties.umath import *

#%% Linear fitting PSO
avgIterPSOli = ufloat(57.2003,4.9135)#number of iterations
avgTimePSOli = ufloat(0.08357,0.01186)#average time
print('Average time per iteration w/ PSO linear fitting',avgTimePSOli/avgIterPSOli)

#%% Linear fitting LM
avgIterLMli = ufloat(3.3749,0.5958)
avgTimeLMli = ufloat(0.06188,0.01077)

print('Average time per iteration w/ LM linear fitting',avgTimeLMli/avgIterLMli)

print((avgTimePSOli/avgIterPSOli)/(avgTimeLMli/avgIterLMli)*100)


#%% Springs PSO
avgIterPSOsp = ufloat(101.1498,9.5930)
avgTimePSOsp = ufloat(0.1213,0.01789)

print('Average time per iteration w/ PSO springs',avgTimePSOsp/avgIterPSOsp)


#%% Springs LM
avgIterLMsp = ufloat(4,0)
avgTimeLMsp = ufloat( 0.04291,0.00454)
print('Average time per iteration w/ LM springs',avgTimeLMsp/avgIterLMsp)

