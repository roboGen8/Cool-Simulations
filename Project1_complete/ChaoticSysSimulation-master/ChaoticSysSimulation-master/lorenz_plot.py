#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation, rc
from math import sqrt


rc('animation', html='jshtml')

def lorenz_deriv(params, t0, sigma=10., beta=8./3, rho=28.0):
    x, y, z = params
    """Compute the time-derivative of a Lorentz system."""
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]

def lorenzAnimation(N, s0=None):
    # Choose random starting points
    np.random.seed(1)
    if not s0:
        state0 = -15 + 30 * np.random.random((N, 3))
    else:
        state0 = s0
    
    for i, state0i in enumerate(state0):
        print("Starting point %d: %s" % (i, state0i))
        
    print("Animation: ")


    # Solve for the trajectories
    t = np.arange(0.0, 30.0, 0.01)
    x_t = np.asarray([odeint(lorenz_deriv, state0i, t)
                    for state0i in state0])

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
                                frames=600, interval=20, blit=True)
    
    # return anim
    # Save as mp4. This requires mplayer or ffmpeg to be installed
    #anim.save('lorentz_attractor.mp4', fps=15, extra_args=['-vcodec', 'libx264'])
    plt.show()

    # return anim


lorenzAnimation(2, [[2.50, 6.60, 15.00], [2.49, 6.61, 14.99]])

# HTML(anim.to_jshtml())