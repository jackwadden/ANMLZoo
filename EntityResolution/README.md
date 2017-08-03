# **Entity Resolution**

## **Description**

Entity Resolution (ER) is the process of finding identical entities across different da\
tabases. Given the recent explosion of data, there are many different pieces of data ac\
ross multiple sources which actually point to the same entity. For example, a sample us\
er account on a given social media application likely requires roughly the same informa\
tion that is needed to create an account on another social network, but, in all likelih\
ood, that information may be stored differently in each application. Oftentimes, the sa\
me user can appear differently across different databases for multiple reasons. The use\
r might misspell their data or they might decide to enter an alternate shortening of th\
eir data. In either case, the same person will appear, to most programs, as two separat\
e entities. This problem, which is the most common matching bottleneck in Entity Resolu\
tion, is known as approximate matching.

The automata model to be a useful and efficient way to recognize and resolve instances \
of Entity Resolution problems. In this model, each automata uses fuzzy-matching techniq\
ues in order to recognize misspellings or alternate spellings of some piece of data. Ad\
ditionally, these automata can be set to recognize arbitrary Hamming distance differenc\
es, which allows further customization when it comes to resolving approximate matches.

### **Helpful and Instructive Images**

  
   ![](images/er_image1.png?raw=true)

-The above image demonstrates the general type of setup each automaton has in the Entit\
y Resolution solver. Note that the automaton in this image does not implement fuzzy mat\
ching, which is used to solve Entity Resolution instances efficiently. Instead, it is a\
 direct-recognition automaton, which recognizes the name Adam Smith. In this automaton,\
 the $ and # are meant to deal with unnecessary spaces in the input, the + signs are in\
cluded for architecture-specific reasons and are not vital to the overall name-recognit\
ion process. Also, the “,” sign is a reporting state.

  
   ![](images/er_image2.png?raw=true)

-This image provides an instructive example of a Hamming distance automaton. Note that \
this automaton has the ability to recognize pieces of data with a Hamming distance of 0\
 or 1. In our implementation, the Hamming distance recognition properties of each autom\
aton can be arbitrarily edited in order to recognize different Hamming distances.

---

## **Automata**
The ER standard automata was constructed by running the nametoanml.py script on the 100\
0.names input file. This script takes each name and converts it to a widget described a\
bove to recognize all other entries in a database within Hamming distance 1.

## **Inputs**
Input streams to ER automata consist of full names separated by ‘$’ delimiters. Each in\
dividual name is an independent problem and so no dependencies exist across ‘$’ boundar\
ies.

### **Standard Inputs**
The 1MB and 10MB input files were constructed using the 1000.names input file. Each nam\
e entry is concatenated together and delimited with a ‘$’ until the desired file size i\
s created. The 1000.names input file was originally derived from the SNAC organization \
database
[Source Link](http://socialarchive.iath.virginia.edu/).


## References
[1] Chunkun Bo, Ke Wang, Jeffrey J. Fox, and Kevin Skadron. “Entity Resolution Acceleration using Micron’s Automata Processor.”  In Proceedings of the Workshop on Architectures and Systems for Big Data (ASBD), in conjunction with ISCA, June 2015.
