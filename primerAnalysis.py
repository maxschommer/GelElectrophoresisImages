import csv
import matplotlib as plt
import numpy as np
import pprint 

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

print(header.shape)
print(data.shape)
optimizedIndices = []
for i in range(int(data.shape[0]/5)):
	idx = np.argmin(np.abs(data[i:i+5, 6].astype(int) - 68))
	optimizedIndices.append(idx + i * 5)

goodData = np.take(data, optimizedIndices, axis=0)
with open('NEBSelectedPrimers.csv', 'w') as csvfile:
    outputWriter = csv.writer(csvfile, delimiter='	',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    outputWriter.writerows(np.vstack((header, goodData)))
# pp.pprint(goodData)
# print(allAnealTemps)
# np.histogram(np.asarray(allAnealTemps))
# plt.plot()
