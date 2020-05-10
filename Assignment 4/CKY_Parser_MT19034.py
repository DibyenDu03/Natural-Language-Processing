# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 15:39:31 2019

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




############################################_CFG_TO_CNF_CONVERTER_###################################################


cfg = nltk.data.load("grammars/large_grammars/atis.cfg")

path='cfg.txt'
fp = codecs.open(path,"w",encoding='utf-8', errors='ignore')
fp.write(str(cfg))
fp.close()
intermediate=nltk.CFG.binarize(cfg,padding='$')
cnf_gr=nltk.CFG.remove_unitary_rules(intermediate)
path='cfg.txt'

fp = codecs.open(path,"r",encoding='utf-8', errors='ignore')
text=fp.read()
production=text.split('\n')
cfg=[]
docu=""
for rule in range(1,len(production)):
    #print(rule)
    cfg.append(production[rule].strip())
    docu=docu+production[rule].strip()+"\n"
'''
path34='C:\\Users\\Dibyendu\\Desktop\\cfg1.txt'
f= codecs.open(path34,"w",encoding='utf-8', errors='ignore')
f.write(docu)
'''

count=0
count2=0
count3=0
count1=0
cnf={}
new={}
count_id=0
final={}
c=0
cfg1=[]
name='dib'
tol=0
for rule in cfg:
    tol=tol+1
    part=rule.split(' -> ')
    part2=part[1].split(' ')
    if(len(part2)==1):
        count=count+1
        if(part2[0][0]=="'" or part2[0][0]=='"'):
            count1=count1+1
            if(part[1] not in cnf.keys()):
                cnf[part[1]]=[]
                cnf[part[1]].append(part[0])
            else:
                
                #if(part[0] not in cnf[part[1]]):
                    cnf[part[1]].append(part[0])
                    
        else:
            cfg1.append(rule)
            
    else:
        if(len(part2)==2):
            count2=count2+1
            if(part[1] not in cnf.keys()):
                cnf[part[1]]=[]
                cnf[part[1]].append(part[0])
            else:
                #if(part[0] not in cnf[part[1]]):
                    cnf[part[1]].append(part[0])
        else:
            pro=part2[len(part2)-2]+' '+part2[len(part2)-1]
            if pro in new.keys():
                pro=new[pro]
            else:
                new[pro]=name+'_'+str(count_id)
                #new[pro]=part2[0]+"$"+part2[1]
                count_id=count_id+1
                pro=new[pro]
            for i in range(len(part2)-3,0,-1):
                #pr0=pro
                pro=part2[i]+' '+pro
                
                if pro in new.keys():
                    pro=new[pro]
                else:
                    new[pro]=name+'_'+str(count_id)
                    #new[pro]=pr0+"$"+part2[i]
                    count_id=count_id+1
                    pro=new[pro]
            #pr0=pro
            pro=part2[0]+' '+pro
            if pro in final.keys():
                final[pro].append(part[0])
            else:
                final[pro]=[]
                final[pro].append(part[0])
            '''
            if pro in new.keys():
                pro=new[pro]
            else:
                #new[pro]=name+'_'+str(count_id)
                new[pro]=pr0+"$"+part2[len(part2)-1]
                count_id=count_id+1
                pro=part[0]
            '''
            
                
            count3=count3+1
#print(count+count2+count3)
for rule in final.keys():
    if rule not in cnf.keys():
        cnf[rule]=final[rule]
    else:
        for j in range(0,len(final[rule])):
            if(final[rule][j] not in cnf[rule] ):
                cnf[rule].append(final[rule][j])
for rule in new.keys():
    if rule not in cnf.keys():
        cnf[rule]=[]
        cnf[rule].append(new[rule])
    else:
        if new[rule] not in cnf[rule]:
            cnf[rule].append(new[rule])
            
c_n_f={}
c=0
for prod in cnf.keys():
    for i in range(0,len(cnf[prod])):
        if(cnf[prod][i] in c_n_f.keys()):
            c_n_f[cnf[prod][i]].append(prod)
            c=c+1
        else:
            c_n_f[cnf[prod][i]]=[]
            c_n_f[cnf[prod][i]].append(prod)
            c=c+1
