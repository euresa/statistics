#**************************************************************
#Author: Samuel Eure  +++++++++++++++++++++++++++++++++++++++++
#June 27, 2018; DataPlus2018 ++++++++++++++++++++++++++++++++++ 
#Used to obtain district plans after sampling +++++++++++++++++ 
#Obtains unique plans that have been translated from clusters +
#--------------------------------------------------------------



#**************************************************************
#++++++++++++++++++++++++ INPUT +++++++++++++++++++++++++++++++
#--------------------------------------------------------------
#       Specify Machine
machine = "macbook"
#machine = "windows"

#       Specify the map sampled on located in the first folder 


mapChosen 		  = "MDPrecinct_MID_CROSS"
crossing          = "MID_CROSS"
samplingRun       = "20180723_16.51.37_ensemble_incumbency"
dataPrefix  	  = "Precinct"
usedMPI  = False

#Do you only want the unique maps? 
#Good luck if false
onlyGettingUnique = True
translatingData   = False
PrecinctToCluster = "PrecinctToCluster"


#**************************************************************
#+++++++++++++++++++++ BEGIN SCRIPT +++++++++++++++++++++++++++
#--------------------------------------------------------------


import os
import shutil
from glob import glob

machineMap = {'macbook':"/", "windows": "\\"}
S = machineMap[machine.lower()]

#Checking input

rootDir = ".."+S+".."+S+".."+S+"MDSamplingData"+S+"SamplingData"

if not os.path.exists(rootDir):
	print "ERROR: Invalid root directory", rootDir
	exit()

#Making Directories
print "Making Folders..."


if not os.path.exists(rootDir+S+crossing+S):
	os.mkdir(rootDir+S+crossing+S)
if not os.path.exists(rootDir+S+crossing+S+samplingRun+S):
	os.mkdir(rootDir+S+crossing+S+samplingRun+S)
if not os.path.exists(rootDir+S+crossing+S+samplingRun+S+"Unique"):
	os.mkdir(rootDir+S+crossing+S+samplingRun+S+"Unique")

outputDir = rootDir+S+crossing+S+samplingRun+S+"Unique"


if not os.path.exists(os.path.join(outputDir,"districtingMaps")):
	os.mkdir(os.path.join(outputDir,"districtingMaps"))
if not os.path.exists(os.path.join(outputDir,"energy")):
	os.mkdir(os.path.join(outputDir,"energy"))
if not os.path.exists(os.path.join(outputDir,"IsoperimetricRatio")):
	os.mkdir(os.path.join(outputDir,"IsoperimetricRatio"))
if not os.path.exists(os.path.join(outputDir,"FractionalPopulationDeviation")):
	os.mkdir(os.path.join(outputDir,"FractionalPopulationDeviation"))


print "Getting data", samplingRun


#Account for 
rankList = glob(os.path.join(rootDir+S+crossing+S+samplingRun) + "/rank_*")
SamplingDir = os.path.join(rootDir+S+crossing+S+samplingRun)
INDEX = 0
uniqueList = []
if len(rankList) > 0:
	for i in range(len(rankList)):
		dList   =glob(SamplingDir + "/rank_"+str(i)+ "/districtingMaps/*")
		eList   =glob(SamplingDir +  "/rank_"+str(i)+ "/energy/*")
		irmList =glob(SamplingDir  + "/rank_"+str(i)+ "/IsoperimetricRatio/*")
		fpdList =glob(SamplingDir  + "/rank_"+str(i)+ "/FractionalPopulationDeviation/*")
		if not len(dList) == len(irmList):
			print "weird input, lengths of samplings results are not equal"
			exit()
		print
		print "on rank ", str(i)
		for sampleIndex in range(1,len(dList)):

			dDirectory = SamplingDir + S + "rank_"+str(i) + S

			f = open(dDirectory+ "districtingMaps"+"/districtingMap" + str(sampleIndex) + ".txt","r");
			lines = [str(line) for line in f.readlines()]
			lines.sort()
			R = str("".join(lines))
			f.close()
		
			f = open(dDirectory + "energy"+"/energy" + str(sampleIndex) + ".txt","r");
			lines = [str(line) for line in f.readlines()]
			lines.sort()
			A = str("".join(lines))
			f.close()
		
			f = open(dDirectory+ "IsoperimetricRatio"+"/IsoperimetricRatio" + str(sampleIndex) + ".txt","r");
			lines = [str(line) for line in f.readlines()]
			lines.sort()
			H = str("".join(lines))
			f.close()
		
			f = open(dDirectory+ "FractionalPopulationDeviation"+"/FractionalPopulationDeviation" + str(sampleIndex) + ".txt","r");
			lines = [str(line) for line in f.readlines()]
			lines.sort()
			UL = str("".join(lines))
			f.close()
		
			#HASH = hash(R+A+H+UL) 
			HASH = hash(R+A+H+UL)
			isUnique = HASH not in uniqueList
		
			if isUnique and onlyGettingUnique:
				uniqueList.append(HASH)
		
				shutil.copy(os.path.join(SamplingDir,"rank_"+str(i), "districtingMaps",
					                     "districtingMap"+str(sampleIndex)+".txt"),
					        os.path.join(outputDir,"districtingMaps",
					                     "districtingMap"+str(INDEX)+".txt"))
		
				shutil.copy(os.path.join(SamplingDir,"rank_"+str(i), "energy",
					                     "energy"+str(sampleIndex)+".txt"),
					        os.path.join(outputDir,"energy",
					                     "energy"+str(INDEX)+".txt"))
		
				shutil.copy(os.path.join(SamplingDir,"rank_"+str(i), "IsoperimetricRatio",
					                     "IsoperimetricRatio"+str(sampleIndex)+".txt"),
					        os.path.join(outputDir,"IsoperimetricRatio",
					                     "IsoperimetricRatio"+str(INDEX)+".txt"))
		
				shutil.copy(os.path.join(SamplingDir,"rank_"+str(i), "FractionalPopulationDeviation",
					                     "FractionalPopulationDeviation"+str(sampleIndex)+".txt"),
					        os.path.join(outputDir,"FractionalPopulationDeviation",
					                     "FractionalPopulationDeviation"+str(INDEX)+".txt"))
				INDEX+=1
	print "Finished.  Reduced to ", len(uniqueList), " plans"
