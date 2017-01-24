

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


# data("ICsBPhumanall")
# library(GOSim)
# ancestorsX = getAncestors() ## all the ancestors of the go terms, depend on the go data base  
# ancestorsX$`GO:2001317`
# ancestorsX['GO:2001317']

## implement average ic method. in song et. al. 

# compare 2 go terms 

keepGOwithIC = function(go){
	icgo = IC[go]
	# icgo = icgo [ which(icgo != 0) ]
	# icgo = icgo [ which(icgo != Inf) ]
	# icgo = icgo [ which(icgo != -Inf) ]
	icgo = icgo [ which(is.na(icgo) == FALSE) ]
	return (names(icgo))
}


# get sw of a go term 
getSw = function (term){
	ICofTerm = IC[term]
	#ICofTerm = ICofTerm [ which(ICofTerm != Inf) ]
	Kt = abs(1/ICofTerm)
	# Kt = keepGOwithIC(Kt)
	if (length(Kt)==0){
		print ('no IC found for all inputs')
		return (NA)
	}
	return ( 1/( 1+ exp( -1*Kt ) ) ) 
}

# get sv(x) of a go term x 
getSv = function(term){
	ancestors = ancestorsX[term][[1]]
	ancestors = keepGOwithIC (ancestors)
	if (length(ancestors)==0){
		return (getSw(term))
	}
	swOfAncestors = sum ( getSw ( ancestors ) )
	return ( swOfAncestors + getSw(term) ) ## add itself 
}

sum2Sw = function (term1,term2){
	common = intersect( c ( term1, ancestorsX[term1][[1]] ),
		c ( term2, ancestorsX[term2][[1]]) )
	# if (term1==term2){
	# 	common = c(common,term1) ## same set, then add the term 
	# }
	common = common[ which ( ! common %in% c("all")) ] # ""GO:0008150","GO:0003674" are roots
	if (length(common)==0){ ## no possible common ancestor
		return (0)
	}
	#	IF COMES TO THIS STEP: THEN THERE IS COMMON ANCESTORS, BUT POSSIBLE, THESE ANCESTORS DON'T HAVE IC-VALUE 
	common = keepGOwithIC (common) ## if the ancestors have invalid IC, then remove them 
	if (length(common)==0){
		return (NA) ## common ancestors of 2 terms all have invalid IC 
	}
	return ( 2* sum ( getSw ( common ) ) )
}

simGO_aic = function (term1,term2){
	svA = getSv(term1)
	svB = getSv(term2)
	if (is.na(svA) | is.na(svB)){ ## if 2 terms have common ancestors with invalid IC, or they themselves have invalid IC, then return a NA here. 
		return (NA)
	}
	numerator = sum2Sw(term1,term2)
	if (is.na(numerator)){
		return (NA)
	}
	return ( as.numeric( numerator/(svA+svB) ) )
}

hd1elemToVec2 = function(v11,vec2,repNum) {
	v1 = rep(v11,repNum) ## so that we can use mapply ( func, [v11,v11...] [v21,v22,...] ) 
	dist1to2 = mapply(simGO_aic,v1,vec2)
	dist1to2 = dist1to2[ ! is.na(dist1to2) ] ## if 2 terms have common ancestors with invalid IC, or they themselves have invalid IC, then return a NA here. 
	if (length(dist1to2)==0){
		return (NA) ## the element v11 in v1 when compared to each element in v2 gives NA. 
	}
	return ( max ( dist1to2 ) ) 
}

hd1to2 = function(vec1,vec2){ # hausdorf distance at vec1 to vec2 (hausdorf is not symmetric)
	repNum = length(vec2) 
	d1to2 = sapply(vec1,hd1elemToVec2,vec2,repNum)
	return ( d1to2 ) 
}

hdOf2sets = function(vec1,vec2){
	d1to2 = hd1to2(vec1,vec2)
	d1to2 = d1to2 [ !is.na(d1to2) ]
	d2to1 = hd1to2(vec2,vec1)
	d2to1 = d2to1 [ !is.na(d2to1) ]
	if (length(d1to2)==0 | length(d2to1)==0){ ## every single element v11 in v1 when compared to each element in v2 gives NA. 
		return (NA)
	}
	return (min(mean(d1to2),mean(d2to1))) # best ( ave in 1, ave in 2 )
}

hdOf2sets_parallel = function(i,GOtermsPerGenes){
	distance = NULL 
	numGenes = length(GOtermsPerGenes)
	for (j in i:numGenes){
		# print (c(i,j))
		if ( setequal(GOtermsPerGenes[[i]], GOtermsPerGenes[[j]]) ) {
			distance = c(distance, NA )
			next
		}
		distance = c (distance, hdOf2sets(GOtermsPerGenes[[i]], GOtermsPerGenes[[j]]) )
		# distance[j,i] = distance[i,j]
	}
	return (distance)
}

formatDistance2Matrix = function (distance2){
	dimMat = length(distance2[[1]])
	returnMat = matrix(0,nrow=dimMat,ncol=dimMat)
	for (i in 1:dimMat){
		returnMat [ i, i:dimMat] = distance2[[i]]
	}
	return (returnMat)
}


# getSw(c("GO:0007166","GO:0007267","GO:0007584","GO:0007165","GO:0007186"))
# getSv("GO:0007166")
# simGO_aic("GO:0007166","GO:0007267")
# vec1 = c("GO:0007166","GO:0007267","GO:0007584","GO:0007165","GO:0007186")
# vec2 = c("GO:0007166","GO:0007267","GO:0007584")
# hdOf2sets (vec1,vec2)


