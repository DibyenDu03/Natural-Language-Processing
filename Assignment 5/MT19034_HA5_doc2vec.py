# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 00:33:10 2019

@author: Dibyendu
"""

import os
import codecs
import string
import os
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import pickle
import math
import numpy as np
from nltk.tree import *
from nltk.stem import WordNetLemmatizer 

path='db1.txt'
path1='data.txt'
fp = codecs.open(path,"r",encoding='utf-8', errors='ignore')
text=fp.read()
fp = codecs.open(path1,"r",encoding='utf-8', errors='ignore')
text1=fp.read()
data=text1.split('\n')
quest=text.split("\n")
arr=[]
brr=[]
answerkey=[]
for i in range(0,len(data)):
    str1=""
    data1=data[i].lower().strip()
    #data1=data[i]
    
    for j in range(0,len(data1)):
        #if((data1[j]>='a' and data1[j]<='z') or(data1[j]>='0' and data1[j]<='9')or (data1[j]==' ')or (data1[j]=="'")or (data1[j]=="-")):
        #       str1=str1+data1[j]
        if(data1[j]=='.')or (data1[j]=="/") or (data1[j]==":")or (data1[j]==","):
            str1=str1+" "
        else:
            str1=str1+data1[j]
    

    brr.append(str1)
        
for i in range(1,len(quest)):
    ques=quest[i].lower().strip().split(",")
    str1=""
    a=[]
    if(len(ques)>1):
        answerkey.append((ques[10]))
        #str1=ques[1]
        
        for j in range(0,(len(ques[1])-1)):
            #if((ques[1][j]>='a' and ques[1][j]<='z') or(ques[1][j]>='0' and ques[1][j]<='9') or (ques[1][j]==' ')or (ques[1][j]=="'")or (ques[1][j]=="-")):
            #    str1=str1+ques[1][j]
            if (ques[1][j]=='.')or (ques[1][j]=="/")or (ques[1][j]==":")or (ques[1][j]==","):
                str1=str1+" "
            else:
                str1=str1+ques[1][j]
        #str1=ques[1].strip()
        str2=""
        for j in range(0,(len(ques[2])-1)):
            #if((ques[2][j]>='a' and ques[2][j]<='z') or(ques[2][j]>='0' and ques[2][j]<='9') or (ques[2][j]==' ')or (ques[2][j]=="'")or (ques[2][j]=="-")):
            #    str2=str2+ques[2][j]
            if (ques[2][j]=='.')or (ques[2][j]=="/")or (ques[2][j]==":")or (ques[2][j]==","):
                str2=str2+" "
            else:
                str2=str2+ques[2][j]
        #str2=ques[2].strip()
        a.append(str1+" "+str2.strip())
        str2=""
        for j in range(0,(len(ques[4])-1)):
            #if((ques[4][j]>='a' and ques[4][j]<='z') or(ques[4][j]>='0' and ques[4][j]<='9') or (ques[4][j]==' ')or (ques[4][j]=="'")or (ques[4][j]=="-")):
            #    str2=str2+ques[4][j]
            if (ques[4][j]=='.')or (ques[4][j]=="/")or (ques[4][j]==":")or (ques[4][j]==","):
                str2=str2+" "
            else:
                str2=str2+ques[4][j]
        #str2=ques[2].strip()
        a.append(str1+" "+str2.strip())
        str2=""
        for j in range(0,(len(ques[6])-1)):
            #if((ques[6][j]>='a' and ques[6][j]<='z') or(ques[6][j]>='0' and ques[6][j]<='9') or (ques[6][j]==' ')or (ques[6][j]=="'")or (ques[6][j]=="-")):
            #    str2=str2+ques[6][j]
            if (ques[6][j]=='.')or (ques[6][j]=="/")or (ques[6][j]==":")or (ques[6][j]==","):
                str2=str2+" "
            else:
                str2=str2+ques[6][j]
        #str2=ques[2].strip()
        a.append(str1+" "+str2.strip())
        str2=""
        for j in range(0,(len(ques[8])-1)):
            #if((ques[8][j]>='a' and ques[8][j]<='z') or(ques[8][j]>='0' and ques[8][j]<='9') or (ques[8][j]==' ')or (ques[8][j]=="'")or (ques[8][j]=="-")):
            #    str2=str2+ques[8][j]
            if (ques[8][j]=='.')or (ques[8][j]=="/")or (ques[8][j]==":")or (ques[8][j]==","):
                str2=str2+" "
            else:
                str2=str2+ques[8][j]
        #str2=ques[2].strip()
        a.append(str1+" "+str2.strip())
        arr.append(a)
        
########################################################_DOC_TO_VEC_#############################################    
#Import all the dependencies
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
'''
data = ["I love machine learning. Its awesome.",
        "I love coding in python",
        "I love building chatbots",
        "they chat amagingly well"]
'''

tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(brr)]
max_epochs = 100
vec_size = 20
alpha = 0.025

model = Doc2Vec(size=vec_size,alpha=alpha, 
                min_alpha=0.00025,
                min_count=1,
                dm =1)
  
model.build_vocab(tagged_data)

for epoch in range(max_epochs):
    #print('iteration {0}'.format(epoch))
    model.train(tagged_data,
                total_examples=model.corpus_count,
                epochs=model.iter)
    # decrease the learning rate
    model.alpha -= 0.0002
    # fix the learning rate, no decay
    model.min_alpha = model.alpha

model.save("d2v.model")
print("Model Saved")
from gensim.models.doc2vec import Doc2Vec

model= Doc2Vec.load("d2v.model")
Query=[]
for i in range(0,len(arr)):
    test_data1 = word_tokenize(arr[i][0].lower())
    test_data2 = word_tokenize(arr[i][1].lower())
    test_data3 = word_tokenize(arr[i][2].lower())
    test_data4 = word_tokenize(arr[i][3].lower())
    v1 = model.infer_vector(test_data1)
    v2 = model.infer_vector(test_data2)
    v3 = model.infer_vector(test_data3)
    v4 = model.infer_vector(test_data4)
    query=[]
    query.append(v1)
    query.append(v2)
    query.append(v3)
    query.append(v4)
    Query.append(query)
cou=0
score=0.0
co=0.0
for i in range(0,len(arr)):
    maxi=0.0
    number=0.0
    ans=[]
    print(i,end=" ")
    for j in range(0,4):
        m=0.0
        for k in range(0,1000):
                cal=0.0
                down=0.0
                down1=0.0
                #print(test_data)
                for s in range(0,vec_size):
                    cal=cal+Query[i][j][s]*model[k][s]
                    down=down+Query[i][j][s]*Query[i][j][s]
                    down1=down1+model[k][s]*model[k][s]
                if down!=0 and down1!=0:
                    cal=cal/(math.sqrt(down)*math.sqrt(down1))
                else:
                    cal=0.0
                if(cal>m):
                    m=cal
                #print(cal)
        if(maxi<m):
                maxi=m
                number=0.0
                ans.clear()
                ans.append(chr(j+97))
        if(maxi==m):
                number+=1.0
                ans.append(chr(j+97))
    if answerkey[i] in ans:
        score=score+1.0/number
        co=co+1
        cou=cou+1
db = {} 

print()
print("Acuracy of the model is ",score/len(arr))  
db['Accuracy'] = score/len(arr)
dbfile = open('Accuracy_doc2vec', 'ab')  
pickle.dump(db, dbfile)                      
dbfile.close() 
