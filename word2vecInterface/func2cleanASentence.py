import stat
import fileinput
import os
import time
import random
import sys, traceback
import subprocess
from subprocess import Popen, PIPE
import numpy as np
import cPickle
# import nltk
# from nltk.corpus import stopwords
# from nltk.probability import FreqDist
# from nltk import word_tokenize
import string 
import re 

##	
def grepPatternInVec (pattern,array) : 
	return filter(lambda x:re.search(pattern, x), array)

##	
def subPatternInVec (pattern,array) : 
	vec2 = []
	for d in array: 
		vec2.append(re.sub(pattern,"",d).rstrip()) ## sub strip
	return vec2
	
def stripEleInAVec (vec): 
	return map(lambda i: i.strip(), vec) 

def keepOnlyWordsInModel (textInFile,model): ## "model" is from w2v model 
	# l2 = []
	# for l22 in textInFile.split():
		# l22 = l22.strip()
		# if l22 in model.vocab: 
			# l2.append(l22)
	l2 = map(lambda x: x.strip(), textInFile.split())	### textInFile: is a string like 'abcdef'
	l2 = filter(lambda x: x in model.vocab, l2)
	return l2 
	
def keepOnlyWordsInModel2 (l1,model): ## l1 is a vector=['abc','defg'], "model" is from w2v model 
	## !! USE THIS, AFTER CONVERTING TO BIGRAM OR TRIGRAM 
	# l2 = []
	# for l22 in l1:
		# l22 = l22.strip()
		# if l22 in model.vocab: 
			# l2.append(l22)
	l2 = map(lambda x: x.strip(), l1)	
	l2 = filter(lambda x: x in model.vocab, l2)
	return l2
	
def removeArrowBrackets (textInFile):
	textInFile = re.sub(r'<.*?>'," ",textInFile) ## remove stuffs in the <> symbols
	return textInFile		

def cleanASentence (textInFile): 	## textInFile: is a string like 'abcdef' 
## remove \n\r\some_character 
	stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)
	textInFile = stripped(textInFile)	
	## convert to lower 
	textInFile = textInFile.lower()
	## remove punctuation 
	punc2remove = '!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~' # want to keep the co-expression
	outtab = "                              "                                   
	trantab = string.maketrans(punc2remove, outtab)
	textInFile = textInFile.translate(trantab)
	## remove lone numbers (save words like CCR5)	
	# for rep in range(0,10): ## repeat many times to remove "xx xx xx xx" repeat
		# # p = re.compile("\s\d+\.\d+(\s|\.)") ## proper way of using regex??
		# # textInFile = p.sub(" ",textInFile) 
	textInFile = re.sub(r"\b\d+\.\d+\b"," ",textInFile) ## remove decimal xxx.xxx format
	textInFile = re.sub(r"\b\d+\b"," ",textInFile)## remove lone number xxx
	## many white space to 1 white space
	textInFile = re.sub('\s+', ' ', textInFile)
	## remove stop-words 
	# from stop_words import get_stop_words
	# cachedStopWords = get_stop_words('english')
	# textInFile = ' '.join([word for word in textInFile.split() if word not in cachedStopWords])
	## remove more stop-words
	stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
	stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
	stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
	stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
	stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
	stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
	stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
	stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
	stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
	stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
	stopwords += ['computer', 'con', 'could', 'couldnt', 'cry']
	stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
	stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
	stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
	stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
	stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
	stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
	stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
	stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
	stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
	stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
	stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
	stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
	stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
	stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
	stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
	stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
	stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
	stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
	stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
	stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
	stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
	stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
	stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
	stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
	stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
	stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
	stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
	stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
	stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
	stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
	stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
	stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
	stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
	stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
	stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
	stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
	stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
	stopwords += ['whoever', 'whom', 'whose', 'why', 'will', 'with'] # whole blood ? 
	stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
	stopwords += ['yours', 'yourself', 'yourselves']
	for key in stopwords:
		# textInFile = re.sub("\s+"+key+"\s+"," ",textInFile) ## remove "space"world"space"
		# textInFile = re.sub("\."+key+"\s+"," ",textInFile)	
		# textInFile = re.sub("\s+"+key+"\."," ",textInFile)
		textInFile = re.sub("\\b"+key+"\\b"," ",textInFile)
		textInFile = re.sub("^"+key+" "," ",textInFile) ## begin word
		textInFile = re.sub(" "+key+"$"," ",textInFile) ## end word 
		# textInFile = re.sub("(\.|\s)+"+key+"(\.|\s)+"," ",textInFile)
	timewords = ['monday', 'tuesday', 'wednesday','thursday','friday','saturday','sunday','week','weeks','day','days','month','months','years', 'year', 'etal', "et al"] ## not important 
	for key in timewords:
		# textInFile = re.sub("\s+"+key+"\s+"," ",textInFile) ## remove "space"world"space"
		# textInFile = re.sub("\."+key+"\s+"," ",textInFile)	
		# textInFile = re.sub("\s+"+key+"\."," ",textInFile)
		textInFile = re.sub("\\b"+key+"\\b"," ",textInFile)
		textInFile = re.sub("^"+key+" "," ",textInFile) ## begin word
		textInFile = re.sub(" "+key+"$"," ",textInFile) ## end word 
		textInFile = re.sub("(\.|\s|\d)+"+key+"(\.|\d|\s)+"," ",textInFile)	
	# re.findall(r"([^.]*?would[^.]*\.)",textInFile)
	# textInFile = textInFile.translate(None, punc2remove)
	## remove single letter "l" "x" "y"
	textInFile = re.sub(r'\b[A-z]\b', ' ', textInFile)
	## tokenize words like co-expression right-handedness 
	textInFile = re.sub(r"-",r"_",textInFile)
	textInFile = re.sub(r"\b_\b"," ",textInFile) ## remove lone symbol _ 
	textInFile = re.sub(r" _"," ",textInFile) ## remove lone symbol _xyz
	textInFile = re.sub(r"_ "," ",textInFile) ## remove lone symbol _xyz	
	## split into sentences (one per line)
	textInFile = re.sub(r"\.",r" ",textInFile)	
	textInFile = re.sub(r'\s+', ' ', textInFile)
	## redo white space
	# textInFile = re.sub('\s+', ' ', textInFile)	# SOMEHOW \s removes the \n too. 
	return (textInFile) ## return as a list 
	