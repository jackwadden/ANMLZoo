
# **Automata Generator Scripts**

#### **name_generator.py**
name_generator asks for five initial values: the number of total names, the number of first names, the number of last names, a random seed from which to generate first and last name combinations, and a name delimiter symbol. Note that the order each parameter is mentioned in the prior sentence is the order that each parameter should be entered in the command line.

name_generator.py outputs a text file of arbitrary size. A name file delimited by ~ characters would look like the following:

```
LastName1, FirstName1~
LastName2, FirstName2~
LastName3, FirstName3~
etc. …
```

This script allows for different sizes of random first and last names to be generated and picked from for ‘total_names’ number of times each. The resulting output file can be used in automata generation (via nametoanml.py, which is built into the script).

#### **Name Randomization Process**
The randomization for name_generator.py takes place through two steps. In step one, a number of first names is drawn from the first names source file for <first_names> times, and a number of last names is drawn from the last names source file for <last_names> times. All names drawn are selected randomly, based on the random seed provided in the command line argument. Two intermediate files are then created, one for the first names drawn, and one for the last names drawn, respectively. After this, step one is concluded. In step two, <total_names> names are selected from the intermediate first name and last name file, randomly. Note that the script is compatible with differently sized first_name and last_name parameters as step two uses a random range that depends on the number of names in a given file to select the final names.

#### **Example Usage**
```
$ python name_generator.py <total_names> <num_first_names> <num_last_names> <random_ seed> <delimiter>
```

To generate a file for nametoanml.py, use ‘$’ as the delimiter symbol.
```
$ python name_generator.py 1000 200 10000 7 $
```

### **name_to_anml.py**
nametoanml.py converts input name files delimited by $’s to automata widgets described above. To generate an ANML file simply run nametoanml.py with the properly formatted name file as input.

```
$ python nametoanml.py <input name file>
```

name_generator.py allows you to create random automata files of the proper format (delimited by $ characters) that can then be used to generate automata ANML files using nametoanml.py. Please see the input generator section below for exact instructions on how to generate a random input name file.


---

# **Input Generator**

### **random_error_gen.py**

#### **Command Line Arguments**
Random_error_gen.py takes 9 command line arguments: <total_names_num>, <first_names_num>, <last_names_num>, <output_file_name>, <random_seed>, <hamming_or_random_caps>, <delimiter>, <line_error_frequency>, <letter_error_frequency>, in the order described.

#### **Description**
This script generates name files, and then uses those name files to output new files, which contain errors. Currently, two error types are supported: capitalization errors and hamming distance errors. The <line_error_frequency> parameter is used to determine what percentage of the script’s output file should have errors. If a ‘1’ is entered for the <hamming_or_random_caps> parameter, then random capitalization errors will be applied to <line_error_frequency> % of the final output file. A number of capitalization errors is generated randomly every time the line error percentage is triggered. If a ‘0’ is entered for the <hamming_or_random_caps> parameter, then hamming distance errors will be applied to <line_error_frequency>% of the final output file. Furthermore, the number of hamming distance errors present in a given name after the script has concluded is dependent on the <letter_error_frequency> parameter. The greater this parameter is, the more likely a name within an error line will have a greater number of hamming distance errors. The <delimiter> parameter is used to separate each first and last name pair within the final output error file. The <output_file_name> parameter will be the name of the final output file. The <random_seed> is included for repeatability of trials and is used as the seed of the random generator at the beginning of the script. <total_names_num>, <first_names_num>, and <last_names_num> are used to generate the intermediate name file, from which errors are generated. If you are unsure how this process occurs, consult the name_generator.py description for a more in-depth explanation. 
*Note: all percentage parameters are floating-point, so feel free to use non-integer percentages.

#### **Example Usage**
```
$ python random_error_gen.py 1000 100 100 50errors.txt 11 0 $ 5 50.0
```

#### **Example Explanation**
This line will create an output with 1000 names, from an intermediate source of 100 randomly first and last names. The line error percent rate is 5 percent here, so roughly 50 lines will contain errors of some kind. In this specific command, hamming distance errors will appear in the final file, and there will be a 50 percent chance that each letter in each word inside a given error line will be different than the original letter (have a hamming distance of 1). Note that the output file will be 50errors.txt and that the file will have $'s as delimiters between each first and last name pair.

#### **Example Format**
```
LastNameError1, FirstNameError1$
LastNameError2, FirstNameError2$
LastNameError3, FirstNameError3$
etc. …
```

---

# **Data Sources**


[Last Names] (https://www.census.gov/topics/population/genealogy.html)

#### Census Bureau License Declaration
This project uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau.


[First Names] (https://www.ssa.gov/oact/babynames/limits.html)

#### Social Security Administration License Declaration
This project uses data published under a Creative Commons License by the Social Security Administration but is not endorsed or certified by the Social Security Administration.

---

## **Backup**

### **fileCombiner.py**

#### **Description**
This script is made to combine every text file in a given directory into one output file. Note that the output name is currently hard coded, along with the directory path. Going forward, one or both of these can be changed by asking for input, and then running the script with the user input. This script was used twice, once to generate the first names input generator source file, and once to generate the last names input generator source file.

#### **Usage**
To use the script, enter the following, after modifying the directory path and output filename inside the script to your liking:
```
$ python fileCombiner.py
```
**Note:** Once you have entered this command, the script will have combined every text file in the target directory into one file. The current output filename is set to “all_output_names.txt” .


### **csvExtractor.py**

#### **Description**
This script is made to extract data from a given csv file. For the data we used in this project, it was only necessary to target the data from one column of the source csv file, but this can be changed by adding another variable, to which you can append more data from a given csv file, if you find it necessary. To run this file automatically over a whole directory's contents, use the dataIterator.sh script included in the code directory. Change the filepath in dataIterator.sh to fit your machine's filepath as necessary. 

#### **Usage**
To use the script, enter the following command into terminal:
```
$ python csvExtractor.py <fileName.txt>
```
where <fileName.txt> is the desired file you wish to extract your data from.

**Note:** as the script is currently written, the file you enter as an argument will be rewritten with only the data you select in the script, so if you wish to preserve the original data, make a copy or change the source code of the script itself.


### **fileCombiner.py**

#### **Description**
This script is made to combine multiple text files into a singular text file. In our case, it was used to create the all_first_names.txt and all_last_names.txt source files. 

#### **Usage**
To use the script, enter the following into terminal:
```
$ python fileCombiner.py
```
**Note:** the filepath will need to be edited to specifically fit the directory path one is 
working with in order for the script to have its intended effect. Therefore, edit the path 
to fit the directory path before running the script. 
