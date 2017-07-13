# -*- coding: utf-8 -*-
"""

@author: bochunkun
"""

import sys

filename = sys.argv[1]

def firstnamestartmacro (i,name):
     
    commaid= i+32
    spaceid= i+31
    namelength=len(name)
    name_upper=name.upper()
    name_lower=name.lower()
    if namelength <11:
        for j in range(0,namelength):
            if j==0:           
                print '        <state-transition-element id="%d" symbol-set="[%s%s]" start="all-input">' %(i,name_upper[j],name_lower[j])
                print '                <activate-on-match element="%d"/>' %(i+1) 
                print '                <activate-on-match element="%d"/>' %(i+11)
                print "        </state-transition-element> "  
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]" start="all-input">' %((i+10),name_upper[j],name_lower[j])
                print '                <activate-on-match element="%d"/>' %(i+21) 
                print "        </state-transition-element> " 
                i=i+1

            if j==1:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+11) 
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+10),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+20),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+11) 
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+10),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+20),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print "        </state-transition-element> " 
                    i=i+1

            if j>1:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+11)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+10),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+20),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+11)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+10),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+20),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    i=i+1

        for j in range(namelength,12):
            if j<9:
                print '        <state-transition-element id="%d" symbol-set="+">' %(i)
                print '                <activate-on-match element="%d"/>' %(i+1)
                print '                <activate-on-match element="%d"/>' %(i+11)
                print '                <activate-on-match element="%d"/>' %commaid
                print '                <activate-on-match element="%d"/>' %spaceid
                print "        </state-transition-element> " 
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+10))
                print '                <activate-on-match element="%d"/>' %(i+21)                        
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+20))
                print '                <activate-on-match element="%d"/>' %(i+21)
                print '                <activate-on-match element="%d"/>' %commaid
                print '                <activate-on-match element="%d"/>' %spaceid
                print "        </state-transition-element> " 
                i=i+1
            
            if j==9:
                print '        <state-transition-element id="%d" symbol-set="+">' %(i)
                print '                <activate-on-match element="%d"/>' %(i+11)
                print '                <activate-on-match element="%d"/>' %commaid
                print '                <activate-on-match element="%d"/>' %spaceid
                print "        </state-transition-element> " 
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+10))
                print '                <activate-on-match element="%d"/>' %(i+21)                        
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+20))
                print '                <activate-on-match element="%d"/>' %(i+21)
                print '                <activate-on-match element="%d"/>' %commaid
                print '                <activate-on-match element="%d"/>' %spaceid
                print "        </state-transition-element> " 
                i=i+1
            
            if j==10:
                print '        <state-transition-element id="%d" symbol-set="+">' %(i+10)
                print '                <activate-on-match element="%d"/>' %commaid
                print '                <activate-on-match element="%d"/>' %spaceid
                print "        </state-transition-element> " 

                print '        <state-transition-element id="%d" symbol-set="+">' %((i+20))
                print '                <activate-on-match element="%d"/>' %commaid
                print '                <activate-on-match element="%d"/>' %spaceid
                print "        </state-transition-element> " 
                i=i+1
       
    if namelength ==11:
        for j in range(0,namelength):
            if j==0:           
                print '        <state-transition-element id="%d" symbol-set="[%s%s]" start="all-input">' %(i,name_upper[j],name_lower[j])
                print '                <activate-on-match element="%d"/>' %(i+1) 
                print '                <activate-on-match element="%d"/>' %(i+11)
                print "        </state-transition-element> "  
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]" start="all-input">' %((i+10),name_upper[j],name_lower[j])
                print '                <activate-on-match element="%d"/>' %(i+21) 
                print "        </state-transition-element> " 
                i=i+1

            if j==1:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+11) 
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+10),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+20),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+11) 
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+10),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+20),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print "        </state-transition-element> " 
                    i=i+1


            if j>1 and j<9:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+11)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+10),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+20),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+11)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+10),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+20),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    i=i+1
            
            if j==9:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+11)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+10),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+20),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+11)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+10),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+20),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    i=i+1
            
            if j==10:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(i+10,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
    
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i+20,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %(i+10,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
    
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i+20,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    i=i+1

def familynamestartmacro (i,name):
     
    commaid= i+82
    spaceid= i+81
    namelength=len(name)
    name_upper=name.upper()
    name_lower=name.lower()
    i=i+50
    if namelength <11:
        for j in range(0,namelength):
            if j==0:           
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                print '                <activate-on-match element="%d"/>' %(i+1) 
                print '                <activate-on-match element="%d"/>' %(i+11)
                print "        </state-transition-element> "  
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+10),name_upper[j],name_lower[j])
                print '                <activate-on-match element="%d"/>' %(i+21) 
                print "        </state-transition-element> " 
                i=i+1

            if j==1:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+11) 
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+10),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+20),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+11) 
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+10),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+20),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print "        </state-transition-element> " 
                    i=i+1

            if j>1:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+11)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+10),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+20),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+11)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+10),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+20),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    i=i+1

        for j in range(namelength,12):
            if j<9:
                print '        <state-transition-element id="%d" symbol-set="+">' %(i)
                print '                <activate-on-match element="%d"/>' %(i+1)
                print '                <activate-on-match element="%d"/>' %(i+11)
                print '                <activate-on-match element="%d"/>' %commaid
                print '                <activate-on-match element="%d"/>' %spaceid
                print "        </state-transition-element> " 
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+10))
                print '                <activate-on-match element="%d"/>' %(i+21)                        
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+20))
                print '                <activate-on-match element="%d"/>' %(i+21)
                print '                <activate-on-match element="%d"/>' %commaid
                print '                <activate-on-match element="%d"/>' %spaceid
                print "        </state-transition-element> " 
                i=i+1
            
            if j==9:
                print '        <state-transition-element id="%d" symbol-set="+">' %(i)
                print '                <activate-on-match element="%d"/>' %(i+11)
                print '                <activate-on-match element="%d"/>' %commaid
                print '                <activate-on-match element="%d"/>' %spaceid
                print "        </state-transition-element> " 
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+10))
                print '                <activate-on-match element="%d"/>' %(i+21)                        
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+20))
                print '                <activate-on-match element="%d"/>' %(i+21)
                print '                <activate-on-match element="%d"/>' %commaid
                print '                <activate-on-match element="%d"/>' %spaceid
                print "        </state-transition-element> " 
                i=i+1
            
            if j==10:
                print '        <state-transition-element id="%d" symbol-set="+">' %(i+10)
                print '                <activate-on-match element="%d"/>' %commaid
                print '                <activate-on-match element="%d"/>' %spaceid
                print "        </state-transition-element> " 

                print '        <state-transition-element id="%d" symbol-set="+">' %((i+20))
                print '                <activate-on-match element="%d"/>' %commaid
                print '                <activate-on-match element="%d"/>' %spaceid
                print "        </state-transition-element> " 
                i=i+1
       
    if namelength ==11:
        for j in range(0,namelength):
            if j==0:           
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                print '                <activate-on-match element="%d"/>' %(i+1) 
                print '                <activate-on-match element="%d"/>' %(i+11)
                print "        </state-transition-element> "  
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+10),name_upper[j],name_lower[j])
                print '                <activate-on-match element="%d"/>' %(i+21) 
                print "        </state-transition-element> " 
                i=i+1

            if j==1:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+11) 
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+10),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+20),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+11) 
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+10),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+20),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print "        </state-transition-element> " 
                    i=i+1

            if j>1 and j<9:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+11)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+10),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+20),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+11)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+10),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+20),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    i=i+1
            
            if j==9:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+11)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+10),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+20),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+11)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+10),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+20),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+21)
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    i=i+1
            
            if j==10:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(i+10,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
    
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i+20,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %(i+10,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
    
                    print '        <state-transition-element id="%d" symbol-set=“%s">' %(i+20,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %commaid
                    print '                <activate-on-match element="%d"/>' %spaceid
                    print "        </state-transition-element> " 
                    i=i+1

def firstnameshortmacro (i,name):
         
    notcommaid= i+46
    commaid=i+47
    namelength=len(name)
    
    if namelength > 5:
        new_name=name[:5]
        name_upper=new_name.upper()
        name_lower=new_name.lower()
    else:       
        name_upper=name.upper()
        name_lower=name.lower()
    
    i = i+33
        
    if namelength <5:
        for j in range(0,namelength):
            if j==0:           
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                print '                <activate-on-match element="%d"/>' %(i+1) 
                print '                <activate-on-match element="%d"/>' %(i+5)
                print "        </state-transition-element> "  
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+4),name_upper[j],name_lower[j])
                print '                <activate-on-match element="%d"/>' %(i+9) 
                print "        </state-transition-element> " 
                i=i+1

            if j==1:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+5) 
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+4),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+8),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+5) 
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+4),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+8),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print "        </state-transition-element> " 
                    i=i+1

            if j>1:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+5)
                    print '                <activate-on-match element="%d"/>' %notcommaid
                    print '                <activate-on-match element="%d"/>' %commaid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+4),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+8),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print '                <activate-on-match element="%d"/>' %notcommaid
                    print '                <activate-on-match element="%d"/>' %commaid
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+5)
                    print '                <activate-on-match element="%d"/>' %notcommaid
                    print '                <activate-on-match element="%d"/>' %commaid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+4),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+8),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print '                <activate-on-match element="%d"/>' %notcommaid
                    print '                <activate-on-match element="%d"/>' %commaid
                    print "        </state-transition-element> " 
                    i=i+1

        for j in range(namelength,5):
            if j<2:
                print '        <state-transition-element id="%d" symbol-set="+">' %(i)
                print '                <activate-on-match element="%d"/>' %(i+1)
                print '                <activate-on-match element="%d"/>' %(i+5)
                print '                <activate-on-match element="%d"/>' %notcommaid
                print '                <activate-on-match element="%d"/>' %commaid
                print "        </state-transition-element> " 
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+4))
                print '                <activate-on-match element="%d"/>' %(i+9)                        
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+8))
                print '                <activate-on-match element="%d"/>' %(i+9)
                print '                <activate-on-match element="%d"/>' %notcommaid
                print '                <activate-on-match element="%d"/>' %commaid
                print "        </state-transition-element> " 
                i=i+1
            
            if j==3:
                print '        <state-transition-element id="%d" symbol-set="+">' %(i)
                print '                <activate-on-match element="%d"/>' %(i+5)
                print '                <activate-on-match element="%d"/>' %notcommaid
                print '                <activate-on-match element="%d"/>' %commaid
                print "        </state-transition-element> " 
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+4))
                print '                <activate-on-match element="%d"/>' %(i+9)                        
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+8))
                print '                <activate-on-match element="%d"/>' %(i+9)
                print '                <activate-on-match element="%d"/>' %notcommaid
                print '                <activate-on-match element="%d"/>' %commaid
                print "        </state-transition-element> " 
                i=i+1
            
            if j==4:
                print '        <state-transition-element id="%d" symbol-set="+">' %(i+4)
                print '                <activate-on-match element="%d"/>' %notcommaid
                print '                <activate-on-match element="%d"/>' %commaid
                print "        </state-transition-element> " 

                print '        <state-transition-element id="%d" symbol-set="+">' %((i+8))
                print '                <activate-on-match element="%d"/>' %notcommaid
                print '                <activate-on-match element="%d"/>' %commaid
                print "        </state-transition-element> " 
                i=i+1
       
    if namelength >=5:
        for j in range(0,namelength):
            if j==0:           
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                print '                <activate-on-match element="%d"/>' %(i+1) 
                print '                <activate-on-match element="%d"/>' %(i+5)
                print "        </state-transition-element> "  
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+4),name_upper[j],name_lower[j])
                print '                <activate-on-match element="%d"/>' %(i+9) 
                print "        </state-transition-element> " 
                i=i+1

            if j==1:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+5) 
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+4),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+8),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+5) 
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+4),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+8),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print "        </state-transition-element> " 
                    i=i+1

            if j>1 and j<3:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+5)
                    print '                <activate-on-match element="%d"/>' %notcommaid
                    print '                <activate-on-match element="%d"/>' %commaid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+4),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+8),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print '                <activate-on-match element="%d"/>' %notcommaid
                    print '                <activate-on-match element="%d"/>' %commaid
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+5)
                    print '                <activate-on-match element="%d"/>' %notcommaid
                    print '                <activate-on-match element="%d"/>' %commaid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+4),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+8),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print '                <activate-on-match element="%d"/>' %notcommaid
                    print '                <activate-on-match element="%d"/>' %commaid
                    print "        </state-transition-element> " 
                    i=i+1
            
            if j==3:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+5)
                    print '                <activate-on-match element="%d"/>' %notcommaid
                    print '                <activate-on-match element="%d"/>' %commaid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+4),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+8),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print '                <activate-on-match element="%d"/>' %notcommaid
                    print '                <activate-on-match element="%d"/>' %commaid
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+5)
                    print '                <activate-on-match element="%d"/>' %notcommaid
                    print '                <activate-on-match element="%d"/>' %commaid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+4),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+8),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print '                <activate-on-match element="%d"/>' %notcommaid
                    print '                <activate-on-match element="%d"/>' %commaid
                    print "        </state-transition-element> " 
                    i=i+1
            
            if j==4:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(i+4,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %notcommaid
                    print '                <activate-on-match element="%d"/>' %commaid
                    print "        </state-transition-element> " 
    
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+8),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %notcommaid
                    print '                <activate-on-match element="%d"/>' %commaid
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %(i+4,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %notcommaid
                    print '                <activate-on-match element="%d"/>' %commaid
                    print "        </state-transition-element> " 
    
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+8),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %notcommaid
                    print '                <activate-on-match element="%d"/>' %commaid
                    print "        </state-transition-element> " 
                    i=i+1

