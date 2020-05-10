import codecs
import string
import os
from nltk.tokenize import sent_tokenize


# define function

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

def preprocess(file):
	text=""
	file=file.lower()
	for i in file:
		if (i>='a' and i<='z') or (i>='0' and i<='9') or (i==' ') or (i=='\n'):
			text=text+i
		else:
			if (i=='?') or (i=='!') or (i=='.') or (i==',') or (i=='"') or (i=="'"):
				text=text+i
			else:
				text=text+" "
	return text

# Main

f =raw_input("Enter your file name (including file path) ")
text=read(f)
skip_text=skip_header(text)
work=preprocess(skip_text)
print(work)
