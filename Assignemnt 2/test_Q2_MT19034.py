import os
import codecs
import string
import os
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import pickle
import math

line=10
choice=input(' Enter 1) for class1 and 2) for class2 ')
if choice==1:
	dbfile = open('Q2taskws6', 'rb')
else:
	dbfile = open('Q2taskws5', 'rb')

db = pickle.load(dbfile) 
#print db['uni']
##unigram
def unigram():
	sentence=""
	limit=[]
	for j in range(0,line):
		max=0
		key=''
		for k in db['uni'].keys():
			if(max<db['uni'][k] and (k not in limit) and len(k)>0 and k!='<S>' and k!='<E>'):
				max=db['uni'][k]
				key=k
		#limit=max
		limit.append(key)
		sentence=sentence+" "+key
	add_one('<S> '+sentence.strip()+' <E>')
	return '<S> '+sentence.strip()+' <E>'


## Bigram
def bigram():
	max=0
	sen=""
	list=[]
	last=""
	for k in db['bi'].keys():
		l=k.split('_')
		if(l[0]=='<S>'):
			if(max<db['bi'][k] and len(l[1])>0):
				max=db['bi'][k]
				sen=l[0]+" "+l[1]
				last=l[1]
	for i in range(0,line):
		max=0
		sen1=""
		key=""
		s=''
		for k in db['bi'].keys():
			l=k.split('_')
			if(l[0]==last and max<db['bi'][k] and k not in list and l[1]!='<E>'):
				max=db['bi'][k]
				sen1=l[1]
				key=k
				s=l[1]
		if(max==-1):
			for k in db['bi'].keys():
				l=k.split('_')
				if(l[0]!='<S>' and l[1]!='<E>'):
					if(max<db['bi'][k] and len(l[1])>0 and k not in list):
						max=db['bi'][k]
						sen1=l[0]+" "+l[1]
						key=k
						s=l[1]
		last=s
		#print sen1
		sen=sen+" "+sen1
		list.append(key)
	add_one(sen+' <E>')
	return sen+' <E>'

## Trigram
def trigram():
	max=0
	sen_tri=""
	list1=[]
	key1=""
	for k in db['tri'].keys():
		l=k.split('_')
		if(l[0]=='<S>'):
			if(max<db['tri'][k] and len(l[1])>0 and len(l[2])>0):
				max=db['tri'][k]
				sen_tri=l[0]+" "+l[1]+" "+l[2]
				key1=l[1]+"_"+l[2]
	for i in range(0,line):
		max=0
		s=key1.split('_')
		key=""
		sen1=""
		for k in db['tri'].keys():
			l=k.split('_')
			if(l[0]+"_"+l[1]==key1 and max<db['tri'][k] and k not in list1 and len(l[1])>0 and (len(l[2])>0)):
				max=db['tri'][k]
				sen1=l[2]

		sen_tri=sen_tri+" "+sen1
		list1.append((key1+"_"+sen1))
		key1=s[1]+"_"+sen1
		
	add_one(sen_tri.strip())
	return sen_tri.strip()
def add_one(text):
	words=text.split(' ')
	log_uni=0.0
	v=len(db['uni'])
	tol=0.0
	per_u=1.0
	uni=[]
	for i in db['uni'].keys():
		tol=tol+db['uni'][i] 
	for i in words:
		if i in db['uni'].keys():
			if i not in uni:
				uni.append(i)
			log_uni=log_uni+math.log((db['uni'][i]+1)/(v+tol))
			per_u=per_u*(db['uni'][i]+1)/(v+tol)
			#print i," -> ",( db['uni'][i]+1 )/( v+tol )," ",
			#print i," -> ",db['uni'][i]+1," ",
	print "\nunigram add_one value- ",log_uni," perflexity ",pow((1/per_u),(1.0/(len(uni)-2)))

	log_bi=0.0
	per_b=1.0
	tol=0.0
	#print len(words)
	i=0
	bi=[]
	#v=len(db['bi'])
	while i<(len(words)-1):
		key=words[i]+"_"+words[i+1]
		#print i
		if key in db['bi'].keys():
			if key not in bi:
				bi.append(key)
			log_bi=log_bi+math.log((db['bi'][key]+1)/(v+db['uni'][words[i]]))
			per_b=per_b*(db['bi'][key]+1)/(v+db['uni'][words[i]])
