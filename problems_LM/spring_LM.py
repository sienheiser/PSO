# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 14:28:43 2020

@author: coolb
"""

import optimizer as opt
#%%

def residual(k, v1, v2):
    return v2[0] - v1[0] - k

pts = [opt.Vec(x) for x in [-2, -1, 0, 0.5, 1.5, 2.5]]

o = opt.Optimizer()
o.add_residual(opt.partial(residual, 1), pts[0], pts[1])
o.add_residual(opt.partial(residual, -1), pts[2], pts[1])
o.add_residual(opt.partial(residual, 1), pts[2], pts[3])
o.add_residual(opt.partial(residual, -1), pts[4], pts[3])
o.add_residual(opt.partial(residual, 1), pts[4], pts[5])
    
o.optimize()

print('The points are',pts)