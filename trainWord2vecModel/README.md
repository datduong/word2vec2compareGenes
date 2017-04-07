
This code shows you how to train a word2vec model. 

Suppose you want to train the model on the file Eur_J_Neurosci_2015_Jun_10_41_1438-1447.txt. 

You would need to clean this file (remove stop-words, and punctuations). 
```
mkdir /u/home/d/datduong/sourceFiles/ ## create folder 
vim Eur_J_Neurosci_2015_Jun_10_41_1438-1447.txt ## download the file into this folder, and read it. 

python cleanOneFile4github.py /u/home/d/datduong/sourceFiles/Eur_J_Neurosci_2015_Jun_10_41_1438-1447.txt /u/home/d/datduong/files2train/Eur_J_Neurosci_2015_Jun_10_41_1438-1447_CLEAN.txt
```

Now you can train the word2vec model. Use the command 
```
python trainWord2VecModel4github.py path2TextFiles file2savePath modelName2save doBigram bigramPath minCountOfWord dimensionOfVec
```

For example, your command can look like this 

```
python trainWord2VecModel4github.py /u/home/d/datduong/files2train/ /u/home/d/datduong/w2vModel/ w2vModelMMDDYY 0 none 100 200
```

The parameters 
```
minCountOfWord=100 will remove words with counts less than 100.
dimensionOfVec=200 will create a vector of dim 200 for each word.
```

To use a bigram, you will need to train the data first (or you can download an existing bigram some where else) to recognize bigram. For example, you need to train the data so that words like "los angeles" are converted into "los_angeles". Most likely, you won't need to use bigram if you can preprocess your input files. The parameters, 
```
doBigram=1 will trigger the bigram to be used. 
bigramPath is the path to the bigram. 
```
