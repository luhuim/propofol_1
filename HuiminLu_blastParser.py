#!/usr/bin/python3
"""
Title: Blast_parser
Date: 2022-01-25
Arthor: Huimin Lu

Description:
    This program will output the blast parser. 
    I use a function to package the script
    The input file is a default BLAST output file.

List of functions:
    blast(input_file)
    
List of "non standaerd" modules:
    None
    
Procedure:
    open the input file
    write the header of output file
    searching the query, containing the query into the variable "query"
    If there is no hits under this query,containing "***", it would write in the output file
    If there is no character "**", that means this query have hits, in this case directly searching ">"
    every time found ">", contain the header ">" into variable "target"
    after taht searching score and identity, generating variable "score", "identity","evalue"
    write these variable into the output file, under the ">"
    found all ">" under one query, that means a circle finishes, and the loop continue

Usage:
    Run it in terminal.
    python3 HuiminLu_blastParser.py yeast_vs_Paxillus.blastp
"""
#%%
def blast(input_file):
    f=open(input_file,'r')
    output_file = input_file + ".out" #construct a name of output file that is related to input file.
    t=open(output_file,'w')
    #writing the header of output file
    t.write("#query\ttarget\te-value\tidentity(%)\tscore\n")
    
    #Processing every unit
    for line in f: #regart query as a processing unit
        if line.startswith ('Query='):#finding the title
            # i=0
            # print(line) #extract the line start with "Query="
            word=line.split() #split this line into list 
            # print(word)
            query=word[1] #extract the name of query, assign the variable "quary"
            query=query.strip()
            # print(query)
        if line.startswith ("***** No hits found *****"):#case one
            # print("no")
            t.write("{}\t\t\t\t\n".format(query))
        # elif line.startswith ("Sequences producing significant alignments: "):#case two
            # print("yes")
        if line.startswith (">"):
            # i+1=1
    #obtain target
            target=line[1:].strip()#the header of hits
            # print("target",target)
            next(f)#next line is length,skip
            next(f)#third line is empty,skip
            fourth=next(f).split()#fourth line starts with "score",extract score and expect
            # print(fourth)
    #obtain score,eavlue,identity
            score=fourth[2]
            evalue=fourth[7][:-1]
            # print("score is ",score)
            # print("evalue is",evalue)
            fifth=next(f).split()#fifth line starts with "identity", extract identity
            print(fifth)
            identity=fifth[3][1:-3]
            # print("identity is ",identity)
    #write variables into file
            # if i==1:#write the first hit
            t.write("{}\t{}\t{}\t{}\t{}\n".format(query,target,evalue,identity,score))
            # if i>=2:#write the following hit, if necessary
                # t.write("{}\t{}\t{}\t{}\t{}\n".format(query,target,evalue,identity,score))
    f.close()
    t.close()
# blast("yeast_vs_Paxillus.blastp")
# #%%
# import sys
# input_file = sys.argv[1]
# blast(input_file)

    
        
    
    

    
        
