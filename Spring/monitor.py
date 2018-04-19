import serial

ser1 = serial.Serial("/dev/ttyACM+PATH1", 9600, timeout = 0)
ser2 = serial.Serial("/dev/ttyACM+PATH2", 9600, timeout = 0)
ser3 = serial.Serial("/dev/ttyACM+PATH3", 9600, timeout = 0)
ser4 = serial.Serial("/dev/ttyACM+PATH4", 9600, timeout = 0)
# timeout = 0 means non-blocking mode, return immediately up to req
# number of bytes
ser1.open()
ser2.open()
ser3.open()
ser4.open()

# arduinos should fill up a buffer with floats, RPi will get one float at a
# time from each port and process the graph

total1 = 0.0
total2 = 0.0
total3 = 0.0
total4 = 0.0
try:
	while True:
		response1 = ser1.read(8)
    	response2 = ser2.read(8)
    	response3 = ser3.read(8)
    	response4 = ser4.read(8)
    	# gets 8 bytes (1 double) from each of the 4 serial ports
    	# non-blocking mode, so get a float if one has been sent, otherwise
    	# move on to the next port

		total1 += float(response1)
		total2 += float(response2)
		total3 += float(response3)
		total4 += float(response4)

		# display the contributions
		

except KeyboardInterrupt:
	ser1.close()
	ser2.close()
	ser3.close()
	ser4.close()
