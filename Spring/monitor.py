import serial
import struct
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
import numpy as np
import sys

ser1 = serial.Serial("/dev/ttyACM+PATH1", 9600, timeout = 0)
# ser2 = serial.Serial("/dev/ttyACM+PATH2", 9600, timeout = 0)
# ser3 = serial.Serial("/dev/ttyACM+PATH3", 9600, timeout = 0)
# ser4 = serial.Serial("/dev/ttyACM+PATH4", 9600, timeout = 0)
# timeout = 0 means non-blocking mode, return immediately up to req
# number of bytes

ser1.open()
# ser2.open()
# ser3.open()
# ser4.open()

# arduinos should fill up a buffer with floats, RPi will get one float at a
# time from each port and process the graph

total1 = 0.0
total2 = 0.0
total3 = 0.0
total4 = 0.0

n_groups = 4

fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.4
error_config = {'ecolor': '0.3'}

try:
    while True:
        response1 = ser1.readline()
        # response2 = ser2.readline()
        # response3 = ser3.readline()
        # response4 = ser4.readline()
        # gets 8 bytes (1 double) from each of the 4 serial ports
        # non-blocking mode, so get a double if one has been sent, otherwise
        # move on to the next port

        total1 += struct.unpack('d', response1)
        # total2 += struct.unpack('d', response2)
        # total3 += struct.unpack('d', response3)
        # total4 += struct.unpack('d', response4)
        # add the double value to each total
        print total1

        totals = (total1, total2, total3, total4)

        # display the contributions
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