#Created by Matthew Wallace for use by CAP


for file in /home/Documents/ANMLZoo/EntityResolution/last_names/*

do
    python csvExtractor.py "$file"
done
