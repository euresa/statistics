import pandas as pd
import numpy as np
import os



#Should be run from /NCStateData/ElectionData/
clusterDir = '../../NCClusterAnalysis/Data/ExtractedData/ClusterSenate/'


def getP(df):
    return df.precinct.unique()
    
def splitCluster(cluster):
    cluster = cluster.replace("_C_", "\t")
    cluster = cluster.replace("_P_", "\t")
    cluster = cluster[:-1].split('\t')
    cluster = [c.upper() for c in cluster]
    return cluster

def getClusterDf(df, cluster):
    cluster = splitCluster(cluster)
    dfList = []
    for c in cluster:
        if c == 'NEWHANOVER':
            c = "NEW HANOVER" 
        dfList.append(df[df.county == c])
    clusterDf = pd.concat(dfList)
    return clusterDf

def getCountyDf(df, myCounty):
    if myCounty == 'NEWHANOVER':
        myCounty = "NEW HANOVER" 
    return df[df.county == myCounty.upper()]

def takeAwayPrecincts(df, precinctList):
    for p in precinctList:
        df = df[df.precinct != p]
    return df


def filterElections(cdf, partyMap):
    electionIndex = range(len(cdf))
    for i in range(len(cdf)):
        if cdf.contest[i] in elections:
            electionIndex[i] = True
        else:
            electionIndex[i] = False
    filteredCDF = cdf.iloc[electionIndex,:]
    
    filteredCDF = filteredCDF[filteredCDF.candidate != "OVER VOTES"]
    filteredCDF = filteredCDF[filteredCDF.candidate != "UNDER VOTES"]
    smalldf = filteredCDF[filteredCDF.candidate != "WRITE-IN"]
    smalldf = smalldf[smalldf.precinct != "MISC"]
    smalldf = smalldf[smalldf.precinct != "PROVISIONAL"]
    smalldf = smalldf[smalldf.precinct != "Curbside;Provisional"]
    smalldf = smalldf[smalldf.precinct != 'CURBSIDE']
    smalldf = smalldf[smalldf.precinct != "TRANSFER"]
    smalldf = smalldf[smalldf.precinct != "ABSENTEE"]

    takeOut = ['PROVI ', 'ABSEN ', "TRANS ", 'OS ', 
               'OS-', 'ABSENTEE ', 'CURBSIDE ', 'PROVISIONAL ']
    for out in takeOut: 
        smalldf = smalldf[~smalldf["precinct"].str.contains(out)]

    
    
    allCandidates = smalldf.candidate.unique()
    
    for c in allCandidates:
        if c not in partyMap.keys():
            partyMap[c] = 'UN'
    
    smalldf['candidate'] = smalldf['candidate'].map(partyMap)

    return smalldf

def getElectionDf(newDf, election):
    edf = newDf[newDf.contest == election]
    return edf


def prepareCountyElectionData(eDf):
    dem   = sum(eDf[eDf.candidate == 'DEM'].votes.tolist())
    rep   = sum(eDf[eDf.candidate == 'REP'].votes.tolist())
    total = sum(eDf.votes.tolist())
    return dem, rep, total


def prepareElectionData(eDf):
    voteTypes = eDf.candidate.unique().tolist()
    columnLength = int(len(eDf)/float(len(voteTypes)))
    if 'DEM' in voteTypes:
        demVotes = eDf[eDf.candidate == 'DEM'].votes.tolist()
    else:
        demVotes = np.zeros(columnLength)
    if "REP" in voteTypes:
        repVotes = eDf[eDf.candidate == 'REP'].votes.tolist()
    else:
        repVotes = np.zeros(columnLength)
        
    totalVotes = np.zeros(columnLength)
    for i in range(columnLength):
        tVotes = 0
        for j in range(len(voteTypes)):
            row = eDf.iloc[i+j,:]
            tVotes += row.votes
        totalVotes[i] = tVotes

    precincts = eDf.precinct.unique().tolist()
    myDf = pd.DataFrame()
    myDf['precinct'] = precincts
    myDf["DEM"] = demVotes
    myDf["REP"] = repVotes
    myDf['TOTAL'] = totalVotes

    return myDf

def duplicates(potentialMap):
    check = set()
   #Returns true if there are not duplicates, false otherwise
    for keys in potentialMap.values():
        for k in keys:
            if k in check:
                return False
            else:
                check.add(k)
    return True

