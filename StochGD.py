from __future__ import division,unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('UTF8')
import numpy as np
import csv
import itertools
import math
from nltk.corpus import brown
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk import sent_tokenize
import string
from textblob import TextBlob as tb
from nltk.stem.wordnet import WordNetLemmatizer 
lem = WordNetLemmatizer()
from nltk.stem.porter import PorterStemmer 
stem = PorterStemmer()

# def tf(word, blob):
#     tf=(float)(brown.words(fileids=blob).count(word)) / (float)(len(brown.words(fileids=blob)))

# # def n_containing(word, bloblist):
# #     return sum(1 for blob in bloblist if word in blob)

# def idf(word, bloblist):
# 	p=sum(1 for blob in bloblist if word in blob)
#     return 
#     idf=math.log(len(bloblist) / (1 + p))

# def tfidfFunc(word, blob, bloblist):
#     return tf * idf

stop_words = set(stopwords.words('english'))
punctuations = list(string.punctuation)
lr=0.2

#fil contains all the filtered words of the brown corpus
fil_brown=[]
c1=0
c2=0
c3=0
lr=0.5
#####################
for i in brown.fileids():
	for j in brown.words(fileids=i):
		c1=c1+1

print "Original ",c1 #1161192


for doc in brown.fileids():
	for w in brown.words(fileids=doc):
		if w not in (stop_words and punctuations):
			w=w.lower()  #Lower case conversion
			w=w.strip() #removing blank spaces
			w=w.strip('*') #removing *
			w=w.strip('_') #removing _
			w=lem.lemmatize(w, "v") #lemmatizing
			w=stem.stem(w) #stemming
			fil_brown.append(w)

fil_brown=set(fil_brown)
fil_brown=list(fil_brown)

print "Filtered ",len(fil_brown)  #34245
listWords = ["" for x in range(34)]
# listWords=[]
# for i in range(len(fil_brown)):
for i in range(34):
	listWords[i]=fil_brown[i]

tfidf=np.random.uniform(low=0.0,high=0.0,size=(50,34)) #size number of documents , size of fil_brownie
param=np.random.uniform(low=0.0,high=0.0,size=(15,34)) #size of classes , size of fil_brownie

countDocs=-1
for f in brown.fileids():
	countWords=0
	countDocs=countDocs+1
	if(countDocs==50):
		break;
	for w in fil_brown:
		countWords+=1
		if(countWords==34):
			break;
		tf=(float)(brown.words(fileids=f).count(w)) / (float)(len(brown.words(fileids=f)))
		p=0
		for blob in brown.fileids():
			if w in blob:
				p+=1
		idf=math.log(len(brown.fileids()) / (1 + p))	
		tfidf[countDocs,countWords]=tf * idf

countDoc=-1
for i in brown.fileids():
	countDoc=countDoc+1
	if(countDoc==50):
		break
	
	sumDeno=0.0
	countClass=-1
	for j in brown.categories():
		countClass=countClass+1
		for k in range(len(listWords)):
			sumDeno=sumDeno+param[countClass,k]*tfidf[countDoc,k]
	countClass=-1		
	for j in brown.categories():
		countClass=countClass+1
		sumNum=0.0
		for k in range(len(listWords)):
			sumNum=sumNum+param[countClass,k]*tfidf[countDoc,k]
		prob=float(math.exp(sumNum)/(1.0*math.exp(sumDeno)))
		if(j==brown.categories(fileids=i)):
			for kp in range(len(listWords)):
				param[countClass,kp]=param[countClass,kp]-lr*(prob-1)*(tfidf[countDoc,kp])
		else:
			for kp in range(len(listWords)):
				param[countClass,kp]=param[countClass,kp]-lr*(prob-0)*(tfidf[countDoc,kp])

		
			



