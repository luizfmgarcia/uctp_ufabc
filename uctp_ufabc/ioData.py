# Data Input/Output Methods

import objects
import uctp
import csv
import os
import shutil
import cProfile
import pstats
import io

# Set '1' to allow, during the run, the print on terminal of some steps
printSteps = 0

#==============================================================================================================
# GLOBAL VARIABLES - Patterns

# In/Output directories' names
mainOutputDirName = 'results'
currOutputDirName = 'run'
inputDirPathName = 'workdata'

# In/Output directories' path
rootDirPath = os.getcwd()
inputDirPath = rootDirPath + os.sep + inputDirPathName + os.sep
mainOutputDirPath = rootDirPath + os.sep + mainOutputDirName + os.sep
currOutputDirPath = ''
currOutputDirNum = '_'

# In/Output Files names
MMA_FileName = 'totalMinMaxAvg'
professors_FileName = 'professors.csv'
subjects_FileName = 'subjects.csv'
runInfo_FileName = 'runInfo_cProfile'

# Main titles to output data
titles1_objFeat = ['sLevel', 'sCode', 'sName', 'sQuadri', 'sPeriod', 'sCampus', 'sCharge', 'sTimetableList','pName', 
                        'pPeriod', 'pCharge', 'pQuadriSabbath', 'pPrefCampus', 'pPrefSubjQ1List', 'pPrefSubjQ2List', 
                        'pPrefSubjQ3List', 'pPrefSubjLimList']
titles2_bestSolFeat = ['pName', 'numSubj', 'notPrefRestr', '/Relax', 'notPeriod', 'isSabbath', 'notCampus', 'numI2', 
                            'numI3', 'difCharge']
titles3_configVar = ['maxNum_Iter', 'maxNumCand_perPop', 'numCandInit', 'convergDetect', 'stopFitValue', 'pctParentsCross', 'pctMut_childCross', 
                    'pctElitism', 'w_alpha', 'w_beta', 'w_gamma', 'w_delta', 'w_omega', 'w_sigma', 'w_pi', 'w_rho', 
                    'w_lambda', 'w_theta']

#==============================================================================================================

