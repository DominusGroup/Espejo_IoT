from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# Inicializando la camara

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size = (640, 480))

# Calentar la camara
time.sleep(0.1)

# Captura de los frames

for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port =  True) :
    # Obtiene el arreglo numerico NumPy
    image = frame.array

    # Mostrando el frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    # Limpia para pasar al siguiente frame
    rawCapture.truncate(0)

    # Termina el lazo con la llave 'q'
    if key == ord("q") :
        break
    
