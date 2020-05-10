# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 19:29:20 2019

@author: Dibyendu
"""

######################################################_Cosine_Similarity_########################################
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
    #str1=data1.strip()
    

    brr.append(str1)
chk=600
chm=1
for i in range(1,len(quest)):
    ques=quest[i].lower().strip().split(",")
    #ques=quest[i]
    str1=""
    a=[]
    if(len(ques)>chm):
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

word={}
word_i={}
lem = WordNetLemmatizer() 
for i in range(0,len(brr)):
    s=brr[i].split(' ')
    
    for j in s:
        tfd=[]
        tf=[]
        for d in range(0,1001):
            tfd.append(0.0)
        for d in range(0,1000):
            tf.append(0.0)
        w=lem.lemmatize(j).strip()
        if w not in word.keys() and len(w)>chm:
            word[w]=tfd
            word_i[w]=tf
#print(len(word))
for i in range(0,len(brr)):
    s=brr[i].split(' ')
    for j in s:
        w=lem.lemmatize(j).strip()
        if w in word.keys():
            word[w][i]=word[w][i]+1.0
        
for i in word.keys():
    count=0
    for j in range(0,1000):
        if(word[i][j]>0):
            count+=1
    word[i][1000]=count

for i in word.keys():
    for j in range(0,1000):
        #word_i[i][j]=(1+ math.log(word[i][j]+1) )*( math.log( 1000/(word[i][1000]+chk) ))
        word_i[i][j]=word[i][j]

cosine=[]
for i in range(0,1000):
    val=0.0
    for key in word.keys():
        val+=word_i[key][i]*word_i[key][i]
    cosine.append(math.sqrt(val))
Quer=[]  
for i in range(0,len(arr)):
    test_data1 = word_tokenize(arr[i][0].lower())
    test_data2 = word_tokenize(arr[i][1].lower())
    test_data3 = word_tokenize(arr[i][2].lower())
    test_data4 = word_tokenize(arr[i][3].lower())
    quer=[] 
    v_1={}
    for s in test_data1:
        if (len(s.strip())>chm):
            if(lem.lemmatize(s) not in v_1.keys()):
                v_1[lem.lemmatize(s).strip()]=1.0
            else:
                v_1[lem.lemmatize(s).strip()]+=1.0
    quer.append(v_1)
    v_2={}
    for s in test_data2:
        if (len(s.strip())>chm):
            if(lem.lemmatize(s) not in v_2.keys()):
                v_2[lem.lemmatize(s).strip()]=1.0
            else:
                v_2[lem.lemmatize(s).strip()]+=1.0
    quer.append(v_2)
    v_3={}
    for s in test_data3:
        if (len(s.strip())>chm):
            if(lem.lemmatize(s) not in v_3.keys()):
                v_3[lem.lemmatize(s).strip()]=1.0
            else:
                v_3[lem.lemmatize(s).strip()]+=1.0
    quer.append(v_3)
    v_4={}
    for s in test_data4:
        if (len(s.strip())>chm):
            if(lem.lemmatize(s) not in v_4.keys()):
                v_4[lem.lemmatize(s).strip()]=1.0
            else:
                v_4[lem.lemmatize(s).strip()]+=1.0
    quer.append(v_4)
    Quer.append(quer)
cou=0
score=0.0
co=0.0
a=[]
a.append([])
a.append([])
a.append([])
a.append([])
for i in range(0,len(arr)):
    print(i,end=" ")
    maxi=0.0
    number=0.0
    ans=[]
    for j in range(0,4):
        m=0.0
        test_data = word_tokenize(arr[i][j].lower())
        for k in range(0,1000):
                cal=0.0
                down=0.0
                #print(test_data)
                for s in test_data:
                    w=lem.lemmatize(s)
                    if (len(w)>chm) and (w in word.keys()):
                        #print(w)
                        cal=cal+((1+math.log(Quer[i][j][w]+1))*(math.log(1000/(word[w][1000]+chk))))*(word_i[w][k])
                        down=down+((1+math.log(Quer[i][j][w]+1))*(math.log(1000/(word[w][1000]+chk))))*((1+math.log(Quer[i][j][w]+chk))*(math.log(1000/(word[w][1000]+chk))))
                    
                    if (len(w)>chm) and (w not in word.keys()):
                        #print(w)
                        w
                        #cal=cal+((1+math.log(Quer[i][j][w]+1))*(math.log(1000/(0+1))))*(0)
                        #down=down+((1+math.log(Quer[i][j][w]+1))*(math.log(1000/(0+1))))*((1+math.log(Quer[i][j][w]+1))*(math.log(1000/(0+1))))
                if down!=0:
                    cal=cal/(math.sqrt(down)*cosine[k])
                else:
                    cal=0.0
                if(cal>m):
                    m=cal
                a[j].append(cal)
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
dbfile = open('Accuracy_cosine', 'ab')  
pickle.dump(db, dbfile)                      
dbfile.close()                   
                
                    
                    
        
        
    
    
    
    
        

