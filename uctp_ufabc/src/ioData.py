# Data Input/Output Methods

import objects
import uctp
import csv
import os
import io
import sys
import time
import shutil
import cProfile
import pstats
import pandas

# Set '1' to allow, during the run, the print on terminal of some steps
printSteps = 0

#==============================================================================================================
# GLOBAL VARIABLES - Patterns

# In/Output directories' names
mainOutputDirName = 'results'
currOutputDirName = 'run'
inputDirPathName = 'workdata'

# In/Output directories' path
rootDirPath = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
inputDirPath = rootDirPath + os.sep + inputDirPathName + os.sep
mainOutputDirPath = rootDirPath + os.sep + mainOutputDirName + os.sep
currOutputDirPath = ''
currOutputDirNum = '_'

# In/Output Files names
subjects_FileName = 'subjects.csv'
professors_FileName = 'professors.csv'
MMA_FileName = 'totalMinMaxAvg'
runInfo_FileName = 'runInfo_cProfile'
final_FileName = 'runConfigResult'

# Main titles to output data
titles1_objFeat = ['sLevel', 'sCode', 'sName', 'sQuadri', 'sPeriod', 'sCampus', 'sCharge', 'sTimetableList','pName', 
                    'pPeriod', 'pCharge', 'pQuadriSabbath', 'pPrefCampus', 'pPrefSubjQ1List', 'pPrefSubjQ2List', 
                    'pPrefSubjQ3List', 'pPrefSubjLimList']
titles2_bestSolFeat = ['pName', 'numSubj', 'notPrefRestr', '/Relax', 'notPeriod', 'isSabbath', 'notCampus', 'numI2', 
                    'numI3', 'difCharge']
titles3_configVar = ['maxNum_Iter', 'maxNumCand_perPop', 'convergDetect', 'pctParentsCross', 'pctElitism', 'twoPointsCross',
                    'reposCross', 'reposSelInf', 'reposSelFea', 'w_alpha', 'w_beta', 'w_gamma', 
                    'w_delta', 'w_omega', 'w_sigma', 'w_pi', 'w_rho', 'w_lambda', 'w_theta']

#==============================================================================================================

# Ask to user if wants to continue the run with more iterations
def askStop():
    ask = 'a'
    while(True):
        ask = input("How many more iterations? Yes(Positive Number) / No('Enter' or '0'): ")
        if(ask == ""): return True # If 'Enter'
        try:
            ask = int(ask)
            if(ask >= 0):
                if(ask == 0): return True # If Zero
                else: return ask # More iterations
        except ValueError: None

#==============================================================================================================

# Get current directory and (re)create new mainOutputDirPath directory - may delete past 'runs' data
def startOutputDirs(asks):
    # Verify if already exists main folder
    if not os.path.exists(mainOutputDirPath): os.makedirs(mainOutputDirPath)
    else:
        if(asks == 1): # If enabled the 'Ask'
            # Ask to user if wants to delete past 'runs' folders/files
            ask = 'a'
            while(ask != "y" and ask != "Y" and ask != ""): 
                ask = input("Do you want to erase old results? Yes('y')/No('Enter'): ")
            if(ask == "y" or ask == "Y"):
                shutil.rmtree(mainOutputDirPath)
                os.makedirs(mainOutputDirPath)
    
    # Creating a new folder for this run
    global currOutputDirPath, currOutputDirNum
    i = 1
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

