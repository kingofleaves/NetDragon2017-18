from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import ctypes
import _ctypes
import pygame
import sys
import numpy as np
import cv2
import bluetooth
import simplejson as json

if sys.hexversion >= 0x03000000:
    import _thread as thread
else:
    import thread

# colors for drawing different bodies 
SKELETON_COLORS = [pygame.color.THECOLORS["red"],
                    pygame.color.THECOLORS["blue"], 
                    pygame.color.THECOLORS["green"],
                    pygame.color.THECOLORS["orange"], 
                    pygame.color.THECOLORS["purple"], 
                    pygame.color.THECOLORS["yellow"], 
                    pygame.color.THECOLORS["violet"]]

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

class InfraRedRuntime(object):
    def __init__(self):
        pygame.init()

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Loop until the user clicks the close button.
        self._done = False

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Kinect runtime object, we want only color and body frames 
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Infrared)

        # back buffer surface for getting Kinect infrared frames, 8bit grey, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface((self._kinect.infrared_frame_desc.Width, self._kinect.infrared_frame_desc.Height), 0, 24)
        # here we will store skeleton data 
        self._bodies = None
        
        # Set the width and height of the screen [width, height]
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._kinect.infrared_frame_desc.Width, self._kinect.infrared_frame_desc.Height), 
                                                pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)

        pygame.display.set_caption("Kinect for Windows v2 Infrared")

        target_name = "HC-05"
        target_address = None

        while(target_address is None):
            nearby_devices = bluetooth.discover_devices()
            print(nearby_devices)

            for bdaddr in nearby_devices:
                print(bluetooth.lookup_name( bdaddr ))
                if target_name == bluetooth.lookup_name( bdaddr ):
                    target_address = bdaddr
                    break
            
        if target_address is not None:
            print("found target bluetooth device with address ", target_address)
            self.sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

            print("Trying connection")

            i=0 # ---- your port range starts here
            maxPort = 3 # ---- your port range ends here
            err = True
            while err == True and i <= maxPort:
                print("Checking Port ",i)
                port = i
                try:

                    self.sock.connect((target_address, port))
                    err = False
                except Exception:
                    ## print the exception if you like
                    i += 1
            if i > maxPort:
                print("Port detection Failed.")
                return

            # print("Trying sending")
            # self.sock.send("1 2 3")
            # print("Finished sending")
        else:
            print("could not find target bluetooth device nearby")

    def draw_infrared_frame(self, frame, target_surface):
        if frame is None:  # some usb hub do not provide the infrared image. it works with Kinect studio though
            return
        target_surface.lock()
        f8=np.uint8(frame.clip(1,65535)/256.)
        frame8bit=np.dstack((f8,f8,f8))
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame8bit.ctypes.data, frame8bit.size)
        del address
        target_surface.unlock()
    
    def run(self):
        # -------- Main Program Loop -----------
        while not self._done:
            # --- Main event loop
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self._done = True # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE: # window resized
                    self._screen = pygame.display.set_mode(event.dict['size'], 
                                                pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
                    

            # --- Getting frames and drawing  
            if self._kinect.has_new_infrared_frame():
                frame = self._kinect.get_last_infrared_frame()
                self.draw_infrared_frame(frame, self._frame_surface)
                frame = None
                
            # print(self._frame_surface.get_size());
            # self._screen.blit(self._frame_surface, (0,0), (0, 20, 480, 360))

            # Analyze IR frame to extract position data for markers
            frame_array = pygame.surfarray.array2d(self._frame_surface)
            #img = cv2.imdecode(frame_array, 0)

            img = np.uint8(frame_array/256.)
            ret,thresh = cv2.threshold(img,127,255,0)
            image,contours,hierarchy = cv2.findContours(thresh, 1, 2)
            print("new frame:")
            centroids = []
            for cntID in range(len(contours)):
                cnt = contours[cntID]
                if cv2.contourArea(cnt) < 3:   # TODO: Adjust size to match markers
                    continue
                M = cv2.moments(cnt)
                if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    print(cx, cy)
                    centroids.append( (cx, cy) )

            markerColor = (255, 0, 0, 255)
            if len(centroids) == 2:

                if centroids[0] > centroids[1]:
                    front = centroids[0]
                    back = centroids[1]
                else:
                    front = centroids[1]
                    back = centroids[0]
                
                for i in range(0, 10):
                    # flipping cy and cx because of top left convention for Surface
                    self._frame_surface.set_at((front[1] - 10+i, front[0] - i), markerColor)
                    self._frame_surface.set_at((front[1] - 10+i, front[0] + i), markerColor)
                    self._frame_surface.set_at((front[1] + 10-i, front[0] - i), markerColor)
                    self._frame_surface.set_at((front[1] + 10-i, front[0] + i), markerColor)
                # TODO: Send cx, cy to robot
                # print(front)
                # print(back)
                temp = 100
                message = {"Front": [np.int32(front[0]), np.int32(front[1])], "Back": [np.int32(back[0]), np.int32(back[1])], "Target": [temp, temp]}
                jsonMessage = json.dumps(message, cls=MyEncoder)
                self.sock.send(jsonMessage)

            for centroid in centroids:
                for i in range(-10, 10):
                    # flipping cy and cx because of top left convention for Surface
                    self._frame_surface.set_at((centroid[1] + i, centroid[0]), markerColor)
                    self._frame_surface.set_at((centroid[1], centroid[0] + i), markerColor)

                        # for Target                           
                        # self._frame_surface.set_at((cy + i, cx + i), markerColor)
                        # self._frame_surface.set_at((cy - i, cx + i), markerColor)

                
            
            # cv2.imshow('ImageWindow',image)

            # End Analyze

            # send delimiter "-" through bluetooth
            self.sock.send(b"-");
            
            self._screen.blit(self._frame_surface, (0,0))
            pygame.display.update()

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self._clock.tick(60)

        # Close our Kinect sensor, close the window and quit.
        self.sock.close()
        self._kinect.close()
        pygame.quit()


__main__ = "Kinect v2 InfraRed"
game =InfraRedRuntime();
game.run();