def familynameshortmacro (i,name):
         
    notendid= i+98
    endid=i+99
    rightparenthisid=i+84
    namelength=len(name)
    
    if namelength > 5:
        new_name=name[:5]
        name_upper=new_name.upper()
        name_lower=new_name.lower()
    else:       
        name_upper=name.upper()
        name_lower=name.lower()
    
    i = i+85
        
    if namelength <5:
        for j in range(0,namelength):
            if j==0:           
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                print '                <activate-on-match element="%d"/>' %(i+1) 
                print '                <activate-on-match element="%d"/>' %(i+5)
                print "        </state-transition-element> "  
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+4),name_upper[j],name_lower[j])
                print '                <activate-on-match element="%d"/>' %(i+9) 
                print "        </state-transition-element> " 
                i=i+1

            if j==1:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+5) 
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+4),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+8),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+5) 
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+4),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+8),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print "        </state-transition-element> " 
                    i=i+1

            if j>1:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+5)
                    print '                <activate-on-match element="%d"/>' %notendid
                    print '                <activate-on-match element="%d"/>' %endid
                    print '                <activate-on-match element="%d"/>' %rightparenthisid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+4),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+8),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print '                <activate-on-match element="%d"/>' %notendid
                    print '                <activate-on-match element="%d"/>' %endid
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+5)
                    print '                <activate-on-match element="%d"/>' %notendid
                    print '                <activate-on-match element="%d"/>' %endid
                    print '                <activate-on-match element="%d"/>' %rightparenthisid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+4),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+8),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print '                <activate-on-match element="%d"/>' %notendid
                    print '                <activate-on-match element="%d"/>' %endid
                    print "        </state-transition-element> " 
                    i=i+1

        for j in range(namelength,5):
            if j<2:
                print '        <state-transition-element id="%d" symbol-set="+">' %(i)
                print '                <activate-on-match element="%d"/>' %(i+1)
                print '                <activate-on-match element="%d"/>' %(i+5)
                print '                <activate-on-match element="%d"/>' %notendid
                print '                <activate-on-match element="%d"/>' %endid
                print '                <activate-on-match element="%d"/>' %rightparenthisid
                print "        </state-transition-element> " 
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+4))
                print '                <activate-on-match element="%d"/>' %(i+9)                        
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+8))
                print '                <activate-on-match element="%d"/>' %(i+9)
                print '                <activate-on-match element="%d"/>' %notendid
                print '                <activate-on-match element="%d"/>' %endid
                print '                <activate-on-match element="%d"/>' %rightparenthisid
                print "        </state-transition-element> " 
                i=i+1
            
            if j==3:
                print '        <state-transition-element id="%d" symbol-set="+">' %(i)
                print '                <activate-on-match element="%d"/>' %(i+5)
                print '                <activate-on-match element="%d"/>' %notendid
                print '                <activate-on-match element="%d"/>' %endid
                print '                <activate-on-match element="%d"/>' %rightparenthisid
                print "        </state-transition-element> " 
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+4))
                print '                <activate-on-match element="%d"/>' %(i+9)                        
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+8))
                print '                <activate-on-match element="%d"/>' %(i+9)
                print '                <activate-on-match element="%d"/>' %notendid
                print '                <activate-on-match element="%d"/>' %endid
                print '                <activate-on-match element="%d"/>' %rightparenthisid
                print "        </state-transition-element> " 
                i=i+1
            
            if j==4:
                print '        <state-transition-element id="%d" symbol-set="+">' %(i+4)
                print '                <activate-on-match element="%d"/>' %notendid
                print '                <activate-on-match element="%d"/>' %endid
                print '                <activate-on-match element="%d"/>' %rightparenthisid
                print "        </state-transition-element> " 

                print '        <state-transition-element id="%d" symbol-set="+">' %((i+8))
                print '                <activate-on-match element="%d"/>' %notendid
                print '                <activate-on-match element="%d"/>' %endid
                print '                <activate-on-match element="%d"/>' %rightparenthisid
                print "        </state-transition-element> " 
                i=i+1
       
    if namelength >=5:
        for j in range(0,namelength):
            if j==0:           
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                print '                <activate-on-match element="%d"/>' %(i+1) 
                print '                <activate-on-match element="%d"/>' %(i+5)
                print "        </state-transition-element> "  
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+4),name_upper[j],name_lower[j])
                print '                <activate-on-match element="%d"/>' %(i+9) 
                print "        </state-transition-element> " 
                i=i+1

            if j==1:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+5) 
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+4),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+8),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+5) 
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+4),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+8),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print "        </state-transition-element> " 
                    i=i+1

            if j>1 and j<3:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+5)
                    print '                <activate-on-match element="%d"/>' %notendid
                    print '                <activate-on-match element="%d"/>' %endid
                    print '                <activate-on-match element="%d"/>' %rightparenthisid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+4),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+8),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print '                <activate-on-match element="%d"/>' %notendid
                    print '                <activate-on-match element="%d"/>' %endid
                    print '                <activate-on-match element="%d"/>' %rightparenthisid
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+1)
                    print '                <activate-on-match element="%d"/>' %(i+5)
                    print '                <activate-on-match element="%d"/>' %notendid
                    print '                <activate-on-match element="%d"/>' %endid
                    print '                <activate-on-match element="%d"/>' %rightparenthisid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+4),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+8),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print '                <activate-on-match element="%d"/>' %notendid
                    print '                <activate-on-match element="%d"/>' %endid
                    print '                <activate-on-match element="%d"/>' %rightparenthisid
                    print "        </state-transition-element> " 
                    i=i+1
            
            if j==3:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(i,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+5)
                    print '                <activate-on-match element="%d"/>' %notendid
                    print '                <activate-on-match element="%d"/>' %endid
                    print '                <activate-on-match element="%d"/>' %rightparenthisid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((i+4),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+8),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print '                <activate-on-match element="%d"/>' %notendid
                    print '                <activate-on-match element="%d"/>' %endid
                    print '                <activate-on-match element="%d"/>' %rightparenthisid
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="%s">' %(i,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+5)
                    print '                <activate-on-match element="%d"/>' %notendid
                    print '                <activate-on-match element="%d"/>' %endid
                    print '                <activate-on-match element="%d"/>' %rightparenthisid
                    print "        </state-transition-element> " 
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %((i+4),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)                        
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+8),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %(i+9)
                    print '                <activate-on-match element="%d"/>' %notendid
                    print '                <activate-on-match element="%d"/>' %endid
                    print '                <activate-on-match element="%d"/>' %rightparenthisid
                    print "        </state-transition-element> " 
                    i=i+1
            
            if j==4:
                if(name_upper[j]!="."):
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(i+4,name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %notendid
                    print '                <activate-on-match element="%d"/>' %endid
                    print '                <activate-on-match element="%d"/>' %rightparenthisid
                    print "        </state-transition-element> " 
    
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((i+8),name_upper[j],name_lower[j])
                    print '                <activate-on-match element="%d"/>' %notendid
                    print '                <activate-on-match element="%d"/>' %endid
                    print '                <activate-on-match element="%d"/>' %rightparenthisid
                    print "        </state-transition-element> " 
                    i=i+1
                else:
                    print '        <state-transition-element id="%d" symbol-set="[^%s]">' %(i+4,name_upper[j])
                    print '                <activate-on-match element="%d"/>' %notendid
                    print '                <activate-on-match element="%d"/>' %endid
                    print '                <activate-on-match element="%d"/>' %rightparenthisid
                    print "        </state-transition-element> " 
    
                    print '        <state-transition-element id="%d" symbol-set="%s">' %((i+8),name_upper[j])
                    print '                <activate-on-match element="%d"/>' %notendid
                    print '                <activate-on-match element="%d"/>' %endid
                    print '                <activate-on-match element="%d"/>' %rightparenthisid
                    print "        </state-transition-element> " 
                    i=i+1
                

def allpulslong(i):
    commaid=1500000
    for j in range(0,11):
            if j==0:           
                print '        <state-transition-element id="%d" symbol-set="+">' %(i)
                print '                <activate-on-match element="%d"/>' %(i+1) 
                print '                <activate-on-match element="%d"/>' %(i+11)
                print "        </state-transition-element> "  
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+10))
                print '                <activate-on-match element="%d"/>' %(i+21) 
                print "        </state-transition-element> " 
                i=i+1

            if j==1:
                print '        <state-transition-element id="%d" symbol-set="+">' %(i)
                print '                <activate-on-match element="%d"/>' %(i+1)
                print '                <activate-on-match element="%d"/>' %(i+11) 
                print "        </state-transition-element> " 
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+10))
                print '                <activate-on-match element="%d"/>' %(i+21)                        
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+20))
                print '                <activate-on-match element="%d"/>' %(i+21)
                print "        </state-transition-element> " 
                i=i+1

            if j>1 and j<9:
                print '        <state-transition-element id="%d" symbol-set="+">' %(i)
                print '                <activate-on-match element="%d"/>' %(i+1)
                print '                <activate-on-match element="%d"/>' %(i+11)
                print '                <activate-on-match element="%d"/>' %commaid
                print "        </state-transition-element> " 
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+10))
                print '                <activate-on-match element="%d"/>' %(i+21)                        
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+20))
                print '                <activate-on-match element="%d"/>' %(i+21)
                print '                <activate-on-match element="%d"/>' %commaid
                print "        </state-transition-element> " 
                i=i+1
            
            if j==9:
                print '        <state-transition-element id="%d" symbol-set="+">' %(i)
                print '                <activate-on-match element="%d"/>' %(i+11)
                print '                <activate-on-match element="%d"/>' %commaid
                print "        </state-transition-element> " 
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+10))
                print '                <activate-on-match element="%d"/>' %(i+21)                        
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="+">' %((i+20))
                print '                <activate-on-match element="%d"/>' %(i+21)
                print '                <activate-on-match element="%d"/>' %commaid
                print "        </state-transition-element> " 
                i=i+1
            
            if j==10:
                print '        <state-transition-element id="%d" symbol-set="+">' %(i+10)
                print '                <activate-on-match element="%d"/>' %commaid
                print "        </state-transition-element> " 

                print '        <state-transition-element id="%d" symbol-set="+">' %(i+20)
                print '                <activate-on-match element="%d"/>' %commaid
                print "        </state-transition-element> " 
                i=i+1
    
