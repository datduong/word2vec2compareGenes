
rm(list=ls())

args = commandArgs(TRUE) # R CMD BATCH --no-save --no-restore "--arg in1 in2" Rcode Rcode.out

startPoint = as.numeric(args[1])
endPoint = as.numeric(args[2])

fileoutname = paste0 ( "/u/scratch/d/datduong/PPI_AicBP/AicBP_HDF",startPoint,".",endPoint,".txt") 
if (file.exists(fileoutname)){
	q() 
}

library(GOSim)
setOntology(ont = "BP")
data("ICsBPhumanall") ## change this if want to use a different Ontology 
ancestorsX = getAncestors() 

source("/u/home/d/datduong/simGO_aic.R")
# source("/u/home/d/datduong/simGO_resnik.R")


## read a pairs file # proteinPairsCESSM
pairs = read.table("/u/scratch/d/datduong/ppiS2.txt",header=FALSE,stringsAsFactors=FALSE)

## create a mapping # proteinPairsCESSMmapping
mapping = read.table ("/u/scratch/d/datduong/geneNameMappingS1.txt",header=FALSE,stringsAsFactors=FALSE)

func2map = function (codeName,mapping){
	where = which(mapping[,1]==codeName)
	where = where[1]
	if (length(where)==0) {
		return (NA)
	}
	return (mapping[where,2])
}

## map the pairs into gene names 
validPairs = NULL
for (line in 1:nrow(pairs)){
	name1 = func2map(pairs[line,1],mapping)
	name2 = func2map(pairs[line,2],mapping)
	if ( is.na(name1) | is.na(name2) ){
		next 
	} 
	validPairs = rbind ( validPairs, c(name1,name2) ) 
}

## ------------------
## ------------------

getGOterms = function (vec){
	vec = strsplit(vec," ")[[1]]
	return ( vec[ grep('GO',vec) ] ) 
}

getGOterms2 = function (vec){
	return ( vec[ grep('GO',vec) ] ) 
}

compare2randomGenes = function (GENES,num){
	samps = sample(size=2,x=1:num,replace=FALSE)
	gene1 = getGOterms2 ( GENES[[samps[1]]] )
	gene2 = getGOterms2 ( GENES[[samps[2]]] )
	d = hdOf2sets(gene1, gene2)
	return (d)
}

compare2randomGenes2 = function (GENES,num){
	samps = sample(size=2,x=1:num,replace=FALSE)
	gene1 = GENES[[samps[1]]][-1] ## remove 1st entry 
	gene2 = GENES[[samps[2]]][-1]
	## add in the "GO:" because of the IC function 
	d = hdOf2sets(gene1, gene2)
	return (d)
}

keepGOwithIC2 = function(vec){
	vec1 = strsplit(vec," ")[[1]][1] ## the name of gene 
	vec = getGOterms(vec)
	icgo = IC[vec]
	icgo = icgo [ which(icgo != 0) ] ## this remove the root go term from the gene. 
	icgo = icgo [ which(icgo != Inf) ]
	icgo = icgo [ which(icgo != -Inf) ]
	icgo = icgo [ which(is.na(icgo) == FALSE) ]
	return (c(vec1,names(icgo)))
}

keepValidGenes = function ( GOtermsPerGenes ){
	GOtermsPerGenes = lapply(GOtermsPerGenes,keepGOwithIC2)
	len = lapply(GOtermsPerGenes,length)
	return ( GOtermsPerGenes [ which(len>1) ] ) 
}

format1Line2List = function (vec){
	vec1 = strsplit(vec," ")[[1]]
	name = vec1[1]
	vec1 = paste("GO:",vec1[-1],sep="")
	return (c(name,vec1))
}

text2List = function ( textFullPath ) {
	GENES = readLines(textFullPath)
	GENES = lapply(GENES,format1Line2List)
	return (GENES)
}


text2ListNoNameInEntry = function (list1){
	return (list1[-1]) ## remove the name from the go list-> nameOfGene goterm1 goterm2 ... 
}
text2ListNameInEntry = function (list1){
	return (list1[1])
}

GENES = text2List ( paste0 ("/u/scratch/d/datduong/","GENEKEGG_GOSIMBP",".txt") ) ## all the genes from kegg
allGeneNamesInKegg = lapply (GENES,text2ListNameInEntry)
GENES = lapply(GENES,text2ListNoNameInEntry)
names(GENES) = allGeneNamesInKegg


## ------------------
## ------------------

if (endPoint>nrow(validPairs)){
	endPoint = nrow(validPairs)
}
validPairs = validPairs [ startPoint: endPoint, ]


distance2output = NULL 
ptm <- proc.time()
for (i in 1:nrow(validPairs)){
	name1 = validPairs[i,1]
	name2 = validPairs[i,2]
	score = hdOf2sets(GENES[[name1]], GENES[[name2]])
	distance2output = rbind(distance2output,c(name1,name2,score))
}
proc.time() - ptm

write.table(distance2output,file=fileoutname,row.names=FALSE,col.names=FALSE,quote=FALSE)

# library('BiocParallel')
# library('BatchJobs')

# X = 1:numGenes
# param <- BatchJobsParam(workers = 4)
# ptm <- proc.time()
# distance2 = bplapply(X, resnik_parallel, GOtermsPerGenes ,BPPARAM = param)
# proc.time() - ptm

# distance = formatDistance2Matrix (distance2)

# write.table(distance,file=fileName,row.names=F,col.names=F,quote=F)

# v1 = GOtermsPerGenes[[4]] 
# v2 = GOtermsPerGenes[[5]]
