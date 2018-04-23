import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

# ser1 = serial.Serial("/dev/ttyACM0")
# ser2 = serial.Serial("/dev/ttyACM1")
# ser3 = serial.Serial("/dev/ttyACM2")
# ser4 = serial.Serial("/dev/ttyACM3")

total1 = 0.0
total2 = 0.0
total3 = 0.0
total4 = 0.0
totals = [total1, total2, total3, total4]

def refresh_totals(totals):
    # add the float from Arduino for each totals[], now just simulated data
    totals[0] += random.random() * 4
    totals[1] += random.random() * 0.5
    totals[2] += random.random() * 2
    totals[3] += random.random()
    all_totals = totals[0] + totals[1] + totals[2] + totals[3]
    percentages = (totals[0] / all_totals * 100, totals[1] / all_totals * 100, totals[2] / all_totals * 100, totals[3] / all_totals * 100)
    return totals, percentages

def animate(frameno):
    global totals
    global percentages
    global ind
    global width
    totals, percentages = refresh_totals(totals)
    for index, rect in enumerate(rects):
        rect.set_height(percentages[index])
    return plt.bar(ind, percentages, width, color='r',)

N = 4
ind = np.arange(N)
width = 0.35

totals, percentages = refresh_totals(totals)

fig, ax = plt.subplots()

ax.set_ylabel('Percentage of time talking')
ax.set_ylim(0, 100)
ax.set_xticks(ind)
ax.set_xticklabels(('A', 'B', 'C', 'D',))

rects = plt.bar(ind, percentages, width, color='r',)

ani = animation.FuncAnimation(fig, animate, blit = True, repeat = True)

plt.show()