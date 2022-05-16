#!/usr/bin/python3

"""
Title: Alignmnet tool
Date: 2021 October 20th
Author: Huimin Lu

Description:
    This program is to evalue the fasta file firstly, and align the sequence in fasta file.
    Finally,output the result in another file.
    This program will filter unqualified fasta file. For example:
        the amount of sequence is not even
        the header is empty
        whether there is wierd character exist in in the sequence(only allow:A/C/T/G/-)
        whether the length of sequence is equal

List of function:
    evalue(file_name)
    test(file_name, output_file, parameters_file=0)

Procedure:
    1. check the fasta file. filtering the wierd mark and letter
    2. put the header and the sequence in dictionary
    3. make the combination
    4. aligning letter by letter under each combination and output the result
    5. write the result in txt file.

Usage: type code below in the command line:
    python Running2.py example.txt Alignment_Result.txt


"""
#%%
#define a function to evaluate the file
#filter fastaq
def evalue(file_name):
    fi=open(file_name,'r')
    i=0
    standard={"A","G","C","T","-"}
    total_sequence=""
    previous_length=[]
    for line in fi:
#(I)--Tackling the header------------------------------------------------------------
        if line.startswith('>'): # if it is a standard fasta file, the first letter in each line is ">" or "A/C/T/G".
            i=i+1
#i is for count ">" ,filter one_sequence file
#filter empty header, len(">\n")is 2--------------------------
            l=len(line)
            if l<=2:
                print("There is an empty header")
                break 
#-----------------------------------------------------------------------            
#finding other strange mark in header
#(II)Tackling the sequence
#comparing the length,assigning here, and comparing at the end
            
#tip 1: set collect unique element

            total_sequence=""
#tip 2: the minus, if seq is part of sdandard but not equeal, the result is 'set()',length is 0 


        else:#not start with ">". checking whether it starts with A/C/T/G
            if line[0] in standard:
                total_sequence += line.strip()
                long=len(total_sequence) # storing length of sequence intp variable "long" 
                previous_length.append(long) # add the length in to the list "privious_length"
                seq=set(total_sequence.upper()) #transforming the letter into upper case
                test = seq-standard  # if there is letter exist in the "seq" but not in the "satndard", that is "test">0,
                                     #that means there is wierd character inside the seqeunce 
                if len(test) == 0 or seq == standard: 
                    pass
                else:
                    print("It's not DNA sequence.")
                    break

#tip 4, combine separeted sequence into one sequence, 
            else: # no ">" and "A/C/T/G"
                print("finding strange mark")
                break

#tip 3,strip() is to remove \n  
#-------count the number of header '>'-------------------------------------------------       
    if i<2:
        print("You should prepare more sequences")
        return False
#comparing the length
    
    length=set(previous_length)
    #print(length)
    if len(length)>=2 :
#there are 2 element in previous length [0,25]
        print("sequences not equal")
        return False
        
#--------------------------------------------------------------------------------        
    fi.close()
    return True

    
#%%
def test(file_name, output_file, parameters_file=0):
#1, define parameters a b t1(transition) t2(transversion), I have default.
      
    if parameters_file:
#tip 5, if the varible have value,that means it is true, and this can continue.
        p=open(parameters_file,'r')          
        abcd = []
#list is to extract the value
        for line in p:
            abcd.append(line.strip().split('\t'))
        a=abcd[1][0]
        b=abcd[1][1]
        t1=abcd[1][2]
        t2=abcd[1][3]
        p.close()
    else:
#assign default value, if do not input the parameters file
        a=1
        b=-1
        t1=-1
        t2=-2
#2,preparing combination 
#2.1 dictionnary
    f=open(file_name,'r')
    t=open(output_file,'w')
    dic={}
    for line in f:
        if line.startswith ('>'):
# tip 6, add element in dictionary
# tip 7, [:-1] is to remove "\n"
            header=line[:-1]
            # print("header",header)
            dic[header]=next(f)[:-1]
            # print("seq",dic[header])
            # print("len",len(dic[header]))
            
#2.2 combination and output result each pair
# tip 8, combination(,2)
    from itertools import combinations
    for c,d in combinations(dic,2):
        #print("combination",c,d)
        i=0
        score=0
        gap=0
        match=0
        for i in range(0,len(dic[c])):
            #print(dic[c])
# #comparing the length of two sequence
            
            base1=dic[c][i]
            base2=dic[d][i]
            #print("loop",i,base1,base2)
#-- 
            if base1+base2=="--":
                score=score+0
                gap+=1
#match +1 a
            elif base1==base2:
                score=score+int(a)
                match=match+1
#gap -1 b
            elif base1=='-' or base2=='-':
                score=score+int(b)
                gap=gap+1
#transition -1 t1
            elif base1+base2=='AG'or base1+base2=='GA'or base1+base2=='CT'or base1+base2=='TC':
                score=score+int(t1)
            else:
                score=score+int(t2)
#transversion -2 t2
#calculate percent serve 2bit round(number,2)

        identity=round(match/len(dic[c])*100,2)
        gap_percent=round(gap/len(dic[c])*100,2)  
        
        # print(c.strip()[1:],d.strip()[1:])
        # write the result into the file
        t.write("{}-{}: Identity:{}/{}({}%), Gaps:{}/{}({}%), Score={}\n".format(c.strip()[1:].title(),d.strip()[1:],match,len(dic[c]),identity,gap,len(dic[c]),gap_percent,score))

#format statement print("I want to {} and {}".format(varible1,varible2))
    f.close()
    t.close()
    return

#%%

import sys
input_file = sys.argv[1]
if evalue(input_file):
    output = sys.argv[2]
    test(input_file,output)




 

