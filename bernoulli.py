from nltk.corpus import brown, movie_reviews, reuters
import random
import math
import operator
import collections

#Function for separating the docs 
# def separate(c,C,D):
# 	docs_in_each_class=[]
# 	for x in C:
# 		if(x == c):
# 			for d in D:
# 				if(c == movie_reviews.categories(d)):
# 					docs_in_each_class.append(d)
# 	return docs_in_each_class



def TrainBernoulli(C,D):
		#print D 
		#print len(D)
		#voc=[]		#Contains vocabularies
		#voc=movie_reviews.words()
		#docs=[]		#Contains all docs irrespective of category
		#docs=movie_reviews.fileids()
		#C=[]
		#C=movie_review.categories()	#Contains all the categories
		
		V=[]	
		t=[]		#V is vocabulary
		for x in D:
			t = movie_reviews.words(fileids=x)
			for i in t:
				V.append(i)
		#print V
		V=list(set(V))			#Removing duplicate elements
		N=len(D)				#Count of docs
		prior={}
		condprob=collections.defaultdict(dict)
		# Nc=0
		countd={}
		shah=[]
		docs_in_each_class=[]
		for c in C:
			shah=movie_reviews.fileids(categories=c)
			t=0
			for k in shah:
				if k in D:
					t=t+1
					docs_in_each_class.append(k)
			countd[c]=t

		#print countd
		for c in C:
					# Nc=Nc+1
					# print Nc
			prior[c] = countd[c]/N
			#print prior[c]
			

		
			#Nc=len(movie_reviews.fileids(x))
			# docs_in_each_class=[]		#contains docs of category c
			# docs_in_each_class=movie_reviews.fileids(categories=c)


						
		# 	#print Nc
			
			#Nctl=[]
			for t in V:
				#condprob[t]={}
				Nct=0
				for d in docs_in_each_class:
					if t in movie_reviews.words(fileids=d):
						Nct=Nct+1
				print t , Nct
				#print Nct
				#Nctl.append(Nct)
				Nc=countd[c]
				condprob[t][c]=(Nct+1)/(Nc+2)
		return V,prior,condprob


def ApplyBernoulliNB(C,V,prior,condprob,d):
	score_fin = []
	for x in d:
		Vd = movie_reviews.words(fileids=x)
		score = {}
		for c in C:
			score[c] = math.log(prior[c])
			for t in V:
				if t in Vd:
					score[c]+=math.log(condprob[t][c])
				else:
					score[c]+=math.log(1-condprob[t][c])
		k=max(score.iteritems(),key=operator.itemgetter(1))[0]
		score_fin.append(k)
	return score_fin





#Function for splitting the data set
def splitDataset(docs,splitRatio_train,splitRatio_test,splitRatio_cross):
	trainSize = int(len(docs) * splitRatio_train)
	testSize =  int(len(docs) * splitRatio_test)
	trainSet = []
	testSet = []
	copy = list(docs)
	
	while len(trainSet) < trainSize:
		index = random.randrange(len(copy))
		trainSet.append(copy.pop(index))


	while len(testSet) < testSize:
		#print len(copy)
		index = random.randrange(len(copy))
		testSet.append(copy.pop(index))
	
	return [trainSet, testSet, copy]


#Function for calculating the accuracy
def getAccuracy(test, predictions):
	correct = 0
	p=0
	for x in test:
		#print "Hey1 ",movie_reviews.categories(fileids=x), type(movie_reviews.categories(fileids=x))
		#print "Hey2 ",predicitions,type(predictions)
		s=movie_reviews.categories(fileids=x)[0]
		s=s.encode('utf8')
		if  s == predictions[p]:
			correct += 1
		p=p+1
	return (correct/float(len(test))) * 100.0



#The calling code
voc=[]		#Contains vocabularies
voc=movie_reviews.words()

docs=[]		#Contains all docs irrespective of category
docs=movie_reviews.fileids()

C=[]
C=movie_reviews.categories() 		##Contains all the categories

#splitting the data set
splitRatio_train = 0.60
splitRatio_test = 0.20
splitRatio_cross = 0.20
train, test ,cross = splitDataset(docs,splitRatio_train,splitRatio_test,splitRatio_cross)

#Calling the TrainBernoulli function with the training data
V,prior,condprob = TrainBernoulli(C,train)

#Calling the ApplyBernoulliNB function
score=[]  #List that stores the predicted class labels of the test data
score=ApplyBernoulliNB(C,V,prior,condprob,test)


#Calculating the accuracy
acc=getAccuracy(test, score)
print('Accuracy: {0}').format(acc)









