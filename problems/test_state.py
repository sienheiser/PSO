# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 12:06:01 2020

@author: coolb
"""
#%%
import numpy as np
import math_utils as ma



#%%  test state for bundle adjustment

points = [ma.Vec(*[-0.50183952461055, 1.8028572256396647, 3.9279757672456204]), 
          ma.Vec(*[0.3946339367881464, -1.375925438230254, 1.6239780813448106]),
          ma.Vec(*[-1.7676655513272022, 1.4647045830997407, 3.404460046972835]), 
          ma.Vec(*[0.832290311184182, -1.9176620228167902, 4.879639408647977]), 
          ma.Vec(*[1.329770563201687, -1.1506435572868954, 1.7272998688284025]), 
          ma.Vec(*[-1.2663819605862647, -0.7830310281618491, 3.0990257265289514]), 
          ma.Vec(*[-0.27221992543153695, -0.8350834392078323, 3.447411578889518]), 
          ma.Vec(*[-1.4420245573918327, -0.8314214058591274, 2.465447373174767]), 
          ma.Vec(*[-0.17572006313185629, 1.1407038455720544, 1.798695128633439]), 
          ma.Vec(*[0.05693775365444642, 0.36965827544816987, 1.185801650879991])]

cameras = [(ma.Quat(1.0, 0.0, 0.0, 0.0), ma.Vec(0.0, 0.5, 0.0)),
                    (ma.Quat(1.0, 0.0, 0.0, 0.0), ma.Vec(0.0, -0.5, 0.0)) ]

observations = [(i, j, (cam_q(pt) + cam_t).normalized())
                        for i, pt in enumerate(points)
                        for j, (cam_q, cam_t) in enumerate(cameras)]

noisy_points = [p + (np.random.rand(3)*0.4 - 0.2) for p in points]

noisy_cameras =  [
            (ma.Quat(q + (np.random.rand(4)*0.1-0.05), normalize=True), t + (np.random.rand(3)*0.2-0.1))
            for q,t in cameras
        ]


#%%

def residual(feature_vec, point, camera_quat, camera_tr):
    point_cap = ma.Quat(*camera_quat)(point) + camera_tr
    observed_dir = point_cap.normalized()
    chordal_length = ma.sqrt((observed_dir - feature_vec).squared_norm() + 1e-32)
    return chordal_length

#%% defining bundle adjustmnet state where noisy_points are the only parameters 
# observations and cameras are given
def bundle_adjust(observations,cameras,noisy_points):
    cost = 0
    for i,j,feat in observations:
        cost += residual(feat,noisy_points[i],cameras[j][0],cameras[j][1])**2
    return cost

#%%

        


