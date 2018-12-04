import cv2 
import numpy as np
import matplotlib.pyplot as plt

showImages = True
skipFrames = 1000

vidFps = 30
numContours = 3
height = int(400)
width = int(height * (1536/864))
inc = 0
cap = cv2.VideoCapture('gelvid4.mp4')
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
matLen = int(np.ceil(length/skipFrames))
distMat = np.zeros((matLen, numContours))
time = np.linspace(0, length/vidFps, matLen)
print(len(time))
while(cap.isOpened()):
	frameNum = skipFrames*inc
	if (frameNum >= length):
		break
	print(frameNum/vidFps)
	cap.set(1, frameNum)
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	resized_image = cv2.resize(gray, (width,height)) 
	cropped_image = resized_image[70:350, 237:356]  
	size = cropped_image.shape
	newWidth = size[1] 
	newHeight = size[0]
	spacer = np.ones((newHeight, 2), np.uint8)*255
	ret,thresh1 = cv2.threshold(cropped_image,55,255,cv2.THRESH_BINARY)
	im2, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours = [i for i in contours if cv2.contourArea(i) >= 40]

	contours = sorted(contours, key=lambda x : cv2.moments(x)['m01']/cv2.moments(x)['m00'] )
	contours = contours[-numContours:]
	for i, contour in enumerate(contours):
		M = cv2.moments(contour)
		cy = M['m01']/M['m00']
		distMat[inc, i] = cy
	justContours = np.zeros_like(im2)
	# cv2.line(cropped_image, (0, 10), (200,10), (255, 255, 255))
	if showImages:
		cv2.drawContours(justContours, contours, -1, (255,255,255), 1)
		cv2.imshow('frame',np.hstack((justContours, spacer, thresh1, spacer, cropped_image)))
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	inc += 1


cap.release()
cv2.destroyAllWindows()

# diffPos = 
# for i in range(numContours-1):

cutOff = 6
distMat = distMat[:-cutOff, :]
time = time[:-cutOff]

for i in range(numContours):

	plt.subplot(2, numContours, i + 1)
	plt.plot(time, distMat[:, i])
	plt.xlabel("Time (s)")
	plt.ylabel("Distance (px)")
	diff = np.diff(distMat, axis=0)
	plt.subplot(2, numContours, numContours + i + 1)
	plt.plot(time[:-1], diff[:, i]/skipFrames * vidFps)
	plt.xlabel("Time (s)")
	plt.ylabel("Velocity (px/s)")


plt.show()
