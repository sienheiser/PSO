# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 13:56:28 2020

@author: coolb
"""

import numpy as np
import matplotlib.pyplot as plt

#%%





def FLOP_PSO(N,n,m):
    '''
    N: number of particles
    n: number of residuals
    m: number of parameters
    '''
    return N*(3*n+8*m)

def FLOP_LM(n,m):
    return 2*m*(n**2+n*m-n+1)

def FLOP_NM(n,m):
    return 4*m**2+7*m+6*n-1


#%%

n = np.array([10,20,30,40,50])#number of residuals
m = 2#number of parameters
N = 20#number of particles
#
#plt.plot(n,FLOP_PSO(N,n,m),'ro')
#plt.plot(n,FLOP_LM(n,m),'go')
#plt.plot(n,FLOP_NM(n,m),'bo')
#plt.legend()



#%% Continuous plot
axis = np.linspace(0,50)


plt.plot(axis,FLOP_LM(axis,m),'r',label = 'LM')
plt.plot(axis,FLOP_PSO(N,axis,m),'g',label = 'PSO')
plt.plot(axis,FLOP_NM(axis,m),'b',label = 'NM')

size = 16
plt.xlabel('Number of residual',size = size)
plt.ylabel('FLOPS', size = size)

plt.xticks(size = size)
plt.yticks(size = size)

plt.legend(prop = {'size':size})
plt.savefig('FLOPS_line.eps')



#%% PLotting number of points vs average time
num_points = [10,20,30,40,50]#number of points
axis = np.linspace(0,50)#creating axis for continous distribution after fitting

avg_timeLM = [0.0557,0.1064,0.1559,0.2057,0.2556]#average time LM takes to solve
avg_timeErrLM = [0.0022,0.0051,0.005,0.0049,0.0057]#error in time LM takes to solve

avg_timePSO = [0.079,0.137,0.195,0.249,0.309]
avg_timeErrPSO = [0.008,0.013,0.023,0.022,0.029]

avg_timeNM = [0.011,0.02,0.03,0.039,0.048]
avg_timeErrNM = [0.001,0.002,0.003,0.004,0.005]

mTimeLM,cTimeLM = np.polyfit(num_points,avg_timeLM,1)#doing a linear fit
lineTimeLM = np.poly1d([0,mTimeLM,cTimeLM])#creating line

mTimePSO,cTimePSO = np.polyfit(num_points,avg_timePSO,1)
lineTimePSO = np.poly1d([0,mTimePSO,cTimePSO])

mTimeNM,cTimeNM = np.polyfit(num_points,avg_timeNM,1)
lineTimeNM = np.poly1d([0,mTimeNM,cTimeNM])


plt.plot(axis,lineTimeLM(axis),'r',label = 'LM')#ploting line created
plt.errorbar(num_points,avg_timeLM, yerr = avg_timeErrLM, fmt = 'none',ecolor = 'r',capsize = 3 )#error bar

plt.plot(axis,lineTimePSO(axis),'g',label = 'PSO')
plt.errorbar(num_points,avg_timePSO, yerr = avg_timeErrPSO, fmt = 'none',ecolor = 'g',capsize = 3 )


plt.plot(axis,lineTimeNM(axis),'b',label = 'NM')
plt.errorbar(num_points,avg_timeNM, yerr = avg_timeErrNM, fmt = 'none',ecolor = 'b',capsize = 3 )

size = 14
plt.ylabel('Average time [s]',size = size)
plt.xlabel('Number of residuals',size = size)
plt.legend()
plt.show()



#%% Plotting number of points vs average iterations
avg_iterLM = [3,3,3,3,3]

avg_iterPSO = [63.534,65.656,66.055,66.646,67.275]
avg_iterErrPSO = [5.138,5.394,5.3,5.167,5.326]

avg_iterNM = [54.305,54.82,55.83,56.742,56.784]
avg_iterErrNM = [4.273,4.566,5.351,4.749,4.628]

mIterLM,cIterLM = np.polyfit(num_points,avg_iterLM,1)
lineIterLM = np.poly1d([0,mIterLM,cIterLM])

mIterPSO,cIterPSO = np.polyfit(num_points,avg_iterPSO,1)
lineIterPSO = np.poly1d([0,mIterPSO,cIterPSO])

mIterNM,cIterNM = np.polyfit(num_points,avg_iterNM,1)
lineIterNM = np.poly1d([0,mIterNM,cIterNM])

plt.plot(axis,lineIterLM(axis),'r',label = 'LM')#ploting line created

plt.plot(axis,lineIterPSO(axis),'g',label = 'PSO')
plt.errorbar(num_points,avg_iterPSO, yerr = avg_iterErrPSO, fmt = 'none',ecolor = 'g',capsize = 3 )

plt.plot(axis,lineIterNM(axis),'b',label = 'NM')
plt.errorbar(num_points,avg_iterNM, yerr = avg_iterErrNM, fmt = 'none',ecolor = 'b',capsize = 3 )


plt.yticks([0,3,10,20,30,40,50,60,70],size = size)
plt.xticks(size = size)

plt.ylabel('Average number of iterations')
plt.xlabel('Number of residuals')
plt.legend()


#%% Plotting number of points vs average time per iteration
avg_tpriLM = [0.01856,0.03546,0.05197,0.06855,0.08518]
avg_tpriErrLM = [0.0007463,0.001693,0.001655,0.001650,0.001906]

avg_tpriPSO = [0.001244,0.002086,0.002946,0.003737,0.004587]
avg_tpriErrPSO = [0.0001560,0.0002612,0.0004178,0.0004438,0.0005641]

avg_tpriNM = [0.0002008,0.0003659,0.00052887,0.0006905,0.0008533]
avg_tpriErrNM = [2.994e-5,5.309e-5,7.819e-5,8.795e-5,0.0001063]

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
    
    plt.plot(axis,line(axis),color = color, label = label)
    plt.errorbar(x,y,yerr = yerr, fmt = 'none',ecolor = color ,capsize = 3)
    
    size = 14
    plt.xlabel(xlabel,size = size)
    plt.ylabel(ylabel,size = size)
    plt.legend()

plottingscript(num_points,avg_tpriLM,avg_tpriErrLM,'r','LM','Number of residuals','Average time per iterations [s]')
plottingscript(num_points,avg_tpriPSO,avg_tpriErrPSO,'g','PSO','Number of residuals','Average time per iterations [s]')
plottingscript(num_points,avg_tpriNM,avg_tpriErrNM,'b','NM','Number of residuals','Average time per iterations [s]')