def firstnameallplusshort(i):
    commaid=i+47
    notcommaid = i+46
    
    i=i+33
    
    
    for j in range(0,5):
        if j==0:           
            print '        <state-transition-element id="%d" symbol-set="+">' %(i)
            print '                <activate-on-match element="%d"/>' %(i+1) 
            print '                <activate-on-match element="%d"/>' %(i+5)
            print "        </state-transition-element> "  
            print '        <state-transition-element id="%d" symbol-set="+">' %((i+4))
            print '                <activate-on-match element="%d"/>' %(i+9) 
            print "        </state-transition-element> " 
            i=i+1

        if j==1:
            print '        <state-transition-element id="%d" symbol-set="+">' %(i)
            print '                <activate-on-match element="%d"/>' %(i+1)
            print '                <activate-on-match element="%d"/>' %(i+5) 
            print "        </state-transition-element> " 
            print '        <state-transition-element id="%d" symbol-set="+">' %((i+4))
            print '                <activate-on-match element="%d"/>' %(i+9)                        
            print "        </state-transition-element> "
            print '        <state-transition-element id="%d" symbol-set="+">' %((i+8))
            print '                <activate-on-match element="%d"/>' %(i+9)
            print "        </state-transition-element> " 
            i=i+1

        if j>1 and j<3:
            print '        <state-transition-element id="%d" symbol-set="+">' %(i)
            print '                <activate-on-match element="%d"/>' %(i+1)
            print '                <activate-on-match element="%d"/>' %(i+5)
            print '                <activate-on-match element="%d"/>' %commaid
            print '                <activate-on-match element="%d"/>' %notcommaid
            print "        </state-transition-element> " 
            print '        <state-transition-element id="%d" symbol-set="+">' %((i+4))
            print '                <activate-on-match element="%d"/>' %(i+9)                        
            print "        </state-transition-element> "
            print '        <state-transition-element id="%d" symbol-set="+">' %((i+8))
            print '                <activate-on-match element="%d"/>' %(i+9)
            print '                <activate-on-match element="%d"/>' %commaid
            print '                <activate-on-match element="%d"/>' %notcommaid
            print "        </state-transition-element> " 
            i=i+1
        
        if j==3:
            print '        <state-transition-element id="%d" symbol-set="+">' %(i)
            print '                <activate-on-match element="%d"/>' %(i+5)
            print '                <activate-on-match element="%d"/>' %commaid
            print '                <activate-on-match element="%d"/>' %notcommaid
            print "        </state-transition-element> " 
            print '        <state-transition-element id="%d" symbol-set="+">' %((i+4))
            print '                <activate-on-match element="%d"/>' %(i+9)                        
            print "        </state-transition-element> "
            print '        <state-transition-element id="%d" symbol-set="+">' %((i+8))
            print '                <activate-on-match element="%d"/>' %(i+9)
            print '                <activate-on-match element="%d"/>' %commaid
            print '                <activate-on-match element="%d"/>' %notcommaid
            print "        </state-transition-element> " 
            i=i+1
        
        if j==4:
            print '        <state-transition-element id="%d" symbol-set="+">' %(i+4)
            print '                <activate-on-match element="%d"/>' %commaid
            print '                <activate-on-match element="%d"/>' %notcommaid
            print "        </state-transition-element> " 

            print '        <state-transition-element id="%d" symbol-set="+">' %((i+8))
            print '                <activate-on-match element="%d"/>' %commaid
            print '                <activate-on-match element="%d"/>' %notcommaid
            print "        </state-transition-element> " 
            i=i+1   
 
