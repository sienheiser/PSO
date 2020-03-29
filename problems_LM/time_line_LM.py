# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 14:32:00 2020

@author: coolb
"""

import timeit as tt

mycode = '''
opt.np.random.seed(42)
def vert_dist(x,y,a,b):
    return y-a[0]*x-b[0]
pts = opt.np.random.rand(10,2)
li = [opt.Vec(1),opt.Vec(1)]
u = opt.Optimizer()
for x,y in pts:
    u.add_residual(opt.partial(vert_dist,x,y),li[0],li[1])

u.optimize()
'''

mysetup = '''
import optimizer as opt
'''

print('This time is',tt.timeit(setup = mysetup,stmt = mycode, number = 100)/100)

