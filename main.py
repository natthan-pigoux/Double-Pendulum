#!/usr/bin/python3.6
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import double_pendulum as dp
from time import time
import Interface as interface

class Interface_Plot(Frame):

    def __init__(self, root, pendulum ,**kwargs):

        Frame.__init__(self, root, pendulum, width=1000, height=1000, **kwargs)
        self.pack()
        self.pendulum = pendulum
        label = Label(root,text="Double Pendule")
        label.pack()
        label_2 = Label(root,text="l1 = %.1f m"%self.pendulum.params[0] )
        label_2.pack()
        label_3 = Label(root,text="l2 = %.1f m"%self.pendulum.params[1] )
        label_3.pack()
        label_4 = Label(root,text="m1 = %.1f kg"%self.pendulum.params[2] )
        label_4.pack()
        label_5 = Label(root,text="m2 = %.1f kg"%self.pendulum.params[3] )
        label_5.pack()
        label_6 = Label(root,text="g = %.1f m.s-2"%self.pendulum.params[4] )
        label_6.pack()
        change = Button(root,text='Change parameters')
        change.pack()

    def animate(i):
        self.pendulum.step(dt)
        line.set_data(*self.pendulum.position())
        time_text.set_text('time= %.1f s' %self.pendulum.time_elapsed)
        return line, time_text

    def anim(self):
        global dt,line, time_text

        fig = Figure()
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().grid(column=0,row=6)
        ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-(self.pendulum.params[0]+self.pendulum.params[1]),(self.pendulum.params[0]+self.pendulum.params[1])), ylim=(-(self.pendulum.params[0]+self.pendulum.params[1]),(self.pendulum.params[0]+self.pendulum.params[1])))
        line, = ax.plot([],'o-',lw=2)
        time_text=ax.text(0.02,0.95,'',transform=ax.transAxes)
        dt = 1./30
        ax.grid()
        t0 = time()
        animate(i=0)
        t1 = time()
        interval = 1000 * dt - (t1 - t0)
        ani = animation.FuncAnimation(fig, animate, frames=150, interval=interval, blit=False)



    
fenetre = Tk()

interface_1 = interface.Interface(fenetre)
interface_1.mainloop()

root = Tk()
pendulum = dp.Double_Pendulum(init_state=[120.0,0.0,-20.0,0.0],l1=float(interface_1.values[0]), l2 = float(interface_1.values[1]), m1=float(interface_1.values[2]), m2 = float(interface_1.values[3]), g= float(interface_1.values[4]))
interface_2 = Interface_Plot(root,pendulum)
interface_2.mainloop()


if interface_1.a != 0:
    interface_2.anim(pendulum)