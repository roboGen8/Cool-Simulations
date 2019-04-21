#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation, rc
from math import sqrt

rho = 28.0
sigma = 10.0
beta = 8.0 / 3.0

def lorenz_deriv(state, t0, sigma=sigma, beta=beta, rho=rho):
    x, y, z = state
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]


def receiver_deriv(state, t0, sender_xt):
    x, y, z = state
    return [sigma * (y - x), 
            sender_xt(t0) * (rho - z) - y, 
            sender_xt(t0) * y - beta * z]

def messageDemo(N_receiver):
    N = N_receiver + 1
    
    # Choose random starting points
    np.random.seed(1)
    state0 = -15 + 30 * np.random.random((N, 3))
    
    for i, state0i in enumerate(state0):
        if i == 0:
            print("Sender starting point: %s" % (state0i,))
        else:
            print("Receiver %d starting point: %s" % (i, state0i))

    # Solve for the trajectories
    start = 0.0
    end = 20.0
    step = 0.01
    t = np.arange(start, end, step)
    
    sender_states = odeint(lorenz_deriv, state0[0], t)
    # print(sender_states)
    sender_xs = sender_states[:, 0]
    sender_xt = lambda t: sender_xs[int((t - start) / step)]
    
    receiver_states = [odeint(receiver_deriv, state0i, t, (sender_xt,))
            for state0i in state0[1:]]
    # print(receiver_states)

    x_t = np.asarray([sender_states] + receiver_states)

    err_t = [
        [sqrt((r[0]-s[0])**2 + (r[1]-s[1])**2 + (r[2]-s[2])**2) 
            for r, s in zip(sender_states, receiver_states_i)]
        for receiver_states_i in receiver_states    
    ]
  

    # Set up figure & 3D axis for animation
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    ax.axis('off')

    # choose a different color for each trajectory
    colors = plt.cm.jet(np.linspace(0, 1, N))

    # set up lines and points
    lines = sum([ax.plot([], [], [], '-', c=c)
                for c in colors], [])
    pts = sum([ax.plot([], [], [], 'o', c=c)
            for c in colors], [])

    # prepare the axes limits
    ax.set_xlim((-25, 25))
    ax.set_ylim((-35, 35))
    ax.set_zlim((5, 55))

    # set point-of-view: specified by (altitude degrees, azimuth degrees)
    ax.view_init(30, 0)

    # initialization function: plot the background of each frame
    def init():
        for line, pt in zip(lines, pts):
            line.set_data([], [])
            line.set_3d_properties([])

            pt.set_data([], [])
            pt.set_3d_properties([])
        return lines + pts

    # animation function.  This will be called sequentially with the frame number
    def animate(i):
        # we'll step two time-steps per frame.  This leads to nice results.
        i = (2 * i) % x_t.shape[1]

        for line, pt, xi in zip(lines, pts, x_t):
            x, y, z = xi[:i].T
            line.set_data(x, y)
            line.set_3d_properties(z)

            pt.set_data(x[-1:], y[-1:])
            pt.set_3d_properties(z[-1:])

        ax.view_init(30, 0.3 * i)
        fig.canvas.draw()
        return lines + pts

    # instantiate the animator.
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                frames=400, interval=20, blit=True)

    # Save as mp4. This requires mplayer or ffmpeg to be installed
    #anim.save('lorenz_attractor.mp4', fps=15, extra_args=['-vcodec', 'libx264'])
    plt.show()
    
    fig, ax = plt.subplots()
    for i in range(N_receiver):
        ax.plot(t, err_t[i])

    ax.set(xlabel='t', ylabel='error',
           title='')
    ax.grid()

    plt.show()

    # return anim

messageDemo(2)