# Get current directory and (re)create new mainOutputDirPath directory - may delete past 'runs' data
def startOutputDirs():
    # Verify if already exists main folder
    if not os.path.exists(mainOutputDirPath): os.makedirs(mainOutputDirPath)
    else:
        # Ask to user if wants to delete past 'runs' folders/files
        ask = 'a'
        while(ask != "y" and ask != "Y" and ask != ""): 
            ask = input("Do you want to erase old results? Yes('y')/No('Enter'): ")
        if(ask == "y" or ask == "Y"):
            shutil.rmtree(mainOutputDirPath)
            os.makedirs(mainOutputDirPath)
    
    # Creating a new folder for this run
    global currOutputDirPath, currOutputDirNum
    i = 0
    while(os.path.exists(mainOutputDirPath + currOutputDirName + currOutputDirNum + str(i))): i = i + 1
    currOutputDirNum = currOutputDirNum + str(i)
    currOutputDirPath = mainOutputDirPath + currOutputDirName + currOutputDirNum + os.sep
    os.makedirs(currOutputDirPath)

    # Starting the MAIN OUT CSV with the titles (MinMaxAvg)
    outName = currOutputDirPath + MMA_FileName + currOutputDirNum + '.csv'
    with open(outName, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Pop', 'Iter', 'Min', 'Max', 'Avg'])
    # if(printSteps == 1): print("Created: " + outName + "in" + newDir + "...")
    csvfile.close()

#==============================================================================================================
    
# Get all data to work with
def getData(subjList, profList):
    getDataProf(profList)
    getDataSubj(subjList)
    if(printSteps == 1): print("Data Obtained!")
    
#==============================================================================================================

# Read the data of Professors and create the respective objects
def getDataProf(profList):
    if(printSteps == 1): print("Getting data of Professors...", end='')
    with open(inputDirPath + professors_FileName, encoding='unicode_escape') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        if(printSteps == 1): print("Setting Professors...")
        for row in spamreader:
            # Transform every letter to upper case to impose a pattern
            obtainedData = [row[0].upper(), row[1].upper(), row[2].upper(), row[3].upper(), row[4].upper(), row[5].upper(), 
                     row[6].upper(), row[7].upper(), row[8].upper()]
            # Verify if exist some important blank data (data 0 to 4)
            if((not obtainedData[0] == '') and (not obtainedData[1] == '') and (not obtainedData[2] == '') and (not obtainedData[3] == '') and (not obtainedData[4] == '')):
                # Separating the Subjects Pref., transforming into lists (data 5 to 8)
                obtainedData[5] = obtainedData[5].split('/')
                obtainedData[6] = obtainedData[6].split('/')
                obtainedData[7] = obtainedData[7].split('/')
                obtainedData[8] = obtainedData[8].split('/')
                # Creating and saving a new Prof.
                profList.append(objects.Prof(obtainedData[0], obtainedData[1], obtainedData[2], obtainedData[3], obtainedData[4], obtainedData[5], obtainedData[6], obtainedData[7], obtainedData[8]))
                #if(printSteps == 1): print(obtainedData)
            else:
                if(printSteps == 1):
                    print("This professor register has some missing data! It will not be used.")
                    print(obtainedData)
    csvfile.close()

#==============================================================================================================

# Read the data of Subjects and create the respective objects
def getDataSubj(subjList):
    if(printSteps == 1): print("\nGetting data of Subjects...", end='')
    with open(inputDirPath + subjects_FileName, encoding='unicode_escape') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        if(printSteps == 1): print("Setting Subjects...")
        
        for row in spamreader:
            # Transform every letter to upper case to impose a pattern
            obtainedData = [row[0].upper(), row[1].upper(), row[2].upper(), row[3].upper(), row[4].upper(), row[5].upper(), 
                     row[6].upper(), row[7].upper(), row[8].upper()]
            
            # Verify if exist some important blank data (rows 0 to 8)
            if((not obtainedData[0] == '') and (not obtainedData[1] == '') and (not obtainedData[2] == '') and (not obtainedData[3] == '') and (not obtainedData[4] == '') 
                and (not obtainedData[5] == '') and (not obtainedData[6] == '') and (not obtainedData[7] == '#N/D') and (not obtainedData[8] == '#N/D')):
                # Choose some specifics subjects
                if(obtainedData[0] == 'G' and ('MCTA' in obtainedData[1] or 'MCZA' in obtainedData[1])):
                    # Separating the Timetables of Subj. and transforming into lists of lists: [...,[day/hour/frequency],...] - (data 7 and 8)
                    t0 = []
                    
                    # Theory classes
                    if(not obtainedData[7] == '0'):
                        t1 = obtainedData[7].split('/')
                        for r in t1:
                            day_rest = r.split(' DAS ')
                            hour_room_freq = day_rest[1].split(', ')
                            # Take only: day, hour and freq.
                            if(' E ' in hour_room_freq[2]): final = [day_rest[0], hour_room_freq[0], 'SEMANAL']
                            else: final = [day_rest[0], hour_room_freq[0], hour_room_freq[2]]
                            t0.append(final)
                    
                    # Practice classes
                    if(not obtainedData[8] == '0'):
                        t2 = obtainedData[8].split('/')
                        for r in t2:
                            day_rest = r.split(' DAS ')
                            hour_room_freq = day_rest[1].split(', ')
                            # Take only: day, hour and freq.
                            if(' E ' in hour_room_freq[2]): final = [day_rest[0], hour_room_freq[0], 'SEMANAL']
                            else: final = [day_rest[0], hour_room_freq[0], hour_room_freq[2]]
                            t0.append(final)
                    
                    # Putting t0 (list of lists of timetables back into 'obtainedData'
                    obtainedData[7] = t0
                    # Removing obtainedData[8] that is not useful
                    obtainedData.pop(8)
                    # Creating and saving the new Subj.
                    subjList.append(objects.Subject(obtainedData[0], obtainedData[1], obtainedData[2], obtainedData[3], obtainedData[4], obtainedData[5], obtainedData[6], obtainedData[7]))
                    #if(printSteps == 1): print(obtainedData)
            else:
                if(printSteps == 1): print("This subject register has some missing data! It will not be used.")
                if(printSteps == 1): print(obtainedData)
    csvfile.close()

#==============================================================================================================

# Start Record Run Info with cProfile
def startRunData():
    runProfile = cProfile.Profile()
    runProfile.enable()
    return runProfile

# Output run data obtained by cProfile
def outRunData(runProfile):
    runProfile.disable()
    s = io.StringIO()
    ps = pstats.Stats(runProfile, stream=s).sort_stats('tottime')
    ps.print_stats()
    outName = currOutputDirPath + runInfo_FileName + currOutputDirNum + '.txt'
    with open(outName, 'w+') as f: f.write(s.getvalue())

#==============================================================================================================

# Extract information - auxiliary function to gathering all important info of a solution
def extractInfo(cand, profList, subjList, subjIsPrefList):
    # Collecting Profs names in 'profList'
    profData = [p.get() for p in profList]
    profName = [pName for pName, _, _, _, _, _, _, _, _ in profData]

    # Getting others info
    prof_relationsList, i2_conflictsList, i3_conflictsList = cand.getInfVariables()
    prof_relationsList, numSubjPrefList, periodPrefList, quadSabbNotPrefList, campPrefList, difChargeList = cand.getFeaVariables()
    
    # If does not have some of the FeaVariables - probably the Cand is Infeasible
    if(len(difChargeList) == 0): _, difChargeList = uctp.calc_f1(subjList, profList, prof_relationsList)
    if(len(numSubjPrefList) == 0): _, numSubjPrefList = uctp.calc_f2(subjList, profList, prof_relationsList, subjIsPrefList)
    if(len(quadSabbNotPrefList) == 0): _, quadSabbNotPrefList = uctp.calc_f3(subjList, profList, prof_relationsList)
    if(len(periodPrefList) == 0): _, periodPrefList = uctp.calc_f4(subjList, profList, prof_relationsList)
    if(len(campPrefList) == 0): _, campPrefList = uctp.calc_f5(subjList, profList, prof_relationsList)
    # Counting the relaxed number of subjPref for each Prof (Considering subj of preference but not same Quadri)
    relaxedList = [sum([1 for j in prof_relationsList[i] if subjIsPrefList[i][j] != 0]) for i in range(len(prof_relationsList))]
    
    # Extracting the number of each occurrence for each professor and its relations
    # [profName, numSubjs, numSubjNotPrefered, numPeriodNotPref, numQuadriSabbathPref, numCampusNotPref, numI2, numI3, difCharge]
    info = [[profName[i],
            len(prof_relationsList[i]), 
            len(prof_relationsList[i]) - numSubjPrefList[i], 
            len(prof_relationsList[i]) - relaxedList[i], 
            len(prof_relationsList[i]) - len(periodPrefList[i]), 
            len(prof_relationsList[i]) - len(quadSabbNotPrefList[i]), 
            len(prof_relationsList[i]) - len(campPrefList[i]),
            len(i2_conflictsList[i]), 
            len(i3_conflictsList[i]), 
            difChargeList[i]] for i in range(len(profList))]
        
    # Last line sums all professors data
    total = ['Total'] + [0 for _ in range(len(info[0]) - 1)]
    for j in range(1, len(total)): total[j] = sum([i[j] for i in info])
    info.append(total)

    return  info

#==============================================================================================================

# Put out on 'totalMinMaxAvg.csv' the current generation Min/Max/Avg Fitness
def outDataMMA(solutionsI, solutionsF, iter):
    if(printSteps == 1): print("Exporting data....", end='')
    
    # Find Min/Max Fitness in the Infeasible Pop.
    minFitInf, maxFitInf, avgFitInf = 0, -1, 0
    for cand in solutionsI.getCandList():
        avgFitInf = avgFitInf + cand.getFitness()
        if(cand.getFitness() > maxFitInf): maxFitInf = cand.getFitness()
        if(cand.getFitness() < minFitInf): minFitInf = cand.getFitness()
    if(len(solutionsI.getCandList()) != 0): avgFitInf = avgFitInf / len(solutionsI.getCandList())
    
    # Find Min/Max Fitness in the Feasible Pop.
    minFitFea, maxFitFea, avgFitFea = 1, 0, 0
    maxFitFeaIndex = [] # Recording the best solutions found
    for cand in solutionsF.getCandList():
        avgFitFea = avgFitFea + cand.getFitness()
        if(cand.getFitness() == maxFitFea):
            maxFitFeaIndex.append(solutionsF.getCandList().index(cand))
        if(cand.getFitness() > maxFitFea):
            maxFitFea = cand.getFitness()
            maxFitFeaIndex = [solutionsF.getCandList().index(cand)]
        if(cand.getFitness() < minFitFea):
            minFitFea = cand.getFitness()
    if(len(solutionsF.getCandList()) != 0): avgFitFea = avgFitFea / len(solutionsF.getCandList())
    
    # Get 'currOutputDirPath' and CSV file to be modified with current generation Min/Max Fitness
    outName = currOutputDirPath + MMA_FileName + currOutputDirNum + '.csv'
    with open(outName, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        if(minFitInf != 0): spamwriter.writerow(['Inf', iter, minFitInf, maxFitInf, avgFitInf])
        if(minFitFea != 1): spamwriter.writerow(['Fea', iter, minFitFea, maxFitFea, avgFitFea])
    csvfile.close()

    if(printSteps == 1): print("Data Exported!")
    
    return maxFitFeaIndex, minFitInf, maxFitInf, avgFitInf, minFitFea, maxFitFea, avgFitFea

#==============================================================================================================

# Export all Candidates in a generation into CSV files
# Create a CSV File for each Candidate and one CSV to gather the Fitness of all Candidates:
def outDataGeneration(solutionsI, solutionsF, num, profList, subjList, subjIsPrefList):
    if(printSteps == 1): print("Exporting all Generation (Solutions) data....", end='')
    
    # In 'currOutputDirPath', create new 'gen' Dir.
    newDir = currOutputDirPath + 'Gen' + str(num) + os.sep
    if not os.path.exists(newDir): os.makedirs(newDir)
    
    # Each population, that will be iterate, info
    pop, typePop = [solutionsI.getCandList(), solutionsF.getCandList()], ['Inf', 'Fea']

    # Each population
    for j in range(len(pop)):
        # All Candidates
        for i in range(len(pop[j])):
            # Start output info of the solution
            outName = newDir + 'Gen' + str(num) + '_cand' + typePop[j] + str(i) + '.csv'
            with open(outName, 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)

                # All relations in a Candidate of a Generation
                spamwriter.writerow(titles1_objFeat)
                for s, p in pop[j][i].getRelationsList():
                    row = s.get() + p.get()
                    spamwriter.writerow(row)
                spamwriter.writerow(" ")
                
                # Fitness information
                spamwriter.writerow([typePop[j], pop[j][i].getFitness()])
                spamwriter.writerow(" ")
                
                # Extracting all important info to analyze the quality of the solution
                info = extractInfo(pop[j][i], profList, subjList, subjIsPrefList)
                # Output extra information for analysis
                spamwriter.writerow(titles2_bestSolFeat)
                for row in info: spamwriter.writerow(row)
            csvfile.close()
            i = i + 1
    
    # Output all Fitness in a Generation
    outName = newDir + 'gen' +  str(num) + '.csv'
    with open(outName, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        
        spamwriter.writerow(['Candidate', 'Population', 'Fitness'])
        for j in range(len(pop)):
            for i in range(len(pop[j])): spamwriter.writerow([i, typePop[j], pop[j][i].getFitness()])
    csvfile.close()

    if(printSteps == 1): print("All Generation (Solutions) data Exported!")
    
#==============================================================================================================

def finalOutData(solutionsI, solutionsF, num, profList, subjList, subjIsPrefList, maxFitFeaIndex=[], configVarList=[]):
    print("Exporting final data....", end='')
        
    # Output Run-Config and Final best results (different of each other)
    outName = currOutputDirPath + 'runConfigResult' + currOutputDirNum + '.csv'
    with open(outName, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        
        # All Config info
        for i in range(len(titles3_configVar)): spamwriter.writerow([titles3_configVar[i], configVarList[i]])
        spamwriter.writerow('')

        # Some variables that maybe will be used
        maxCand, fitMaxData, maxData, resumeMaxData, maxInfo, info_alreadyShow = [], [], [], [], [], []
        
        # If feasible solutions were found
        if(len(maxFitFeaIndex)!=0):
            # Lists of data of all different solutions with same max fit found
            # Every feasible solution with same max fit
            for m in range(len(maxFitFeaIndex)):
                # Getting the solution and its fitness
                maxCand.append(solutionsF.getCandList()[maxFitFeaIndex[m]])
                # Getting and recording its data
                fitMaxData.append(maxCand[m].getFitness())
                maxData.append([s.get() + p.get() for s, p in maxCand[m].getRelationsList()])
                maxInfo.append(extractInfo(maxCand[m], profList, subjList, subjIsPrefList))

                # Checks if is different from something that was already output
                if(info_alreadyShow.count(maxInfo[m]) == 0): 
                    # Adding to Lists
                    info_alreadyShow.append(maxInfo[m])
                    # Resuming the result to show only 'sName' and 'pName' of each relation
                    resumeMaxData.append([[row[2], row[8]] for row in maxData[m]])

                    # Best Feasible Solution info
                    if(m == 0): spamwriter.writerow(["Best solutions found:", maxFitFeaIndex])
                    spamwriter.writerow(["Index/Fit:", maxFitFeaIndex[m], fitMaxData[m]])
                    spamwriter.writerow('')
                    
                    # sName + pName
                    spamwriter.writerow(['index', titles1_objFeat[2], titles1_objFeat[8]])
                    for i in range(len(resumeMaxData[-1])): spamwriter.writerow([i+1] + resumeMaxData[-1][i])
                    
                    # Extracted Info of one of the best Solutions found
                    spamwriter.writerow('')
                    spamwriter.writerow(titles2_bestSolFeat)
                    for i in range(len(maxInfo[m])): spamwriter.writerow([i+1] + maxInfo[m][i])
                    
                    # All Details of same solution
                    spamwriter.writerow('')
                    spamwriter.writerow(titles1_objFeat)
                    for row in maxData[m]: spamwriter.writerow(row)
                    spamwriter.writerow('')    

        else: spamwriter.writerow("Do not found feasible solutions.")
    csvfile.close()

    # Showing important Info on terminal for user
    print("Final Data Exported!", '\n')
    
    return fitMaxData, resumeMaxData, maxInfo
        
#==============================================================================================================

# First print of a round
def printHead(profList, subjList, curr_Iter, maxNum_Iter, firstFeasSol_Iter, lastMaxFitFea_Iter):
    if(curr_Iter == 0): print("\nStarting hard work...\n")
    print('Iteration:', curr_Iter, 'of', maxNum_Iter, '/ Working with (Prof/Subj):', len(profList), '/', len(subjList))
    if(firstFeasSol_Iter != -1):
        print('First Feas Sol at (iter): ', firstFeasSol_Iter, '/ Cur Max Feas Sol at (iter): ', lastMaxFitFea_Iter, '/ Num Iter since last Max:', curr_Iter - lastMaxFitFea_Iter)

#==============================================================================================================

# Last print of a round
def printTail(solutionsI, solutionsF, minFitInf, maxFitInf, avgFitInf, minFitFea, maxFitFea, avgFitFea):
    if(minFitInf != 0): print('Infeasibles (', len(solutionsI.getCandList()), ') Min:', minFitInf, 'Max:', maxFitInf, 'Avg:', avgFitInf)
    else: print('No Infeasibles Solutions!')
    if(minFitFea != 1): print('Feasibles (', len(solutionsF.getCandList()), ') Min:', minFitFea, 'Max:', maxFitFea, 'Avg:', avgFitFea)
    else: print('No Feasibles Solutions!')
    print("")

#==============================================================================================================

# Print (Config + First best solution found) Info
def printFinalResults(configVarList, maxFitFeaIndex, fitMaxData, resumeMaxData, maxInfo):
    import pandas
    # Printing the Run-Config
    print("Run-Config values of the algorithm:")
    with pandas.option_context('display.max_rows', 999):
        print(pandas.DataFrame(data=[[titles3_configVar[i], configVarList[i]] for i in range(len(configVarList))], columns=['config', 'value'], index=None), '\n')
    
    # Printing one of the best solutions found
    if(len(maxFitFeaIndex)!=0):
        print("These are the best solutions found:", maxFitFeaIndex[0])
        print("Index/Fit:", maxFitFeaIndex[0], '/', fitMaxData[0])
        with pandas.option_context('display.max_rows', 999):
            print(pandas.DataFrame(data=resumeMaxData[0], index=None, columns=[titles1_objFeat[2], titles1_objFeat[8]]), '\n')
            print(pandas.DataFrame(data=maxInfo[0], index=None, columns=titles2_bestSolFeat), '\n')       

#==============================================================================================================

# Print all Obj data in a list
def printObjDataList(objList):
    for i in objList: print(i.get())

#==============================================================================================================

# Print all Prof's Subj Preference
def printSubjPref(profList, subjList, subjIsPrefList):
    for pIndex in range(len(profList)):
        # Getting data of current Prof
        pName, _, _, _, _, _, _, _, _ = profList[pIndex].get()
        # All Relations of one Prof
        for sIndex in range(len(subjList)):
            # Getting data of current Subj
            _, _, sName, _, _, _, _, _ = subjList[sIndex].get()
            if(subjIsPrefList[pIndex][sIndex]!=0): print(pName, sName, subjIsPrefList[pIndex][sIndex])

#==============================================================================================================
       
# Print all data of a Candidate (Professor-Subject Relations)
def printOneCand(candidate):
    i = 0
    for s, p in candidate.getRelationsList():
        print(i, s.get(), p.get())
        i = i + 1

#==============================================================================================================

# Print the data of all Candidates (Professor-Subject Relations) of a generation
def printAllCand(solutionsI=None, solutionsF=None):
    for cand in solutionsI.getCandList(): printOneCand(cand)
    for cand in solutionsF.getCandList(): printOneCand(cand)
    print("--------")
        
#==============================================================================================================

# Print MinMaxAvg Fitness of a generation
def printMMAFit(solutionsI=None, solutionsF=None):
    minFitInf, maxFitInf, avgFitInf = 0, -1, 0
    # Find Min/Max Fitness in the Infeasible Pop.
    for cand in solutionsI.getCandList():
        avgFitInf = avgFitInf + cand.getFitness()
        if(cand.getFitness() > maxFitInf): maxFitInf = cand.getFitness()
        if(cand.getFitness() < minFitInf): minFitInf = cand.getFitness()
    if(len(solutionsI.getCandList()) != 0): avgFitInf = avgFitInf / len(solutionsI.getCandList())
    
    minFitFea, maxFitFea, avgFitFea = 1, 0, 0
    # Find Min/Max Fitness in the Feasible Pop.
    for cand in solutionsF.getCandList():
        avgFitFea = avgFitFea + cand.getFitness()
        if(cand.getFitness() > maxFitFea):
            maxFitFea = cand.getFitness()
        if(cand.getFitness() < minFitFea):
            minFitFea = cand.getFitness()
    if(len(solutionsF.getCandList()) != 0): avgFitFea = avgFitFea / len(solutionsF.getCandList())
    
    if(minFitInf != 0): print('Infeasibles - Num:', len(solutionsI.getCandList()), 'Min:', minFitInf, 'Max:', maxFitInf, 'Avg:', avgFitInf)
    else: print('No Infeasibles Solutions!')
    if(minFitFea != 1): print('Feasibles - Num:', len(solutionsF.getCandList()), 'Min:', minFitFea, 'Max:', maxFitFea, 'Avg:', avgFitFea)
    else: print('No Feasibles Solutions!')

#==============================================================================================================

# Print the Fitness of all candidates in a population
def printAllPopFit(solutions, text=''):
    if(len(solutions.getCandList()) != 0):
        print(text)
        for n in range(len(solutions.getCandList())): print(str(n), ': ', str(solutions.getCandList()[n].getFitness()), '/ ', end='')
    else: print('No Solutions in:' + text)

#==============================================================================================================