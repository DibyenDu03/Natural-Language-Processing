import os
import codecs
import string
import os
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import pickle
import math
from collections import OrderedDict
import sys


def read(file):
	fp = codecs.open(file,"r",encoding='utf-8', errors='ignore')
	#fp=open(file)
	text = fp.read()
	return text

def skip_header(file):
	text=file.split('\n\n')
	final=""
	for i in range(1,len(text)):
		final=final+text[i]
	return final
def remove_stop(file):
	stop_words = set(stopwords.words('english')) 
	words=file.split(" ")
	text=""
	for r in words: 
		if not r in stop_words:
			text=text+r+" "
	return text 

def preprocess(doc):
	text=""
	new_file=doc.split('\n')
	file1=""
	for i in range(0,len(new_file)):
		file1=file1+" "+new_file[i]
	file1=file1.lower()
	mod_file=file1.split('\t')
	file=""
	for i in range(0,len(mod_file)):
		file=file+mod_file[i]+" "
	#file=remove_stop(file)
	for i in file:
		if (i>='a' and i<='z') or (i>='0' and i<='9') or (i==' ') or (i=="'") or (i==" "):
			text=text+i
		else:
			text=text+" "
		'''else:
			if (i=='?') or (i=='!') or (i=='.') or (i==','):
				text=text+i
			else:
				text=text+" "'''
	#print text
	text_doc=text.split(" ")
	process_text=""
	#print text_doc
	for i in text_doc:
#		print i
		if (len(i)>1):
			flag=1
			for r in i:
				if (r>='0' and r<='9'):
					flag=0
			if(flag==1):
				process_text=process_text+i+" "
	#print process_text
	process_text=remove_stop(process_text)
	return process_text


def loadData(): 
    choice=input("Enter\n\t 1) 2 Classes\n\t2) 20 classes\n\t")
    if(choice==1):
    	dbfile = open('examplePickle', 'rb') 
    else:
	dbfile = open('examplePicklefull', 'rb')  

    # for reading also binary mode is important 
        
    db = pickle.load(dbfile) 
    #print db['document']
    lis=[]
    for keys in db['document'].keys():
	lis.append(keys)
    #print db['word_list']
    count=len(db['word_list'])
    choice=input("Enter\n\t 1) for file input\n\t2) for sentence input\n\t")
    if(choice==1):
    	file1=raw_input("Enter the file name ")
	#print file1
    	text=read(file1)
    else:
	text=raw_input("Enter the sentence ")
	
    work=preprocess(text)
    #print work
    check=work.split(' ')
    flag=0
    word_list={}
    tol=0.0
    log={}
    log['sci.med']=0.0
    log['rec.autos']=0.0
    log['sci.electronics']=0.0
    log['misc.forsale']=0.0
    log['comp.windows.x']=0.0
    log['rec.sport.baseball']=0.0
    log['sci.crypt']=0.0
    log['rec.motorcycles']=0.0
    log['comp.os.ms-windows.misc']=0.0
    log['comp.graphics']=0.0
    log['talk.politics.mideast']=0.0
    log['rec.sport.hockey']=0.0
    log['soc.religion.christian']=0.0
    log['sci.space']=0.0
    log['comp.sys.ibm.pc.hardware']=0.0
    log['talk.religion.misc']=0.0
    log['comp.sys.mac.hardware']=0.0
    log['alt.atheism']=0.0
    log['talk.politics.misc']=0.0
    log['talk.politics.guns']=0.0
    for i in db['document'].keys():
	tol=tol+db['document'][i][0]
    for i in db['document'].keys():
	log[i]=math.log(db['document'][i][0]/tol)
    #print tol
    for i in check:
		if not i in word_list.keys() and len(i)>1:
			word_list[i]=[1.0,0.0]
			if not i in db['word_list'].keys():
				#print i," >",
				flag=1
				word_list[i][1]=1
		else:
			if len(i)>1:
				word_list[i][0]=word_list[i][0]+1


    k=5

    if flag==0:
	for i in word_list.keys():
		#print i," -->",db['word_list'][i][0]," ",db['word_list'][i][1]
		for j in db['document'].keys():
			log[j]=log[j]+ math.log((db['word_list'][i][j]+k)/(count+ db['document'][j][1]*k ) )*word_list[i][0]
    else:
	for i in word_list.keys():
		if word_list[i][1]==0:
			#print i," -->",
			#print i," -->",db['word_list'][i][0]," ",db['word_list'][i][1]
			for j in db['document'].keys():
				log[j]=log[j]+math.log((db['word_list'][i][j]+k)/(count+1+ db['document'][j][1]*k ) )*word_list[i][0]
			#print word_list[i][0]
		else:
			#print i," --XXXXX>",
			for j in db['document'].keys():
				log[j]=log[j]+math.log((k+0)/(count+1+ db['document'][j][1]*k ) )*word_list[i][0]
    max=-sys.maxsize
    class1=""
    for i in log.keys():
	if(log[i]!=0):
		print i," ------> ",log[i]
        if(max<log[i] and log[i]!=0):
		max=log[i]
    		class1=i
    print class1," have highest log(probability) value ",max

'''
    for i in db['word_list'].keys():
	print i,"---->",
	for j in range(0,20):
		print math.log((db['word_list'][i][j]+1)/(count+1+db['document'][lis[j]][1]))," ",
		#print db['word_list'][i][j]
		#print db['document'][list[j]][1],
		print db['word_list'][i][j]," --- ",
	print '\n'
'''
   
'''
    for keys in db: 
        print(keys," ---> ",db[keys])
    dbfile.close()
'''
loadData()
