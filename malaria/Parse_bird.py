#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 16:52:00 2022

@author: inf-31-2021

"""
f=open("Haemoproteus_tartakovskyi.fna",'r') #f is fasta
l=open("scaffolds.txt",'r') #l contain the scaffold that need to be removed 
o=open("gffParse_no_bird.fna",'w') 
bird = []#a new alist containing the headerof bird
for line in l:
    line=line.strip()#remove the new line sign
    bird.append(line)#adding the line into list "bird"
print (bird)

for line in f:
    header=[] #list to contain the header
    if line.startswith('>'):
        line.strip()
        # print(line)
        header=line.split() 
        print(header[0][1:])
        if header[0][1:] in bird:
            # print(line)
            next(f)
        else: #store the rest content into the empty file  
            # print(line)
            o.write("{}\n".format(line.strip()))
            o.write("{}\n".format(next(f).strip()))
f.close()
l.close()
o.close()