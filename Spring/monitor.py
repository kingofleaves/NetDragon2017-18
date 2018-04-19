import serial
import struct

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

total1 = double(0.0)
total2 = double(0.0)
total3 = double(0.0)
total4 = double(0.0)
try:
	while True:
		response1 = ser1.read(8)
    	response2 = ser2.read(8)
    	response3 = ser3.read(8)
    	response4 = ser4.read(8)
    	# gets 8 bytes (1 double) from each of the 4 serial ports
    	# non-blocking mode, so get a double if one has been sent, otherwise
    	# move on to the next port

		total1 += struct.unpack('d', response1)
		total2 += struct.unpack('d', response2)
		total3 += struct.unpack('d', response3)
		total4 += struct.unpack('d', response4)

		# display the contributions
		

except KeyboardInterrupt:
	ser1.close()
	ser2.close()
	ser3.close()
	ser4.close()
