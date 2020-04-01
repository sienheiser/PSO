# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 16:32:05 2020

@author: coolb
"""
import optimizer as opt
import time
#%%
    
opt.np.random.seed(42)
#def residual(k, v1, v2):
#    return v2[0] - v1[0] - k
#
#pts = [Vec(x) for x in [-2, -1, 0, 0.5, 1.5, 2.5]]
#
#o = Optimizer()
#o.add_residual(partial(residual, 1), pts[0], pts[1])
#o.add_residual(partial(residual, -1), pts[2], pts[1])
#o.add_residual(partial(residual, 1), pts[2], pts[3])
#o.add_residual(partial(residual, -1), pts[4], pts[3])
#o.add_residual(partial(residual, 1), pts[4], pts[5])
#    
#print(o.residuals)
#o.optimize()



    
def vert_dist(x,y,a,b):
    '''
    pt: point (x,y)
    a: slope of line
    b: y-intercept
    '''
    return y-a[0]*x-b[0]



iterations = 1000
i = 0
avg_time = 0
avg_iter = 0

while i < iterations:

    pts = opt.np.random.rand(10,2)
    li = [opt.Vec(1),opt.Vec(1)]
    u = opt.Optimizer()
    
    for x,y in pts:
        u.add_residual(opt.partial(vert_dist,x,y),li[0],li[1])
        
    t0 = time.time()
    u.optimize()
    t1 = time.time()
    avg_iter += u.iterations/iterations
    avg_time += (t1-t0)/iterations
    i += 1


print('average iterations',avg_iter)
print('average_time',avg_time)

    

