import matplotlib.pyplot as plt
import numpy as np
import cv2 
verticalPixels=40
horizontalPixels=30

#Note to see how the image looks when horizontalpixels number is altered
data = np.genfromtxt('averaged1kbplus.csv', delimiter=',', skip_header=1, names=['distance','seqlen'])

plt.plot(data["distance"], data["seqlen"])
plt.xlabel("Distance")
plt.ylabel("Sequence Length")
x = data["distance"]
y = data["seqlen"]
#xvals = np.linspace(data["distance"][0], data["distance"][-1], verticalPixels)
xvals = np.linspace(data["distance"][0], data["distance"][-1], verticalPixels)
yinterp = np.interp(xvals, x, y)
plt.plot(x, y, 'o')
plt.plot(xvals, yinterp, '-x')
print(yinterp)

img = cv2.imread('ecoli.png',0)
ret,thresh1 = cv2.threshold(img,200,255,cv2.THRESH_BINARY)
resized_image = cv2.resize(thresh1, (horizontalPixels,verticalPixels)) 

# cv2.imshow('ecoli',resized_image)

# k = cv2.waitKey(0)
# if k == 27:         # wait for ESC key to exit
#     cv2.destroyAllWindows()
# indicesofpixels = np.where(resized_image == 0)[0]
# print(indicesofpixels)
indicesofpixels = []
finalist = []
for row in resized_image:
    for pixel in row:
        index = 0
        if pixel == 0:
            indicesofpixels.append(index)
        index+=1 
        if index == len(row):
            finalist.append(indicesofpixels)
            indicesofpixels = []
print(finalist)
plt.show()