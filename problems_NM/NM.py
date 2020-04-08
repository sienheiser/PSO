# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 14:52:57 2020

@author: coolb
"""



import numpy as np
import random
from functools import partial


#%%
class Simplex:
    
    def __init__(self,guess):
        self.dimensions = len(guess)
        self.basis = []#test to see if basis vector were being created correctly 
        self.vertices = []
        self.vertices.append(guess)
        j = 0
        for i in range(self.dimensions):
            u = np.zeros(self.dimensions)
            u[j] = 1
#            self.basis.append(u)
            self.vertices.append(guess+random.uniform(0,2)*u)
            j += 1
            
class SimpTransform:
    def __init__(self,simplex):
        self.simplex = simplex
        
    @staticmethod 
    def evaluate(costfunction,vertex):
        return costfunction(vertex)
        
    def ordering(self,costfunction):
        costlist = [SimpTransform.evaluate(costfunction,x) for x in self.simplex.vertices]#get a list of costs
#        print('costlist \n',costlist)
#        print('vertivces \n',self.simplex.vertices)
        
        self.i_h = costlist.index(max(costlist))#finds index of vertex that gives highest cost
        self.f_h = max(costlist)#sets the max cost
        
        self.i_l = costlist.index(min(costlist))#finds index of vertex that gives lowest cost
        self.f_l = min(costlist)#sets the min cost
        
        costlist[costlist.index(max(costlist))] = min(costlist)#switches highest cost to lowest so that 2nd highest becomes highest
        
        self.i_s = costlist.index(max(costlist))#finds the index of vertex that gives the second highest cost
        self.f_s = max(costlist)#sets the 2nd highest cost
    def centroid(self):
        self.c = np.zeros(self.simplex.dimensions)#used in centroid to add up all the vectors 
        for i in range(len(self.simplex.vertices)):
            if i == self.i_h:#used for not adding the vertex that gives highest cost
#                print('+++++++++++++++')
#                print(vertex)
                pass
            else:
#                print('--------------')
#                print('the vertex in',vertex)
                self.c += 1/self.simplex.dimensions*self.simplex.vertices[i]#adding the rest of the vertices
#                print('c',self.c)
    def reflection(self,costfunction):
        a = 1 #constans reflaction
        self.x_r = self.c + a*(self.c-self.simplex.vertices[self.i_h])#computing reflections
        self.simplex.vertices[self.i_h] = self.x_r#updating simplex vertex that gives highest cost
        return SimpTransform.evaluate(costfunction,self.x_r)
        
    def expand(self,costfunction):
        g = 2
        self.x_e = self.c + g*(self.x_r-self.c)#computing expansion
        self.simplex.vertices[self.i_h] = self.x_e#updating simplex vertex
        return SimpTransform.evaluate(costfunction,self.x_e)
    
    def contractO(self,costfunction):
        b = 1/2
        self.x_c = self.c+b*(self.x_r-self.c)
        self.simplex.vertices[self.i_h] = self.x_c
        return SimpTransform.evaluate(costfunction,self.x_c)
        
    def contractI(self,costfunction):
        b = 1/2
        self.x_c = self.c+b*(self.x_h-self.c)
        self.simplex.vertices[self.i_h] = self.x_c
        return SimpTransform.evaluate(costfunction,self.x_c)
        
    def shrink(self):
        for i in range(len(self.simplex.vertices)):
            d = 1/2
            self.simplex.vertices[i] = self.simplex.vertices[self.f_l]+d*(self.simplex.vertices[i]-self.simplex.vertices[self.f_l])

        
#%%
class NMalgorithm():
    def __init__(self,transformations,simplex,costfunction,iterations):
        self.trans = transformations(simplex)
        i = 0
        while i<iterations:
            self.trans.ordering(costfunction)
            self.trans.centroid()
            ref = self.trans.reflection(costfunction)
            if self.trans.f_l <= ref < self.trans.f_s:
                #terminate iterations and take x_r
                pass
            
            elif ref < self.trans.f_l:
                exp = self.trans.expand(costfunction)
                if exp < ref:
                    #terminate iteration and accept x_e
                    pass
                elif exp >= ref:
                    #terminate iteration and accept x_r
                    pass
                
            elif ref >= self.f_s:
                if self.trans.f_s <= self.trans.f_r <self.trans.f_h:
                    conO = self.trans.contractO(costfunction)
                    if conO <= self.trans.f_r:
                        #terminate iteration and accept x_c
                        pass
                    else:
                        self.trans.shrink()
            
                    if self.trans.f_r >= self.trans.f_h:
                        conI = self.trans.contractI(costfunction)
                        if conI < self.trans.f_h:
                            #terminate iteration and accept x_c
                            pass
                        else:
                            self.trans.shrink()
                            
                        
                        
            
                
                    
                    
                        
                        
                    
                    
                
                    
                    
                
            
            
        
        
        
        
        
        
        
        
#%% Testing simplex
            
guess = np.array([1,2])

simp = Simplex(guess)
print(simp.vertices)


#%% initilizing problem
np.random.seed(42)
pts = np.random.rand(10,2)
X = [x for x,y in pts]
Y = [y for x,y in pts]

def residuals(x,y,a,b):
    return y-a*x-b

def costfunc(pts,pos):#defining the cost function
    cost = 0
    for x,y in pts:
        cost += residuals(x,y,pos[0],pos[1])*residuals(x,y,pos[0],pos[1])
    return cost


position = [2,2]#[a,b]

#%%Testing transform ordering

f = partial(costfunc,pts)

sit = SimpTransform(simp)
sit.ordering(f)
print('vertex that gives highest cost',sit.f_h)
print('vertex that gives second highest cost',sit.f_s)
print('vertex that gives lowest cost',sit.f_l)


#%%Testing centroid

sit.centroid()
sit.c


#%% Testing reflections

sit.reflection()
print('reflected',sit.x_r)