'''          
dib=0
for i in c_n_f.keys():
    dib=dib+len(c_n_f[i])

print(dib)
'''

cou=0
cou1=0
cou2=0
cou3=0
last={}
recheck=[]
#thres=0

rec={}
correct={}
for rule in cfg1:
    part=rule.split(' -> ')
    part2=part[1].split(' ')
    if part[0]in rec.keys():
        rec[part[0]].append(part[1])
    else:
        rec[part[0]]=[]
        rec[part[0]].append(part[1])
        
def check(index,cor,rec):
    if index in cor.keys():
        return cor[index],cor
    else:
        a=[]
        cor[index]=[]
        if index in rec.keys():
            for i in rec[index]:
                if(i[0]=='"'):
                    a.append(i)
                else:
                    b,cor=check(i,cor,rec)
                    for kk in b:
                        if kk not in a:
                            a.append(kk)
                    a.append(i)
        else:
            a.append(index)
        for j in a:
            if j not in cor[index]:
                cor[index].append(j)
    return a,cor
        
        
for rule in rec.keys():
    correct[rule]=[]
    for ind in range(0,len(rec[rule])):
        if(rec[rule][ind][0]=='"'):
            correct[rule].append(rec[rule][ind])
        else:
            array,correct=check(rec[rule][ind],correct,rec)
            array.append(rec[rule][ind])
            for j in array:
                if j not in correct[rule]:
                    correct[rule].append(j)
    

cfg3=[]

for rule in correct.keys():
    regulation=""
    for i in correct[rule]:
        regulation=rule+" -> "+i
        cfg3.append(regulation)
        
'''
dib=0
for i in c_n_f.keys():
    dib=dib+len(c_n_f[i])
print(dib)
'''
'''
print(len(last))
for rule in cfg3:
    part=rule.split(' -> ')
    part2=part[1].split(' ')
    if part[0] in last.keys():
        if part2[0] in c_n_f.keys():
                    cou1=cou1+1
                    for ind in range(0,len(c_n_f[part2[0]])):
                        if c_n_f[part2[0]][ind] not in last[part[0]]:
                            last[part[0]].append(c_n_f[part2[0]][ind])
    else:
        last[part[0]]=[]
        if part2[0] in c_n_f.keys():
                    cou1=cou1+1
                    
                    for ind in range(0,len(c_n_f[part2[0]])):
                        if c_n_f[part2[0]][ind] not in last[part[0]]:
                            last[part[0]].append(c_n_f[part2[0]][ind])
    

'''
for rule in cfg3:
            part=rule.split(' -> ')
            part2=part[1].split(' ')
            cou=cou+1
            #print(rule)
            
            
            if part[0] in last.keys():
                #last[part[0]].append(cnf[part2[0][0]])
                if part2[0] in c_n_f.keys():
                    cou1=cou1+1
                    for ind in range(0,len(c_n_f[part2[0]])):
                        if c_n_f[part2[0]][ind] not in last[part[0]]:
                            last[part[0]].append(c_n_f[part2[0]][ind])
                else:
                    #recheck
                    #print(part2[0]," ",c_n_f[part2[0]])
                    recheck.append(rule)
            else:
                last[part[0]]=[]
                if part2[0] in c_n_f.keys():
                    cou1=cou1+1
                    
                    for ind in range(0,len(c_n_f[part2[0]])):
                        if c_n_f[part2[0]][ind] not in last[part[0]]:
                            last[part[0]].append(c_n_f[part2[0]][ind])
                    
                    #last[part[0]]=c_n_f[part2[0]]
                else:
                    #print(rule)
                    recheck.append(rule)

            #print(rule," ",last[part[0]]," ",c_n_f[part2[0]])

'''
dib=0
for i in c_n_f.keys():
    dib=dib+len(c_n_f[i])
print(dib)
'''
'''
for rule in recheck:
    part=rule.split(' -> ')
    part2=part[1].split(' ')
    #print(rule)
    if part[0] in last.keys() and part2[0] in last.keys():
        cou1=cou1+1
        for ind in range(0,len(last[part2[0]])):
            if last[part2[0]][ind] not in last[part[0]]:
                last[part[0]].append(last[part2[0]][ind])
    else:
        #print(rule)
        cou1=cou1+1
        if part[0] in last.keys():
            last[part[0]]=[]
            last[part[0]].append(part2[0])

'''
che=0  

