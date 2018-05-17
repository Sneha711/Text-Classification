from nltk.corpus import brown
# from itertools import groupby
import collections
import math
import random

def TrainMultinomialNB(train):
#V Extract Vocabulary
	for i in train:
		v=brown.words(fileids=i)
	# print v
	vsort=sorted(set(v))
	print vsort
	#Count docs
	count=len(train)
	# for j in brown.fileids():
	
	#Count docs in each class
	# out=0
	countd=[]
	dicti={}
	condprob=collections.defaultdict(dict)
	for i in brown.categories():
		# if i=="adventure":
		gho=0
		print "Hey1"
		for j in brown.fileids(categories=i):
			if j in train:
				gho=gho+1  #Nc = Number of documents in each class
		countd.append(gho)

		# out=out+1
		prior[i]=float(gho/(1.0*count))
		textc=[]
		for t in brown.fileids(categories=i):
			if t in train:
				tp=brown.words(fileids=t)
				for ko in tp:
					textc.append(ko)
		# print textc
		for j in vsort:
			# print "Hey2"			
			freq=0
			for k in textc:
				if j==k:
					freq=freq+1 #Tct
			dicti[j]=freq
			tot=0
		for t in range(len(dicti)):
			tot=tot+dicti[j]
		for t in vsort:
			condprob[t][i]=float((dicti[t]+1)/(1.0*tot))

	return v,prior,condprob

			# print dicti[j]
			# print dicti		



	# print countd
def ApplyMultinomialNB(v,prior,condprob,test):
	
	score_fin=[]
	for x in test:
		bhabs=[]
		yo=brown.words(fileids=x)
		for j in yo:
			bhabs.append(j)
		score=[]
		for c in brown.categories():
			score[c]=math.log(prior[c])
			for i in bhabs:
				score[c]+=math.log(condprob[i][c])
		k=max(score.iteritems(),key=operator.itemgetter(1))[0]
		score_fin.append(k)
	return score_fin

def trainandtest(docs,testratio,trainratio): 
	trainlen=trainratio*len(docs)
	testlen=testratio*len(docs)
	trainset=[]
	testset=[]
	copy=list(docs)
	indextr=[]
	indexte=[]
	while trainlen>len(trainset):
		index=random.randrange(len(copy))
		indextr.append(index)
		trainset.append(copy.pop(index))
		o=random.randrange(len(copy))
		if o in indextr:
			pass
		else:
			testset.append(copy.pop(o))
	return testset,trainset


def accuracy(test,score_fin):	
	p=0
	correct=0
	for x in test:
		s=brown.categories(fileids==x)[0]
		s=s.encode('utf8')
		if s==score_fin[p]:
			correct+=1
		p=p+1
	return float(correct/(1.0*len(test))*100.0

# dop=[]
# dop=brown.fileids()
# testratio=0.8
# testratio=0.2
# test,train=trainandtest(d,testratio,testratio)
# v,prior,condprob=TrainMultinomialNB(train)
# score=[]
# score=ApplyMultinomialNB(v,prior,condprob,test):
# acc=accuracy(test,score)
# print('Accuracy:{0}').format(acc)
print "Hey"
