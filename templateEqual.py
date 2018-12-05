#Steps for use:
#(1)Export Benchling file as FASTA and put it in folder containing this code.
#(2)Find reference plasmid on Addgene and Export it into the same folder as FASTA file.
#(4)Assign 'plasmidName' in templateEqual.py to a string of the plasmid name used on Benchling.
#(5)Replace file names accordingly as 'addgenePlasmid' and 'benchlingPlasmid' in templateEqual.py.
#(6)Run code!
plasmidName = "pPSU1"
with open('addgenereferenceppsu1.fa', 'r') as addgenePlasmid:
    data1 = addgenePlasmid.read().splitlines(True)
addgeneOutput = ''
for lineNumber in range(1, len(data1)):
    data1[lineNumber].replace('\n', '')
    for base in data1[lineNumber]:
        addgeneOutput += base
with open('benchlingppsu1.fasta', 'r') as benchlingPlasmid:
    data2=benchlingPlasmid.read().replace('>' + plasmidName, '')
addgeneOutput = addgeneOutput.upper()
consensusSeq = ''
impurities = 0
addgeneOutput = "".join(addgeneOutput.split()) 
data2 = "".join(data2.split())
if len(addgeneOutput) == len(data2):
    for baseindex in range(0, len(data2)):
        if addgeneOutput[baseindex] == data2[baseindex]:
            consensusSeq+=addgeneOutput[baseindex]
        else:
            consensusSeq += '***'+addgeneOutput[baseindex].lower()+'***'
            impurities+=1
    if impurities > 0:
        print("Benchling sequence differs from reference sequence at lower case base pairs surrounded by asterisks to make it easier to identify in the reference sequence below:")
        print(consensusSeq)
    else:
        print("Benchling sequence matches reference sequence.")
else:
    print("Sequences are of different lengths listed below and thus unequal. We cannot perform the operation.")
    print("benchling:")
    print(len(data2))
    print("addgene:")
    print(len(addgeneOutput))
    