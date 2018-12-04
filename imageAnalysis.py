import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
import cv2


cropSettings = [[.35, .40, .17, .88],
				[.32, .38, .23, .84],
				[.39, .48, .05, .93],
				[.49, .56, .25, .86],
				[.45, .52, .24, .92]]


scaling = [283, 240, 364, 256, 267] # Pixels per cm

gelTime = 2183 # Time gel is run in seconds

def cropImages(cropSettings):
	croppedImgs = []

	for imgNum, cropSetting in enumerate(cropSettings, 1):
		img = cv2.imread("gel{}.png".format(imgNum),0)

		size = img.shape
		width = size[1] 
		height = size[0]

		cropMinX = cropSetting[0]
		cropMaxX = cropSetting[1]
		cropMinY = cropSetting[2]
		cropMaxY = cropSetting[3]

		croppedImgs.append(img[int(cropMinY*height):int(cropMaxY*height), int(cropMinX*width):int(cropMaxX*width)])

	return croppedImgs


	# cv2.imshow('image',img)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

def getPeaks(img, scaling, ax):
	height = img.shape[0]
	pltVals = np.mean(img, axis=1)

	peaks, _ = find_peaks(pltVals, prominence=(10, None))

	dist = np.linspace(0, height/scaling, height)
	ax.set_xlim(0, height/scaling)
	ax.plot(dist, pltVals)
	ax.plot(peaks/scaling, pltVals[peaks], "x", label="Peaks")
	ax.plot(np.zeros_like(pltVals), "--", color="gray")
	plt.xlabel("Distance (cm)")
	plt.ylabel("Brightness")
	plt.legend()

	return peaks

def squaredError(distGroup1, distGroup2):
	accumulator = 0
	for dist in distGroup1:
		matchedDist = distGroup2[np.argmin(np.abs(distGroup2 - dist))]
		error = dist - matchedDist
		accumulator += error ** 2 

	return accumulator

def sweepVelShift(distGroup1, distGroup2, sweepRange):
	errors = []
	for velShift in sweepRange:
		shiftedOther = distGroup2 * velShift
		errors.append(squaredError(distGroup1, shiftedOther))

	idx = np.argmin(errors)
	res = sweepRange[idx]
	return res, errors

def plotPeakLines(peaks, scaling, color=(1,1,1,1)):
	for peak in peaks:
		plt.axvline(peak/scaling, color=color, label="Peak Lines")

def scalePeaks(peaks, scaleVal):
	scaledPeaks = []
	for peak in peaks: 
		scaledPeaks.append( peak * scaleVal)
	return scaledPeaks

def main():
	croppedImgs = cropImages(cropSettings)

	velGroup = []
	distGroup = []
	for idx, img in enumerate(croppedImgs):
		
		height = img.shape[0]

		ax = plt.subplot(2, 1, 1)
		peaks = getPeaks(img, scaling[idx], ax)
		# plt.show()
		img = np.transpose(img)

		# Draw lines on image for peaks
		ax2 = plt.subplot(2, 1, 2)
		plotPeakLines(peaks, scaling[idx])
			# cv2.line(img, (0, peak), (img.shape[1], peak), (255,255,255), 2)

		vels = []
		dists = []
		for peak in peaks:
			vels.append((peak/scaling[idx])/gelTime)
			dists.append(peak/scaling[idx])
		velGroup.append(np.asarray(vels))
		distGroup.append(np.asarray(dists))
		
		plt.xlabel("Distance (cm)")
		plt.ylabel("Unitless")
		plt.legend(["Peak Lines"])
		ax2.imshow(img, extent=(0,height/scaling[idx], 0, 1))
		ax2.set_xlim(0, height/scaling[idx])

		plt.show()

	sweepRange = np.linspace(.8,1.2, 100)

	plt.clf()
	for idx, group in enumerate(distGroup, 1):
		if idx == 1:
			ax = plt.subplot(5,1, 1)
			plotPeakLines(group, 1, color=(1,0,0,1))
			# ax.imshow(np.transpose(croppedImgs[idx - 1]), extent=(0,height/scaling[idx-1], 0, 1))

		else:
			ax = plt.subplot(5, 1, idx)
			shift, error = sweepVelShift(distGroup[0], group, sweepRange)
			scaledPeaks = scalePeaks(group, shift)
			plotPeakLines(scaledPeaks, 1, color=(1,0,0,1))
		plt.xlabel("Distance (cm)")
		plt.ylabel("Gel %i" %(idx))
		ax.set_xlim(0, 4)
	plt.show()


	distGroup = np.asarray(distGroup)
	shift, firstPlot = sweepVelShift(distGroup[0], distGroup[1], sweepRange)
	# plt.figure()

	plt.clf()
	plt.plot(sweepRange, firstPlot)
	plt.show()



if __name__ == '__main__':
	main()