# Get/Set CONFIG Values
def getConfig():
    #----------------------------------------------------------------------------------------------------------
    # Default CONFIGURATION

    # RUN CONFIG
    printSteps = 1 # Set '1' to allow, during the run, the print on terminal of some important steps
    asks = 1 # Set '1' to allow, during the run, some asks
    maxNum_Iter = 10000 # Max Number of iterations to get a solution
    maxNumCand_perPop = 20 # Number of candidates in a generation (same for each Pop Feas./Inf.)
    # Convergence Detector: number of iterations passed since last MaxFit found
    convergDetect = 500 # equal '0' to not consider this condition
 
    # OPERATORS CONFIG (Must be between '0' and '100')
    # Percentage of candidates from Feasible Pop. that will be selected, to become Parents and make Crossovers, through a Roulette Wheel with Reposition
    pctParentsCross = 80 # The rest (to complete 100%) will pass through Mutation
    pctElitism = 5 # Percentage of selection by elitism of feasible candidates, the rest of them will pass through a Roulette Wheel
    twoPointsCross = 1 # Crossover using 2 cut points (1), 1 cut Point (0), Random (-1)
    # Main Roulettes Reposition Config (1: True / 0: False)
    reposCross = 1
    reposSelInf = 0
    reposSelFea = 0

    # WEIGHTS CONFIG (must be Float)
    w_alpha = 1.0   # i1 - Prof without Subj
    w_beta = 1.0    # i2 - Subjs (same Prof), same quadri and timetable conflicts
    w_gamma = 1.0   # i3 - Subjs (same Prof), same quadri and day but in different campus
    
    w_delta = 0.25   # f1 - Balance of distribution of Subjs between Profs with each pCharge
    w_omega = 0.25   # f2 - Profs preference Subjects
    w_sigma = 0.25   # f3 - Profs with Subjs in quadriSabbath
    w_pi = 0.25      # f4 - Profs with Subjs in Period
    w_rho = 0.25     # f5 - Profs with Subjs in Campus
    w_lambda = 0.75  # f6 - Balance of distribution of Subjs between Profs with an average
    w_theta = 0.75   # f7 - Quality of relations (subj (not) appears in some list of pref or/and same quadriList)

    #----------------------------------------------------------------------------------------------------------
    # CONFIGURATION by Command Line
    if(len(sys.argv) > 3):
        printSteps, asks, maxNum_Iter, maxNumCand_perPop, convergDetect, pctParentsCross, pctElitism, twoPointsCross, reposCross, reposSelInf, reposSelFea, w_alpha, w_beta, w_gamma, w_delta, w_omega, w_sigma, w_pi, w_rho, w_lambda, w_theta = (value for value in sys.argv[1:])
    #----------------------------------------------------------------------------------------------------------

    return int(printSteps), int(asks), int(maxNum_Iter), int(maxNumCand_perPop), int(convergDetect), int(pctParentsCross), int(pctElitism), int(twoPointsCross), int(reposCross), int(reposSelInf), int(reposSelFea), float(w_alpha), float(w_beta), float(w_gamma), float(w_delta), float(w_omega), float(w_sigma), float(w_pi), float(w_rho), float(w_lambda), float(w_theta)

#==============================================================================================================

# Get all data to work with
def getData():
    profList = getDataProf()
    subjList = getDataSubj()
    if(printSteps == 1): print("Data Obtained!")
    return subjList, profList

#-------------------------------------------------------

# Read the data of Professors and create the respective objects
def getDataProf():
    # Base List
    profList = []

    if(printSteps == 1): print("Getting data of Professors...", end='')
    with open(inputDirPath + professors_FileName, encoding='unicode_escape') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        if(printSteps == 1): print("Setting Professors...")
        for row in spamreader:
            # Transform every letter to upper case to impose a pattern
            obtainedData = [row[0].upper(), row[1].upper(), row[2].upper(), row[3].upper(), row[4].upper(), row[5].upper(), 
                            row[6].upper(), row[7].upper(), row[8].upper()]
            # Verify if exist some important blank data (rows 0 to 4)
            if((not obtainedData[0] == '') and (not obtainedData[1] == '') and (not obtainedData[2] == '') and 
                (not obtainedData[3] == '') and (not obtainedData[4] == '')):
                # Separating the Subjects Pref., transforming into lists (rows 5 to 8)
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
    return profList

#-------------------------------------------------------

