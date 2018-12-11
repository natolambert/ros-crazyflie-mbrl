# -*- coding: utf-8 -*-
import torch
import rlkit
import joblib
from quad_env import QuadEnv
import numpy as np
import matplotlib.pyplot as plt

data = joblib.load('/home/hiro/dynamics-learn/output/tsac-quad/tsac-quad_2018_12_04_14_42_45_0000--s-0/params.pkl')


policy = data['policy']
env = data['env']

o  = env.reset()
print(o)

h = 50
a1, a2, a3, a4 = [], [], [], []
pitch, roll, yaw = [], [], []
for i in range(h):
    a, _ = policy.get_action(o)
    o, _, _, _ = env.step(a)
    # o = env.reset()

    rescale = lambda v: (v+1)*(50000-30000.0)/2 + 30000
    unnormalized_a = np.fromiter((rescale(xi) for xi in a), a.dtype, count=len(a))
    a1.append(unnormalized_a[0])
    a2.append(unnormalized_a[1])
    a3.append(unnormalized_a[2])
    a4.append(unnormalized_a[3])
    pitch.append(o[3])
    roll.append(o[4])
    yaw.append(o[5])


ax1 = plt.subplot(421)
plt.plot(range(h), a1)

ax2 = plt.subplot(423)
plt.plot(range(h), a2)

ax3 = plt.subplot(425)
plt.plot(range(h), a3)

ax4 = plt.subplot(427)
plt.plot(range(h), a4)

ax5 = plt.subplot(422)
plt.plot(range(h), pitch)

ax6 = plt.subplot(424)
plt.plot(range(h), roll)

ax6 = plt.subplot(426)
plt.plot(range(h), yaw)

plt.show()
