#Written by Matthew Wallace for use by CAP

import random
import string
import sys
import os


class Hamming_Object():
    def __init__(self, name1,name2):
        #Each hamming object will have a list that holds mutated hamming names
        self.hamming_list = [name1,name2]


total_names_str = str(sys.argv[1])
first_names_str = str(sys.argv[2])
last_names_str = str(sys.argv[3])
#input_file_name_str = str(sys.argv[4])
output_file_name_str = str(sys.argv[4])
random_seed = int(sys.argv[5])
hamming_or_caps_str = str(sys.argv[6]) # 0 for hamming, 1 for random caps
delimiter_used_str = str(sys.argv[7])
err_primary_freq = float(sys.argv[8])
err_secondary_freq = float(sys.argv[9])
#Int form:
total_names = int(total_names_str)
first_names = int(first_names_str)
last_names = int(last_names_str)


random.seed(random_seed)



#Error correction for numbers entered that are larger
#than one or more of the source name files:

if first_names > 1891894 and last_names <= 313925:
     print "Please enter a number that is not larger than the first name file size, which is 313925 lines long."
     first_names = int(raw_input('How many first names do you want to use?'))

elif last_names > 313925 and first_names <= 1891894:
     print "Please enter a number that is not larger than the last name file size, which is 1891894."
     last_names = int(raw_input('How many last names do you want to use?'))
     
elif first_names > 1891894 and last_names > 313925:
     print "Please enter a number for the first name file and last name file that is not larger than the respective file it is entered for."
     first_names = int(raw_input('How many first names do you want to use?'))
     last_names = int(raw_input('How many last names do you want to use?'))
else:
     print "Your input is acceptable."

''' 
larger and smaller variable assignment
to control number of name picks in
step 1 for each respective file:    
'''

if first_names >= last_names:
     larger = first_names
     smaller = last_names
    
else:
     larger = last_names
     smaller = first_names
     
'''
This function creates a copy of the all_first_names and all_last_names text
files so that we can pick names randomly without replacement in the
intermediate step of the randomization process without harming the
original source name files
'''
def file_copy_creator(input_filename,output_filename):
     
     with open(input_filename, 'r') as f:
         with open(output_filename, 'w+') as f1:
             for line in f:
                 f1.write(line)



def step1_intermed_file_gen(names_to_add_list,intermed_filename):
    #Write first_names list to an intermediate file:
    with open(intermed_filename,'w+') as file:
        for name in names_to_add_list:
            file.write(name)
            file.write('\n')

          
'''
Step 1 of two-step randomization process;
create intermediate first_name and last_name files
from which to pick from total_names number of times
in step 2 :
'''
def randomization_step1(first_name_inputfile,last_name_inputfile,first_name_intermed_file,last_name_intermed_file):
     
     #Creating readlines list variables in order to access lines from the
     #copy files during the randomization process

     ff_edit_copy = open('first_names_copy.txt','r') # first name file line copy source
     ff_cpy_lines = ff_edit_copy.readlines()


     lf_edit_copy = open('last_names_copy.txt','r') # last name file line copy source
     lf_cpy_lines = lf_edit_copy.readlines()

     first_names_to_add = []
     first_name_lines_picked = []

     last_names_to_add = []
     last_name_lines_picked = []

     #First name block:
     with open(first_name_inputfile,'r') as file:
          if first_names >= last_names:
              for i in range(0,larger):
                  curr_num = random.randint(0,larger)
                  if curr_num not in first_name_lines_picked:
                      first_name_to_add = ff_cpy_lines[curr_num] #grab a random word in file
                    
                      first_name_lines_picked.append(curr_num)
                  else:
                      alt_num = random.randint(0,larger)
                      first_name_to_add = ff_cpy_lines[alt_num] #grab a diff random word
                    
                      first_name_lines_picked.append(alt_num)
                                                   
                  first_name_to_add_f = first_name_to_add.replace('\n','')
                  first_names_to_add.append(first_name_to_add_f)
          else:
              for i in range(0,larger):
                  curr_num = random.randint(0,smaller)
                  if curr_num not in first_name_lines_picked:
                      first_name_to_add = ff_cpy_lines[curr_num]
                      first_name_lines_picked.append(curr_num)
                  else:
                      alt_num = random.randint(0,smaller)
                      first_name_to_add = ff_cpy_lines[alt_num]
                      first_name_lines_picked.append(alt_num)
          
                  first_name_to_add_f = first_name_to_add.replace('\n','')
                  first_names_to_add.append(first_name_to_add_f)

     #Last name block:
     with open(last_name_inputfile,'r') as file1:
          if first_names >= last_names:
              for i in range(0,larger):
                  curr_num = random.randint(0,smaller)
                  if curr_num not in last_name_lines_picked:
                      last_name_to_add = lf_cpy_lines[curr_num]
                      last_name_lines_picked.append(curr_num)
                  else:
                      alt_num = random.randint(0,smaller)
                      last_name_to_add = lf_cpy_lines[alt_num]
                      last_name_lines_picked.append(alt_num)
                      
                  last_name_to_add_f = last_name_to_add.replace('\n','')
                  last_names_to_add.append(last_name_to_add_f)
          else:
              for i in range(0,larger):
                  curr_num = random.randint(0,larger)
                  if curr_num not in last_name_lines_picked:
                      last_name_to_add = lf_cpy_lines[curr_num]
                      last_name_lines_picked.append(curr_num)
                  else:
                      alt_num = random.randint(0,larger)
                      last_name_to_add = lf_cpy_lines[alt_num]
                      last_name_lines_picked.append(alt_num)
                      
                  last_name_to_add_f = last_name_to_add.replace('\n','')
                  last_names_to_add.append(last_name_to_add_f)

     #Create the intermediate files to be drawn from for total_number of times
     #later on:
     step1_intermed_file_gen(first_names_to_add,first_name_intermed_file)
     step1_intermed_file_gen(last_names_to_add,last_name_intermed_file)


