# compare 2 sentences using 'word ordering' 

# vocab_obj = w2v.vocab["word"]
# vocab_obj.count

# combine 2 sentences into 1 set. 

## !!!!! NEED TO CONVERT SINGULAR INTO PLURAL ??? 
## !!!!! NEED TO CONVERT SINGULAR INTO PLURAL ??? 


#
import gensim 
import numpy as np
import re, copy 
import sklearn.metrics 

def infoContentOfWord (w1,model): 
	# print w1
	# return -1*np.log ( model.vocab[w1].count*1.0 / model.corpus_count )
	a = np.log(model.vocab[w1].count*1.0)
	b = np.log(model.corpus_count)
	return 1.0 - a/b 
	
def convert2bigram (s1,bigram): 
	return list ( bigram[s1] )
	
def convert2trigram (s1,trigram):
	return list ( trigram[s1] )

def removeGO (term): 
		return (re.sub("GO:","",term)) ## dont want GO:xyz, just need xyz 
		
def compute_jaccard_index(set_1, set_2):
	set_1 = set(set_1)
	set_2 = set(set_2)
	n = len(set_1.intersection(set_2))
	return n / float(len(set_1) + len(set_2) - n) 
		
def convertSen2SemSet (T1,T,model): # make the S1 set for the sentence T1 
	semvec = [] ## semantic set 
	T1 = list(set(T1)) ## enough to look at only unique elments 
	for t11 in T: ## each element in both sentences
		# print infoContentOfWord(t11,model)
		if t11 in T1: 
			semvec.append(infoContentOfWord(t11,model)**2) 
		else: 
			bestMatch = findWordBestMatch(T1,t11,model)
			maxWord = bestMatch[0]
			max = bestMatch[1]
			semvec.append(max * infoContentOfWord(maxWord,model) * infoContentOfWord(t11,model)) 
	return (semvec)

def findWordBestMatch(v1,w1,model): 
	wordArray = np.repeat(w1,len(v1),axis=0).tolist()
	ret = map(model.similarity,wordArray,v1)
	max = np.max(ret)
	maxWord = v1[np.where(ret==max)[0][0]]
	return [maxWord,max]
	
def findWordBestMatchWted(v1,w1,model): 
	if w1 in v1: 
		return [w1,1.0,infoContentOfWord(w1,model)**2]
	## not not the same word in the vector. then...	
	wordArray = np.repeat(w1,len(v1),axis=0).tolist()
	ret = np.array ( map(model.similarity,wordArray,v1) ) ## simple cosine distance (angle). NOT WEIGHTED 
	infoW1 = np.array ( map (lambda x: infoContentOfWord(x,model=model), wordArray) )
	infoV1 = np.array ( map (lambda x: infoContentOfWord(x,model=model), v1) )
	# infoV1 = infoV1 / np.sum(infoV1)
	pairWt = infoV1 * infoW1 ## WEIGHT OF THE BEST MATCHING PAIR 
	# ret = ret * pairWt ## similarity * word information 
	max = np.max(ret)
	maxIndx = np.where(ret==max)[0][0]
	maxWord = v1[maxIndx]
	maxInfo = pairWt[maxIndx]
	return [maxWord,max,maxInfo]

def convertSen2SemSet2 (T1,T,model): # make the S1 set for the sentence T1 
	semvec = [] ## semantic set 
	T1 = list(set(T1)) ## enough to look at only unique elments 
	for t11 in T: ## each element in both sentences
		if t11 in T1: ## if it is in T1, give a 1 times weights 
			semvec.append(infoContentOfWord(t11,model)**2) 
		else: ## word in T (the space to be projected on) not found in T1
			bestMatch = findWordBestMatch(T1,t11,model)
			maxWord = bestMatch[0]
			max = bestMatch[1]
			if max > 0.3: ## threshold 
				semvec.append(max * infoContentOfWord(maxWord,model) * infoContentOfWord(t11,model)) 
			else: 
				semvec.append(0) 
	return (semvec)
	