def lookThrough(potentialMap):
    valueMap = {}
    for p in potentialMap:
        keys = potentialMap[p]
        for k in keys:
            if k not in valueMap.keys():
                valueMap[k] = []
            valueMap[k].append(p)
    valueMap = {p:valueMap[p] for p in valueMap.keys() if len(valueMap[p]) >1}

    for key in valueMap.keys():
        candidates = valueMap[key]
        bestCandidate = candidates[0]
        for c in candidates:
            if len(c) > len(bestCandidate):
                bestCandidate = c
        candidates.remove(bestCandidate)
        for c in candidates:
            potentialMap[c].remove(key)
    return potentialMap

def findSimular(key, keyList):
    simular = []
    for k in keyList:
        if key[:2] == k[:2]:
            simular.append(k)
    return simular

def findPotential(key, allKeys, county):
    potential = []
    if ";" not in key:
        for ukey in allKeys:
            if key in ukey:
                potential.append(ukey)
    else:
        if county not in ["GASTON", "ROBESON"]:
            potential = key.split(";")
            potential = [p for p in potential if p in allKeys]
        else:
            if key == '38;43':
                potential = ['39', '43']
            if key == '03;5;11A;38;PROV':
                potential = ['03', '15', '11A', '38']
    return potential


def getPotentialMap(countyDf, ucountyDf):
    county = countyDf.county.unique().tolist()[0].upper()
    sorted = countyDf.precinct.unique().tolist()
    unsorted = ucountyDf.precinct.unique().tolist()

    unmatchedSorted = []
    potentialMap = {}
    found = []
    for key in sorted:
        potential = findPotential(key, unsorted, county)
        found += potential
        if len(potential) == 0:
            unmatchedSorted.append(key)
        potentialMap[key] = potential
    
    if not duplicates(potentialMap):
        potentialMap = lookThrough(potentialMap)
    
    unmatchedUnsorted = [m for m in ucountyDf.precinct.unique() if m not in found]

    return potentialMap

def getClusterIdMap(cluster):
    mapDir = clusterDir + cluster + "/"+cluster+"_GEOIDS.txt"
    f = open(mapDir,'r')
    d = f.readlines()
    f.close()
    indexIdMap = {l.split("\t")[1] + "_"+ l.split("\t")[2][:-1] : int(l.split("\t")[0]) for l in d}
    return indexIdMap

def getSplitPrecincts(preparedTroubleDf, hopefulMatches, countyIdMap, Registered):
    splitPrecincts = {}
    for match in hopefulMatches.keys():
        
        matchDf = preparedTroubleDf[preparedTroubleDf.precinct == match]
        
        row = matchDf.iloc[0,:]
        precinct = row.precinct
        totalDem = row.DEM
        totalRep = row.REP
        totalVotes = row.TOTAL

        splits = hopefulMatches[precinct]
        demMap = {}
        repMap = {}
        totalMap = {}
 
        for s in splits:
            
            index = countyIdMap[s]
            reg = Registered[index]

            adjDem = reg[2]*(reg[0]/float(sum(reg[:-1])))
            adjRep = reg[2]*(reg[1]/float(sum(reg[:-1])))
            demMap[index] = adjDem
            repMap[index] = adjRep
            totalMap[index] = reg[2]

        for s in splits:
            index = countyIdMap[s]

            dem = int(totalDem*(demMap[index]/float(sum((demMap.values()))))+.5)
            rep = int(totalRep*(repMap[index]/float(sum((repMap.values()))))+.5)
            total = int(totalVotes*(totalMap[index]/float(sum(totalMap.values())))+.5)
            if total < dem + rep:
                total = dem + rep
            splitPrecincts[s] = [dem, rep, total]
            if election == "US SENATE":
                print '          handled', s
        
    return splitPrecincts

def getHopefulMatches(leftOver, unmatched):
    hopefulMatches = {}
    for lone in unmatched:
        matches = []
        for left in leftOver:
            if lone[:2] == left[:2]:
                matches.append(left)
        hopefulMatches[lone] = matches
    return hopefulMatches


