import re,sys,gensim

# sys.path.append('/u/home/d/datduong/')
from func2cleanASentence import * 
from func2getSimOf2GoTerms import * ## import functions needed to compare go terms 
from SentenceSimilarity import * ## import functions needed to compare go terms 

import cPickle
FILE = open("goAnnotOboOwlBioProcClean.cPickle", 'r')
goAnnot2 = cPickle.load(FILE)
FILE.close()

def user_input (): 
	x = raw_input('Enter GO id number:')
	return x

print "loading gensim library, and the already trained word model from 15GB of Pubmed open access articles (may take 1-2 minutes)"

model = gensim.models.Word2Vec.load("modelWord2Vec")
bigram = gensim.models.phrases.Phraser.load(
'bigram.data')
trigram = gensim.models.phrases.Phraser.load('trigram.data')

print "finished loading."



def main(model,bigram,trigram): 
	repeat = 'yes'
	while repeat=='yes':
		print 'Input 2 GO terms. Use only the Id numbers. For example try : 0007166 and 0007267. The similarity score is for only terms in Biological Processes ontology. '
		s1 = user_input()
		s2 = user_input()
		print w2v2GoTerms (s1,s2,goAnnot2,hausdorffDistModWted,model,bigram,trigram,toTrigram=0)
		repeat = raw_input('repeat? (yes/no)')
		while repeat not in ['yes','no']:
			print 'enter yes or no'
			repeat = raw_input('repeat with new sentences? (yes/no)')

main(model,bigram,trigram)	