def convert2rankVec (T1,T,model): 
	rankvec = [] 
	for t11 in T: 
		if t11 in T1: 
			rankvec.append( T1.index(t11) + 1)
		else: 
			#rankvec.append( 0 ) ## too harsh ??
			max = -1 
			maxWord = ""
			for wInT1 in T1: 
				sim = model.similarity(t11, wInT1) ## each word in full set vs each word in sen1.
				if sim > max: 
					max = sim 
					maxWord = wInT1
			if max > 0.3: 
				rankvec.append(T1.index(maxWord)+1)
			else: 
				rankvec.append(0)
	return rankvec

def cosineSim (v1, v2): 
	v1 = np.array(v1)
	v2 = np.array(v2) 
	a = sklearn.metrics.pairwise.cosine_similarity(v1.reshape(1,-1), v2.reshape(1,-1))
	# 1 - scipy.spatial.distance.cosine(u, v) ## u, v are array  ??
	return a[0][0] ## array -> number ??

def distOf2RankVec (v1,v2): 
	v1 = np.array(v1)
	v2 = np.array(v2) 
	numer = np.linalg.norm(v1-v2)
	denom = np.linalg.norm(v1+v2)
	return 1 - numer/denom

def sim2Sentences (T1,T2,model): 
	T = T1+T2 
	# Tset = set(T) 
	# T = list(Tset) ## get unique elements 
	# print T
	S1 = convertSen2SemSet(T1,T,model) # semset 
	S2 = convertSen2SemSet(T2,T,model)	
	return cosineSim(S1,S2) 
	
def sim2SentencesHardThreshold (T1,T2,model): 
	T = T1+T2 
	# Tset = set(T) 
	# T = list(Tset) ## get unique elements 
	# print T
	S1 = convertSen2SemSet2(T1,T,model) # semset 
	S2 = convertSen2SemSet2(T2,T,model)	
	return cosineSim(S1,S2) 
	
def inAnotInB (v1,v2): 
	s1 = set(v1)
	s2 = set(v2)
	return list(s1.difference(s2))

# def sim2Sentences2 (T1,T2,model): 
	# fullsim = sim2Sentences(T1,T2,model)
	# s1 = inAnotInB (T1,T2) ## words only in sentence 1
	# if (len(s1)==0) | ( len(s1)==len(list(set(T1))) ) : ## if len 0 use the full sentence ?? what if sentences don't overlap 
		# return fullsim
	# s2 = inAnotInB (T2,T1)
	# if len(s2)==0: 
		# return fullsim	
	# return sim2Sentences (s1,s2,model)/fullsim 
	
# def sim2Sentences3 (T1,T2,model): 
	# s1 = inAnotInB (T1,T2) ## words only in sentence 1
	# s2 = inAnotInB (T2,T1)
	# return sim2Sentences (s1,s2,model)
	
def shiftBy1toRight (v1): 
	return v1.pop(0)

def matchOrdering (v1,v2,model): 
	if (len(v1)>len(v2)) : 
		v3 = v2 ## save a version of the shorter sentence (v2 at the moment)
		v2 = v1 ## v2 is the name of the longer sentence 
		v1 = v3 ## rename v1 as the shorter sentence 
	#####	
	stop = len(v2)-len(v1)
	max = -1 
	# matchIndicator = np.repeat(0,len(v1))
	# rank = np.linspace( 0,len(v1)-1,num=len(v1) )
	v2copy = copy.deepcopy(v2)
	for id in range(0,stop+1): ## move along setence 2 
		v2new = v2copy[0:len(v1)] ## only look same length as sentence 1
		# for wordid in range(0,len(v1)): 
			# if model.similarity(v2new[wordid],v1[wordid]) > 0.3: 
				# matchIndicator[wordid] = 1
		# print (v1)
		# print (v2new)
		T = v2new + v1 
		r1 = convert2rankVec(v1,T,model)
		r2 = convert2rankVec(v2new,T,model)
		max1 = distOf2RankVec (r1,r2)
		if max1 > max: 
			max = max1
		# v2copy = shiftBy1toRight(v2copy) ## move along the sentence 2 
		v2copy.pop(0)
		# print (v2copy)
	return max 
		
