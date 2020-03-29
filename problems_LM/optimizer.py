# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 14:24:08 2020

@author: coolb
"""

#%%
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import spsolve as sparse_solve
from math_utils import *
from functools import partial
from ascii_art import *


#%%





#%%   
class Optimizer:

    def __init__(self):
        self.elim_blocks, self.elim_plen = {}, 0
        self.surv_blocks, self.surv_plen = {}, 0
        self.residuals = []

    @staticmethod
    def add_block(blocks, tot_plen, arg):
        uid = id(arg)
        if uid not in blocks:
            l, pl = len(arg), param_len(arg)
            blocks[uid] = (arg, (tot_plen, tot_plen+pl))
            return tot_plen+pl
        return tot_plen

    def add_residual(self, func, *arguments):
        self.elim_plen = Optimizer.add_block(self.elim_blocks, self.elim_plen, arguments[0])
        for argx in arguments[1:]:
            self.surv_plen = Optimizer.add_block(self.surv_blocks, self.surv_plen, argx)
        pranges = [(self.elim_blocks if i==0 else self.surv_blocks)[id(arg)][1] for i, arg in enumerate(arguments)]
        self.residuals.append((func, arguments, pranges))

    # optimize only `eliminee` blocks (ie. points in bundle adjustment)
    def optimize_eliminees(self, dampingL=0.1, dampingQ=0.01):

        self.elim_grad.fill(0)
        self.C.data.fill(0)

        cost = 0
        for f, args, pranges in self.residuals:

            res, pders = Jet.compute_first_order_d_arg0(f, *args)
            cost += res*res*0.5 # cost contribution

            i0, iz = pranges[0]
            self.elim_grad[i0:iz] += res * pders
            self.C[i0:iz, i0:iz] += pders.reshape(-1,1) * pders

        yield 'updated_eliminees_gradient'

        for arg, (a0, az) in self.elim_blocks.values():
            block = self.C[a0:az, a0:az].toarray()
            damped_block = block + np.diag(block.diagonal() * dampingL + dampingQ)
            step = -np.linalg.solve(damped_block, self.elim_grad[a0:az])
            self.elim_step[a0:az] += step #account in done step
            apply_parametrized_step(arg, step)

        yield 'applied_eliminees_step'

#        print('...cost={0}, applying micro step'.format(cost))

    # run optimization
    def optimize(self):
#        print('-------------------Starting optimize---------------------------------')
        for event in self.optimize_it():
            pass

    # run optimization, with control inversion on events
    def optimize_it(self):
#        print('Baby-Apophis is up and toddling its baby optimization-steps!\n\n' + ASCII_BABY)

        # create gradient, step vectors (state stays in given block refs)
        self.elim_grad = np.ndarray(self.elim_plen, dtype=np.float64)
        self.surv_grad = np.ndarray(self.surv_plen, dtype=np.float64)
        self.elim_step = np.ndarray(self.elim_plen, dtype=np.float64)
        self.surv_step = np.ndarray(self.surv_plen, dtype=np.float64)
        
#        print('The value of elim_plen is {0} and surv_plen is {1}'.format(self.elim_plen,self.surv_plen))
#        print('This elim_grad',self.elim_grad)
#        print('This is surv_grad',self.surv_grad)
#        print('This is elim_step',self.elim_step)
#        print('This is surv_step',self.surv_step)
#        print('----------------Passing the first step-----------------------------')

        # create matrices
        self.B = lil_matrix((self.surv_plen, self.surv_plen))
        self.C = lil_matrix((self.elim_plen, self.elim_plen))
        self.E = lil_matrix((self.surv_plen, self.elim_plen))
        for f, args, pranges in self.residuals:
            for i, (i0, iz) in enumerate(pranges):
                for j, (j0, jz) in zip(range(i+1), pranges):
                    mat = self.B if j>=1 else (self.E if i>=1 else self.C)
                    mat[i0:iz, j0:jz] = 1.0
        self.B = (self.B + self.B.T).tocsr()  # make B symmetric
        self.C = self.C.tocsr()
        self.dampedCinv = self.C.copy()
        self.E = self.E.tocsr()
        
#        print('This is matrix B \n',self.B.todense())
#        print('This is matrix C \n',self.C.todense())
#        print('This is matrix dampedCin \n',self.dampedCinv.todense())
#        print('This is matrix E \n',self.E.todense())
#        print('-----------------Passing the second step---------------------------')

        dampingL = 0.01
        dampingQ = 0.01
        

        # main loop
        model_cost_change, prev_cost = None, None
        for num_iterations in range(1000):
            self.elim_grad.fill(0)
            self.surv_grad.fill(0)
            self.B.data.fill(0)
            self.C.data.fill(0)
            self.E.data.fill(0)
#            print('This elim_grad',self.elim_grad)
#            print('This is surv_grad',self.surv_grad)
#            print('This is matrix B \n',self.B.todense())
#            print('This is matrix C \n',self.C.todense())
#            print('This is matrix E \n',self.E.todense())

            # evaluate all residuals, add contributions to cost, gradient, hessian
            cost = 0
#            print('-------------------Passing the third step-------------------')
            for f, args, pranges in self.residuals:
#                print('this is f',f)
                res, pders = Jet.compute_first_order(f, *args)
#                print('res,pders',res,pders)
#                print('args',args)
               
                cost += res*res*0.5 # cost contribution
#                print('pranges',pranges)
#                print('=========cost',cost)
                

                for i, (i0, iz) in enumerate(pranges):
#                    print('++++++++i',i)
                    (self.surv_grad if i>=1 else self.elim_grad)[i0:iz] += res * pders[i] # gradient block
#                    if i>=1:
#                        print('This is surv_grad',self.surv_grad)
#                    else:
#                        print('This is elim_grad',self.elim_grad)
                    for j, (j0, jz) in zip(range(i+1), pranges):
#                        print('----------j',j)
                        mat = self.B if j>=1 else (self.E if i>=1 else self.C)
                        
#                        print('pders[i] is {0} and pders[j] is {1}'.format(pders[i],pders[j]))
                        block = pders[i].reshape(-1,1) * pders[j]
#                        print('block',block)
                        
                        mat[i0:iz, j0:jz] += block  # B, C, E blocks
                        if 1 <= j < i:
                            mat[j0:jz, i0:iz] += block.T  # make B symmetric
                            
#            print('----------------Passing the fourth step-------------------')
            yield 'updated_gradient' # invert control, gradient was computed
                            
            # tweak damping parameter (lambda)
#            print('The model_cost_change and prev_cost are',model_cost_change,prev_cost)
            if model_cost_change is not None:
                model_cost_change += 0.5 * (self.elim_grad.dot(self.elim_step) + self.surv_grad.dot(self.surv_step))
                #print('cost={0}, prev_cost={1}, model_delta={2}'.format(cost, prev_cost, model_cost_change))
                mood = Moods.Excited
                if model_cost_change >= 0 or (prev_cost-cost < -0.25 * model_cost_change):
                    dampingL *= 1.5
                    mood = Moods.Worried
                elif prev_cost - cost > -0.5 * model_cost_change:
                    dampingL *= 0.7
                if cost > prev_cost:
                    mood = Moods.Crying
            else:
                mood = Moods.Facepalm
#            print('--------------Passing the fifth step----------------------')
#            print('The model_cost_change and prev_cost are',model_cost_change,prev_cost)
            # print status, 1/2
#            print('{0} cost={1} mΔ={2} λ={3} |∇ₛ|∞={4} |∇ₑ|∞={5}'.format(mood.value, cost,
#                                           model_cost_change, dampingL,
#                                           np.max(self.surv_grad), np.max(self.elim_grad)), end='')
            if (max(np.max(self.surv_grad), np.max(self.elim_grad)) < 1e-12
                or (prev_cost is not None and prev_cost - 1e-6 < cost < prev_cost)):
#                print('\n{0} unable to improve cost further, stopping'.format(Moods.Shrug.value))
                break
#            print('\n -------------------passing the sixth step-------------------')
#            print('The model_cost_change and prev_cost are',model_cost_change,prev_cost)
            # damp and invert all blocks in C, putting them into dampedCinv
            for arg, (a0, az) in self.elim_blocks.values():
#                print('This is matrix C \n',self.C.todense())
                block = self.C[a0:az, a0:az].toarray()
#                print('This is block \n',block)
                self.dampedCinv[a0:az, a0:az] = np.linalg.inv(block + np.diag(block.diagonal() * dampingL + dampingQ))
#                print('This is dampedCinv \n',self.dampedCinv.todense())
#            print('--------------------passing the seventh step---------------')
#            print('The model_cost_change and prev_cost are',model_cost_change,prev_cost)
            # compute Schur complement
            self.B.setdiag(self.B.diagonal()*(1 + dampingL) + dampingQ)  # damp B
#            print('This is matrix B \n',self.B.todense())
            
            S = self.B - self.E @ (self.dampedCinv @ self.E.T)
#            print('This is S \n',S.todense())
#            print('----------------------passing the eigth step---------------')
            # compute the steps
            self.surv_step = -sparse_solve(S, self.surv_grad - self.E @ (self.dampedCinv @ self.elim_grad))
#            print('surv_step',self.surv_step)
            
            self.elim_step = self.dampedCinv @ (-self.elim_grad - self.E.T @ self.surv_step)
#            print('elim_step',self.elim_step)
            # print status, 2/2
#            print(' |Sₛ|∞={0} |Sₑ|∞={1}'.format(np.max(self.surv_step), np.max(self.elim_step)))
#            print('-------------------------passing the ninth step-----------------')

            # apply step
#            print('surv_block',self.surv_blocks)
            for arg, (a0, az) in self.surv_blocks.values():
                apply_parametrized_step(arg, self.surv_step[a0:az])
#            print('surv_block',self.surv_blocks)

            for arg, (a0, az) in self.elim_blocks.values():
                apply_parametrized_step(arg, self.elim_step[a0:az])

            yield 'applied_step' # invert control, step was applied
#            print('-------------------------passing the tenth step-----------------')
            # compute model change, save cost
            model_cost_change = 0.5 * (self.elim_grad.dot(self.elim_step) + self.surv_grad.dot(self.surv_step))
            prev_cost = cost
#            print('model_cost_change',model_cost_change)
#            print('prev_cost',prev_cost)
#            print('-------------------------passing the eleventh step-----------------')
            # here, optimize eliminees? a few steps?
            for i in range(2):
                for event in self.optimize_eliminees():
                    yield event
#            print('-------------------------passing the twelfth step-----------------')