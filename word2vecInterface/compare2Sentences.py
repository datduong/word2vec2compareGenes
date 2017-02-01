import sys
# sys.setrecursionlimit(5000)
import warnings
warnings.filterwarnings('ignore')

# import gensim 
# import numpy as np 
# import nltk  

def user_input (): 
	x = raw_input('Enter sentence (or phrase):')
	return x

print "loading gensim library, and the already trained word model from 15GB of Pubmed open access articles (may take 1-2 minutes)"
import gensim 
model = gensim.models.Word2Vec.load('modelWord2Vec')

print "finished loading."
print "the model is trained using biology articles and does not handle generic sentences too well. however, it does fine with biology related sentences, for example, you can try 'cell division' and 'mitosis'."
# print "from empirical experiment, sentences with similarity score > 0.62 are statistically similar."

from func2cleanASentence import * ## import functions needed to clean setences 
from func2getSimOf2GoTerms import * ## import functions needed to compare go terms 
from SentenceSimilarity import * ## import functions needed to compare go terms 

def main(model): 
	repeat = 'yes'
	while repeat=='yes':
		s1 = user_input()
		s2 = user_input()
		print 'Similarity score (min=0, max=1):'
		s1=keepOnlyWordsInModel (cleanASentence(s1),model)
		s2=keepOnlyWordsInModel (cleanASentence(s2),model)
		print "words not found in trained data are removed."
		print s1
		print s2
		if (len(s1)==0 | len(s2)==0):
			print "words not found in trained data"
		print hausdorffDistModWted (s1,s2,model)
	# print model.similarity(s1,s2)
		repeat = raw_input('repeat with new sentences? (yes/no)')
		while repeat not in ['yes','no']:
			print 'enter yes or no'
			repeat = raw_input('repeat with new sentences? (yes/no)')

main(model)	
