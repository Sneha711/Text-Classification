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
fil_brownie=list(fil_brown)

print "Filtered ",len(fil_brownie)  #34245
listWords = ["" for x in range(34)]
# listWords=[]
tfidf=[0.0]*34
# for i in range(len(fil_brown)):
for i in range(34):
	listWords[i]=fil_brownie[i]
	tfidf[i]=0.0

# print len(fil_brown_tfidf)
# print fil_brown_tfidf


weight1=np.random.uniform(low=0.0,high=0.0,size=(34,17))
weight2=np.random.uniform(low=0.0,high=0.0,size=(17,17))
weight3=np.random.uniform(low=0.0,high=0.0,size=(17,15))

# print np.matrix(weight1)
for i in range(34):
	for j in range(17):
		weight1[i,j]=float(1/(1.0*34))
for i in range(17):
	for j in range(17):
		weight2[i,j]=float(1/(1.0*17))
for i in range(17):
	for j in range(15):
		weight3[i,j]=float(1/(1.0*17))
classes = ["" for x in range(len(brown.categories()))]
count=0
for i in brown.categories():
	classes[count]=i
	count+=1

print classes
output1=[0.0]*17
output2=[0.0]*17
output3=[0.0]*15
error1=[0.0]*17
error2=[0.0]*17
error3=[0.0]*15
index=-1
for f in brown.fileids():
	print "Fileids ",f
	if(f=="ca34"):
	 	break
	actualCat=brown.categories(fileids=f)
	for cou in range(15):
		if(actualCat==classes[cou]):
			index=cou
	count=0
	print "1, ",f
	for w in listWords:
		if w in brown.words(fileids=f):
			print "Hey1"
			tf=(float)(brown.words(fileids=f).count(w)) / (float)(len(brown.words(fileids=f)))
			p=0
			for blob in brown.fileids():
				if w in blob:
					p+=1
			idf=math.log(len(brown.fileids()) / (1 + p))	
			tfidf[count]=tf * idf
			print "hey2"
		count+=1
	print "2, ",f
	for i in range(17):
		for j in range(34):
			d=float(tfidf[j])
			output1[i]=output1[i]+weight1[j,i]*d
		output1[i]=1/(1+math.exp(-1*output1[i]))
	print "3, ",f
	for i in range(17):
		for j in range(17):
			d=float(output1[j])
			output2[i]=output2[i]+weight2[j,i]*d
		output2[i]=1/(1+math.exp(-1*output2[i]))		
	print "4, ",f
	for i in range(15):
		for j in range(17):
			d=float(output2[j])
			output3[i]=output3[i]+weight3[j,i]*d
		output3[i]=1/(1+math.exp(-1*output3[i]))	
	print "5, ",f
	for i in range(15):
		if(i==index):
			error3[i]=abs(output3[i]*(1-output3[i])*(1-output3[i]))
		else:
			error3[i]=abs(output3[i]*(1-output3[i])*(output3[i]-0))
	print "6, ",f
	for i in range(17):
		sum=0.0
		for j in range(15):
			sum=sum+weight3[i,j]*error3[j]
		error2[i]=output2[i]*(1-output2[i])*sum
	print "7, ",f
	for i in range(17):
		sum=0.0
		for j in range(17):
			sum=sum+weight2[i,j]*error2[j]
		error1[i]=output1[i]*(1-output1[i])*sum
	print "8, ",f
	for i in range(34):
		for j in range(17):
			weight1[i,j]=weight1[i,j]+lr*(error1[j]*output1[j])
	print "9, ",f
	for i in range(17):
		for j in range(17):
			weight2[i,j]=weight2[i,j]+lr*(error2[j]*output2[j])
	
	print "10, ",f
	for i in range(17):
		for j in range(15):
			weight3[i,j]=weight3[i,j]+lr*(error3[j]*output3[j])


					










