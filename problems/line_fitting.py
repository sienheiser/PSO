# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 12:10:41 2020

@author: coolb
"""
#%%
import ba_PSO as ba
import matplotlib.pyplot as plt


#%% initilizing problem
pts = ba.np.random.rand(10,2)
X = [x for x,y in pts]
Y = [y for x,y in pts]



def residuals(x,y,a,b):
    return y-a[0]*x-b[0]


#%%
def costfunc(pts,pos):#defining the cost function
    cost = 0
    for x,y in pts:
        cost += residuals(x,y,pos[0],pos[1])*residuals(x,y,pos[0],pos[1])
    return cost

position = [ba.ma.Vec(2),ba.ma.Vec(2)]#[a,b]
print(costfunc(pts,position))


#%%
costfunction = ba.partial(costfunc,pts)

po = ba.PSO(position,costfunction,20,100)

#%%

m,b = ba.np.polyfit(X,Y,1)

def line(x,a,b):
    return x*a+b
x = ba.np.linspace(0,1)

plt.plot(x,line(x,m,b),label = 'inbuilt method')
plt.plot(x,line(x,po.best_position[0][0],po.best_position[1][0]),label='PSO')
plt.plot(X,Y,'o')