def prepareOutput(eDf, ueDf, cluster, election):
    indexIdMap = getClusterIdMap(cluster)
    outData = range(len(indexIdMap))
    clusterName = cluster
    cluster = splitCluster(cluster)
    for c in cluster:
        if c != 'NEWHANOVER':
            countyIdMap = {p.split("_")[0]:indexIdMap[p] for p in indexIdMap.keys() if c.upper() in p}
        else:
            countyIdMap = {p.split("_")[0]:indexIdMap[p] for p in indexIdMap.keys() if "NEW" in p}
            
        gran = countyGranularity[c]
        countyDf =  getCountyDf(eDf,  c)
        ucountyDf = getCountyDf(ueDf, c)

        if gran == "C":
            [dem, rep, total]  = prepareCountyElectionData(countyDf)
            countyId         = C2FIP[c]
            index            = countyIdMap[countyId]
            outData[index]   = [dem, rep, total]
        
        elif gran == "P":
            properDf, troubleDf, utroubleDf = checkPrecincts(countyDf, ucountyDf, countyIdMap)

            unmatchedSorted = troubleDf.precinct.unique()
            unmatchedSorted = [s for s in unmatchedSorted if ';' not in s]
            unmatchedUnsorted = utroubleDf.precinct.unique()

            sortedToUnsortedMap = getPotentialMap(countyDf, ucountyDf)
                
            #Figure out which keys are left in countyIdMap
            handle = list(countyIdMap.keys())
            handle = [h for h in handle if h not in sortedToUnsortedMap.keys()]
            for v in sortedToUnsortedMap.values():
                handle = [h for h in handle if h not in v]
            actualPrecincts = list(countyIdMap.keys())
            crossing = [l for l in countyIdMap.keys() if l in unmatchedUnsorted]
            handle = [h for h in handle if h not in crossing]
            #---------------------------------------------
            
            if len(handle)>0:
                if election == "US SENATE":
                    print 'handle', handle  
                hopefulMatches = getHopefulMatches(handle, unmatchedSorted)
                sortedToUnsortedMap = {s:sortedToUnsortedMap[s] for s in 
                                       sortedToUnsortedMap.keys() if s not in hopefulMatches.keys()}
                
            #note
            outData, alpha = distributeVotes(countyDf, ucountyDf, sortedToUnsortedMap, 
                                      countyIdMap, outData, election, c.upper())
            if len(handle) > 0:
                pTroubleDf = prepareElectionData(troubleDf)
                splitPrecincts = getSplitPrecincts(pTroubleDf, hopefulMatches,
                                                       countyIdMap, C2Reg[clusterName])
                for split in splitPrecincts:
                    outData[countyIdMap[split]] = splitPrecincts[split]
                    
        else:
            print 'ERROR: Check Granularity'
    
    
    preppedDataFrame = pd.DataFrame(outData)
    
    preppedDataFrame.columns = ['DEM', 'REP', "TOTAL"]
    
    errors = [d for d in outData if len(d) == 1]
    if len(errors) > 0:
        print 'ERROR: Need to fill index', errors
    return preppedDataFrame

def saveData(df, cluster, election):
    filename = clusterDir + cluster + "/"+ cluster +"_"+election+".txt"
    df.to_csv(filename, sep = '\t', header = None)
    
def mapVotes(countyDf, ucountyDf):
    sorted = countyDf.precinct.unique().tolist()
    unsorted = ucountyDf.precinct.unique().tolist()
    
    uvoteMap = {}    
    for key in unsorted:
        precinctDf = ucountyDf[ucountyDf.precinct  == key]
        uvoteMap[key] = {"DEM": 0, "REP": 0, 'TOTAL': 0}
        uvoteMap[key]["TOTAL"] = sum(precinctDf.votes)
        for voteType in ["DEM", "REP"]:
            precinctPartyDf = precinctDf[precinctDf.candidate == voteType]
            votes = sum(precinctPartyDf.votes.tolist())
            uvoteMap[key][voteType] += votes 
            
    voteMap = {}    
    for key in sorted:
        precinctDf = countyDf[countyDf.precinct  == key]
        voteMap[key] = {"DEM": 0, "REP": 0, 'TOTAL': 0}
        voteMap[key]["TOTAL"] = sum(precinctDf.votes)
        for voteType in ["DEM", "REP"]:
            precinctPartyDf = precinctDf[precinctDf.candidate == voteType]
            votes = sum(precinctPartyDf.votes.tolist())
            voteMap[key][voteType] += votes  
            
    return voteMap, uvoteMap 