def familynameallplusshort(i):
    endid=i+99
    notendid = i+98
    rightparenthisid=i+84
    
    i=i+85
    
    for j in range(0,5):
        if j==0:           
            print '        <state-transition-element id="%d" symbol-set="+">' %(i)
            print '                <activate-on-match element="%d"/>' %(i+1) 
            print '                <activate-on-match element="%d"/>' %(i+5)
            print "        </state-transition-element> "  
            print '        <state-transition-element id="%d" symbol-set="+">' %((i+4))
            print '                <activate-on-match element="%d"/>' %(i+9) 
            print "        </state-transition-element> " 
            i=i+1

        if j==1:
            print '        <state-transition-element id="%d" symbol-set="+">' %(i)
            print '                <activate-on-match element="%d"/>' %(i+1)
            print '                <activate-on-match element="%d"/>' %(i+5) 
            print "        </state-transition-element> " 
            print '        <state-transition-element id="%d" symbol-set="+">' %((i+4))
            print '                <activate-on-match element="%d"/>' %(i+9)                        
            print "        </state-transition-element> "
            print '        <state-transition-element id="%d" symbol-set="+">' %((i+8))
            print '                <activate-on-match element="%d"/>' %(i+9)
            print "        </state-transition-element> " 
            i=i+1

        if j>1 and j<3:
            print '        <state-transition-element id="%d" symbol-set="+">' %(i)
            print '                <activate-on-match element="%d"/>' %(i+1)
            print '                <activate-on-match element="%d"/>' %(i+5)
            print '                <activate-on-match element="%d"/>' %endid
            print '                <activate-on-match element="%d"/>' %notendid
            print '                <activate-on-match element="%d"/>' %rightparenthisid
            print "        </state-transition-element> " 
            print '        <state-transition-element id="%d" symbol-set="+">' %((i+4))
            print '                <activate-on-match element="%d"/>' %(i+9)                        
            print "        </state-transition-element> "
            print '        <state-transition-element id="%d" symbol-set="+">' %((i+8))
            print '                <activate-on-match element="%d"/>' %(i+9)
            print '                <activate-on-match element="%d"/>' %endid
            print '                <activate-on-match element="%d"/>' %notendid
            print '                <activate-on-match element="%d"/>' %rightparenthisid
            print "        </state-transition-element> " 
            i=i+1
        
        if j==3:
            print '        <state-transition-element id="%d" symbol-set="+">' %(i)
            print '                <activate-on-match element="%d"/>' %(i+5)
            print '                <activate-on-match element="%d"/>' %endid
            print '                <activate-on-match element="%d"/>' %notendid
            print '                <activate-on-match element="%d"/>' %rightparenthisid
            print "        </state-transition-element> " 
            print '        <state-transition-element id="%d" symbol-set="+">' %((i+4))
            print '                <activate-on-match element="%d"/>' %(i+9)                        
            print "        </state-transition-element> "
            print '        <state-transition-element id="%d" symbol-set="+">' %((i+8))
            print '                <activate-on-match element="%d"/>' %(i+9)
            print '                <activate-on-match element="%d"/>' %endid
            print '                <activate-on-match element="%d"/>' %notendid
            print '                <activate-on-match element="%d"/>' %rightparenthisid
            print "        </state-transition-element> " 
            i=i+1
        
        if j==4:
            print '        <state-transition-element id="%d" symbol-set="+">' %(i+4)
            print '                <activate-on-match element="%d"/>' %endid
            print '                <activate-on-match element="%d"/>' %notendid
            print '                <activate-on-match element="%d"/>' %rightparenthisid
            print "        </state-transition-element> " 

            print '        <state-transition-element id="%d" symbol-set="+">' %((i+8))
            print '                <activate-on-match element="%d"/>' %endid
            print '                <activate-on-match element="%d"/>' %notendid
            print '                <activate-on-match element="%d"/>' %rightparenthisid
            print "        </state-transition-element> " 
            i=i+1    
 
