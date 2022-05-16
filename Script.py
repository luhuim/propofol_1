#!/usr/bin/python3
"""
Title: simulating short-read sequencing
Date: 2021-11-28
Author: Huimin Lu

Description:
    This program will randomly genereate a sequence with given lenghth
    simulating the process: chopping it to very small, overlapping segments (=reads), 
    maintaining the first read, and mixing the rest read
    extension the new sequance, I default the first read is settles
    and then aligned them. 
    output the accuracy of alignmnet.
List of function:
    simulate (n=100,l=20)
    n is the lenghth of sequence, default 100
    l is the lenghth of read,default 20
Procedure:
    1,randomly genereate a sequence with given lenghth
    2,copping the sequence into read
    3,extract the first element maintaining the first read, and mixing the rest read
    4,simulating the extension of new sequence
    5,alignment the new sequence with seqeunce generated in procedure one
    6,output the accuracy of alignmnet.
Usage:
    Firstly, call the fonction "simulate"
    Then run the function, n=100/1000/10000, l=20/10/5
"""
#%%
def simulate (n=100,l=20):
#1,randomly genereate a sequence with given lenghth
    #l means the length of piece, default 20
    #n means the length of sequence default 100
    import string    
    import random # define the random module  
    # n = 100  # number of characters in the string.  
    # call random.choices() string module to find the string in Uppercase + numeric data.  
    base=['A','T','C','G']
    seq = ''.join(random.choices(base, k = n))
    print("seq",seq)
#2,copping the sequence into read
    #extract the segment from sequence and adding the segment into a list called"seq_list"
    seq_list=[]#generate an empty list containing reads
    #using while loop, adding one segment every time
    i=0
    while i in range(0,n-l+1):#the number of segment euqal to: n-l+1
        seq_list.append(seq[i:i+l])#this is the regulation of every read's start and end index
        i+=1
    # print(seq_list)
    print(len(seq_list))
#3,extract the first element maintaining the first read, and mixing the rest read
    first=seq_list[0]
    # print("first",first)
    seq_list.pop(0)
    # # print("old list",seq_list)
    random.shuffle(seq_list)
    # print("mix list",seq_list)#mix up
    # print("length of mix",len(seq_list))
#4,extension the new sequance
    new_seq=""
    new_seq+=first# first read is settled
    # print("original new seq",new_seq)
    m=len(seq_list)
    # print(m)
    x=1
    for x in range(1,m+1):# m+2 is the number of times of while loop/extension the letter
    #x is to calculaing the times of while loop
        for read in seq_list:#every extension is to searching the matched read, using if statement
            # print("read",read)
            # print("new_seq[-19:]",new_seq[-19:])
            # print("read[:19]",read[:19])
            if new_seq[-(l-1):]==read[:(l-1)]:#matching requirement: totally matched excepet the last letter in read
                # print("read",read)
                new_seq+=read[-1]#add the last letter into new sequence
                # print("new_seq",new_seq)
                seq_list.remove(read)#remove the matched read from the mixed "seq_list"
                # print(seq_list)
                # print(len(seq_list))
                break#if matched, executing the if statement, and break, jumping out of if statement,
                # which means, the rest of "read" would never be read, directly leaving
        
        x+=1#leaving the if statement, plus one time
        # continue
    print("new sequence",new_seq)
    # print("x",x)
#5, aligned them.
    # print("new_seq",new_seq)
    # print("new",len(new_seq))
    # print("actual",len(seq))
    estimate=list(new_seq)
    actual=list(seq)
    #separate them letter by letter
    y=0
    identity=0
    for y in range(0,len(new_seq)):
        if actual[y]==estimate[y]:
            identity+=1
#6, output the accuracy of alignmnet.
    print("identity",round(identity/len(seq)*100,2),"%")
    
    return
#%%
simulate (10000,20)
#%% 
"""
Summary

Given n=100, if l=20, the identity is 100%.
If l=10, the identity is 100%, most of time.
If l=9, the identity is 100%, most of time.
But, if l=8, the identity decrease to around 50%, sometimes.
If l=5, the identity range from 12% to 55%.

Given n=1000, if l=20, the identity is 100%,
If l=10, the identity is 100% sometimes, sometimes decrease to 10%.
If l=5, the identity range from 7% to 41%.

Given n=10000, if l=20, the identity is 100%,
If l=10, the identity is around 20%,
If l=5, the identity is around 20%.

In conclusion, when l>=20, sequence with any lenghth can match 100% accuracy.
If 8<l<20, the result is 100% most of time when the lenghth is 100, but with the lenghth increasing,
the accuracy would decrease.
If l<=8, sequence with any length would get low accuracy.

The reason is that when l=20, there would be 4^20 types of result, 
which make the segment unique and easy to be matched to the place where it should have located.
But when l=5, there would be 4^5 types of result, which make the segment repeat serously,
and easy to be matched to incorrect place, and the new seqeunce even couldn't extend to the previous lenght, 
so the accuracy is very low.
"""



