import serial
import sys
import time

if len(sys.argv) == 2:
    ser = serial.Serial(sys.argv[1])

    print('1')
    ser.write('1')
    time.sleep(5.0)

    print('2')
    ser.write('2')
    time.sleep(5.0)

    print('3')
    ser.write('3')
    time.sleep(5.0)

    print('4')
    ser.write('4')
    time.sleep(5.0)

    print('5')
    ser.write('5')
    time.sleep(5.0)

    print('6')
    ser.write('6')
    time.sleep(5.0)

    print('0')
    ser.write('0')
    time.sleep(5.0)

else:
    print('FAIL')