for rule in last.keys():
    che=che+len(last[rule])
    for i in range(0,len(last[rule])):
        if last[rule][i] in cnf.keys():
            if rule not in cnf[last[rule][i]]:
                #che=che+1
                cnf[last[rule][i]].append(rule)
            '''
            else:
                #cnf[last[rule][i]]=[]
                #che=che+1
                cnf[last[rule][i]].append(rule)
            '''
            
        else:
            cnf[last[rule][i]]=[]
            cnf[last[rule][i]].append(rule)
            
                
#print(che)
che=0 
for rule in last.keys(): 
    che=che+len(last[rule])
    if rule in c_n_f.keys():
        for i in range(0,len(last[rule])):
            if last[rule][i] not in c_n_f[rule]:
                c_n_f[rule].append(last[rule][i])
    else:
        c_n_f[rule]=[]
        
        for ind in range(0,len(last[rule])):
            c_n_f[rule].append(last[rule][ind])
        #print(c_n_f[rule]," ",rule)
'''
grammar = nltk.data.load("grammars/large_grammars/atis.cfg")    
grammer=nltk.CFG.binarize(grammar,padding='$')
gr=nltk.CFG.remove_unitary_rules(grammer)
'''
dib=0
for i in c_n_f.keys():
    dib=dib+len(c_n_f[i])
print("Total CFG RULE -------------------> ",tol)
print("Total CNF RULE -------------------> ",dib)


'''
d=0   
cn_f={}
for prod in cnf.keys():
    for i in range(0,len(cnf[prod])):
        if(cnf[prod][i] in cn_f.keys()):
            cn_f[cnf[prod][i]].append(prod)
            d=d+1
        else:
            cn_f[cnf[prod][i]]=[]
            cn_f[cnf[prod][i]].append(prod)
            d=d+1
            
            
            
            1 2 3 4
            1 2 3 4
            1 2 3 4
            1 2 3 4
'''
  
fp.close() 
cnf={}
#c_n_f={}
path56='grammar_cnf.txt'
fp56 = codecs.open(path56,"w",encoding='utf-8', errors='ignore')
fp56.write(str(cnf_gr))
fp56.close()
path56='grammar_cnf.txt'
fp56 = codecs.open(path56,"r",encoding='utf-8', errors='ignore')
text=fp56.read()
production12=text.split('\n')
cfg56=[]
docu=""
for rule in range(1,len(production12)):
    #print(rule)
    cfg56.append(production12[rule].strip())
    docu=docu+production12[rule].strip()+"\n"
count_chai=0
tol1=0
letcheck=[]
for rule in cfg56:
    tol1=tol1+1
    rule=rule.strip()
    part=rule.split(' -> ')
    part2=part[1].split(' ')
    #print(part)
    #if (len(part2)==1):
    if(part[1] not in cnf.keys()):
            count_chai+=1
            tol1=tol1+1
            if part[1] not in letcheck:
                letcheck.append(part[1])
            #print(part[1],end=" | ")
            cnf[part[1]]=[]
            cnf[part[1]].append(part[0])
    else:
            #if(len(part[1])==1):
            #    count_chai+=1
            #print(rule)
            tol1=tol1+1
            if part[0] not in cnf[part[1]]:
                #print(rule)
                cnf[part[1]].append(part[0])
            #cnf[part[1]].append(part[0])

'''
dib=0
for i in cnf.keys():
    dib=dib+len(cnf[i])
print("Total CFG RULE -------------------> ",tol)
print("Total CNF RULE -------------------> ",dib)
'''





####################################################_CKY_PARSER_##################################################### 
   
sen = nltk.data.load("grammars/large_grammars/atis_sentences.txt", "raw") 
path1='sentence.txt'
sen_wp=[]
fp1 = codecs.open(path1,"r",encoding='utf-8', errors='ignore')
text=fp1.read()
production=text.split('\\n')
sen_t=[]
actua=[]
for part in production:
    s=''
    corec=""
    index=0
    sen_wp.append(part)
    for ind in range(0,len(part)):
        
        if(part[ind]==':'):
            index=ind+1
            actua.append(corec)
            break
        corec=corec+part[ind]
    while(index<len(part)):
        if(part[index]!="'"):
            s=s+part[index]
        else:
            #s=s+'"\'"'+part[index]
            s=s+"\'"
        index=index+1
    if(len(s)>1):
        sen_t.append(s.strip())
            
