
This code shows you how to train a word2vec model. 

Use the command 
```
trainWord2VecModel4github path2TextFiles file2savePath modelName2save doBigram bigramPath minCountOfWord dimensionOfVec
```

For example, your command can look like this 

```
trainWord2VecModel4github /u/home/d/datduong/files2train/ /u/home/d/datduong/w2vModel/ w2vModelMMDDYY 0 none 100 200
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
