# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""

import os
import codecs
import string
import os
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import pickle
import math
import numpy as np


path='Training set_HMM.txt'
word={}
count={}
sentence=[]
def read(path):
    fp = codecs.open(path,"r",encoding='utf-8', errors='ignore')
    text=fp.read()
    array=text.split('\n\n')
    for words in array:
        sen='<'
        token=words.split('\n')
        for tok in token:
            part=tok.split('\t')
            #print(part)
            if(len(part)>1):
                sen=sen+" "+part[1]
                if part[0] not in count.keys():
                    count[part[0]]=1.0
                else:
                    count[part[0]]=count[part[0]]+1.0
                    
            if len(part)>1 and part[1] not in word.keys():
                word[part[1]]={}
                word[part[1]][part[0]]=1.0
            else:
                if len(part)>1 and part[0] not in word[part[1]].keys():
                    word[part[1]][part[0]]=1.0
                else:
                    if len(part)>1:
                        word[part[1]][part[0]]=word[part[1]][part[0]]+1
        sen=sen+" "+'>'
        if(len(sen)>3):
            sentence.append(sen)
    #print (len(array))



read(path)
cou=0.0
tol=0.0
wod=0.0
unk={}

for i in count.keys():
    wod=wod+count[i]
    if(count[i]<7):
        for tags in word.keys():
            if i in word[tags].keys():
                if tags not in unk:
                    unk[tags]=word[tags][i]
                else:
                    unk[tags]=unk[tags]+word[tags][i]

Bigrams={}
Bigrams['<']={}
Bigrams['>']={}
for key in word.keys():
    Bigrams[key]={}
for sen in sentence:
    sent=sen.split(' ')
    for i in range(0,len(sent)-1):
        if sent[i+1] not in Bigrams[sent[i]].keys():
            Bigrams[sent[i]][sent[i+1]]=1.0
        else:
            Bigrams[sent[i]][sent[i+1]]=Bigrams[sent[i]][sent[i+1]]+1.0
#print(Bigrams)

#predict=input()
            
            
## Viterbi Algorithm ##    
            
predic="Training set_HMM.txt"
fp1 = codecs.open(predic,"r",encoding='utf-8', errors='ignore')
text1=fp1.read()
new_sen=text1.split('\n\n')
sen_t1=[]
for i in range(0,len(new_sen)):
    se=""
    words_new=new_sen[i].split('\n')
    for j in range(0,len(words_new)):
        part=words_new[j].split('\t')
        if(len(part)>=1):
            se=se+" "+part[0]
    sen_t1.append((se.strip()))

    



#predict="i want to love you ."
#sen_t1=["i wanna go to carl carl carl carl's - jr ."]
#count1=0
for predict in sen_t1:
    target='< '+predict.strip().lower()+' >'
    #print(target)
    size=target.split(' ')
    N=len(size)
    T=len(word)
    #print(len(size))
    viterbi={}
    arr={}
    path={}
    for i in range(1,N-1):
        path[size[i]]={}
    path['>']={}
    alpha=1.0
    for i in Bigrams['<'].keys():
        tol=tol+Bigrams['<'][i]
    tags={}
    for i in word.keys():
        tags[i]={}
    for i in word.keys():
        tol=0.0
        for j in word[i].keys():
            tol=tol+word[i][j]
        tags[i]=tol
        
    start=len(sentence)
    for t in word.keys():
        path[size[1]][t]=' '
        
        '''
        if size[1] in count.keys():
            if size[1] in word[t].keys():
                arr[t]=alpha*word[t][size[1]]/tags[t]*Bigrams['<'][t]/start
        '''
        
        if size[1] in word[t].keys() and t in Bigrams['<'].keys():
            arr[t]=alpha*(Bigrams['<'][t])/(start)*(word[t][size[1]])/(tags[t])
        
        if size[1] not in word[t].keys() and t in Bigrams['<'].keys():
            #arr[t]=alpha*(1+Bigrams['<'][t])/(start+len(word))*(0+1)/(tags[t]+len(count))
            arr[t]=0.0
            
        if size[1] not in word[t].keys() and t not in Bigrams['<'].keys():
            arr[t]=alpha*(1+0)/(start+len(word))*(0+1)/(tags[t]+len(count))
       
        if size[1] in word[t].keys() and t not in Bigrams['<'].keys():
            arr[t]=alpha*(1+0)/(start+len(word))*(word[t][size[1]]+1)/(tags[t]+len(count))
            #arr[t]=0.0
            
    viterbi[size[1]]=arr
    
    for n in range(1,N-1):
        brr={}
        for t in word.keys():
            brr[t]=1.0
        viterbi[size[n+1]]=brr
    
    coi=0
    
    last_tag=""
    
    for n in range(1,N-2):
        maximum=0.0
        for tag in word.keys():
            alpha=1.0
            cal=0.0
            max=0.0
            st=""
            for t in word.keys():
                alpha=viterbi[size[n]][t]
                
                if size[n+1] in word[tag].keys() and tag in Bigrams[t].keys() and t!='.':
                    cal=(1+Bigrams[t][tag])/(tags[t]+len(word))*(word[tag][size[n+1]]+1)/(tags[tag]+len(count))
        
                if size[n+1] not in word[tag].keys() and tag in Bigrams[t].keys() and t!='.':
                    #cal=(1+Bigrams[t][tag])/(tags[t]+len(word))*(0+1)/(tags[tag]+len(count))
                    cal=0.0
        
                if size[n+1] not in word[tag].keys() and tag not in Bigrams[t].keys() and t!='.':
                    cal=(1+0)/(tags[t]+len(word))*(0+1)/(tags[tag]+len(count))
                
                if size[n+1] in word[tag].keys() and tag not in Bigrams[t].keys() and t!='.':
                    #cal=(1+0)/(tags[t]+len(word))*(word[tag][size[n+1]]+1)/(tags[tag]+len(count))
                    cal=0.0
                
                if(t!='.'):
                    cal=alpha*cal
                #if cal>=alpha:
                 #   print(cal," ",t," ",tag)
                if max<cal and t!='.':
                    #print(cal)
                    st=t
                    max=cal
                
                #print(cal,end=" ")
            #print(max)
            viterbi[size[n+1]][tag]=max
            #print(viterbi[size[n+1]][tag]," ",size[n+1]," ",tag)
            #print(max)
            #print("-------------")
            path[size[n+1]][tag]=st
            #print(viterbi[size[n+1]][tag])
            #print(viterbi[size[n+1]][tag])
            if(max>maximum):
                maximum=max
                last_tag=tag
        #print(last_tag," ",size[n+1])
       
        #print()
        #print(maximum)
        #print()
        
    #print('--------------------------------------')
    #print(viterbi['want']['VBP'])
    
    
    sen_tag=last_tag
    i=N-2
    sen_t=''
    while i>0:
        if(size[i]!='')and (last_tag!=''):
            tag1=path[size[i]][last_tag]
            last_tag=tag1
            sen_tag=last_tag+" "+sen_tag
            sen_t=size[i]+" "+sen_t
        i=i-1
    
    display=(sen_tag.strip()).split(' ')
    display_tag=(sen_t.strip()).split(' ')
    if len(display)>1:
        for di in range(0,min(len(display),len(display_tag))):
            print(display_tag[di]," ",display[di])
    print()
    print()
    
    
    #count1=count1+1
    #if(count1>10):
     #   break
    
   

            
        
        
        
        


        

    

