import cv2 
import numpy as np
height = int(400)
width = int(height * (1536/864))
inc = 0
cap = cv2.VideoCapture('gelvid4.mp4')
while(cap.isOpened()):
    cap.set(1, 100*inc)
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(gray, (width,height)) 
    cropped_image = resized_image[100:350, 237:356]  
    size = cropped_image.shape
    newWidth = size[1] 
    newHeight = size[0]
    spacer = np.ones((newHeight, 2), np.uint8)*255
    ret,thresh1 = cv2.threshold(cropped_image,62,255,cv2.THRESH_BINARY)
    im2, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = [i for i in contours if cv2.contourArea(i) >= 40]

    justContours = np.zeros_like(im2)
    cv2.drawContours(justContours, contours, -1, (255,255,255), 1)
    cv2.imshow('frame',np.hstack((justContours, spacer, thresh1, spacer, cropped_image)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    inc += 1
cap.release()
cv2.destroyAllWindows()

