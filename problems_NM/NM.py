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
    '''
        A simplex is an object that has n+1 vertices in an n-dimensional space.
        Guess is a point that is just guessed.
        The guess is used to look at the dimension of the input space.
        
        By convention the first vertex is always taken as the guess.
        
        Then the other n vertices are built from the guess using equation
        xj = x0+hj*ej
        where xj is the jth vertex, x0 is the guess, hj is a step size
        and ej is the unit vector.
        
        The object we get from this class is a simplex. The only attribute
        that need to be called on is self.vertices
    '''
    
    def __init__(self,guess):
       
        self.dimensions = len(guess)
#        self.basis = []#test to see if basis vector were being created correctly 
        self.vertices = []
        self.vertices.append(guess)
        j = 0 #index for choosing basis vector
        for i in range(self.dimensions):
            u = np.zeros(self.dimensions)#creating array of zeros
            u[j] = 1#updating the jth position
#            self.basis.append(u)
            self.vertices.append(guess+random.uniform(0,2)*u)#appending the guess as the first vertex
            j += 1#increasing the value of j to get the right basis array.
            
class SimpTransform:
    '''
    The SimpTransform class deals with transforming the simplex.
    
    To create an object from the class you need to load the
    load a simplex into the class i.e SimpTranform(Simplex(guess)).
    Then you will have access to transforming the simplex.
    
    Each method will have their own documentation.
    
    '''
    def __init__(self,simplex):
        self.simplex = simplex #simplex = Simplex(guess)
        self.costcomparer = -1 # used for comparing lowest cost between the last and current iteration
        self.tol = 1 # used for looking at the absolute difference between the cost of the last and current iteraiton
        
        
    @staticmethod 
    def evaluate(costfunction,vertex):
        '''
        This method takes the cost function and arguments
        and evaluates the costfunction at the argument.
        '''
        return costfunction(vertex)
        
    def ordering(self,costfunction):
        '''
        Looks at the list of vertices from Simplex.vertices and
        finds the vertex the gives the highest cost, 2nd highest cost and
        the lowest cost.
        '''
        costlist = [SimpTransform.evaluate(costfunction,x) for x in self.simplex.vertices]#Evaluates all the positions of the difference vertices
#        print('costlist \n',costlist)
#        print('vertivces \n',self.simplex.vertices)
        
        self.i_h = costlist.index(max(costlist))#finds index of vertex that gives highest cost
        self.f_h = max(costlist)#sets f_h to the max cost
        
        self.i_l = costlist.index(min(costlist))#finds index of vertex that gives lowest cost
        self.f_l = min(costlist)#sets f_l to the min cost
        
        costlist[costlist.index(max(costlist))] = min(costlist)#switches highest cost to lowest so that 2nd highest becomes highest
        
        self.i_s = costlist.index(max(costlist))#finds the index of vertex that gives the second highest cost
        self.f_s = max(costlist)#sets f_s to the 2nd highest cost
        
    def centroid(self):
        '''
        Computes the centroid between all the vertices except the vertex 
        that gives the highest cost.
        '''
        self.c = np.zeros(self.simplex.dimensions)#used later to add up all the vertices
        for i in range(len(self.simplex.vertices)):#goes through the vertex list
            if i == self.i_h:#used for not adding the vertex that gives highest cost
#                print('+++++++++++++++')
#                print(vertex)
                pass
            else:
#                print('--------------')
#                print('the vertex in',vertex)
                self.c += 1/self.simplex.dimensions*self.simplex.vertices[i]#adding the rest of the vertices and divinding by the dimension
#                print('c',self.c)
    def reflection(self,costfunction):
        '''
        'a' is a constant, the value was set from literature.
        The method computes the where the reflection of the point that 
        gives the highest cost gets reflected across the centroid.
        
        returns the cost at the reflected point.
        '''
        a = 1 #constans reflaction
        self.x_r = self.c + a*(self.c-self.simplex.vertices[self.i_h])#computing reflections
        return SimpTransform.evaluate(costfunction,self.x_r)
    
    def updateReflect(self):
        '''
        Used for updating the vertex that gives the highest cost to the reflected position.
        '''
        self.simplex.vertices[self.i_h] = self.x_r#updating simplex vertex that gave highest cost
        
    def expand(self,costfunction):
        '''
        'g' is a constant, the value was set from literature.
        The method computes where the point that gives the highest cost
        will be expanded to.
        
        return the cost at the expanded point.
        '''
        g = 2
        self.x_e = self.c + g*(self.x_r-self.c)#computing expansion
        return SimpTransform.evaluate(costfunction,self.x_e)
    
    def updateExpand(self):
        '''
        Used for updating the vertex that gives the highest cost to the expanded positoin.
        '''
        self.simplex.vertices[self.i_h] = self.x_e#updating simplex vertex
    
    def contractO(self,costfunction):
        '''
        'b' is a constant, the value was set from literature.
        The method computes where the point that gives the highest cost
        will be contracted to after expansion. ContractO stands for
        "contract outside".
        
        returns the cost at the contracted point
        '''
        b = 1/2
        self.x_c = self.c+b*(self.x_r-self.c)
        return SimpTransform.evaluate(costfunction,self.x_c)
        
    def contractI(self,costfunction):
        '''
        'b' is a constant, the value was set from literature.
        The method computes where the point that gives the highest cost
        will be contracted to after expansion. ContractI stands for
        "contract inside".
        
        returns the cost at the contracted point
        '''
        b = 1/2
        self.x_c = self.c+b*(self.simplex.vertices[self.i_h]-self.c)
        return SimpTransform.evaluate(costfunction,self.x_c)
    
    def updateContract(self):
        '''
        Used for updating the vertex that gives the highest cost to the expanded positoin.
        '''
        self.simplex.vertices[self.i_h] = self.x_c
        
        
    def shrink(self):
        '''
        Shrinks the simplex.
        '''
        for i in range(len(self.simplex.vertices)):
            d = 1/2
            self.simplex.vertices[i] = self.simplex.vertices[self.i_l]+d*(self.simplex.vertices[i]-self.simplex.vertices[self.i_l])
    
    def tolerance(self):
        '''
        Sees the difference between the lowest cost between the last iteration
        and current iteration.
        '''
        if self.f_l == self.costcomparer:#just a condition incase the previous and current iteration have the same cost
            pass
        else:
            self.tol = abs(self.f_l-self.costcomparer)
            self.costcomparer = self.f_l#updates costcomparer
        
        
