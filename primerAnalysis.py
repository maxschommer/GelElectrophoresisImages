import csv
import matplotlib as plt
import numpy as np
import pprint 
import scipy.stats as sci



pp = pprint.PrettyPrinter(indent=4)
with open('NEBOutput.csv', 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	
	data = []
	header = []
	for idx, row in enumerate(reader):
		if idx != 0:
			data.append(row)
		else:
			header = row
		# print(index)
		# allAnealTemps.append(row['Anneal temp'])
		# print(row['Tm 1'])
	data = np.asarray(data)
	header = np.asarray(header)

# print(data)
# print(header.shape)
# print(data.shape)
mode = sci.mode(np.asarray(data[:, 6]).astype(int))[0][0]
# print(mode)
lefts = data[:, 1]
rights = data[:, 4]
landr = np.transpose(np.vstack((lefts, rights)))

# pp.pprint(np.transpose(np.vstack((lefts, rights))).shape)

def findDuplicate(data, withSubsetRemoved, i):
	for j in range(5*i, 5*i+5):
		# print(withSubsetRemoved[:, 0])
		if (data[j, 1] in withSubsetRemoved[:,0]) or (data[j, 1] in withSubsetRemoved[:,1]) or (data[j, 4] in withSubsetRemoved[:,0]) or (data[j, 4] in withSubsetRemoved[:,1]):			
			return j
	return None

optimizedIndices = []
for i in range(int(data.shape[0]/5)):
# print(np.array(range(5*i, 5*i+5)))
	withSubsetRemoved = np.delete(landr, np.array(range(5*i, 5*i+5)), axis=0)
	# print(withSubsetRemoved)
	duplicate = findDuplicate(data, withSubsetRemoved, i)
	if duplicate is not None:
		# print(duplicate)
		optimizedIndices.append(duplicate)
	else:
		idx = np.argmin(np.abs(data[5*i:5*i+5, 6].astype(int) - mode))
		optimizedIndices.append(idx + i * 5)

goodData = np.take(data, optimizedIndices, axis=0)

IDTInput = []
for entry in goodData:
	IDTInput.append([entry[0], entry[1], '25nm', 'STD'])
	IDTInput.append([entry[3], entry[4], '25nm', 'STD'])

# print(np.asarray(IDTInput)[:,1])
u, indices = np.unique(np.asarray(IDTInput)[:,1], return_index=True)
IDTInput = np.take(IDTInput, indices, axis=0)

with open('NEBSelectedPrimers.csv', 'w') as csvfile:
    outputWriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    outputWriter.writerows(np.vstack((header, goodData)))

with open('IDTSelectedPrimers.csv', 'w') as csvfile:
    outputWriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    outputWriter.writerows(IDTInput)

# pp.pprint(goodData)
# print(allAnealTemps)
# np.histogram(np.asarray(allAnealTemps))
# plt.plot()
