# word2vec2compareGenes

This is the paper you should read before using the code. http://biorxiv.org/content/early/2017/01/28/103648.

In this project, I train word2vec on Pubmed data. Word2vec model converts a word into a vector, so that one can quantify how similar are two words. I then use this model to compare 2 sentences, 2 GO terms, and 2 genes. 

What are GO terms? 
GO terms are "gene ontology" term. Each term describes a biology feature. For example: term xyz describes "cell division". 

How do GO terms relate to a gene? 
A gene is described by many GO terms. Thus, given a gene and its set of GO terms, one can guess the gene's function in the cell. 

Comparing 2 genes is pretty much equivalent to comparing 2 sets of GO terms. 

In the folder "word2vecInterface" in this github repository, you will see all the source code. However, the trained data is too big. 
The entire trained model (along with any source code) is here https://drive.google.com/open?id=0BzSj4Ecl_7R8T1VJTlhfR09wdlE

This link above also contains a simple Python interface. Please read the Readme.txt in that link. You will need to download all the files in that link into the same folder.
To view the trained model, you must install the Python library "gensim".

The screenshot of the interface looks like this: 
![alt tag](https://github.com/datduong/word2vec2compareGenes/blob/master/instruction1.png)

If you have a lot of GO terms that need to be compared, then the interface is not too useful for obvious reasons. In this case, you can modify the source code "compare2GOtermsInterface.py"; for example, you can use 2 for-loops when comparing many GO terms. 


---- loading the trained word2vec model on Pubmed data 

You can use

import gensim
model = gensim.models.Word2Vec.load("modelWord2Vec") # you need to download the modelWord2Vec data from the google drive. 
bigram = gensim.models.phrases.Phraser.load(
'bigram.data')
trigram = gensim.models.phrases.Phraser.load('trigram.data')
