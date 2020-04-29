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

plt.plot(n,FLOP_PSO(N,n,m),'ro')
plt.plot(n,FLOP_LM(n,m),'go')
plt.plot(n,FLOP_NM(n,m),'bo')
plt.legend()



#%% Continuous plot
axis = np.linspace(0,50)

plt.plot(axis,FLOP_PSO(N,axis,m),'r',label = 'PSO')
plt.plot(axis,FLOP_LM(axis,m),'g',label = 'LM')
plt.plot(axis,FLOP_NM(axis,m),'b',label = 'NM')

plt.xlabel('Number of residual')
plt.ylabel('FLOPS')
plt.legend()
plt.savefig('FLOPS_line.eps')



#%% fitting the data

#Y_PSO = FLOP_PSO(N,n,m)
#Y_LM = FLOP_LM(n,m)
#Y_NM = FLOP_NM(n,m)
#X = n
#
#grad_PSO,inter_PSO = np.polyfit(X,Y_PSO,1)
#grad_NM,inter_NM = np.polyfit(X,Y_NM,1)
#a,b,c,d = np.polyfit(X,Y_LM,3)
#
#def cube(x,a,b,c,d):
#    return a*x**3+b*x**2+c*x+d
#
#def line(x,gradient,intercept):
#    return gradient*x + intercept
#
#plt.plot(axis,line(axis,grad_PSO,inter_PSO),'r'
#         ,label = 'FLOPS_PSO = {0}*x+{1}'.format(round(grad_PSO),round(inter_PSO)))
#
#plt.plot(axis,cube(axis,a,b,c,d),'g'
#         ,label = 'FLOPS_LM = {0}x**2+{1}x+{2}'.format(round(b),round(c),round(d)))
#
#plt.plot(axis,line(axis,grad_NM,inter_NM),'b'
#         ,label = 'FLOPS_NM = {0}*x+{1}'.format(round(grad_NM),round(inter_NM)))
#plt.ylabel('FLOPS [arbitrary units]')
#plt.xlabel('number of points')
#plt.legend()
#plt.show()

