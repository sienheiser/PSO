# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 11:05:19 2020

@author: coolb
"""

import numpy as np
import math
from functools import partial


# simple vector class
class Vec:
    def __init__(self, *values):
        if len(values) == 1 and isinstance(values[0], (Quat, Vec, list, tuple, np.ndarray)):
            self.values = list(values[0])
        else:
            self.values = list(values)

    def __add__(self, other):
        assert(len(self.values) == len(other))
        return Vec(*[v+other[i] for i,v in enumerate(self.values)])

    def __iadd__(self, other):
        for i in range(len(self.values)):
            self.values[i] += other[i]
        return self

    def __radd__(self, other):
        assert(len(self.values) == len(other))
        return Vec(*[v+other[i] for i,v in enumerate(self.values)])

    def __sub__(self, other):
        assert(len(self.values) == len(other))
        return Vec(*[v-other[i] for i,v in enumerate(self.values)])

    def __isub__(self, other):
        for i in range(len(self.values)):
            self.values[i] -= other[i]
        return self

    def __rsub__(self, other):
        assert(len(self.values) == len(other))
        return Vec(*[other[i]-v for i,v in enumerate(self.values)])

    def __mul__(self, other):
        return Vec(*[v*other for v in self.values])

    def __imul__(self, other):
        for i in range(len(self.values)):
            self.values[i] *= other
        return self

    def __rmul__(self, other):
        return Vec(*[v*other for v in self.values])

    def __truediv__(self, other):
        return Vec(*[v/other for v in self.values])

    def __itruediv__(self, other):
        for i in range(len(self.values)):
            self.values[i] /= other
        return self

    def __neg__(self):
        return Vec(*[-v for v in self.values])

    def __repr__(self):
        return "Vec" + str(self.values)

    def __len__(self):
        return len(self.values)
    
    def __getitem__(self, key):
        return self.values[key]
    
    def __setitem__(self, key, value):
        self.values[key] = value

    def __iter__(self):
        return self.values.__iter__()

    def copy(self):
        return Vec(*self)
    
    def dot(self, other):
        assert(len(self.values) == len(other))
        retv = self[0] * other[0]
        for i in range(1, len(self.values)):
            retv += self[1] * other[1]
        return retv

    def squared_norm(self):
        retv = self[0] * self[0]
        for i in range(1, len(self.values)):
            retv += self[i] * self[i]
        return retv

    def norm(self):
        return sqrt(self.squared_norm())

    def normalized(self):
        return self / self.norm()

    def normalize(self):
        self.values = self.normalized().values

    def cross(self, other):
        assert(len(self.values) == 3)
        assert(len(other.values) == 3)
        return Vec(
            self[1]*other[2]-self[2]*other[1],
            self[2]*other[0]-self[0]*other[2],
            self[0]*other[1]-self[1]*other[0])


# quaternion vector class
class Quat:
    def __init__(self, *values, normalize=False):
        if len(values) == 4:
            self.w, self.x, self.y, self.z = values
        elif len(values) == 1 and isinstance(values[0], (Quat, Vec, list, tuple, np.ndarray)) and len(values[0]) == 4:
            self.w, self.x, self.y, self.z = values[0]
        elif len(values) == 0 and isinstance(values[1], (Vec, list, tuple, np.ndarray)) and len(values[1]) == 3:
            self.w, (self.x, self.y, self.z) = values[0], values[1]
        else:
            raise Exception('could not construct Quat from {0}, len={1}'.format(values, len(values)))
        if normalize:
            self.normalize()

    def __invert__(self):
        return Quat(self.w, -self.x, -self.y, -self.z)

    def __repr__(self):
        return "Quat" + str([self.w, self.x, self.y, self.z])

    def __iter__(self):
        return [self.w, self.x, self.y, self.z].__iter__()

    def __getitem__(self, key):
        return getattr(self, 'wxyz'[key])

    def __len__(self):
        return 4

    def __param_len__(self):
        return 3

    def __parametrize__(self, g):
        return Vec(
            Vec(self.x, -self.w, self.z, -self.y).dot(g),
            Vec(self.y, self.z, -self.w, -self.x).dot(g),
            Vec(self.z, -self.y,-self.x, self.w).dot(g)
        )

    def __apply_parametrized_step__(self, dg):
        # print('currq=', self, 'dg=', dg)
        delta = (dg[0] * Vec(self.x, -self.w, self.z, -self.y) +
                 dg[1] * Vec(self.y, self.z, -self.w, -self.x) +
                 dg[2] * Vec(self.z, -self.y,-self.x, self.w))
        self.w, self.x, self.y, self.z = (self.coeffs() + delta).normalized()
        # print('newq=', self)

    @staticmethod
    def _product_coeffs(a, b):
        return (a.w * b.w - a.x * b.x - a.y * b.y - a.z * b.z,
                a.w * b.x + a.x * b.w + a.y * b.z - a.z * b.y,
                a.w * b.y + a.y * b.w + a.z * b.x - a.x * b.z,
                a.w * b.z + a.z * b.w + a.x * b.y - a.y * b.x)
        
    def __mul__(self, other):
        return Quat(*Quat._product_coeffs(self, other))
        
    def __imul__(self, other):
        self.w, self.x, self.y, self.z = Quat._product_coeffs(self, other)

    def copy(self):
        return Vec(*self)

    def angle(self):
        return 2.0 * asin(min(self.vec().norm(), 1.0))
        
    def coeffs(self):
        return Vec(self.w, self.x, self.y, self.z)

    def normalize(self):
        self.w, self.x, self.y, self.z = self.coeffs().normalized()

    def vec(self):
        return Vec(self.x, self.y, self.z)

    def __call__(self, v):
        uv = 2.0 * self.vec().cross(v)
        return v + self.w * uv + self.vec().cross(uv)


# simple transform (quaternion+translation) class
class Transform:
    def __init__(self, q, t):
        self.q, self.t = q, t

    def __call__(self, other):
        return self.q(other) + self.t

    def __mul__(self, other):
        return Transform(self.q * other.q, self.q(other.t) + self.t)

    def __imul__(self, other):
        self.q, self.t = self.q * other.q, self.q(other.t) + self.t

    def __invert__(self):
        return Transform(~self.q, - (~self.q)(self.t))

    def __getitem__(self, key):
        return getattr(self, 'qt'[key])


# simple jet evaluation class
class Jet:
    def __init__(self, value: float, pders: np.ndarray):
        self.value = value
        self.pders = pders

    @staticmethod
    def var(value: float, index: int):
        pders = np.zeros(index+1)
        pders[index] = 1.0
        return Jet(value, pders)

    def block(values: np.array, start_index: int):
        return Vec(*[Jet.var(v, start_index+i) for i,v in enumerate(values)])

    def __repr__(self):
        return "{0}:{1}".format(self.value, list(self.pders))
    
    @staticmethod
    def ensure_pders_same_size(a, b):
        sa = len(a.pders)
        sb = len(b.pders)
        if sa == sb:
            return
        if sa < sb:
            a.pders.resize(sb, refcheck = False) # don't check cross-references
        else:
            b.pders.resize(sa, refcheck = False)

    def __add__(self, other):
        if isinstance(other, (float, int)):
            return Jet(self.value + other, self.pders)
        if not isinstance(other, Jet):
            return NotImplemented
        Jet.ensure_pders_same_size(self, other)
        return Jet(self.value + other.value, self.pders + other.pders)

    def __radd__(self, other):
        if isinstance(other, (float, int)):
            return Jet(self.value + other, self.pders)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, (float, int)):
            return Jet(self.value - other, self.pders)
        if not isinstance(other, Jet):
            return NotImplemented
        Jet.ensure_pders_same_size(self, other)
        return Jet(self.value - other.value, self.pders - other.pders)

    def __rsub__(self, other):
        if isinstance(other, (float, int)):
            return Jet(other - self.value, -self.pders)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return Jet(self.value * other, self.pders * other)
        if not isinstance(other, Jet):
            return NotImplemented
        Jet.ensure_pders_same_size(self, other)
        return Jet(self.value * other.value, self.pders * other.value + other.pders * self.value)

    def __rmul__(self, other):
        if isinstance(other, (float, int)):
            return Jet(self.value * other, self.pders * other)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            return Jet(self.value / other, self.pders / other)
        if not isinstance(other, Jet):
            return NotImplemented
        Jet.ensure_pders_same_size(self, other)
        inv_other_v = 1.0 / other.value
        return Jet(self.value * inv_other_v, self.pders * inv_other_v - other.pders * (self.value * inv_other_v * inv_other_v))

    def __neg__(self):
        return Jet(-self.value, -self.pders)

    def sqrt(self):
        sqrt_val = math.sqrt(self.value)
        return Jet(sqrt_val, self.pders * (0.5 / sqrt_val))

    def asin(self):
        asin_val = math.asin(self.value)
        factor = 1.0 / math.sqrt(1.0 - self.value*self.value)
        return Jet(asin_val, self.pders * factor)

    def acos(self):
        acos_val = math.acos(self.value)
        factor = -1.0 / math.sqrt(1.0 - self.value*self.value)
        return Jet(acos_val, self.pders * factor)

    @staticmethod
    def compute_first_order(function, *argv):
        '''
        function: function whose derivatives need to be computed
        argv: arguments of function
        returns output of function at a point and also the partial derivatives
        of all the arguments at that point.
        Has the form
        result:[pders]
        '''
        first_order_args, indices, lengths = [], [], []
        start_index = 0
        for arg in argv:
            indices.append(start_index)
            if isinstance(arg, (Quat, Vec, np.ndarray, list, tuple)):
                first_order_args.append(Jet.block(arg, start_index))
                start_index += len(arg)
                lengths.append(len(arg))
            else:
                first_order_args.append(Jet.var(arg, start_index))
                start_index += 1
                lengths.append(1)
        result = function(*first_order_args)
#        print('This is result',result)
        if isinstance(result,(Quat, Vec, np.ndarray, list, tuple)):#adding because sometimes result =[result]
            result = result[0]
        else:
            result = result
#        print('This is result',result)
        pders = result.pders
        if len(pders) < start_index:
            pders = np.array(pders)
            pders.resize(start_index)
        return (result.value, [parametrize(arg, pders[i:(i+l)]) for arg, i, l in zip(argv, indices, lengths)])

    @staticmethod
    def compute_first_order_d_arg0(function, *argv):
        if isinstance(argv[0], (Quat, Vec, np.ndarray, list, tuple)):
            arg0 = Jet.block(argv[0], 0)
        else:
            arg0 = Jet.var(argv[0], 0)
        
        
        result = function(arg0, *argv[1:])
#        print('This is result',result)
        if isinstance(result, (Quat, Vec, np.ndarray, list, tuple)):
            result = result[0]
        else:
            result = result
#        print('This is result',result)
        return (result.value, result.pders)

def sqrt(x):
    if isinstance(x, Jet):
        return x.sqrt()
    return np.sqrt(x)

def asin(x):
    if isinstance(x, Jet):
        return x.asin()
    return math.asin(x)

def acos(x):
    if isinstance(x, Jet):
        return x.acos()
    return math.acos(x)

def param_len(x):
    return x.__param_len__() if hasattr(x, '__param_len__') else len(x)

def parametrize(x, dx):
    return np.array(x.__parametrize__(dx)) if hasattr(x, '__parametrize__') else dx

def apply_parametrized_step(x, dx):
    if hasattr(x, '__apply_parametrized_step__'):
        print('I am in if loop')
        x.__apply_parametrized_step__(dx)
    else:
        print('I am in else loop')
        print(x)
        print(dx)
        x += dx


# simple test
if __name__ == "__main__":
    def my_func(xy, zw, q):
        return xy.dot(zw) + sqrt(q)

    retv = Jet.compute_first_order(my_func, [0.1, 0.2], [4, 5], 7)
    print(retv)
    
    
#%%
    





#%%


#%%


#%%

