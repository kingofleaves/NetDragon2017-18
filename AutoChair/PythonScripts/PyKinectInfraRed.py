from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import ctypes
import _ctypes
import pygame
import sys
import numpy as np
import cv2


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
            for cntID in range(len(contours)):
                cnt = contours[cntID]
                if cv2.contourArea(cnt) < 3:   # TODO: Adjust size to match markers
                    continue
                markerColor = (255, 0, 0, 255)
                M = cv2.moments(cnt)
                if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    print(cx, cy)
                    
                    for i in range(-10, 10):
                        # flipping cy and cx because of top left convention for Surface
                        if cv2.contourArea(cnt) < 7.5:
                            self._frame_surface.set_at((cy + i, cx), markerColor)
                            self._frame_surface.set_at((cy, cx + i), markerColor)
                        else:
                            self._frame_surface.set_at((cy + i, cx + i), markerColor)
                            self._frame_surface.set_at((cy - i, cx + i), markerColor)

                        # TODO: Send cx, cy to robot
                

            # cv2.imshow('ImageWindow',image)

            # End Analyze
            
            self._screen.blit(self._frame_surface, (0,0))
            pygame.display.update()

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self._clock.tick(60)

        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        pygame.quit()


__main__ = "Kinect v2 InfraRed"
game =InfraRedRuntime();
game.run();