def firstnamespace(i):
    print '        <state-transition-element id="%d" symbol-set=" ">' %(i+31)
    print '                <activate-on-match element="%d"/>' %(i+33)
    print '                <activate-on-match element="%d"/>' %(i+37)
    print "        </state-transition-element> "

def firstnamenotcomma(i):
    print '        <state-transition-element id="%d" symbol-set="[^,]">' %(i+46)
    print '                <activate-on-match element="%d"/>' %(i+46)
    print '                <activate-on-match element="%d"/>' %(i+47)
    print "        </state-transition-element> "

def firstnamecomma(i):
    print '        <state-transition-element id="%d" symbol-set=",">' %(i+32)
    print '                <activate-on-match element="%d"/>' %(i+50)
    print '                <activate-on-match element="%d"/>' %(i+60)
    print "        </state-transition-element> "

def firstnamecomma_new(i):
    print '        <state-transition-element id="%d" symbol-set=",">' %(i+47)
    print '                <activate-on-match element="%d"/>' %(i+50)
    print '                <activate-on-match element="%d"/>' %(i+60)
    print "        </state-transition-element> "

def familynamespace(i):
    print '        <state-transition-element id="%d" symbol-set=" ">' %(i+81)
    print '                <activate-on-match element="%d"/>' %(i+85)
    print '                <activate-on-match element="%d"/>' %(i+89)
    print '                <activate-on-match element="%d"/>' %(i+83)
    print "        </state-transition-element> "    