# Read the data of Subjects and create the respective objects
def getDataSubj():
    # Base List
    subjList = []

    if(printSteps == 1): print("\nGetting data of Subjects...", end='')
    with open(inputDirPath + subjects_FileName, encoding='unicode_escape') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        if(printSteps == 1): print("Setting Subjects...")
        for row in spamreader:
            # Transform every letter to upper case to impose a pattern
            obtainedData = [row[0].upper(), row[1].upper(), row[2].upper(), row[3].upper(), row[4].upper(), row[5].upper(), 
                            row[6].upper(), row[7].upper(), row[8].upper()]
            # Verify if exist some important blank data (rows 0 to 8)
            if((not obtainedData[0] == '') and (not obtainedData[1] == '') and (not obtainedData[2] == '') and 
                (not obtainedData[3] == '') and (not obtainedData[4] == '') and (not obtainedData[5] == '') and 
                (not obtainedData[6] == '') and (not obtainedData[7] == '#N/D') and (not obtainedData[8] == '#N/D')):
                # Choose some specifics subjects
                if(obtainedData[0] == 'G' and ('MCTA' in obtainedData[1] or 'MCZA' in obtainedData[1])):
                    # Separating the Timetables of Subj. and transforming into lists of lists: [...,[day/hour/frequency],...] - (rows 7 and 8)
                    tmtFinal = []
                    
                    # Theory classes
                    if(not obtainedData[7] == '0'):
                        tmtTheory = obtainedData[7].split('/')
                        for r in tmtTheory:
                            day_rest = r.split(' DAS ')
                            hour_room_freq = day_rest[1].split(', ')
                            # Take only: day, hour and freq.
                            if(' E ' in hour_room_freq[2]): final = [day_rest[0], hour_room_freq[0], 'SEMANAL']
                            else: final = [day_rest[0], hour_room_freq[0], hour_room_freq[2]]
                            tmtFinal.append(final)
                    
                    # Practice classes
                    if(not obtainedData[8] == '0'):
                        tmtPractice = obtainedData[8].split('/')
                        for r in tmtPractice:
                            day_rest = r.split(' DAS ')
                            hour_room_freq = day_rest[1].split(', ')
                            # Take only: day, hour and freq.
                            if(' E ' in hour_room_freq[2]): final = [day_rest[0], hour_room_freq[0], 'SEMANAL']
                            else: final = [day_rest[0], hour_room_freq[0], hour_room_freq[2]]
                            tmtFinal.append(final)
                    
                    # Putting tmtFinal (list of lists of timetables back into 'obtainedData'
                    obtainedData[7] = tmtFinal
                    # Removing obtainedData[8] that is not useful
                    obtainedData.pop(8)
                    # Creating and saving the new Subj.
                    subjList.append(objects.Subject(obtainedData[0], obtainedData[1], obtainedData[2], obtainedData[3], obtainedData[4], obtainedData[5], obtainedData[6], obtainedData[7]))
                    #if(printSteps == 1): print(obtainedData)
            else:
                if(printSteps == 1): print("This subject register has some missing data! It will not be used.")
                if(printSteps == 1): print(obtainedData)
    csvfile.close()
    return subjList

#==============================================================================================================

# Start Record Run Info with cProfile
def startRunData():
    runProfile = cProfile.Profile()
    runProfile.enable()
    return runProfile

#-------------------------------------------------------

# Output run data obtained by cProfile
def outRunData(runProfile):
    runProfile.disable()
    s = io.StringIO()
    ps = pstats.Stats(runProfile, stream=s).sort_stats('tottime')
    ps.print_stats()
    outName = currOutputDirPath + runInfo_FileName + currOutputDirNum + '.txt'
    with open(outName, 'w+') as f: f.write(s.getvalue())

#==============================================================================================================

