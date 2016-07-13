from lib.device import Camera
from lib.processors_noopenmdao import findFaceGetPulse
from lib.interface import plotXY, imshow, waitKey, destroyWindow
from cv2 import moveWindow
import argparse
import numpy as np
import datetime
from serial import Serial
import socket
import sys



class getPulseApp(object):

    def __init__(self, args):
        # Imaging device - must be a connected camera (not an ip camera or mjpeg stream)
        serial = args.serial
        baud = args.baud
        self.send_serial = False
        self.send_udp = False
        if serial:
            self.send_serial = True
            if not baud:
                baud = 9600
            else:
                baud = int(baud)
            self.serial = Serial(port=serial, baudrate=baud)

        udp = args.udp
        if udp:
            self.send_udp = True
            if ":" not in udp:
                ip = udp
                port = 5005
            else:
                ip, port = udp.split(":")
                port = int(port)
            self.udp = (ip, port)
            self.sock = socket.socket(socket.AF_INET, # Internet
                 socket.SOCK_DGRAM) # UDP

        self.cameras = []
        self.selected_cam = 0
        for i in xrange(3):
            camera = Camera(camera=i)  # first camera by default
            if camera.valid or not len(self.cameras):
                self.cameras.append(camera)
            else:
                break
        self.w, self.h = 0, 0
        self.pressed = 0
        # procesamiento de imagenes, parametros
        self.processor = findFaceGetPulse(bpm_limits=[50, 160],data_spike_limit=2500.,face_detector_smoothness=10.)

        # Init parameters for the cardiac data plot
        self.bpm_plot = False
        self.plot_title = "Data display - raw signal (top) and PSD (bottom)"

        # Maps keystrokes to specified methods
        self.key_controls = {"s": self.toggle_search,"c": self.toggle_cam}

    #cambios de camara
    def toggle_cam(self):
        if len(self.cameras) > 1:
            self.processor.find_faces = True
            self.bpm_plot = False
            destroyWindow(self.plot_title)
            self.selected_cam += 1
            self.selected_cam = self.selected_cam % len(self.cameras)

    #busqueda de frente
    def toggle_search(self):
        state = self.processor.find_faces_toggle()
        print "face detection lock =", not state

    def key_handler(self):
        self.pressed = waitKey(10) & 255  # wait for keypress for 10 ms
        for key in self.key_controls.keys():
            if chr(self.pressed) == key:
                self.key_controls[key]()

    #main del objeto
    def main_loop(self):
        i = 0
        while i<100:
            frame = self.cameras[self.selected_cam].get_frame()
            self.h, self.w, _c = frame.shape

            # set current image frame to the processor's input
            self.processor.frame_in = frame
            # process the image frame to perform all needed analysis
            self.processor.run(self.selected_cam)
            # collect the output frame for display
            output_frame = self.processor.frame_out

            # show the processed/annotated output frame
            imshow("Processed", output_frame)
            
           # create and/or update the raw data display if needed
            if self.send_serial:
                self.serial.write(str(self.processor.bpm) + "\r\n")

            if self.send_udp:
                self.sock.sendto(str(self.processor.bpm), self.udp)

            # handle any key presses
            if i == 15:
                self.toggle_search()
            i = i+1
            self.key_handler()

        for cam in self.cameras:
            cam.cam.release()
        if self.send_serial:
            self.serial.close()
        if self.send_udp:
            self.sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Webcam pulse detector.')
    parser.add_argument('--serial', default=None,help='serial port destination for bpm data')
    parser.add_argument('--baud', default=None,help='Baud rate for serial transmission')
    parser.add_argument('--udp', default=None,help='udp address:port destination for bpm data')

    args = parser.parse_args()
    App = getPulseApp(args)
    App.main_loop()
    print(App.processor.bpm)
    sys.exit()
