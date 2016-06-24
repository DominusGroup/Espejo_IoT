import cv2
print(cv2.__version__)
vidcap = cv2.VideoCapture('video.avi')
success = True
success,image = vidcap.read()
count = 0
while success:
  #inicio de filtro a verde, edita el frame actual
  image[:,:,2] = 0
  image[:,:,0] = 0
  #guardar frame
  cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
  count += 1
  #leer un frame
  success,image = vidcap.read()
  print 'Read a new frame: ', success
  
