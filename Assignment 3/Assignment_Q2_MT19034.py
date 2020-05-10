# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 03:33:05 2019

@author: Dibyendu
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

path='train.np'
fp = codecs.open(path,"r",encoding='utf-8', errors='ignore')
text=fp.read()
array=text.split('\n\n')
#print(array)
sentence=[]
tags=[]
Bio={}
Bio['B-NP']={}
Bio['I-NP']={}
Bio['O']={}
unitag={}
tol=0.0
most_fe={}
for words in array:
        sen='<'
        tag='<'
        token=words.split('\n')
        for tok in token:
            part=tok.split('\t')
            if(len(part)>2):
                if part[0] not in most_fe.keys():
                    most_fe[part[0]]=0.0
                tol=tol+1
                sen=sen+" "+part[0]
                tag=tag+" "+part[1]
                if part[1] in unitag.keys():
                    unitag[part[1]]=unitag[part[1]]+1
                else:
                    unitag[part[1]]=1.0
                if part[0] not in Bio[part[2]].keys():
                    Bio[part[2]][part[0]]=1.0
                else:
                    Bio[part[2]][part[0]]=1.0+Bio[part[2]][part[0]]
        tag=tag+" >"
        sen=sen+" >"
        sentence.append(sen)
        tags.append(tag)
start={}
end={}
for i in range(0,len(sentence)):
    index=tags[i].split(' ')
    wo=sentence[i].split(' ')
    for k in range(1,len(wo)-1):
        if(index[k+1]=='NN'):
            most_fe[wo[k]]=most_fe[wo[k]]+1
    
for i in range(0,len(sentence)):
    index=sentence[i].split(' ')
    if len(index)>3 and index[1] not in start.keys():
        start[index[1]]=1.0
    else:
        if(len(index)>3):
            start[index[1]]=start[index[1]]+1.0
            
for i in range(0,len(sentence)):
    index=sentence[i].split(' ')
    if len(index)>3 and index[len(index)-3] not in end.keys():
        end[index[len(index)-3]]=1.0
    else:
        if(len(index)>3):
            end[index[len(index)-3]]=end[index[len(index)-3]]+1.0
   
past={}
for i in unitag.keys():
    past[i]={}
         
for i in range(0,len(sentence)):
    index=sentence[i].split(' ')
    tag1=tags[i].split(' ')
    for j in range(1,len(tag1)-1):
        if index[j+1] in past[tag1[j]]:
            past[tag1[j]][index[j+1]]=past[tag1[j]][index[j+1]]+1.0
        else:
            past[tag1[j]][index[j+1]]=1.0
        

     
sen_count=3420

b_tag=0.0
i_tag=0.0
o_tag=0.0


for i in Bio['B-NP'].keys():
    b_tag=b_tag+Bio['B-NP'][i]
for i in Bio['I-NP'].keys():
    i_tag=i_tag+Bio['I-NP'][i]
for i in Bio['O'].keys():
    o_tag=o_tag+Bio['O'][i]
    
    


path='C:\\Users\\Dibyendu\\Desktop\\NLP\\dev.np'
fp = codecs.open(path,"r",encoding='utf-8', errors='ignore')
text=fp.read()
array=text.split('\n\n')
sen_array=[]
got_tag=[]
bi=[]
#print(array)



#sen_array=['December 1998 .']
#got_tag=['NNP CD .']
#bi=['B-NP I-NP O B-NP O O B-NP O B-NP O O O']

for word in array:
    sen=""
    ta=""
    b=""
    token=word.split('\n')
    for tok in token:
        part=tok.split('\t')
        if(len(part)>2):
            sen=sen+" "+part[0]
            ta=ta+" "+part[1]
            b=b+" "+part[2]
    if(len(part)>2):
        if(sen[len(sen)-1]!='.'):
            sen_array.append((sen+" .").strip())
            got_tag.append((ta+" .").strip())
            bi.append((b+" O").strip())
        else:
            sen_array.append(sen.strip())
            got_tag.append(ta.strip())
            bi.append(b.strip())


count=0
total=0.0
right=0.0
file=""

