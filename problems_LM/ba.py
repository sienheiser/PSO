# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 14:48:28 2020

@author: coolb
"""

from optimizer import *
#%%
class State:
    def __init__(self, NUM_CAMERAS = 2, NUM_POINTS = 10):
        np.random.seed(42)

        # inizialize points and camera vectors.
        self.points = [Vec(v) for v in (np.random.rand(NUM_POINTS,3)*4.0 + [-2,-2,1])]
        self.cameras = [ (Quat(1.0, 0.0, 0.0, 0.0), Vec(0.0, 0.5, 0.0)),
                    (Quat(1.0, 0.0, 0.0, 0.0), Vec(0.0, -0.5, 0.0)) ]
        # construct observation through __call__ magic method of Quat
        self.observations = [(i, j, (cam_q(pt) + cam_t).normalized())
                        for i, pt in enumerate(self.points)
                        for j, (cam_q, cam_t) in enumerate(self.cameras)]

        # prepare input data
        # noisy_points = [Vec(v) for v in (np.random.rand(NUM_POINTS,3)*4.0 + [-2,-2,1])]
        self.noisy_points = [p + (np.random.rand(3)*0.4 - 0.2) for p in self.points]  # apply small perturbation
        # make some random 0.05 variation around the initialized cameras
        self.noisy_cameras = [
            (Quat(q + (np.random.rand(4)*0.1-0.05), normalize=True), t + (np.random.rand(3)*0.2-0.1))
            for q,t in self.cameras
        ]


#%%
# residual
def residual(feature_vec, point, camera_quat, camera_tr):
    '''
    This is the cost function
    feature_vec: Noisless point
    point: Noisy point
    camera_quat: Quaternion (orientation of the camera) w.r.t global coordinate system
    camera_tr: Position of the camera w.r.t a global basis
    
    point_cap finds the observations using noisy points and noisy cameras
    chordal_length is the difference between the observed_dir and where the observations without
    noise are.
    
    '''
    point_cap = Quat(camera_quat)(point) + camera_tr
    observed_dir = point_cap.normalized()
    chordal_length = sqrt((observed_dir - feature_vec).squared_norm() + 1e-32)
    return chordal_length
#%%
def bundle_adjust(state):
    # create problem's Jet (add_residual) and solve it through gradient
    o = Optimizer()
    for i, j, feat in state.observations:
        ''' 
        i: index of points 
        j: index of cameras
        feat: points
        o.add_residual appends to o.redisduals((parital(residual,feat),[noisy_points,noisy_cameras],pranges))
        '''
        o.add_residual(partial(residual, feat), state.noisy_points[i], state.noisy_cameras[j][0], state.noisy_cameras[j][1])
    # note: intervene here with other optimizers
    o.optimize()

    # normalize scale (note: ~ is __invert__, *noisy is __imul__)
    scale = ((~Transform(*state.noisy_cameras[1])).t - (~Transform(*state.noisy_cameras[0])).t).norm()
    for i in range(len(state.noisy_points)):
        state.noisy_points[i] /= scale
    for i in range(len(state.noisy_cameras)):
        state.noisy_cameras[i] = (state.noisy_cameras[i][0], state.noisy_cameras[i][1]/scale)

    # normalize rot/translation
    transf = (~Transform(*state.cameras[0])) * Transform(*state.noisy_cameras[0])
    itransf = ~transf
    for i in range(len(state.noisy_points)):
        state.noisy_points[i] = transf(state.noisy_points[i])
    for i in range(len(state.noisy_cameras)):
        state.noisy_cameras[i] = tuple(Transform(*state.noisy_cameras[i]) * itransf)
        

#%%
def print_state(state):
# print errors in position/rotation for cameras and points
    print('cam errors:')
    for i in range(len(state.cameras)):
        t1 = (~Transform(*state.noisy_cameras[i])).t
        t2 = (~Transform(*state.cameras[i])).t
        dist = (t1-t2).norm()
        angle = (state.cameras[i][0] * (~state.noisy_cameras[i][0])).angle()
        print('  cam[{0}]: rot_err={1}, pos_err={2}\n    opt={3}\n    sol={4}'.format(i, angle, dist, t1, t2))
        break
    print('pt errors:')
    #for i in range(len(state.points)):
        #dist = (state.points[i]-state.noisy_points[i]).norm()
        #print('  pt[{0}]: pos_err={1}\n    opt={2}\n    sol={3}'.format(i, dist, state.noisy_points[i], state.points[i]))
        
        
#%%
state = State()

print("===== Initial State =====")
print_state(state)

bundle_adjust(state)
print("= Bundle Adjusted State =")
print_state(state)

#%%       Testing the code above
#Starting with print_state
print(print_state(state))
print((~Transform(*state.noisy_cameras[0])).t)