#Final step of randomization process - produces the final name file
def randomization_step2(first_name_intermed_file,last_name_intermed_file,delimiter_str):
     first_name_file = open(first_name_intermed_file,'r')
     first_name_cpy_lines = first_name_file.readlines()
     
     last_name_file = open(last_name_intermed_file,'r')
     last_name_cpy_lines = last_name_file.readlines()

     last_name_file.seek(0)
     first_name_file.seek(0)
     
    
     first_name_to_add_list = []
     last_name_to_add_list = []

     first_name_to_add_lines = []
     last_name_to_add_lines = []
     
     with open(total_names_str + 'err_name_file.txt', 'w+') as outputfile:
         if first_names >= last_names:
             for i in range(0,total_names):
                 first_name_to_add = first_name_cpy_lines[random.randint(0,larger-1)]
                 last_name_to_add = last_name_cpy_lines[random.randint(0,smaller-1)]
                 
                 first_name_to_add_f = first_name_to_add.replace("\n","")
                 last_name_to_add_f = last_name_to_add.replace("\n","")
                 
                 outputfile.write(last_name_to_add_f + delimiter_str + first_name_to_add_f)
                 outputfile.write('\n')

         else:
             for i in range(0,total_names):
                 first_name_to_add = first_name_cpy_lines[random.randint(0,smaller-1)]
                 last_name_to_add = last_name_cpy_lines[random.randint(0,larger-1)]

                 
                 first_name_to_add_f = first_name_to_add.replace("\n","")
                 last_name_to_add_f = last_name_to_add.replace("\n","")
                 
                 outputfile.write(last_name_to_add_f + delimiter_str + first_name_to_add_f)
                 outputfile.write('\n')


#File creation block:
file_copy_creator('all_first_names.txt','first_names_copy.txt')
file_copy_creator('all_last_names.txt','last_names_copy.txt')            
randomization_step1('first_names_copy.txt','last_names_copy.txt','first_name_err_intermed.txt','last_name_err_intermed.txt')
randomization_step2('first_name_err_intermed.txt','last_name_err_intermed.txt',delimiter_used_str)


#~~~~~ERROR CREATION BLOCK~~~~~~~~~~~~~~~~~~~~~

#Adds a hamming distance of 1 to a random place in a given name-string
def add_hamming(input_name):
    
    hamming_spot = random.randint(0,len(input_name)-1)
    random_letter = random.choice(string.ascii_lowercase)
    new_str = input_name[0:hamming_spot]+random_letter+input_name[hamming_spot+1:]
    return new_str

#Adds a random number of caps into a given name-string
def add_rand_cap(input_name):
    
    name_list = list(input_name)
    num_caps = random.randint(0,len(input_name)-1)
    for i in range(0,num_caps):
        random_cap_pos = random.randint(0,len(input_name)-1)
        name_list[random_cap_pos] = name_list[random_cap_pos].upper()

    #return name_list.join()
    return "".join(name_list)

def single_hamming(input_letter):
    random_letter = random.choice(string.ascii_lowercase)
    #if random_letter == input_letter:
        #random_letter = random.choice(string.ascii_lowercase)
    return random_letter 

#Reading source file/mutating it into final output file block:

input_file_name = total_names_str + 'err_name_file.txt'
input_file_copy = open(total_names_str + 'err_name_file.txt','r')
input_cpy_lines = input_file_copy.readlines()

if hamming_or_caps_str == '1':
    with open(output_file_name_str,'w+') as outputfile:
        with open(input_file_name,'r') as f:
            for line in f:
                if random.uniform(0,100) <= err_primary_freq:
                    x = line.split(delimiter_used_str)
                    outputfile.write(add_rand_cap(x[0]) + delimiter_used_str + add_rand_cap(x[1]))
else:
   temp_str = ''
   tmp_list = []
   hamming_error_list = []
   count = 0
   with open(output_file_name_str,'w+') as outputfile:
       with open(input_file_name,'r') as f:
           for line in f:
               x = line.split(delimiter_used_str)
               if random.uniform(0.0,100.0) <= err_primary_freq:
                   mutated_names = Hamming_Object(x[0],x[1])
                   for word in x:
                       for letter in word:
                           sec_prob = random.uniform(0.0,100.0)
                           if sec_prob <= err_secondary_freq:
                               temp_str += single_hamming(letter)
                           else:
                               temp_str += letter
                       if len(temp_str) == len(word):
                           str_to_add = temp_str[0:len(word)-1]
                           tmp_list.append(str_to_add)
                           temp_str = ''
        
               else:
                   outputfile.write(x[0] + delimiter_used_str + x[1])
                   
           for j,k in zip(tmp_list[0::2], tmp_list[1::2]):
               outputfile.write(j + delimiter_used_str + k + '\n')
           tmp_list[:] = []
                    
#Shuffle the lines so that the error lines aren't
#all in a row:

file = open(output_file_name_str,'r')
lines = file.readlines()
random.shuffle(lines)
with open(output_file_name_str, 'w+') as final:
    final.writelines(lines)
                       
#The End


