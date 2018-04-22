import serial
import struct
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
import numpy as np
import sys

ser1 = serial.Serial("/dev/ttyACM0")
ser2 = serial.Serial("/dev/ttyACM1")
ser3 = serial.Serial("/dev/ttyACM2")
ser4 = serial.Serial("/dev/ttyACM3")

total1 = 0.0
total2 = 0.0
total3 = 0.0
total4 = 0.0

response1 = 0.0
response2 = 0.0
response3 = 0.0
response4 = 0.0

n_groups = 4

fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.4
error_config = {'ecolor': '0.3'}

try:
    while True:
        try:
            response1 = float(ser1.readline())
            response2 = float(ser2.readline())
            response3 = float(ser3.readline())
            response4 = float(ser4.readline())

        total1 += response1
        total2 += response2
        total3 += response3
        total4 += response4
        # add the double value to each total

        totals = (total1, total2, total3, total4)

        # display the contributions with an updating bar graph

        # rects1 = ax.bar(index, totals, bar_width, alpha = opacity, color = 'b', error_kw = error_config)

        # ax.set_xlabel('Group member')
        # ax.set_ylabel('Total time talking')
        # ax.set_title('Scores by group and gender')
        # ax.set_xticks(index + bar_width / 2)
        # ax.set_xticklabels(('A', 'B', 'C', 'D'))
        # ax.legend()

        # fig.tight_layout()
        # plt.show()

        # ser1.close()
        # ser2.close()
        # ser3.close()
        # ser4.close()
except:
    sys.exit(0)