def distributeVotes(countyDf, ucountyDf, sortedToUnsortedMap, countyIdMap, 
                    outData, election, county):
    
    alpha = -1.0
    voteMap, uvoteMap = mapVotes(countyDf, ucountyDf)
    GROWTH_RATES = []    #The growth rate of each precinct from unsorted to sorted
    readjustMap = {}
    
    #Handling standard keys
    for skey in sortedToUnsortedMap.keys():
        ukey = sortedToUnsortedMap[skey]
        if len(ukey) > 1:
            if len(ukey) >1:
                readjustMap[skey] = ukey

            continue
            
        elif len(ukey) == 1:
            uk = ukey[0]
            index = countyIdMap[uk]
            keyMap = voteMap[skey]
            dem, rep, total = keyMap["DEM"], keyMap["REP"], keyMap["TOTAL"]
            outData[index] = [dem, rep, total]
            #Track localAlpha
            unkeyMap = uvoteMap[uk]
            unDem, unRep, unTotal = unkeyMap["DEM"], unkeyMap["REP"], unkeyMap["TOTAL"]
            localAlpha = total/float(unTotal)
            GROWTH_RATES.append(localAlpha)
        else:
            print 'skey', skey
            print 'ukey', ukey

    if len(GROWTH_RATES) > 0:
        alpha = np.mean(GROWTH_RATES)
    else:
        print 'WARNING: There are no localAlpha values'


    #-------------------------------
    #Assigning votes to the ukeys from a single skey
    
    for adjKey in readjustMap.keys():
        #This is the upper limit on the 
        adjkeyMap = voteMap[adjKey]
        maxDem, maxRep, maxTotal = adjkeyMap["DEM"], adjkeyMap["REP"], adjkeyMap["TOTAL"]
        ukeySet = readjustMap[adjKey] 
        newUVotesMap = {}
        for uk in ukeySet:
            
            ukeyMap = uvoteMap[uk]
            uDem, uRep, uTotal = ukeyMap["DEM"], ukeyMap["REP"], ukeyMap["TOTAL"]
            newDem, newRep, newTotal = [alpha*votes for votes in [uDem, uRep, uTotal]]
            maxDem -= newDem
            maxRep -= newRep
            maxTotal -= newTotal
            newUVotesMap[uk] = [int(newDem+.5), int(newRep+.5), int(newTotal+.5)]
            
        if maxDem >= 0 and maxRep >= 0 and maxTotal >= 0:
            for uk in ukeySet:
                index = countyIdMap[uk]
                outData[index] = newUVotesMap[uk]
        else:
            corrections = [maxDem, maxRep, maxTotal]
            sortedVotes = voteMap[adjKey]
            sortedVotes = [sortedVotes[vote] for vote in ['DEM', "REP", 'TOTAL']]
            correctionAlphas = [sortedVotes[i]/float( (-1*corrections[i]) + sortedVotes[i])
                               for i in range(len(sortedVotes))]
            for uk in ukeySet:
                oldVotes = newUVotesMap[uk]
                newVotes = [int(oldVotes[i]*correctionAlphas[i]+.5) for i in range(len(oldVotes))]
                index = countyIdMap[uk]
                outData[index] = newVotes  
    return outData, alpha

def filterUnsorted(ucdf, properPrecincts, actualPrecincts, trouble):
    weirdPrecinctDf = takeAwayPrecincts(ucdf, actualPrecincts)
    weirdPrecincts = weirdPrecinctDf.precinct.unique().tolist()
    filterList = weirdPrecincts + properPrecincts
    filterList = [f for f in filterList if f not in trouble]
    utroubleDf = takeAwayPrecincts(ucdf, filterList)
    return utroubleDf


def checkPrecincts(cdf, ucdf, countyIdMap):
    actualPrecincts = countyIdMap.keys()
    actualPrecincts = [p.split("_")[0] for p in actualPrecincts]
    troubleDf = takeAwayPrecincts(cdf, actualPrecincts)
    #Find troublesome precincts
    trouble = troubleDf.precinct.unique().tolist()
    #Remove troublesome precincts
    properDf = takeAwayPrecincts(cdf, trouble)
    properPrecincts = properDf.precinct.unique().tolist()
    utroubleDf = filterUnsorted(ucdf, properPrecincts, actualPrecincts, trouble)
    return properDf, troubleDf, utroubleDf