def familynameparenthis(i):
    print '        <state-transition-element id="%d" symbol-set="(">' %(i+83)
    print '                <activate-on-match element="%d"/>' %(i+85)
    print '                <activate-on-match element="%d"/>' %(i+89)
    print '                <activate-on-match element="%d"/>' %(i+84)
    print "        </state-transition-element> "  
    print '        <state-transition-element id="%d" symbol-set=")">' %(i+84)
    print '                <activate-on-match element="%d"/>' %(i+98)
    print '                <activate-on-match element="%d"/>' %(i+99)
    print "        </state-transition-element> "      

def familynamenotend(i):
    print '        <state-transition-element id="%d" symbol-set="[^$]">' %(i+98)
    print '                <activate-on-match element="%d"/>' %(i+98)
    print '                <activate-on-match element="%d"/>' %(i+99)
    print "        </state-transition-element> "     
    
def familynameend(i):
    print '        <state-transition-element id="%d" symbol-set="$">' %(i+82)
    print '                <report-on-match/>'
    print "        </state-transition-element> "    
    
def familynameend_new(i):
    print '        <state-transition-element id="%d" symbol-set="$">' %(i+99)
    print '                <report-on-match/>'
    print "        </state-transition-element> " 
    
def convertpar(name):
    newname=name.replace("(","").replace(")","")
    return newname