# First print of a round
def printHead(profList, subjList, curr_Iter, maxNum_Iter, firstFeasSol_Iter, lastMaxFit_Iter, recordNumIter):
    if(curr_Iter == 1): print("\nStarting hard work...\n")
    print('Run:', currOutputDirNum[1:], 'Iteration:', curr_Iter, 'of', maxNum_Iter, '/ Working with (Prof/Subj):', len(profList), '/', len(subjList),
        '/ First Feas Sol at (iter): ' + str(firstFeasSol_Iter) if firstFeasSol_Iter != -1 else '')
    print('Cur Max Sol at (iter): ', lastMaxFit_Iter, '/ Num Iter since last Max:', curr_Iter - lastMaxFit_Iter,
        '/ Record Num Iter No New Max:', recordNumIter)

#-------------------------------------------------------

# Last print of a round
def printTail(solutionsI, solutionsF, minFitInf, maxFitInf, avgFitInf, minFitFea, maxFitFea, avgFitFea):
    if(minFitInf != 0): print('Infeasibles (', len(solutionsI.getCandList()), ') Min:', minFitInf, 'Max:', maxFitInf, 'Avg:', avgFitInf)
    else: print('No Infeasibles Solutions!')
    if(minFitFea != 1): print('Feasibles (', len(solutionsF.getCandList()), ') Min:', minFitFea, 'Max:', maxFitFea, 'Avg:', avgFitFea)
    else: print('No Feasibles Solutions!')
    print("")

#==============================================================================================================

# Get Min/Max/Avg Fitness of the current generation (iteration) - both Pop
def getDataMMA(solutionsI, solutionsF):
    if(printSteps == 1): print("Exporting data....", end='')
    
    maxFitIndexes = [] # Recording the index of the best solutions found
    
    # Find Min/Max Fitness in the Feasible Pop.
    minFitFea, maxFitFea, avgFitFea, sumFitFea = 1, 0, 0, 0
    for cand in solutionsF.getCandList():
        sumFitFea = sumFitFea + cand.getFitness() # Summing all fitness
        # If there is Feas. Solutions, record the best Fitness
        if(cand.getFitness() == maxFitFea):
            maxFitIndexes.append(solutionsF.getCandList().index(cand))
        # Updating the new 'maxFitFea' found
        if(cand.getFitness() > maxFitFea):
            maxFitFea = cand.getFitness()
            maxFitIndexes = [solutionsF.getCandList().index(cand)]
        # Updating the new 'minFitFea' found
        if(cand.getFitness() < minFitFea):
            minFitFea = cand.getFitness()
    # Get the average fitness
    if(len(solutionsF.getCandList()) != 0): avgFitFea = sumFitFea / len(solutionsF.getCandList())

    # Find Min/Max Fitness in the Infeasible Pop.
    minFitInf, maxFitInf, avgFitInf, sumFitInf = 0, -1, 0, 0
    for cand in solutionsI.getCandList():
        sumFitInf = sumFitInf + cand.getFitness() # Summing all fitness
        # If there is no Feas. Solutions, record the best Inf. Sol. Fitness
        if(len(solutionsF.getCandList()) == 0 and cand.getFitness() == maxFitInf):
            maxFitIndexes.append(solutionsI.getCandList().index(cand))
        # Updating the new 'maxFitInfea' found
        if(cand.getFitness() > maxFitInf):
            maxFitInf = cand.getFitness()
            if(len(solutionsF.getCandList()) == 0): maxFitIndexes = [solutionsI.getCandList().index(cand)]
        # Updating the new 'minFitInfea' found
        if(cand.getFitness() < minFitInf): minFitInf = cand.getFitness()
    # Get the average fitness
    if(len(solutionsI.getCandList()) != 0): avgFitInf = sumFitInf / len(solutionsI.getCandList())
    
    return maxFitIndexes, minFitInf, maxFitInf, avgFitInf, minFitFea, maxFitFea, avgFitFea

#-------------------------------------------------------