#sent = nltk.parse.util.extract_test_sentences(sen)
        
def parse_tree(matrix,i,j):
    a=0
    #print(i," ",j,end=" --->\n")
    for k in range(i,j):
       #print(i," ",k," ",k+1,j)
       
       a=a+parse_tree(matrix,i,k)*parse_tree(matrix,k+1,j)
    #print()
    return a
    

def CKY_Parser(sentence):
    
    part=sentence.split(' ')
    length=len(part)
    target=""
    #print(part)
    for i in range(0,length):
        if "'" in part[i]:
           target=target+' "'+part[i]+'"' 
           #target=target+" '"+part[i]+"'"
        else:
            target=target+" '"+part[i]+"'"
    #print(target," ",length)
    part2=target.strip().split(' ')
    #part2[1]='"\'d"'
    #print(part2)
    for word in part2:
        if word not in cnf.keys():
            print("Some words are out of Vocabulary",end=" ")
            #print(word,end=" ")
            return
    matrix=[]
    for i in range(0,length):
        a=[]
        for j in range(0,length):
            a.append({})
        matrix.append(a)
    
    for i in range(0,len(part)):
        for j in range(i,i+1):#len(part)):
            for k in cnf[part2[i]]:
                #matrix[i][j].append(k)
                #matrix[i][j]
                matrix[i][j][k]=1.0
    #for i in range(1,len(part)):
    #print("Comp")
    
    for i in range(1,len(part)):#len(part)):
        for j in range(0,len(part)-i):#len(part)):#len(part)):
            arrlist={}
            for k in range(j,i+j):
                
                for st in matrix[j][k]:
                    for st1 in matrix[k+1][j+i]:
                        #print(matrix[k+1][j+i])
                        point=st+" "+st1
                        #print(point)
                        if point in cnf.keys():
                            generate=cnf[point]
                            for ru in generate:
                                if ru not in arrlist.keys():
                                    arrlist[ru]=(1.0* int(matrix[j][k][st])*int(matrix[k+1][j+i][st1]))
                                    #arrlist[ru].append(point)
                                else:
                                    arrlist[ru]=arrlist[ru]+int(matrix[j][k][st])*int(matrix[k+1][j+i][st1])
                       
            matrix[j][j+i]=arrlist
    
    
                
            '''  
            #print(" ---> ",j," ",i+j)
            #########################
            if(i+j>=5):#len(part)):
                break
            arrlist=[]
            for k in range(i,j+j):
                print(i," ",k,end=" ---- ")
                print(k+1," ",i+j,end=" ---- ")
                print(i," ",j+i)
                print()
                
                for st in matrix[i][k]:
                    for st1 in matrix[k+1][j+i]:
                        point=st+" "+st1
                        if point not in arrlist:
                            arrlist.append(point)
                       
            matrix[i][j]=arrlist
        print()
        
    '''
    '''          
    for i in range(0,len(part2)):
        print(matrix[i])
        print()
    '''
    if 'SIGMA' in matrix[0][len(part2)-1].keys():
        tol_parse_tree=matrix[0][len(part2)-1]['SIGMA']
    else:
        tol_parse_tree=0
    print("Total number of parse tree is ",tol_parse_tree,end=" -----> ")