print'<?xml version="1.0" encoding="UTF-8"?>' 
print'<automata-network id="mismatch1" name="mismatch1">'
print'        <description></description>'

i=1            
with open (filename, 'r') as f:
    lines=f.read().splitlines()
    for line in lines:
#        print i
        name_tmp = line.split(",")
#        print name_tmp
#        print name_tmp[0]
#        print name_tmp[1]
        if (' ' in name_tmp[0]) == True:
            firstnamefirstpart=name_tmp[0].split()[0]
            firstnamesecondpart=name_tmp[0].split()[1]
            firstnamestartmacro(i,firstnamefirstpart)
            firstnameshortmacro(i,firstnamesecondpart)
        else:
            firstnamestartmacro(i,name_tmp[0])
            firstnameallplusshort(i)
        if (' ' in name_tmp[1]) == True:
            familynamefirstpart=name_tmp[1].split()[0]
            familynamesecondpart=name_tmp[1].split()[1]
            familynamestartmacro(i,familynamefirstpart)
            familynameshortmacro(i,familynamesecondpart)
        else:
            familynamestartmacro(i,name_tmp[1])
            familynameallplusshort(i)
        
        firstnamespace(i)
        firstnamenotcomma(i)
        firstnamecomma(i)
        firstnamecomma_new(i)
        
        familynamespace(i)
        familynameparenthis(i)
        familynamenotend(i)
        familynameend(i)
        familynameend_new(i)
        i=i+100
 
print '</automata-network>'

           