def softJaccard (v1,v2,model): 
	s1 = set(v1)
	s2 = set(v2) 
	# intersectU = len(s1.intersection(s2))
	intersectU = 0 ## nothing intersects at first
	wordsBestSimilar = [] 
	for s11 in s1: 
		for s22 in s2: 
			if model.similarity(s11,s22) > 0.3: ## over threshold, then count as intersection. same words will have dist=1 
				if (s11 not in wordsBestSimilar): 
					wordsBestSimilar.append(s11) 
				if (s22 not in wordsBestSimilar): 
					wordsBestSimilar.append(s22) 
	intersectU = len(wordsBestSimilar) 
	unionU = float(len(s1) + len(s2) - intersectU)
	return intersectU/unionU
			
def ctsJaccard2 (v1,v2,model): ## continuous scale jaccard  
	s1 = set(v1)
	s2 = set(v2) 
	intersectU = 0
	for s11 in s1: 
		unionU = float(len(s1) + len(s2) - intersectU)
	return intersectU/unionU	
	
def ctsJaccard (v1,v2,model): ## continuous scale jaccard  
	s1 = set(v1)
	s2 = set(v2) 
	intersectU = 0
	for s11 in s1: 
		for s22 in s2: 
			intersectU = intersectU + model.similarity(s11,s22) ## adding similarity directly into the numerator 
	unionU = float(len(s1) + len(s2) - intersectU)
	return intersectU/unionU	
		
def softJaccardWted (v1,v2,model): 
	# intersectU = len(s1.intersection(s2))
	intersectU = 0 ## nothing intersects at first 
	for s11 in v1: 
		for s22 in v2: 
			if model.similarity(s11,s22) > 0.3: ## over threshold, then count as intersection. same words will have dist=1 
				intersectU = intersectU + infoContentOfWord(s11,model) * infoContentOfWord(s22,model) 
	unionU = float(len(v1) + len(v2) - intersectU) ## will have problem !!! 
	return intersectU/unionU
	
def getInfoContent2vec (v1,v2,model):
	intersectU = 0 
	for v11 in v1: 
		for v22 in v2: 
			intersectU = intersectU + model.similarity(v11,v22)*infoContentOfWord(v11,model) * infoContentOfWord(v22,model)  
	return intersectU
	
def getSignificantInfoContent2vec (v1,v2,model):
	intersectU = 0 
	for v11 in v1: 
		for v22 in v2: 
			d = model.similarity(v11,v22)
			if d > 0.3: 
				# print [v11,v22]
				intersectU = intersectU + model.similarity(v11,v22)*infoContentOfWord(v11,model) * infoContentOfWord(v22,model)  
	return intersectU
	
def ctsJaccardWted (v1,v2,model): ## continuous scale jaccard 
	v1 = set(v1)
	v2 = set(v2) 
	intersectU = 0
	for s11 in v1: 
		for s22 in v2: 
			intersectU = intersectU + model.similarity(s11,s22)*infoContentOfWord(s11,model) * infoContentOfWord(s22,model)  ## adding similarity directly into the numerator 
	unionU = float(len(v1) + len(v2) - intersectU) ## has problem !!!!, it can be less than 1. 
	return intersectU/unionU	
	
def euclideanDistance (a,b): 
	return ( np.linalg.norm(a-b) ) 
	
def hausdorffDist (v1,v2,model): # TRADITIONAL EUCIDEAN DISTANCE 
	h = 0 
	for v11 in v1: 
		shortest = np.inf
		for v22 in v2: 
			d12 = euclideanDistance(model[v11],model[v22])
			if d12 < shortest: 
				shortest = d12 
		# print shortest
		if shortest > h: 
			h = shortest 
	return h 
	
def hausdorffDist2 (v1,v2,model): 
	worstOfBest = []
	for v11 in v1: 
		# shortest = np.inf
		worstOfBest.append( findWordBestMatch(v2,v11,model)[1] ) ## closest of v11 to sentence 2
		# print closestDist
	return np.min(worstOfBest)

