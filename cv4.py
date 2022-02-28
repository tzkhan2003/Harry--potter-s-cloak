import cv2 ,time
import numpy as np

time.sleep(5)

vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
adrs = 'http://192.168.0.102:8080/video'
vid.open(adrs)
while(1):
  ret, image1 = vid.read()

  image = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)


  image2 = cv2.bilateralFilter(image, 9, 75, 75)
  image = image2
  maskk = cv2.inRange(image, (11, 100, 100), (26,255 ,255))
  maskkk = cv2.inRange(image, (1 , 232 , 117), (44, 255 ,255))
  maskk2 = cv2.inRange(image, (3 , 217 , 71), (179, 255 ,255))

  mask = maskk + maskkk +maskk2

  h, w = mask.shape[:2]
  mask2 = np.zeros((h+2, w+2), dtype=np.uint8)
  holes = cv2.floodFill(mask.copy(), mask2, (0, 0), 255)[1]
  holes = ~holes
  mask[holes == 255] = 255

  black1 = np.zeros_like(image1, np.uint8)
  
 
  # find the contours from the thresholded image
  contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  # draw all contours
  for contour in contours:
    if cv2.contourArea(contour) > 700 and cv2.contourArea(contour) < 2500000:
        cv2.drawContours(image1, contour, -1, (0, 255, 0), -1)
        cv2.fillPoly(image1, pts =[contour], color=(0,255,0))
        cv2.drawContours(black1, contour, -1, (255, 255, 255), -1)
        cv2.fillPoly(black1, pts =[contour], color=(255,255,255))
        #print(cv2.contourArea(contour))


  black2 = cv2.imread("mid.jpg", cv2.IMREAD_UNCHANGED)
  imask = black1>0
  image1[imask] = black2[imask]








  cv2.imshow('Result',image1)
  cv2.imshow('gray',black1)
  
  if cv2.waitKey(20) & 0xFF == 27:
    break
cv2.destroyAllWindows()
vid.release()
#if esc pressed, finish.