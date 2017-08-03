#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Enter the number of random alphabetical/numeric characters you want to be generated after typing in the script name."
    echo "Example:"
    "$ ./inputGen.sh 8 generates 8 random characters to the console."
    echo
    echo "If you wish to output the result to a file, use the > character and append the filename you wish to save the resulting generated text as."
    echo "Example: "
    echo "$ ./inputGen.sh 8 > output.txt saves the output to a file named output.txt"
else
    TMP=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w ${1} | head -n 1)
    echo $TMP
fi
