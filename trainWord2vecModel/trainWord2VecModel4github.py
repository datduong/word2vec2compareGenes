
import gensim, logging, os
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import stat
import fileinput
import time
import random
import sys, traceback
import subprocess
from subprocess import Popen, PIPE
import cPickle
import re 
import gzip 


class MySentences(object):
	def __init__(self, dirname):
		self.dirname = dirname
	def __iter__(self):
		for fname in os.listdir(self.dirname):
			if "txt" not in fname: 
				continue 
			print fname 
			for line in open(os.path.join(self.dirname, fname)):
				line = line.split()
				line = [x.strip() for x in line]
				yield line

class MySentencesBigram(object):
	def __init__(self, dirname,aBigram):
		self.dirname = dirname
		self.bigram = aBigram ## need to train data to get a bigram (or borrow it somewhere else)
	def __iter__(self):
		for fname in os.listdir(self.dirname):
			if "txt" not in fname: 
				continue 
			print fname 
			for line in open(os.path.join(self.dirname, fname)):
				line = line.split()
				line = [x.strip() for x in line]
				line = self.bigram[line] ## convert "los angeles" to "los_angeles"
				yield line
				
def submitJobs (path2TextFiles , file2savePath, modelName2save, doBigram, bigramPath, minCountOfWord, dimensionOfVec):

	if not os.path.exists(file2savePath): 
		os.mkdir(file2savePath)

	print ("begin\n") 
	
	if doBigram == 1: 
		print ("now loading a bigram\n")
		bigram = gensim.models.phrases.Phraser.load(bigramPath)
		print ("now loading sentences\n")
		sentences = MySentencesBigram(path2TextFiles,bigram) 
	else: 
		print ("now loading sentences\n")
		sentences = MySentences(path2TextFiles)
	
	print ('now running model\n') 
	model = gensim.models.Word2Vec(sentences,min_count=minCountOfWord,size=dimensionOfVec,max_vocab_size=120000000,workers=8,window=5)
	print ('finished running, now save file\n')
	model.save(os.path.join(file2savePath,modelName2save))
	print ('finished saving file\n')
	
	
### -------------------------------------------------------
	
if len(sys.argv)<7:
	print("Usage: \n")
	sys.exit(1)
else:
	submitJobs ( sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5] , int(sys.argv[6]), int(sys.argv[7]) ) 
	
	



