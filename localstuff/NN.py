# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 19:57:46 2019

@author: Gen
"""

#dt = 0.01
#T = 8
#t = 0:dt:T
#b = 8/3
#sig = 10
#r= 28

import numpy as np
from scipy import integrate

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict

from sklearn.preprocessing import MultiLabelBinarizer

N_trajectories = 20

ax = plt.axes(projection = '3d')
def lorentz_deriv(xyz, t0, sigma=10., beta=8./3, rho=28.0):
    x, y, z = (xyz)
    """Compute the time-derivative of a Lorentz system."""
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]


# Choose random starting points, uniformly distributed from -15 to 15
np.random.seed(1)
x0 = -15 + 30 * np.random.random((N_trajectories, 3))

# Solve for the trajectories
t = np.linspace(0, 4, 1000)
x_t = np.asarray([integrate.odeint(lorentz_deriv, x0i, t)
                  for x0i in x0])

prev = []
after = []
#print(len(x_t[19]))
for i in range(len(x_t)):
    for j in range(len(x_t[i])):
        data = x_t[i][j]
        if i == 0 and j == 0:
            prev.append(data)
            continue
        if i == len(x_t) - 1 and j == len(x_t[i]) - 1:
            after.append(data)
            continue
        prev.append(data)
        after.append(data)
        
indexList = list(range(0, len(prev)))
trainIndex, testIndex = train_test_split(indexList, test_size = 0.30, random_state=1)
train_prev = []
train_after = []
test_prev = []
test_after = []
for i in trainIndex:
    train_prev.append(prev[i])
    train_after.append(after[i])
    
for i in testIndex:
    test_prev.append(prev[i])
    test_after.append(after[i])
    
#x is after y is prev
training_accuracy = []
validation_accuracy = []
test_accuracy = []
layer_values = range(10)




mlb = MultiLabelBinaarizer()
y_enc = mlb.fit_transform()




#
#
## For the neural network, experiment on different number of hidden layers
#for layer in layer_values:
#
#    # Define the classifier]
#    hiddens = tuple(layer * [32])
#    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=hiddens, random_state=1)
#    clf.fit(train_after, train_prev)
#
#    print 'layer:', layer
#
#    training_accuracy.append(accuracy_score(train_prev, clf.predict(train_after)))
#    test_accuracy.append(accuracy_score(test_prev, clf.predict(test_after)))
#
#
#fig = plt.figure()
#plt.plot(layer_values, training_accuracy, 'r', label="Training Set")
#plt.plot(layer_values, test_accuracy, 'b', label="Testing Set")
#plt.xlabel('Number of Hidden Layers')
#plt.ylabel('Accuracy')
#plt.title('Accuracy vs Number of Hidden Layers for Pulsar Stars')
#plt.legend(loc='best')
#fig.savefig('figures/Pulsar_stars_neural_hidden.png')
#plt.close(fig)
#
## For the neural network, experiment on different number of neurons
#training_accuracy = []
#validation_accuracy = []
#test_accuracy = []
#neurons = range(1,65)
#
#for neuron in neurons:
#    # Define the classifier
#    hiddens = tuple(2 * [neuron])
#    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=hiddens, random_state=1)
#    clf.fit(train_after, train_prev)
#
#    print 'neuron:', neuron
#
#    training_accuracy.append(accuracy_score(train_prev, clf.predict(train_after)))
#    test_accuracy.append(accuracy_score(test_prev, clf.predict(test_after)))
#
#
#fig = plt.figure()
#plt.plot(neurons, training_accuracy, 'r', label="Training Set")
#plt.plot(neurons, test_accuracy, 'b', label="Testing Set")
#plt.xlabel('Number of Neurons')
#plt.ylabel('Accuracy')
#plt.title('Accuracy vs Number of Neurons for Pulsar Stars')
#plt.legend(loc='best')
#fig.savefig('figures/Pulsar stars_neural_neuron.png')
#plt.close(fig)
#
## After finding the right hidden layer value, experiment on training set size
#training_accuracy = []
#test_accuracy = []
#training_size = []
#for k in range(1, 100):
#    training_size.append(k)
