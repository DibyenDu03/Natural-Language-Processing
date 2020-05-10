
import codecs
import string
import os
from nltk.tokenize import sent_tokenize



def read(file):
	fp = codecs.open(file,"r",encoding='utf-8', errors='ignore')
	#fp=open(file)
	text = fp.read()
	return text
	
def sentence(text):
	Sent=sent_tokenize(text)
	print "\n1) Total number of sentence is ",len(Sent)
	return Sent

def word_count(word):
	count=0
	conso=0
	vowel=0
	for i in word:
		i=i.strip()
		str=i.split(" ")
		for j in str:
			if len(j)>0 and (j[0]<='z' and j[0]>='a'):
				if(j[0]=='a' or j[0]=='i' or j[0]=='o' or j[0]=='u' or j[0]=='e'):
					vowel=vowel+1
				else:
					conso=conso+1
				
		count=count+len(str)
	print "   Total number of words is ",count
	print "\n2) Total number of word starting with consonant is ",conso," and vowel is ",vowel
	return count
			
def sent(word,word_name):
	countstart=0
	countend=0
	for i in word:
		i=i.strip()
		str=i.split(" ")
		if (len(str[0]) and (str[0]==word_name)):
			countstart=countstart+1
	print "\n4) NUmber sentence starting with ",word_name," is ",countstart

def sent_end(word,word_name):
	countstart=0
	countend=0
	for i in word:
		i=i.strip()
		str=i.split(" ")
		if (len(str)>0)  and (str[len(str)-1]==word_name or str[len(str)-1]==word_name+"." or str[len(str)-1]==word_name+"?" or str[len(str)-1]==word_name+"!" or str[len(str)-1]==word_name+","):
			countstart=countstart+1
			
	print "\n5) Number sentence end with ",word_name," is ",countstart
	

def sent_mid(word,word_name):
	countend=0
	for i in word:
		i=i.strip()
		str=i.split(" ")
		for j in range(0,len(str)):
			if (len(str)>0) and (str[j]==word_name or str[j]==word_name+"." or str[j]==word_name+"?" or str[j]==word_name+"!" or str[j]==word_name+","):
				countend=countend+1
	print "\n6) Occurence of the ",word_name," is ",countend
		
def email(word):
	count=0
	for i in word:
		i=i.strip()
		str=i.split(" ")
		for j in range(0,len(str)):
			file=str[j].strip()
			part=file.split("@")
			f=1
			if(len(part)==2):
				if(len(part[0])>0):
					if(part[0][0]>'z' or part[0][0]<'a') and (part[0][0]>'9' or part[0][0]<'0') and part[0][0]!='<' and part[0][0]!='-' and part[0][0]!=':':
						f=0
					fil=part[1].split(".")
					for i1 in fil:
						if(len(i1)==0):
							f=0
					if(f==1):
						#print part
						count=count+1
	print "\n3) Total number of email id ",count
						
				

					
		 


f =raw_input("Enter your file name (press enter for all files) ")
path=raw_input("Enter your file path (press enter for current directory) ")
f=path+"/"+f
text=read(f)
text=text.lower()
#print text
word=sentence(text)
#print word
word_count(word)
email(word)
word_name=raw_input("\n Enter the starting word ")
word_name=word_name.lower()
sent(word,word_name)
word_name=raw_input("\n Enter the ending word ")
word_name=word_name.lower()
sent_end(word,word_name)
word_name=raw_input("\n Enter the word ")
word_name=word_name.lower()
sent_mid(word,word_name)