#			print key," -> ",( db['bi'][key]+1 )/( v+db['uni'][words[i]] )," ",
			#print key," -> ",db['bi'][key]," ",
		i=i+1
	print "Bigram add_one value- ",log_bi," perflexity ",pow((1/per_b),(1.0/(len(uni)-2)))

	log_tri=0.0
	per_t=1.0
	tol=0.0
	tri=[]
	#print len(words)
	i=0
	#v=len(db['tri'])
	while i<(len(words)-2):
		key=words[i]+"_"+words[i+1]+"_"+words[i+2]
		#print i
		k=words[i]+"_"+words[i+1]
		if key in db['tri'].keys():
			if key not in tri:
				tri.append(key)
			#print key
			log_tri=log_tri+math.log((db['tri'][key]+1)/(v+db['bi'][k]))
			per_t=per_t*(db['tri'][key]+1)/(v+db['bi'][k])
			#print key," ->",( db['tri'][key]+1 )/( v+db['bi'][k] )," ",
			#print key," ->",db['tri'][key]," ",
		i=i+1
	print "Trgram add_one value- ",log_tri," perflexity ",pow((1/per_t),(1.0/(len(uni)-2)))

def good_turning(text):

	log_uni=0.0
	log_bi=0.0
	log_tri=0.0
	words=text.split(' ')
	#### Unigram
	tol=0.0
	for i in db['uni'].keys():
		tol=tol+db['uni'][i] 
	count=0
	for i in words:
		
		if i in db['uni'].keys() and i!='<S>' and i!='<E>':
				count=db['uni'][i]
				#print db['uni'][i]," ",i,"  --->"
				one=0.0
				same=0.0
				for k in db['uni'].keys():
					if(db['uni'][k]==count):
						same=same+1
					if(db['uni'][k]==count+1):
						one=one+1
				if((one*(count+1) )/(tol*same)!=0):
					log_uni=log_uni+math.log( (one*(count+1) )/(tol*same))
				#print (one*(count+1) )/(tol*same)," ",one," ",count," ",same
	print " Log probability using good turning(unigram) is ",log_uni
	
	### Bigram
	
	count=0
	log_bi=0.0
	for j in range(0,len(words)-1):
		i=words[j]+"_"+words[j+1]
		#print i
		if i in db['bi'].keys():
				count=db['bi'][i]
				#print db['uni'][i]," ",i,"  --->"
				one=0.0
				same=0.0
				for k in db['bi'].keys():
					if(db['bi'][k]==count):
						same=same+1
					if(db['bi'][k]==count+1):
						one=one+1
				if((one*(count+1) )/(tol*same)!=0):
					log_bi=log_bi+math.log( (one*(count+1) )/(tol*same))
				#print (one*(count+1) )/(tol*same)," ",one," ",count," ",same
	print " Log probability using good turning(bigram) is ",log_bi
	
	### Trigram
	
	count=0
	log_tri=0.0
	for j in range(0,len(words)-2):
		i=words[j]+"_"+words[j+1]+"_"+words[j+2]
		#print i
		if i in db['tri'].keys():
				count=db['tri'][i]
				#print db['uni'][i]," ",i,"  --->"
				one=0.0
				same=0.0
				for k in db['tri'].keys():
					if(db['tri'][k]==count):
						same=same+1
					if(db['tri'][k]==count+1):
						one=one+1
				if((one*(count+1) )/(tol*same)!=0):
					log_tri=log_tri+math.log( (one*(count+1) )/(tol*same))
				#print (one*(count+1) )/(tol*same)," ",one," ",count," ",same
	print " Log probability using good turning(Trigram) is ",log_tri
		

text=unigram()
text1=bigram()
text2=trigram()
print()
print text
print text1
print text2
add_one(text)
sen=raw_input('Enter the sentence ')
sen='<S> '+sen.lower()+' <E>'
add_one(sen)
good_turning(sen)				