for predict in sen_array:
    viterbi={}
    path={}
    partof=predict.split(' ')
    gota=got_tag[count].split(' ')
    bio_tag=bi[count].split(' ')
    fre={}
    weight={}
    la={}
    for i in range(0,len(partof)-1):
        viterbi[partof[i]]={'B-NP':1.0,'I-NP':1.0,'O':1.0}
        fre[partof[i]]={}
        weight[partof[i]]={}
        path[partof[i]]={'B-NP':'','I-NP':'','O':''}
        la[partof[i]]={}
        if(i==0):
           
            
            if partof[i] in most_fe.keys():
                if partof[i] not in start.keys():
                    w1=0.0
                else:
                    w1=start[partof[i]]/3420.0
            else:
                w1=1/(3420.0+len(most_fe))
           
            if partof[i] in most_fe.keys():
                if partof[i] not in end.keys():
                    w2=0.0
                else:
                    w2=end[partof[i]]/3420.0
            else:
                w2=1/(3420.0+len(most_fe))
            
            
            w3=0.0
                
                
            w4=0.0    
            if(gota[i+1]=='NN'):
                fre[partof[i]]=[1,0,0,1,1]
                
                if partof[i] in most_fe.keys():
                    w4=most_fe[partof[i]]/unitag['NN']
                
            else:
                fre[partof[i]]=[1,0,0,0,1]
                w4=0.0
            ind=bio_tag[i]
            ind=bio_tag[i]
            if partof[i] in Bio['B-NP'].keys():
                la[partof[i]]['B-NP']=Bio['B-NP'][partof[i]]/b_tag
            else:
                la[partof[i]]['B-NP']=1/(b_tag+len(most_fe))
           
            if partof[i] in Bio['I-NP'].keys():
                la[partof[i]]['I-NP']=Bio['I-NP'][partof[i]]/i_tag
            else:
                la[partof[i]]['I-NP']=1/(i_tag+len(most_fe))
            if partof[i] in Bio['O'].keys():
                la[partof[i]]['O']=Bio['O'][partof[i]]/o_tag
            else:
                la[partof[i]]['O']=1/(o_tag+len(most_fe))
                
            weight[partof[i]]=[w1,w2,w3,w4]
        else:
            
            if partof[i] in most_fe.keys():
                if partof[i] not in start.keys():
                    w1=0.0
                else:
                    w1=start[partof[i]]/3420.0
            else:
                w1=1/(3420.0+len(most_fe))
           
            if partof[i] in most_fe.keys():
                if partof[i] not in end.keys():
                    w2=0.0
                else:
                    w2=end[partof[i]]/3420.0
            else:
                w2=1/(3420.0+len(most_fe))
            
            w3=0.0
            w5=0.0
            w4=0.0
            if partof[i] in past[gota[i-1]].keys() and partof[i] in most_fe.keys():
                w3=past[gota[i-1]][partof[i]]/unitag[gota[i-1]]
            if partof[i] not in most_fe.keys():
                w3=1/(unitag[gota[i-1]]+len(most_fe))
            #print(w3," ",partof[i])
            
            
            if(gota[i+1]=='NN'):
                if partof[i] in most_fe.keys():
                    w4=most_fe[partof[i]]/unitag['NN']
                fre[partof[i]]=[0,0,1,1,1]
            else:
                fre[partof[i]]=[0,0,1,0,1]
                w4=0.0
            ind=bio_tag[i]
            if partof[i] in Bio['B-NP'].keys():
                la[partof[i]]['B-NP']=Bio['B-NP'][partof[i]]/b_tag
            else:
                la[partof[i]]['B-NP']=1/(b_tag+len(most_fe))
           
            if partof[i] in Bio['I-NP'].keys():
                la[partof[i]]['I-NP']=Bio['I-NP'][partof[i]]/i_tag
            else:
                la[partof[i]]['I-NP']=1/(i_tag+len(most_fe))
            if partof[i] in Bio['O'].keys():
                la[partof[i]]['O']=Bio['O'][partof[i]]/o_tag
            else:
                la[partof[i]]['O']=1/(o_tag+len(most_fe))
            
            weight[partof[i]]=[w1,w2,w3,w4]
    fre[partof[len(partof)-1]]=[0,1,1,0,1]
    viterbi[partof[len(partof)-1]]={'B-NP':1.0,'I-NP':1.0,'O':1.0}
    #print(path)
    
    ## Viterbi Calculation
    alpha=1.0
    for inde in range(0,1):
        for j in viterbi[partof[inde]].keys():
            sum=0.0
            sum1=0.0
            sum2=0.0
            sum3=0.0
            for k in range(0,4):
                 sum=sum+fre[partof[inde]][k]*weight[partof[inde]][k]
            #print(weight[partof[inde]][k]['B-NP'])
            add=la[partof[inde]]['O']
            sum1=sum+add
            add=la[partof[inde]]['B-NP']
            sum2=sum+add
            add=la[partof[inde]]['I-NP']
            sum3=sum+add
            sum=sum+la[partof[inde]][j]
            '''
            if bio_tag[inde]==j: 
                sum=sum+fre[partof[inde]][4]*weight[partof[inde]][4]
            '''
            #print(sum," ",sum1," ",sum2," ",sum3)
            #cal=alpha*(math.exp(sum)/(math.exp(sum1)+math.exp(sum2)+math.exp(sum3)))
            cal=alpha*(sum)/(sum1+sum2+sum3)
            viterbi[partof[0]][j]=cal
     
    #print (viterbi['The'])      
    
    for inde in range(1,len(partof)-1):
        for ag in viterbi[partof[inde]].keys():
            sum=0.0
            sum1=0.0
            sum2=0.0
            sum3=0.0
            for k in range(0,4):
                sum=sum+fre[partof[inde]][k]*weight[partof[inde]][k]
            add=la[partof[inde]]['O']
            sum1=sum+add
            add=la[partof[inde]]['B-NP']
            sum2=sum+add
            add=la[partof[inde]]['I-NP']
            sum3=sum+add
            sum=sum+la[partof[inde]][ag]
            cal=(math.exp(sum)/(math.exp(sum1)+math.exp(sum2)+math.exp(sum3)))
            alpha=1.0
            if(viterbi[partof[inde-1]]['O']>viterbi[partof[inde-1]]['B-NP'] and viterbi[partof[inde-1]]['O']>viterbi[partof[inde-1]]['I-NP']):
                alpha=viterbi[partof[inde-1]]['O']
                path[partof[inde-1]][ag]='O'
            if(viterbi[partof[inde-1]]['O']<viterbi[partof[inde-1]]['B-NP'] and viterbi[partof[inde-1]]['B-NP']>viterbi[partof[inde-1]]['I-NP']):
                alpha=viterbi[partof[inde-1]]['B-NP']
                path[partof[inde-1]][ag]='B-NP'
            if(viterbi[partof[inde-1]]['O']<viterbi[partof[inde-1]]['I-NP'] and viterbi[partof[inde-1]]['B-NP']<viterbi[partof[inde-1]]['I-NP']):
                alpha=viterbi[partof[inde-1]]['I-NP']
                path[partof[inde-1]][ag]='I-NP'
            viterbi[partof[inde]][ag]=alpha*cal
    
    last_tag=''
    if(viterbi[partof[inde]]['O']>viterbi[partof[inde]]['B-NP'] and viterbi[partof[inde]]['O']>viterbi[partof[inde]]['I-NP']):
        
        last_tag='O'
    if(viterbi[partof[inde]]['O']<viterbi[partof[inde]]['B-NP'] and viterbi[partof[inde]]['B-NP']>viterbi[partof[inde]]['I-NP']):
        
        last_tag='B-NP'
    if(viterbi[partof[inde]]['O']<viterbi[partof[inde]]['I-NP'] and viterbi[partof[inde-1]]['B-NP']<viterbi[partof[inde]]['I-NP']):
                
        last_tag='I-NP'
    if(last_tag==''):
        last_tag='O'
    indexi=int(inde)
    sen_tag=last_tag+" "+'O'
    while(indexi>0):
        tag1=path[partof[indexi-1]][last_tag]
        last_tag=tag1
        sen_tag=last_tag+" "+sen_tag
        #sen_t=partof[indexi]+" "+sen_t
        indexi=indexi-1
    
    display=predict.split(' ')
    check=sen_tag.split(' ')
    check1=bi[count].split(' ')
    for i in range(0,len(display)):
        file=file+display[i]+"\t"+check1[i]+"\t"+check[i]+"\n"
        if(check[i]==check1[i]):
            right=right+1
        total=total+1
    file=file+"\n"
    
    
            
            
    '''
            max=0.0
            for j in viterbi[partof[inde-1]].keys():
                alpha=viterbi[partof[inde-1]][j]
                sum=0.0
                sum1=0.0
                sum2=0.0
                sum3=0.0
                for k in range(0,4):
                    sum=sum+fre[partof[inde]][k]*weight[partof[inde]][k]
                
                add=la[partof[inde]]['O']
                sum1=sum+add
                add=la[partof[inde]]['B-NP']
                sum2=sum+add
                add=la[partof[inde]]['I-NP']
                sum3=sum+add
                sum=sum+la[partof[inde]][j]
                
                #cal=alpha*(math.exp(sum)/(math.exp(sum1)+math.exp(sum2)+math.exp(sum3)))
                cal=alpha*(sum)/(sum1+sum2+sum3)
                #print(cal," ",j," ",bio_tag[inde]," ",alpha)
                print(sum," ",sum1," ",sum2," ",sum3)
                #print(sum," ",sum1," ",j,alpha)
                if(max<cal):
                    max=cal
            viterbi[partof[inde]][ag]=max
            print('\n',max,'\n')
            #print(ag," ",viterbi[partof[inde]][ag],end=" ")
    '''
        #print()
        
    
    
    
    count=count+1
print("Acuracy of model is "," ",right/total*100)
print(file)
f= open("output.txt","w+")
f.write(file)
    
 
''' 
Your	PRP$	B-NP
contribution	NN	I-NP
to	TO	O
Goodwill	NNP	B-NP
will	MD	O
mean	VB	O
more	JJR	B-NP
than	IN	O
you	PRP	B-NP
may	MD	O
know	VB	O
.	.	O
'''
    
    

    

        


        