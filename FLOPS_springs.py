# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:19:49 2020

@author: coolb
"""

import numpy as np
import matplotlib.pyplot as plt
import numpy as np

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
m = np.linspace(1,50,100)

plt.plot(m,FLOP_LM(m),'r',label = 'LM')
plt.plot(m,FLOP_PSO(m),'g',label = 'PSO')
plt.plot(m,FLOP_NM(m),'b',label = 'NM')

#plt.ylim(0,10000)
#plt.xlim(0,50)

size = 16
plt.xlabel('Number of parameters',size = size)
plt.ylabel('FLOPS',size = size)
plt.xticks(size = size)
plt.yticks(size = size)
plt.legend(prop = {'size':size})
#%%
def plottingscript(x,y,yerr,color,label,xlabel,ylabel):
    '''
    Functions takes x and y data and makes linear fit. Also takes
    error in y-axis. Then plots the linear fit and error
    x: x data in list
    y: y data in list
    yerr: error of y data in list
    color: colour you want to graph in strings
    label: the name of the graph
    '''
    axis = np.linspace(0,50)
    m,c = np.polyfit(x,y,1)
    line = np.poly1d([0,m,c])
    
    plt.semilogy(axis,line(axis),color = color, label = label)
    plt.errorbar(x,y,yerr = yerr, fmt = 'none',ecolor = color ,capsize = 3)
    
    size = 16
    plt.xlabel(xlabel,size = size)
    plt.ylabel(ylabel,size = size)
    plt.xticks(size = size)
    plt.yticks(size = size)
    plt.legend(prop = {'size':size})
    
#%%
num_points = [5,10,20,30,40,50]#number of springs
axis = np.linspace(0,50)#creating axis for continous distribution after fitting

avg_timeLM = [0.0833,0.2546,0.7558,1.4299,2.2181,3.3424]#average time LM takes to solve
avg_timeErrLM = [0.0612,0.0146,0.0591,0.0447,1.5762,0.0628]#error in time LM takes to solve

avg_timePSO = [0.5879,4.2077]
avg_timeErrPSO = [0.0858,0.4621]

avg_timeNM = [0.0214,0.2429,5.6212]
avg_timeErrNM = [0.0026,0.0456,1.5428]


#%%

avg_iterLM = [8,12,19,25,31,36]
avg_iterErrLM = [0,0,0,0,0,0]

avg_iterPSO = np.array([86.838,173.955])
avg_iterErrPSO = np.array([5.2537,16.684])

avg_iterNM = np.array([200.138,858.996,6649.054])
avg_iterErrNM = np.array([23.5137,153.9832,1824.6534])

mIterLM,cIterLM = np.polyfit(num_points,avg_iterLM,1)
lineIterLM = np.poly1d([mIterLM,cIterLM])


plt.plot(axis,lineIterLM(axis),'r',label = 'LM')#ploting line created
plt.plot(num_points,avg_iterLM,'ro')

plt.semilogy([5,10],avg_iterPSO,'go',label = 'PSO')
plt.errorbar([5,10],avg_iterPSO, yerr = avg_iterErrPSO, fmt = 'none',ecolor = 'g',capsize = 3 )


plt.semilogy([5,10,20],avg_iterNM,'bo',label = 'NM')
plt.errorbar([5,10,20],avg_iterNM, yerr = avg_iterErrNM, fmt = 'none',ecolor = 'b',capsize = 3 )
#

size = 16
plt.yticks(size = size)
plt.xticks(size = size)

plt.ylabel('Average number of iterations',size = size)
plt.xlabel('Number of residuals', size = size)
plt.legend(prop = {'size':size})


#%%

avg_tpriLM = [0.01041,0.02121,0.03978,0.05719,0.07155,0.09284]
avg_tpriErrLM = [0.007645,0.001190,0.003111,0.001786,0.05084,0.001744]

avg_tpriPSO = [0.006770,0.02419]
avg_tpriErrPSO = [0.001070,0.003527]

avg_tpriNM = [0.0001069,0.0002827,0.0008454]
avg_tpriErrNM = [1.803e-5,7.338e-5,0.0003281]


plottingscript(num_points,avg_tpriLM,avg_tpriErrLM,'r','LM','Number of springs','Average time per iteration [s]')
plt.semilogy([5,10],avg_tpriPSO,'go',label = 'PSO')
plt.errorbar([5,10],avg_tpriPSO,yerr = avg_tpriErrPSO, fmt = 'none',ecolor = 'g' ,capsize = 3)

plottingscript([5,10,20],avg_tpriNM,avg_tpriErrNM,'b','NM','Number of springs','Average time per iteration [s]')