# Put out on 'MMA_FileName' the current generation Min/Max/Avg Fitness
def outDataMMA(minFitInf, maxFitInf, avgFitInf, minFitFea, maxFitFea, avgFitFea, iter):
    if(printSteps == 1): print("Exporting data....", end='')
    
    # Get 'currOutputDirPath' and CSV file to be modified with current generation Min/Max Fitness
    outName = currOutputDirPath + MMA_FileName + currOutputDirNum + '.csv'
    with open(outName, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        if(minFitInf != 0): spamwriter.writerow(['Inf', iter, minFitInf, maxFitInf, avgFitInf])
        if(minFitFea != 1): spamwriter.writerow(['Fea', iter, minFitFea, maxFitFea, avgFitFea])
    csvfile.close()

    if(printSteps == 1): print("Data Exported!")

#==============================================================================================================

# Extract information - auxiliary function to gathering all important info of a solution
def extractInfo(cand, profList, subjList, subjIsPrefList):
    # Collecting Profs names in 'profList'
    profName = [p.getName() for p in profList]

    # Getting other info
    prof_relationsList, i2_conflictsList, i3_conflictsList = cand.getInfVariables()
    prof_relationsList, numSubjPrefList, periodPrefList, quadSabbNotPrefList, campPrefList, difChargeList = cand.getFeaVariables()
    
    # If does not have some of the FeaVariables (probably if the Cand is Infeasible)
    if(len(difChargeList) == 0): _, difChargeList = uctp.calc_f1(subjList, profList, prof_relationsList)
    if(len(numSubjPrefList) == 0): _, numSubjPrefList = uctp.calc_f2(subjList, profList, prof_relationsList, subjIsPrefList)
    if(len(quadSabbNotPrefList) == 0): _, quadSabbNotPrefList = uctp.calc_f3(subjList, profList, prof_relationsList)
    if(len(periodPrefList) == 0): _, periodPrefList = uctp.calc_f4(subjList, profList, prof_relationsList)
    if(len(campPrefList) == 0): _, campPrefList = uctp.calc_f5(subjList, profList, prof_relationsList)
    
    # Counting the relaxed number of subjPref for each Prof (Considering too the subjs of preference that is not in same Quadri)
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
        
    # Last line its the sums all professors data
    total = ['Total'] + [0 for _ in range(len(info[0]) - 1)]
    for j in range(1, len(total)): total[j] = sum([i[j] for i in info])
    info.append(total)

    return info

#==============================================================================================================

# Output Run-Config Values and All Final best results
def finalOutData(solutionsI, solutionsF, profList, subjList, subjIsPrefList, curr_Iter, firstFeasSol_Iter, lastMaxFit_Iter, recordNumIter, final_time=0.0, maxFitIndexes=[], configVarList=[]):
    if(printSteps == 1): print("Exporting final data....", end='')

    # Output Info
    outName = currOutputDirPath + final_FileName + currOutputDirNum + '.csv'
    with open(outName, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        
        # All Config info/values
        for i in range(len(titles3_configVar)): spamwriter.writerow([titles3_configVar[i], configVarList[i]])

        spamwriter.writerow('')
        spamwriter.writerow(["Time (sec)", final_time]) # Time spent on run
        spamwriter.writerow(['Last Iter:', curr_Iter]) # Last Iteration
        if(firstFeasSol_Iter != -1): spamwriter.writerow(['First Feas Sol at (iter):', str(firstFeasSol_Iter)])
        else: spamwriter.writerow(['No Feas Sol Found'])
        spamwriter.writerow(['Last Max Sol Found at (iter):', lastMaxFit_Iter])
        spamwriter.writerow(['Record Num Iter No New Max:', recordNumIter])
        # All indexes of best solutions found
        spamwriter.writerow(["Best solutions found:", maxFitIndexes])
        spamwriter.writerow('')

        # Some variables that will be used
        bestSol_FitList, bestSol_ResumRelatList, bestSol_extractInfoList = [], [], []
        
        # Data of all solutions with same max fit found
        for m in range(len(maxFitIndexes)):
            # Getting the solution obj (Feasible or Infeasible)
            if(len(solutionsF.getCandList()) != 0): currCand = solutionsF.getCandList()[maxFitIndexes[m]]
            else: currCand = solutionsI.getCandList()[maxFitIndexes[m]]
            
            # Getting all important data
            bestSol_FitList.append(currCand.getFitness()) # Fitness
            currCand_RelList = [s.get() + p.get() for s, p in currCand.getRelationsList()] # Relations Complete
            bestSol_ResumRelatList.append([[row[2], row[8]] for row in currCand_RelList]) # Relations Resumed (only 'sName' and 'pName')
            bestSol_extractInfoList.append(extractInfo(currCand, profList, subjList, subjIsPrefList)) # Extracted Info

            # Recording data on file
            spamwriter.writerow(["Index/Fit:", maxFitIndexes[m], bestSol_FitList[m]]) # Best Feasible Solution info
            spamwriter.writerow('')
            spamwriter.writerow(['index', titles1_objFeat[2], titles1_objFeat[8]]) # sName + pName Info
            for i in range(len(bestSol_ResumRelatList[-1])): spamwriter.writerow([i+1] + bestSol_ResumRelatList[-1][i])
            spamwriter.writerow('')
            spamwriter.writerow(titles2_bestSolFeat) # Extracted Info of current best Solution found
            for i in range(len(bestSol_extractInfoList[m])): spamwriter.writerow([i+1] + bestSol_extractInfoList[m][i])
            spamwriter.writerow('')
            spamwriter.writerow(titles1_objFeat) # All Details of same solution
            for row in currCand_RelList: spamwriter.writerow(row)
            spamwriter.writerow('')
    csvfile.close()

    if(printSteps == 1): print("Final Data Exported!", '\n')

    return bestSol_FitList, bestSol_ResumRelatList, bestSol_extractInfoList

#==============================================================================================================

# Print (Config + First best solution found) Info
def printFinalResults(configVarList, maxFitIndexes, bestSol_FitList, bestSol_ResumRelatList, bestSol_extractInfoList, final_time=0.0):
    # Time spent on run
    print("Total duration (sec):", final_time)

    # Printing the Run-Config
    print("Run-Config values of the algorithm:")
    with pandas.option_context('display.max_rows', 999):
        print(pandas.DataFrame(data=[[titles3_configVar[i], configVarList[i]] for i in range(len(configVarList))], columns=['config', 'value'], index=None), '\n')
    
    # Printing first of the best solutions found
    if(len(maxFitIndexes)!=0):
        print("These are the best solutions found:", maxFitIndexes)
        print("Index/Fit:", maxFitIndexes[0], '/', bestSol_FitList[0])
        with pandas.option_context('display.max_rows', 999):
            print(pandas.DataFrame(data=bestSol_ResumRelatList[0], index=None, columns=[titles1_objFeat[2], titles1_objFeat[8]]), '\n')
            print(pandas.DataFrame(data=bestSol_extractInfoList[0], index=None, columns=titles2_bestSolFeat), '\n')

#==============================================================================================================

# Next there is some auxiliary functions that maybe be useful to see/output more detailed info
# But, for a while, its not used

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

# Print all Obj data in a list
def printObjDataList(objList):
    for i in objList: print(i.get())

#==============================================================================================================

# Print all Prof's Subj Preference
def printSubjPref(profList, subjList, subjIsPrefList):
    for pIndex in range(len(profList)):
        # Getting data of current Prof
        pName = profList[pIndex].getName()
        # All Relations of one Prof
        for sIndex in range(len(subjList)):
            # Getting data of current Subj
            sName = subjList[sIndex].getName()
            # Print the Preference
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
def printAllPopFit(solutions, popName=''):
    if(len(solutions.getCandList()) != 0):
        print(popName)
        for n in range(len(solutions.getCandList())): print(str(n), ': ', str(solutions.getCandList()[n].getFitness()), '/ ', end='')
    else: print('No Solutions in:' + popName)

#==============================================================================================================