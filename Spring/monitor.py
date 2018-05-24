'''
GROUPR: Audio monitor
Glenn M. Davis (gmdavis1@gmail.com)
May 2018

Takes input from 4 microphones connected through USB ports and displays
a real-time chart of total contribution.
'''

import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# adjust the filepaths as needed
serA = serial.Serial("/dev/ttyUSB1")
serB = serial.Serial("/dev/ttyUSB3")
serC = serial.Serial("/dev/ttyUSB2")
serD = serial.Serial("/dev/ttyUSB0")

# avoid divide by 0 error
total1 = 0.00001
total2 = 0.00001
total3 = 0.00001
total4 = 0.00001
totals = [total1, total2, total3, total4]

# try updating the total for one mic or pass if nothing available to read
def add_new(ser_total, ser):
    to_add = ser.readline()
    try:
        ser_total += int(to_add)
    except:
        pass
    if ser == serA:
        print("A adding {}".format(to_add))
    if ser == serB:
        print("B adding {}".format(to_add))
    if ser == serC:
        print("C adding {}".format(to_add))
    if ser == serD:
        print("D adding {}".format(to_add))
    return ser_total

# update all 4 mics and print to console a log of what is happening
def refresh_totals(totals):
    print('-' * 20)
    totals[0] = add_new(totals[0], serA)
    totals[1] = add_new(totals[1], serB)
    totals[2] = add_new(totals[2], serC)
    totals[3] = add_new(totals[3], serD)
    all_totals = totals[0] + totals[1] + totals[2] + totals[3]
    percentages = (totals[0] / all_totals * 100, totals[1] / all_totals * 100, totals[2] / all_totals * 100, totals[3] / all_totals * 100)
    return totals, percentages

# animate function for matplotlib
def animate(frameno):
    global totals
    global percentages
    global ind
    global width
    totals, percentages = refresh_totals(totals)
    for index, rect in enumerate(rects):
        rect.set_height(percentages[index])
    print('CURRENT PERCENTAGES')
    print(str(percentages))
    print('-' * 20)
    return rects

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

ani = animation.FuncAnimation(fig, animate, repeat = True, interval = 500)

plt.show()