else:
	dList   =glob(SamplingDir + "/districtingMaps/*")
	eList   =glob(SamplingDir +  "/energy/*")
	irmList =glob(SamplingDir  + "/IsoperimetricRatio/*")
	fpdList =glob(SamplingDir  + "/FractionalPopulationDeviation/*")
	if not len(dList) == len(irmList):
		print "weird input, lengths of samplings results are not equal"
		exit()
	print
	for sampleIndex in range(len(dList)):
		dDirectory = SamplingDir + S
		f = open(dDirectory+ "districtingMaps"+"/districtingMap" + str(sampleIndex) + ".txt","r");
		lines = [str(line) for line in f.readlines()]
		lines.sort()
		R = str("".join(lines))
		f.close()
	
		f = open(dDirectory + "energy"+"/energy" + str(sampleIndex) + ".txt","r");
		lines = [str(line) for line in f.readlines()]
		lines.sort()
		A = str("".join(lines))
		f.close()
	
		f = open(dDirectory+ "IsoperimetricRatio"+"/IsoperimetricRatio" + str(sampleIndex) + ".txt","r");
		lines = [str(line) for line in f.readlines()]
		lines.sort()
		H = str("".join(lines))
		f.close()
	
		f = open(dDirectory+ "FractionalPopulationDeviation"+"/FractionalPopulationDeviation" + str(sampleIndex) + ".txt","r");
		lines = [str(line) for line in f.readlines()]
		lines.sort()
		UL = str("".join(lines))
		f.close()
	
		#HASH = hash(R+A+H+UL) 
		HASH = hash(R+A+H+UL)
		isUnique = HASH not in uniqueList
	
		if isUnique and onlyGettingUnique:
			uniqueList.append(HASH)
	
			shutil.copy(os.path.join(SamplingDir, "districtingMaps",
				                     "districtingMap"+str(sampleIndex)+".txt"),
				        os.path.join(outputDir,"districtingMaps",
				                     "districtingMap"+str(INDEX)+".txt"))
	
			shutil.copy(os.path.join(SamplingDir, "energy",
				                     "energy"+str(sampleIndex)+".txt"),
				        os.path.join(outputDir,"energy",
				                     "energy"+str(INDEX)+".txt"))
	
			shutil.copy(os.path.join(SamplingDir, "IsoperimetricRatio",
				                     "IsoperimetricRatio"+str(sampleIndex)+".txt"),
				        os.path.join(outputDir,"IsoperimetricRatio",
				                     "IsoperimetricRatio"+str(INDEX)+".txt"))
	
			shutil.copy(os.path.join(SamplingDir,"rank_"+str(i), "FractionalPopulationDeviation",
				                     "FractionalPopulationDeviation"+str(sampleIndex)+".txt"),
				        os.path.join(outputDir,"FractionalPopulationDeviation",
				                     "FractionalPopulationDeviation"+str(INDEX)+".txt"))
			INDEX+=1
	print "Finished.  Reduced to ", len(uniqueList), " plans"


if translatingData:
	translatedDir = rootDir+S+crossing+S+samplingRun+S+"Translated"+S
	if not os.path.exists(translatedDir):
		os.mkdir(translatedDir)
	
	translateDistrictingPlan(mapChosen, translatedDir, outputDir, dataPrefix, PrecinctToCluster)

	
	
exit()