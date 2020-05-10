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




path = 'test23/'
#path ='/home/dibyendu/Desktop/20news-19997/20_newsgroups/'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
	for file in f:
		files.append(os.path.join(r, file))




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



dic1=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
#print len(files)
doc=OrderedDict()
word_list={}
tol=-1
tol1=tol+1
for i in files:
	text=read(i)
	name=i.split('/')
	#string1=str(tol+1)+" "+name[1]
	#print string1," ",tol
	if not name[1] in doc.keys():
		#string=str(tol+2)+name[1]
		tol=tol+1 
		doc[name[1]]=[1.0,0.0]
		#print name[1]
	else:
		doc[name[1]][0]=doc[name[1]][0]+1
			# if '.txt' in file:
	skip_text=skip_header(text)
	work=preprocess(skip_text)
	check=work.split(" ")
	#print tol
	dic1[tol]=dic1[tol]+len(check)
	for i in check:
		if not i in word_list.keys() and len(i)>1:
			#word_list[i]=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
			word_list[i]={}
			word_list[i]['sci.med']=0.0
			word_list[i]['rec.autos']=0.0
			word_list[i]['sci.electronics']=0.0
			word_list[i]['misc.forsale']=0.0
			word_list[i]['comp.windows.x']=0.0
			word_list[i]['rec.sport.baseball']=0.0
			word_list[i]['sci.crypt']=0.0
			word_list[i]['rec.motorcycles']=0.0
			word_list[i]['comp.os.ms-windows.misc']=0.0
			word_list[i]['comp.graphics']=0.0
			word_list[i]['talk.politics.mideast']=0.0
			word_list[i]['rec.sport.hockey']=0.0
			word_list[i]['soc.religion.christian']=0.0
			word_list[i]['sci.space']=0.0
			word_list[i]['comp.sys.ibm.pc.hardware']=0.0
			word_list[i]['talk.religion.misc']=0.0
			word_list[i]['comp.sys.mac.hardware']=0.0
			word_list[i]['alt.atheism']=0.0
			word_list[i]['talk.politics.misc']=0.0
			word_list[i]['talk.politics.guns']=0.0
			word_list[i][name[1]]=1
		else:
			if len(i)>1:
				word_list[i][name[1]]=word_list[i][name[1]]+1
	'''
	for s in check:
		flag=1
		for j in range(0,len(dic)):
			if(dic[j]==s):
				flag=0
		if(flag==1):
			dic.append(s)
	#print i+" is done "

print(len(dic))
print dic
'''
#count=len(word_list)
#print word_list," ",len(word_list)
#print dic1," ",doc
count=0
for i in doc.keys():
	doc[i][1]=dic1[count]
	count=count+1
#print word_list
db={}
db['word_list']=word_list
#db['class']=dic1
db['document']=doc
dbfile = open('examplePicklefull', 'ab') 
pickle.dump(db, dbfile)                      
dbfile.close() 
print "complete"

'''
for i in word_list.keys():
	print i,"---->",
	for j in range(0,20):
		print math.log((word_list[i][j]+1)/(count+1+dic1[j]))," ",
		print word_list[i][j]," ",
	print '\n'
print dic1," ",len(word_list)
'''

'''
for i in doc.keys():
	print math.log(10,(doc[i]/len(files)))
'''
	
