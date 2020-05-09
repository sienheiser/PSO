# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 12:10:41 2020

@author: coolb
"""

import PSO_algorithm as pt
import matplotlib.pyplot as plt
import time 
import tables as tab



#%% initilizing problem
pt.np.random.seed(42)
pts = pt.np.random.rand(10,2)
X = [x for x,y in pts]
Y = [y for x,y in pts]

def residuals(x,y,a,b):
    return y-a[0]*x-b[0]

def costfunc(pts,pos):#defining the cost function
    cost = 0
    for x,y in pts:
        cost += residuals(x,y,pos[0],pos[1])*residuals(x,y,pos[0],pos[1])
    return cost




position = [pt.ma.Vec(2),pt.ma.Vec(2)]#[a,b]
#print(costfunc(pts,position))


f = pt.partial(costfunc,pts)


#po = pt.PSO(position,f,20,40)

m,b = pt.np.polyfit(X,Y,1)
#
def line(x,a,b):
    return x*a+b
x = pt.np.linspace(0,1)

#print('m,b',m,b)
#print('PSO gradient, slope',po.best_position)
#%%
#plt.plot(x,line(x,m,b),label = 'inbuilt method')
#plt.plot(x,line(x,po.best_position[0],po.best_position[1]),label='PSO')
#plt.plot(X,Y,'o')
#plt.legend()
#plt.show()
#%% starting test

num_part_test = [i*10 for i in range(1,5)]#no. of particles that will be placed in PSO
num_iter_test = [] #no. of iterations that will be places in PSO

testcounter = 10
index = 0

while testcounter != 60:
    num_iter_test.append(testcounter)
    index +=1
    
    if index == 5:
        index = 0
        testcounter += 10
print(num_part_test)
print(num_iter_test)
        
#%% Gathering data for fit of PSO
data_line = []

for num_particles in num_part_test:
    u = pt.ma.Vec(0)
    grad_avg = pt.ma.Vec(0)
    inter_avg = pt.ma.Vec(0)
    avg_time = 0
    index = 0
    for iterations in num_iter_test:
       t0 = time.time() 
       po = pt.PSO(position,f,num_particles,iterations)
       t1 = time.time()
       avg_time += (t1-t0)/5
#       print('position',po.best_position)
       grad_avg += po.best_position[0]/5
       inter_avg += po.best_position[1]/5
#       print('average',grad_avg,inter_avg)
       index += 1
#       print('----------------',index,'----------------')
       if index == 5:
           data_line.append((avg_time,num_particles,iterations,grad_avg,inter_avg))
           index = 0
           grad_avg = pt.ma.Vec(0)
           inter_avg = pt.ma.Vec(0)
           avg_time = 0

#%%
print(data_line)

#%% Making table from data_line
print(": average time : no. particles : iterations : average gradient         : average y-intercept :")

for i in range(0,10):
    print(":",round(data_line[i][0],7),"   :",data_line[i][1]," "*len("no. particles"),data_line[i][2]
    ," "*len("iterations"),data_line[i][3]," "*(len(str(data_line[i][3]))),data_line[i][4])
    

#%%

u = pt.ma.Vec(1.23455675324252)
print(round(u,4))         
        
        