def CKY_Parser_tree(sentence):
    
    part=sentence.split(' ')
    length=len(part)
    target=""
    #print(part)
    for i in range(0,length):
        if "'" in part[i]:
           target=target+' "'+part[i]+'"' 
           #target=target+" '"+part[i]+"'"
        else:
            target=target+" '"+part[i]+"'"
    #print(target," ",length)
    part2=target.strip().split(' ')
    #part2[1]='"\'d"'
    #print(part2)
    for word in part2:
        if word not in cnf.keys():
            print("Some words are out of Vocabulary",end=" ")
            #print(word,end=" ")
            return
    matrix=[]
    for i in range(0,length):
        a=[]
        for j in range(0,length):
            a.append({})
        matrix.append(a)
    
    for i in range(0,len(part)):
        for j in range(i,i+1):#len(part)):
            for k in cnf[part2[i]]:
                #matrix[i][j].append(k)
                #matrix[i][j]
                matrix[i][j][k]=[]
                matrix[i][j][k].append(1.0)
                tree=Tree(k,[part2[i]])
                matrix[i][j][k].append(tree)
    #for i in range(1,len(part)):
    #print("Comp")
    
    for i in range(1,len(part)):#len(part)):
        for j in range(0,len(part)-i):#len(part)):#len(part)):
            arrlist={}
            for k in range(j,i+j):
                
                for st in matrix[j][k]:
                    for st1 in matrix[k+1][j+i]:
                        #print(matrix[k+1][j+i])
                        point=st+" "+st1
                        #print(point)
                        if point in cnf.keys():
                            generate=cnf[point]
                            for ru in generate:
                                if ru not in arrlist.keys():
                                    arrlist[ru]=[]
                                    arrlist[ru].append(1.0* int(matrix[j][k][st][0])*int(matrix[k+1][j+i][st1][0]))
                                    
                                    for each in range(1,len(matrix[j][k][st])):
                                        child=matrix[j][k][st][each]
                                        for each1 in range(1,len(matrix[k+1][j+i][st1])):
                                            child1=matrix[k+1][j+i][st1][each1]
                                            tree=Tree(ru,[child,child1])
                                            arrlist[ru].append(tree)
                                    #arrlist[ru].append(point)
                                else:
                                    arrlist[ru][0]=arrlist[ru][0]+int(matrix[j][k][st][0])*int(matrix[k+1][j+i][st1][0])
                                    for each in range(1,len(matrix[j][k][st])):
                                        child=matrix[j][k][st][each]
                                        for each1 in range(1,len(matrix[k+1][j+i][st1])):
                                            child1=matrix[k+1][j+i][st1][each1]
                                            tree=Tree(ru,[child,child1])
                                            arrlist[ru].append(tree)
                                    if point not in arrlist[ru]:
                                        #arrlist[ru].append(point)
                                        point
                                    #arrlist.append(dic)
                                    #print(arrlist)
                        #else:
                        #    print(j," ",k," ",i+j)
                #print(j," ",k," ||| ",k+1,"  ",i+j," ||| ",end=" ")
                       
            matrix[j][j+i]=arrlist
    
    
                
            '''  
            #print(" ---> ",j," ",i+j)
            #########################
            if(i+j>=5):#len(part)):
                break
            arrlist=[]
            for k in range(i,j+j):
                print(i," ",k,end=" ---- ")
                print(k+1," ",i+j,end=" ---- ")
                print(i," ",j+i)
                print()
                
                for st in matrix[i][k]:
                    for st1 in matrix[k+1][j+i]:
                        point=st+" "+st1
                        if point not in arrlist:
                            arrlist.append(point)
                       
            matrix[i][j]=arrlist
        print()
        
    '''
    '''          
    for i in range(0,len(part2)):
        print(matrix[i])
        print()
    '''
    
        
    #################################_BACK_TRACK_############################################################
    if 'SIGMA' in matrix[0][len(part2)-1].keys():
        tol_parse_tree=matrix[0][len(part2)-1]['SIGMA'][0]
    else:
        tol_parse_tree=0
    print("Total number of parse tree is ",tol_parse_tree,end=" -----> ")
    #print()
    #print()
    for i in range(1,int(tol_parse_tree+1)):
        print()
        print()
        matrix[0][len(part2)-1]['SIGMA'][i].pretty_print()
        matrix[0][len(part2)-1]['SIGMA'][i].draw()
    #print(matrix[0][len(part2)-1]['SIGMA'])
    #matrix[0][len(part2)-1]['SIGMA'][1].draw()
    
        
        
    
sentence1="what are the costs ." 
cind=0
for sentence1 in sen_t:
    print(sentence1)
    CKY_Parser(sentence1)
    print(actua[cind])
    cind=cind+1     
sentence1="what are the costs ." 
print()
print("---------------------------------------------------------------------------------------------------------")
print()
print(sentence1)
print()
print("Following are pasrse tree--------------------------------------------------------------------------------")
CKY_Parser_tree(sentence1)
fp1.close()



                

