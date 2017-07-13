#Written by Matthew Wallace for use by CAP

import glob
import sys
import csv
import os

#fileName = str(sys.argv[1])
#read_files = glob.glob('dir.txt')


with open("all_output_names.txt","wb") as outputfile:
    for filename in os.listdir("last_names"):
            with open('/home/Documents/ANMLZoo/EntityResolution/code/last_names/'+filename, "rb") as infile:
                outputfile.write(infile.read())
