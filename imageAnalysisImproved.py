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

velocityScaling = [1, 1.05, 1.1, 1.15, 1]
bP = [10, 8, 6, 5, 4, 3, 2, 1.5, 1.2, 1, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]


gelTime = 2183 # Time gel is run in seconds

def preprocessImages(cropSettings):
	processedImgs = []

	for imgNum, cropSetting in enumerate(cropSettings, 1):
		img = cv2.imread("gel{}.png".format(imgNum),0)

		size = img.shape
		width = size[1] 
		height = size[0]

		cropMinX = cropSetting[0]
		cropMaxX = cropSetting[1]
		cropMinY = cropSetting[2]
		cropMaxY = cropSetting[3]
		croppedImage = img[int(cropMinY*height):int(cropMaxY*height), int(cropMinX*width):int(cropMaxX*width)]
		transposedImage = np.transpose(croppedImage)
		processedImgs.append(transposedImage)


	return processedImgs

def getPeaks(processedImgs):
	resultPeaks = []
	for imageNum, image in enumerate(processedImgs):
		pltVals = np.mean(image, axis=0)
		peaks, _ = find_peaks(pltVals, prominence=(10, None))
		scaledPeaks = peaks / scaling[imageNum]
		resultPeaks.append(scaledPeaks)
	return resultPeaks

def plotPeakLines(peaks, color=(1,1,1,1)):
	for peak in peaks:
		plt.axvline(peak, color=color, label="Peak Lines")

def velocityScalePeaks(allPeaks, velocityScaling):
	velocityScaledPeaks = []
	for idx, peaks in enumerate(allPeaks):
		velocityScaledPeaks.append(peaks*velocityScaling[idx])
	return velocityScaledPeaks

def lineUpGelsFirstLast(allPeaks):
	linedUpPeaks = []
	for peaks in allPeaks:
		newPeaks = (peaks - peaks[2])
		newPeaks = newPeaks * allPeaks[0][-1]/newPeaks[-1]
		linedUpPeaks.append(newPeaks )
	return linedUpPeaks

def compareDiffs(allPeaks):
	newAllPeaks = []
	for idx, peaks in enumerate(allPeaks):
		if idx != 1:
			newAllPeaks.append(np.delete(peaks, [0, 1, 12]))
		else:
			newAllPeaks.append(np.delete(peaks, [0, 1]))
	
	for peaks in newAllPeaks:
		plt.plot(peaks, bP)
	plt.xlabel("Distance Traveled")
	plt.ylabel("Base Pairs of Band")
	peaksDiff = []
	plt.figure()

	plt.plot(np.mean(newAllPeaks, axis=0), bP)
	print(np.mean(newAllPeaks, axis=0))
	plt.xlabel("Distance Traveled")
	plt.ylabel("Base Pairs of Band")
	plt.figure()
	for idx, peaks in enumerate(newAllPeaks, 1):
		peaksDiff.append(np.diff(peaks))
		plt.plot(peaksDiff[-1])
		plt.xlabel("Band Pair Number")
		plt.ylabel("Peak Difference")

	plt.figure()
	variance = np.var(peaksDiff, axis=0)
	plt.plot(variance)
	plt.xlabel("Band Pair Number")
	plt.ylabel("Variance Between Peak Differences")
	plt.figure()
	allRatios = []
	for peakDiff in peaksDiff:
		ratios = []
		for idx, peak in enumerate(peakDiff[1:], 1):
			ratios.append(peakDiff[idx]/peakDiff[idx-1])
		allRatios.append(np.asarray(ratios))


	plt.plot(np.var(allRatios, axis=0)[1:])
	plt.ylabel("Variance Between Ratios Between Band Pairs Number")
	plt.xlabel("Ratios of Pairs of Differences Between Band Pairs")
	plt.figure()
	for ratio in allRatios:
		plt.plot(ratio[2:])
		plt.xlabel("Ratio Between Band Pairs Number")
		plt.ylabel("Ratios of Differences")
	plt.show()



def main():
	processedImgs = preprocessImages(cropSettings)
	allPeaks = getPeaks(processedImgs)
	# allPeaks = velocityScalePeaks(allPeaks, velocityScaling)
	# allPeaks = lineUpGelsFirstLast(allPeaks)
	compareDiffs(allPeaks)

	for idx, peaks in enumerate(allPeaks, 1):
		ax = plt.subplot(5, 1, idx)
		plotPeakLines(peaks, color=(0,0,1,1))
		ax.set_xlim(0, 4.5)

	plt.show()

if __name__ == '__main__':
	main()