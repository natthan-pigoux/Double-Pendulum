import numpy as np
from time import time 
import scipy.integrate as integrate
from math import * 

class Double_Pendulum:

    def __init__(self, init_state=[120,1,-20,0], l1=1, l2 = 1, m1=1, m2 = 1, g= 10, origin=(0,0)):

        self.init_state = np.asarray(init_state, dtype='float')
        self.params = (l1,l2,m1,m2,g)
        self.origin = origin
        self.time_elapsed = 0

        self.state = self.init_state*np.pi/180

    def position(self):

        (l1,l2,m1,m2,g) = self.params

        x = np.cumsum([self.origin[0], l1*sin(self.state[0]), l2*sin(self.state[2])])

        y = np.cumsum([self.origin[1], -l1*cos(self.state[0]), -l2*cos(self.state[2])])


        return x,y

    def energy(self):

        (l1,l2,m1,m2,g) = self.params

        x = np.cumsum( [l1*sin(self.state[0]), l2*sin(self.state[2]) ])

        y = np.cumsum([-l1*cos(self.state[0]), -l2*cos(self.state[2])])

        vx = np.cumsum([l1*self.state[1]*cos(self.state[0]), l2*self.state[3]*cos(self.state[2])])

        vy = np.cumsum([l1*self.state[1]*sin(self.state[0]), l2*self.state[3]*sin(self.state[2])])

        V = g * (m1*y[0] + m2*y[1])

        T = 0.5*(m1*np.dot(vx,vx) + m2*np.dot(vy,vy))

        E = T + K

        return E


    def accel(self,state,t):

        (l1,l2,m1,m2,g) = self.params

        acc= np.zeros_like(state)

        acc[0] = state[1]
        acc[2] = state[3]

        cos12 = cos(state[2]- state[0])
        sin12 = sin(state[2]- state[0])

        den1 = (m1 + m2)*l1 - m2*l1*cos12*cos12

        acc[1] = (m2 * l1 * state[1]*state[1]*sin12*cos12 + m2 * g * sin(state[2]) * cos12  + m2*l2*state[3]*state[3]*sin12 - (m1 + m2)*g*sin(state[0]))/den1

        den2 = (l2/l1)*den1

        acc[3] = (-m2*l2*state[3]*state[3]*sin12*cos12 + (m1 + m2)*g*sin(state[0])*cos12 - (m1 + m2)*l1*state[1]*state[1]*sin12 - (m1 + m2)*g*sin(state[2]))/den2

        return acc



    def step(self,dt):

        self.state = integrate.odeint(self.accel, self.state, [0,dt])[1]
        self.time_elapsed += dt