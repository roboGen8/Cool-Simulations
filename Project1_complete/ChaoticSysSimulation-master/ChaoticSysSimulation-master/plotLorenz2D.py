#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D

rho = 28.0
sigma = 10.0
beta = 8.0 / 3.0

def f(state, t):
  x, y, z = state  # unpack the state vector
  return sigma * (y - x), x * (rho - z) - y, x * y - beta * z  # derivatives

state0 = [1.0, 1.0, 1.0]
t = np.arange(0.0, 40.0, 0.01)

states = odeint(f, state0, t)

# fig = plt.figure()
# ax = fig.gca(projection='3d')
# ax.plot(states[:,0], states[:,1], states[:,2])
# plt.show()

# fig, ax = plt.subplots()
# ax.plot(states[:,0], states[:,2])

# ax.set(xlabel='x', ylabel='z',
#        title='')
# ax.grid()

# plt.show()


# fig, ax = plt.subplots()
# ax.plot(t, states[:,0])

# ax.set(xlabel='t', ylabel='x',
#        title='')
# ax.grid()

# plt.show()


# fig, ax = plt.subplots(nrows=3)

# for i, row in enumerate(ax):
#     # for col in row:
#     row.plot(t, states[:,i])
#     row.set(xlabel='t', ylabel=('x','y','z')[i],
#       title='')
#     row.grid()

# plt.show()


t2 = np.arange(0.0, 1000.0, 0.01)
states2 = odeint(f, state0, t2)
statesz2 = states2[:,2]

zmax = []
for i, z in enumerate(statesz2):
    if i == 0 or i == len(statesz2) - 1:
      continue
    if z > statesz2[i-1] and z > statesz2[i+1]:
      zmax.append(z)

fig, ax = plt.subplots()
ax.scatter(zmax[:-1], zmax[1:], s=1)

ax.set(xlabel='Z(n)', ylabel='Z(n+1)',
       title='')
ax.grid()

plt.show()