def healPrecincts(troubleDf, utroubleDf, county):
    trouble = troubleDf.precinct.unique()
    utrouble = utroubleDf.precinct.unique()
    troubleKeys = {}
    found = []
    for t in trouble:
        if ";" in t:
            troubleKeys[t] = t.split(';')
            troubleKeys[t] = [p for p in troubleKeys[t] if p in utrouble]
            found         += [p for p in troubleKeys[t] if p in utrouble]
    if county == "GASTON":
        print county
        troubleKeys = {'38;43' :['39', '43']}
        found      += ['39', '43']
    if county == "ROBESON":
        print county
        troubleKeys = {'03;5;11A;38;PROV':['03', '15', '11A', '38']}
        found      += ['03', '15', '11A', '38']
        
    unmatched = [k for k in utrouble if k not in found]
    
    return unmatched



clusters = os.listdir(clusterDir)
clusters = [c for c in clusters if "." not in c]


C2Reg = {}

for c in clusters:
    rVoters = open(clusterDir + c + "/" + c+"_VOTEREGISTRATION.txt")
    data = rVoters.readlines()
    allVotes = range(len(data))
    for i in range(len(data)):
        line = data[i].split("\t")
        allVotes[i] = [int(v) for v in line[1:-1]]
    C2Reg[c] = allVotes
    rVoters.close()

countyGranularity = {}
for c in clusters:
    cSplit = c.split("_")
    i = 0
    while i < len(cSplit)-1:
        countyGranularity[cSplit[i].upper()] = cSplit[i+1]
        i += 2
        
pdFile = pd.read_csv("results_sort_20161108.txt", sep = '\t')
df = pd.DataFrame(pdFile)
unsortedFile = pd.read_csv("results_pct_20161108.txt", sep = '\t')
udf = pd.DataFrame(unsortedFile)
#County Fips
fipFile = pd.read_csv("../StateData/CountyFIPsCodes.txt", sep = '\t', header = None)
CountyToFIPdf = pd.DataFrame(fipFile)
CountyToFIPdf.columns = ['county', 'fip']
C2FIP = {}
for i in range(len(CountyToFIPdf)):
    C2FIP[CountyToFIPdf.iloc[i, 0].upper()] = str(CountyToFIPdf.iloc[i, 1])[2:]    


df = df[['county_desc', 'precinct_code', 'contest_name', 'candidate_name', 'votes']]
df.columns = ['county','precinct','contest','candidate','votes']
udf = udf[['County','Precinct','Contest Name','Choice','Choice Party',
             'Total Votes']]
udf.columns = ['county','precinct','contest','candidate','party','votes']


partyDF = udf[['party', "candidate"]]
partyDF = partyDF.drop_duplicates()

partyMap = {}
noParty = set()
for i in range(len(partyDF)):
    if partyDF.iloc[i,0] == "DEM" or partyDF.iloc[i,0] == "REP":
        partyMap[partyDF.iloc[i,1]] = partyDF.iloc[i,0]
    else:
        partyMap[partyDF.iloc[i,1]] = 'UN'
elections = ['NC GOVERNOR','US PRESIDENT','US SENATE','NC COMMISSIONER OF INSURANCE']

electionName ={'NC GOVERNOR':"GOV16",'US PRESIDENT':"PRES16",'US SENATE':"SEN16",
               'NC COMMISSIONER OF INSURANCE':"COI16"}

df = filterElections(df, partyMap)
udf = filterElections(udf, partyMap)



rubbish = []
for cluster in clusters:
    print "---------------------------"
    print cluster
    cdf  = getClusterDf(df,  cluster)
    ucdf = getClusterDf(udf, cluster)
    #note
    if True:
        for election in elections:
            #print election
            eDf  = getElectionDf(cdf,  election)
            ueDf = getElectionDf(ucdf, election)
            dataDF = prepareOutput(eDf, ueDf, cluster, election)

            saveData(dataDF, cluster, electionName[election])
    else:
        try:
            for election in elections:
                eDf  = getElectionDf(cdf,  election)
                ueDf = getElectionDf(ucdf, election)
                dataDF = prepareOutput(eDf, ueDf, cluster, election)
                saveData(dataDF, cluster, electionName[election])
        except Exception as e:
            print 
            print "ERROR FOUND:", e
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            print
            rubbish.append(cluster)

print
print "---------------------------"
print "done"
