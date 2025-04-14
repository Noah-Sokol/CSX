'''
Runs simulation using instance of ball class and plots/animates through matplotlib
Author: Noah Sokol
date: 2/14/24
'''
from ballClass import Ball
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

color = "green"
t = [0]
a = 0
v_i = 3
i_pos = 0
dt = .02
k = 5
m = 2
my_ball = Ball(color, i_pos, v_i, a, m)
trail = False

def animate(i):
    plt.cla()
    #calles function to update ball movement and position
    my_ball.move(dt, k, i)
    #adds time to list of times in order to calculate axies 
    t.append(dt * i)
    
    #plots new data
    if trail is True:
        ax.plot(t, my_ball.y, 'o', markersize=8, color = my_ball.color)
        #updates axies
        plt.axis([t[-1] - 5, t[-1] + 5, -3, 3])
    else:
        # Plot the vertical line using plt.vlines
        plt.vlines(x=0, ymin = my_ball.y[-1], ymax=3, color='grey', linestyles=":")

        ax.plot(0, my_ball.y[-1], 'o', markersize=8, color = my_ball.color)
        #updates axies
        plt.axis([-5, 5, -3, 3])






fig, ax = plt.subplots()
ax.plot([], [], 'o', markersize=8, color = my_ball.color)
x_data, y_data = [], []
ani = FuncAnimation(fig, animate, interval=50)

plt.show()






# sets up the animation object
# plt.gcf() uses the current figure
# animate is the function that updates the data and graph
# interval is the time in milliseconds between frames