def hausdorffDist2vec (v1,v2,model): 
	return np.min([hausdorffDist2 (v1,v2,model),hausdorffDist2 (v2,v1,model)])
	
def hausdorffDistMod1to2 (v1,v2,model): 
	# worstOfBest = 1 
	# ave = 0 
	# for v11 in v1: ## one word in vector 1. 
		# ave = ave + findWordBestMatch(v2,v11,model)[1] ## closest of v11 to sentence 2
	# ave = ave / len(v1) 
	ave = map(lambda x: findWordBestMatch(v2,x,model)[1], v1)	
	return np.average(ave)
	
def hausdorffDistMod1to2Wted (v1,v2,model): 
	# worstOfBest = 1 
	# ave = 0 
	# for v11 in v1: ## one word in vector 1. 
		# ave = ave + findWordBestMatch(v2,v11,model)[1] ## closest of v11 to sentence 2
	# ave = ave / len(v1) 
	v1tov2 = np.array ( map(lambda x: findWordBestMatchWted(v2,x,model)[1:3], v1)	)## each element of v1 to the whole v2
	''' 
	v1tov2 = each row is [best similarity score, weight of the pair]
	'''
	# print v1tov2
	# infoV1 = np.array ( map (lambda x: infoContentOfWord(x,model=model), v1) )
	# print infoV1
	return np.average(v1tov2[:,0],weights=v1tov2[:,1])

def hausdorffDistMod (v1,v2,model): ## USED ON SCALE: 1=CLOSEST 0=FARTHEST
	a = hausdorffDistMod1to2(v1,v2,model) 
	b = hausdorffDistMod1to2(v2,v1,model) ## hausdorffDist is not symmetric
	return np.min([a,b]) # take the worst of the directed hausdorffDist
	
def hausdorffDistModWted (v1,v2,model): ## USED ON SCALE: 1=CLOSEST 0=FARTHEST
	a = hausdorffDistMod1to2Wted(v1,v2,model) 
	b = hausdorffDistMod1to2Wted(v2,v1,model) ## hausdorffDist is not symmetric
	return np.min([a,b]) # take the worst of the directed hausdorffDist
	
	
# hausdorffDist2(s1,s2,model)	
# hausdorffDist2(s2,s1,model)
# hausdorffDist2(T2,T1,model)	
# hausdorffDist(s1,s2,model)
# hausdorffDist2(['cell','division'],['mitosis'],model)
# hausdorffDist(s1,s2,model)
# # model = gensim.models.Word2Vec.load("/u/scratch/d/datduong/word2vecData2trainJ/model250Bi2/modelWord2Vec")
# ['mitosis', 'cell', 0.31956137773148624]
# ['mitosis', 'death', 0.25845012694235503]
# ['mitosis', 'cell', 0.31956137773148624]
# ['mitosis', 'division', 0.51737308941833071]
# ['pole', 'cell', 0.14859302598964724]
# ['pole', 'death', 0.076048699981822815]
# ['pole', 'cell', 0.14859302598964724]
# ['pole', 'division', 0.3201775258158937]
# ['cell', 'cell', 1.0000000000000002]
# ['cell', 'death', 0.03752750531504475]
# ['cell', 'cell', 1.0000000000000002]
# ['cell', 'division', 0.10989206553106531]

# T1 = ["mitosis","pole","cell"]
# T2 = ["cell","death","cell","division"]
# # sim2Sentences(T1,T2,model)
# T = T1 + T2
# # # S1 = convertSen2SemSet(T1,T,model) # semset 
# # # S2 = convertSen2SemSet(T2,T,model)	

# # # cosineSim(S1,S2)

# # R1 = matchOrdering(T1,T2,model) # rank set 
# # R2 = convert2rankVec(T2,T,model) 

# # T1 = ["linear","regression","model"]
# # T2 = ["cell","death","cell","division"]
# # T = T1 + T2

# # ctsJaccard(T1,T2,model)
# # ctsJaccardWted(T1,T2,model)

# getInfoContent2vec(T1,T2,model)
# getSignificantInfoContent2vec(s1,s2,model)/getInfoContent2vec(s1,s2,model)

