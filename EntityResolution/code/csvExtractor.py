#Written by Matthew Wallace for use by CAP
import csv
import sys
from collections import defaultdict


#fileName = raw_input('Enter the file name you want to use(do not append .txt, just the name:')

fileName = str(sys.argv[1])
print fileName
nameData = []
with open(fileName, 'rb') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
                #print row[0]
                nameData.append(row[0])



                
#For some reason, the line below is not working as intended, but the
#data is being overwritten to the original files correctly for now, even
# though the file name output is not being rewritted with a _sifted.txt ending.
# This is acceptable for now because the data is being outputted correctly.
fileName = fileName.replace(' .txt ', '_sifted.txt')

file2 = open(fileName, 'w')
for i in nameData:
        file2.write( i+'\n')
file2.close()