#%%
class NMalgorithm():
    '''
    This class is the algorithm.
    
    transformation: The SimplexTransfrom class without any inputs.
    
    simplex: The Simplex class with inputs so Simplex(guess).
    
    costfunction: The cost function of the problem
    
    tolerance: The difference you want between the cost of the previous and current iteration
                if the cost difference is below this tolerance, then the while loop terminates.
    '''
    def __init__(self,transformations,simplex,costfunction,tolerance):
        self.trans = transformations(simplex)#defines a attribute
        self.best_vertex = None
        self.best_cost = None
        self.iteraitons = None
        i = 0#used for counting iterations
#        print('The simplex before the loop',self.trans.simplex.vertices)
        while tolerance<self.trans.tol:#terminating condition
            self.trans.ordering(costfunction)#Start by ordering the vertices, find best,2nd worst and worst cost.
            self.trans.centroid()#Compute the centroid
            self.trans.tolerance()#Compute the tolerance
            ref = self.trans.reflection(costfunction)#compute the reflection ref := f_r := costfunction(x_r)
            
            if self.trans.f_l <= ref < self.trans.f_s:#condition 1: if cost of reflected point is between lowest and second highest cost.
#                print('IN CONDITION 1')
                self.trans.updateReflect()#update the vertex that gives the highest cost
                i += 1#add one to the iteration counter
                continue#terminates the current iteration and starts a new one from the beginning
            
            elif ref < self.trans.f_l:#condition 2: if cost of reflected point lower than lowest cost
                exp = self.trans.expand(costfunction)#expand the reflected point and compute new cost exp
                if exp < ref:#if cost at expanded point lower than cost at reflected
#                    print('IN CONDITION 2 IF STATEMENT')
                    self.trans.updateExpand()#update the vertex that gives the highest cost to expaned point
                    i += 1
                    continue
                elif exp >= ref:#or else if cost of expanded greater than or equal to cost of reflected point
#                    print('IN CONDITION 2 ELIF STATEMENT')
                    self.trans.updateReflect()#update the vertex that give the highest cost to reflected point
                    i += 1
                    continue
                
            elif ref >= self.trans.f_s:#if cost of reflected point greater than or equal to the lowest cost
                if self.trans.f_s <= ref <self.trans.f_h:#if cost of reflected point between second worst and worst
                    conO = self.trans.contractO(costfunction)#compute outside contracted point and cost
                    if conO <= ref:#if cost of outside contracted point less than or equal to reflected point cost
#                        print('IN CONDITION 3  1ST IF STATEMENT')
                        self.trans.updateContract()#update vertex that gives highest cost to outside contracted point
                        i += 1
                        continue
                    else:
#                        print('IN CONDITION 3  1ST ELSE STATEMENT')
                        self.trans.shrink()#else shirnk the simplex
            
                if ref >= self.trans.f_h:#if cost of reflected point greater than or equal to highest cost
                    conI = self.trans.contractI(costfunction)#compute inside contractions point and cost
                    if conI < self.trans.f_h:# if cost of inside contracted point lower than highest cost
#                        print('IN CONDITION 3  2ND IF STATEMENT')
                            #terminate iteration and accept x_c
                        self.trans.updateContract()#update vertex that gives the highest cost to inside contracted point
                        i += 1
                        continue
                    else:
#                        print('IN CONDITION 3  2ND ELSE STATEMENT')
                        self.trans.shrink()#else shrink the simplex
            i += 1
        self.iterations = i
        self.best_cost = self.trans.f_l
        self.best_vertex = self.trans.simplex.vertices[self.trans.i_h]
        print('The number of iterations',i)    
#        print('The simplex after the loop',self.trans.simplex.vertices)
        print('The best vertex',self.best_vertex)
        print('The cost',self.best_cost)
                            
                        
                        
            
                
                    
                    
                        
                        
                    
                    
                
                    
                    
                
            
            
        
        
        
        
        
        
        
        
#%% Testing simplex
            
#guess = np.array([1,2])
#
#simp = Simplex(guess)
#print(simp.vertices)


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

#%%Testing transform ordering
#f = partial(costfunc,pts)
#sit = SimpTransform(simp)
#sit.ordering(f)
#print('vertex that gives highest cost',sit.f_h)
#print('vertex that gives second highest cost',sit.f_s)
#print('vertex that gives lowest cost',sit.f_l)
#%%Testing centroid
#sit.centroid()
#sit.c
#%% Testing reflections
#sit.reflection(f)
#print('reflected',sit.x_r)

#%% Testing NM algorithm

#transformations = SimpTransform
#simplex = Simplex(guess)
#iterations = 90
#tolerance = 1e-15
#NM = NMalgorithm(transformations,simplex,f,tolerance)
#m,b = np.polyfit(X,Y,1)
#print(m,b)