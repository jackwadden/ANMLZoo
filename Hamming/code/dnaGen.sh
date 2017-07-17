#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Enter the number of random DNA sequence characters you want to be generateda fter typing in the script name."
    echo "Example:" 
    echo "$ ./dnaGen.sh 10 generates 10 random characters to the console."
    echo
    echo "If you wish to output the result to a file, use the > character and append the filename you wish to save the resulting generated text as."
    echo "Example: "
    echo "$ ./dnaGen.sh 10 > output.txt saves the output to a file named output.txt"
else
    TMP=$(cat /dev/urandom | tr -dc 'ATGC' | fold -w ${1} | head -n 1)
    echo $TMP
fi
