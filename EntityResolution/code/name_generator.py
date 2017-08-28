#Written by Matthew Wallace for use by CAP
import random
import os
import sys

#Command Line Arguments:

#String form:
total_names_str = str(sys.argv[1])
first_names_str = str(sys.argv[2])
last_names_str = str(sys.argv[3])
seed_value_str = str(sys.argv[4])
delimiter_str = str(sys.argv[5])

#Int form:
total_names = int(total_names_str)
first_names = int(first_names_str)
last_names = int(last_names_str)
seed_value = int(seed_value_str)
#Set the random seed:
random.seed(seed_value)

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


def step1_intermed_file_gen(names_to_add_list,intermed_filename):
    #Write first_names list to an intermediate file:
    with open(intermed_filename,'w+') as file:
        for name in names_to_add_list:
            file.write(name)
            file.write('\n')

            

def randomization_step2(first_name_intermed_file,last_name_intermed_file,delimiter):
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
     
     with open(total_names_str + 'final_name_file.txt', 'w+') as outputfile:
         if first_names >= last_names:
             for i in range(0,total_names):
                 first_name_to_add = first_name_cpy_lines[random.randint(0,larger-1)]
                 last_name_to_add = last_name_cpy_lines[random.randint(0,smaller-1)]
                 
                 first_name_to_add_f = first_name_to_add.replace("\n","")
                 last_name_to_add_f = last_name_to_add.replace("\n","")
                 
                 outputfile.write(last_name_to_add_f +','+ first_name_to_add_f+ delimiter_str )
                 outputfile.write('\n')

         else:
             for i in range(0,total_names):
                 first_name_to_add = first_name_cpy_lines[random.randint(0,smaller-1)]
                 last_name_to_add = last_name_cpy_lines[random.randint(0,larger-1)]

                 
                 first_name_to_add_f = first_name_to_add.replace("\n","")
                 last_name_to_add_f = last_name_to_add.replace("\n","")
                 
                 outputfile.write(last_name_to_add_f +','+ first_name_to_add_f + delimiter_str)
                 outputfile.write('\n')

                  
           
file_copy_creator('all_first_names.txt','first_names_copy.txt')
file_copy_creator('all_last_names.txt','last_names_copy.txt')            
randomization_step1('first_names_copy.txt','last_names_copy.txt','first_name_intermed.txt','last_name_intermed.txt')
randomization_step2('first_name_intermed.txt','last_name_intermed.txt',delimiter_str)
