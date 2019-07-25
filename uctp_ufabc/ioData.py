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
prt = 0

# Output directory name
mainOutName = 'results'
currOutName = 'run_'
inputName = 'workdata'
# Output directories path
originaltDir = os.getcwd()
inputDir = originaltDir + os.sep + inputName + os.sep
mainFilePath = originaltDir + os.sep + mainOutName + os.sep
currFilePath = ''

#==============================================================================================================

# Get current directory and (re)create new mainFilePath directory - may delete past runs' data
def startOutFolders():
    # Verify if already exists main folder
    if not os.path.exists(mainFilePath): os.makedirs(mainFilePath)
    else:
        # Ask to user if wants delete past runs folders/files
        ask = 'a'
        while(ask != "s" and ask != ""): ask = input("Deseja apagar antigos resultados? Sim('s')/Não('enter'): ")
        if(ask == "s"):
            shutil.rmtree(mainFilePath)
            os.makedirs(mainFilePath)
    
    # Creating a new folder for this run
    i = 0
    while(os.path.exists(mainFilePath + currOutName + str(i))): i = i + 1
    global currFilePath 
    currFilePath = mainFilePath + currOutName + str(i) + os.sep
    os.makedirs(currFilePath)

    # Starting the MAIN OUT CSV with the titles (MinMaxAvg)
    outName = currFilePath + 'totalMinMaxAvg.csv'
    with open(outName, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Pop', 'Iter', 'Min', 'Max', 'Avg'])
    # if(prt == 1): print("Created: " + outName + "in" + newDir + "...")
    csvfile.close()

#==============================================================================================================
    
# Get all data to work
def getData(subj, prof):
    # Read the data of Professors and create the respective objects
    if(prt == 1): print("Getting data of Professors...", end='')
    with open(inputDir + 'professors.csv', encoding='unicode_escape') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        if(prt == 1): print("Setting Professors...")
        for row in spamreader:
            # Transform every letter to upper case to impose a pattern
            datas = [row[0].upper(), row[1].upper(), row[2].upper(), row[3].upper(), row[4].upper(), row[5].upper(), row[6].upper(), row[7].upper(), row[8].upper()]
            # Verify if exist some important blank data (data 0 to 4)
            if((not datas[0] == '') and (not datas[1] == '') and (not datas[2] == '') and (not datas[3] == '') and (not datas[4] == '')):
                # Separating the Subjects Pref., transforming into lists (data 5 to 8)
                datas[5] = datas[5].split('/')
                datas[6] = datas[6].split('/')
                datas[7] = datas[7].split('/')
                datas[8] = datas[8].split('/')
                # Creating and saving a new Prof.
                prof.append(objects.Prof(datas[0], datas[1], datas[2], datas[3], datas[4], datas[5], datas[6], datas[7], datas[8]))
                #if(prt == 1): print(datas)
            else:
                if(prt == 1):
                    print("This professor register has some missing data! It will not be used.")
                    print(datas)
    csvfile.close()
    
    # Read the data of Subjects and create the respective objects
    if(prt == 1): print("\nGetting datas of Subjects...", end='')
    with open(inputDir + 'subjects.csv', encoding='unicode_escape') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        if(prt == 1): print("Setting Subjects...")
        for row in spamreader:
            # Transform every letter to upper case to impose a pattern
            datas = [row[0].upper(), row[1].upper(), row[2].upper(), row[3].upper(), row[4].upper(), row[5].upper(), row[6].upper(), row[7].upper(), row[8].upper()]
            # Verify if exist some important blank data (rows 0 to 8)
            if((not datas[0] == '') and (not datas[1] == '') and (not datas[2] == '') and (not datas[3] == '') and (not datas[4] == '') and (not datas[5] == '') and (not datas[6] == '') and (not datas[7] == '#N/D') and (not datas[8] == '#N/D')):
                # Choose some specifics subjects
                if(datas[0] == 'G' and ('MCTA' in datas[1] or 'MCZA' in datas[1])):
                    # Separating the Timetables of Subj. and transforming into lists of lists: [...,[day/hour/frequency],...] - (data 7 and 8)
                    t0 = []
                    # Theory classes
                    if(not datas[7] == '0'):
                        t1 = datas[7].split('/')
                        for r in t1:
                            day_rest = r.split(' DAS ')
                            hour_room_freq = day_rest[1].split(', ')
                            # Take only: day, hour and freq.
                            if(' E ' in hour_room_freq[2]):
                                final = [day_rest[0], hour_room_freq[0], 'SEMANAL']
                            else:
                                final = [day_rest[0], hour_room_freq[0], hour_room_freq[2]]
                            t0.append(final)
                    # Practice classes
                    if(not datas[8] == '0'):
                        t2 = datas[8].split('/')
                        for r in t2:
                            day_rest = r.split(' DAS ')
                            hour_room_freq = day_rest[1].split(', ')
                            # Take only: day, hour and freq.
                            if(' E ' in hour_room_freq[2]):
                                final = [day_rest[0], hour_room_freq[0], 'SEMANAL']
                            else:
                                final = [day_rest[0], hour_room_freq[0], hour_room_freq[2]]
                            t0.append(final)
                    
                    # Putting t0 (list of lists of timetables back into 'datas'
                    datas[7] = t0
                    # Removing datas[8] that is not useful
                    datas.pop(8)
                    # Creating and saving the new Subj.
                    subj.append(objects.Subject(datas[0], datas[1], datas[2], datas[3], datas[4], datas[5], datas[6], datas[7]))
                    #if(prt == 1): print(datas)
            else:
                if(prt == 1): print("This subject register has some missing data! It will not be used.")
                if(prt == 1): print(datas)
    csvfile.close()
    
    if(prt == 1): print("Data Obtained!")

#==============================================================================================================

# Output run data obtained by cProfile
def outRunData(pr):
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
    ps.print_stats()
    outName = currFilePath + 'runInfo_cProfile.txt'
    with open(outName, 'w+') as f:
        f.write(s.getvalue())

#==============================================================================================================

# Extract information - auxiliary function to gathering all important info of a solution
def extractInfo(cand, prof, subj):
    # Collecting Profs names in 'prof'
    profData = [p.get() for p in prof]
    profName = [pName for pName, _, _, _, _, _, _, _, _ in profData]

    # Getting others info
    prof_relations, conflicts_i2, conflicts_i3 = cand.getInfVariables()
    prof_relations, subjPref, periodPref, quadSabbNotPref, campusPref, difCharge = cand.getFeaVariables()
    
    # If does not have some of the FeaVariables - probably the Cand is Infeasible
    if(len(difCharge) == 0): _, difCharge = uctp.UCTP().f1(subj, prof, prof_relations)
    if(len(subjPref) == 0): _, subjPref = uctp.UCTP().f2(subj, prof, prof_relations)
    if(len(quadSabbNotPref) == 0): _, quadSabbNotPref = uctp.UCTP().f3(subj, prof, prof_relations)
    if(len(periodPref) == 0): _, periodPref = uctp.UCTP().f4(subj, prof, prof_relations)
    if(len(campusPref) == 0): _, campusPref = uctp.UCTP().f5(subj, prof, prof_relations)

    # Extracting the number of each occurence for each professor and its relations
    # [profName, numSubjs, numSubjNotPrefered, numPeriodNotPref, numQuadriSabbathPref, numCampusNotPref, numI2, numI3, difCharge]
    info = [[profName[i],
            len(prof_relations[i]), 
            len(prof_relations[i]) - subjPref[i], 
            len(prof_relations[i]) - periodPref[i], 
            len(prof_relations[i]) - quadSabbNotPref[i], 
            len(prof_relations[i]) - campusPref[i],
            len(conflicts_i2[i]),
            len(conflicts_i3[i]),
            difCharge[i]] for i in range(len(prof))]
        
    # Last line sums all professors data
    total = ['Total', 0, 0, 0, 0, 0, 0, 0, 0]
    for j in range(1,9): total[j] = sum([i[j] for i in info])
    info.append(total)

    return  info

#==============================================================================================================

# Put out on 'totalMinMaxAvg.csv' the current generation Min/Max/Avg Fitness
def outDataMMA(solutionsI, solutionsF, iter):
    if(prt == 1): print("Exporting data....", end='')
    
    # Find Min/Max Fitness in the Infeasible Pop.
    minInf, maxInf, avgInf = 0, -1, 0
    for cand in solutionsI.getList():
        avgInf = avgInf + cand.getFitness()
        if(cand.getFitness() > maxInf): maxInf = cand.getFitness()
        if(cand.getFitness() < minInf): minInf = cand.getFitness()
    if(len(solutionsI.getList()) != 0): avgInf = avgInf / len(solutionsI.getList())
    
    # Find Min/Max Fitness in the Feasible Pop.
    minFea, maxFea, avgFea = 1, 0, 0
    maxFeaIndex = [] # Recording the best solutions found
    for cand in solutionsF.getList():
        avgFea = avgFea + cand.getFitness()
        if(cand.getFitness() == maxFea):
            maxFeaIndex.append(solutionsF.getList().index(cand))
        if(cand.getFitness() > maxFea):
            maxFea = cand.getFitness()
            maxFeaIndex = [solutionsF.getList().index(cand)]
        if(cand.getFitness() < minFea):
            minFea = cand.getFitness()
    if(len(solutionsF.getList()) != 0): avgFea = avgFea / len(solutionsF.getList())
    
    # Get current directory, currFilePath dir., and CSV file to be modified with current generation Min/Max Fitness
    outName = currFilePath + 'totalMinMaxAvg.csv'
    with open(outName, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        if(minInf != 0): spamwriter.writerow(['Inf', iter, minInf, maxInf, avgInf])
        if(minFea != 1): spamwriter.writerow(['Fea', iter, minFea, maxFea, avgFea])
    csvfile.close()

    if(prt == 1): print("Data Exported!")
    
    return maxFeaIndex, minInf, maxInf, avgInf, minFea, maxFea, avgFea

#==============================================================================================================

# Export all Candidates in a generation into CSV files
# Create a CSV File for each Candidate and one CSV to gather the Fitness of all Candidates:
def outDataGeneration(solutionsI, solutionsF, num, prof, subj):
    if(prt == 1): print("Exporting all Generation (Solutions) data....", end='')
    
    # In currFilePath dir, create new 'gen' dir
    newDir = currFilePath + 'Gen' + str(num) + os.sep
    if not os.path.exists(newDir): os.makedirs(newDir)
    
    # Main titles used when output datas
    titles1 = ['sLevel', 'sCode', 'sName', 'sQuadri', 'sPeriod', 'sCampus', 'sCharge', 'sTimetableList','pName', 'pPeriod', 'pCharge', 'pQuadriSabbath', 'pPrefCampus', 'pPrefSubjQ1List', 'pPrefSubjQ2List', 'pPrefSubjQ3List', 'pPrefSubjLimList']
    titles2 = ['pName', 'numSubjects', 'notPref', 'notPeriod', 'isSabbath', 'notCampus', 'numI2', 'numI3', 'difCharge']
    # Each population info will be iterate
    pop, typePop = [solutionsI.getList(), solutionsF.getList()], ['Inf', 'Fea']

    # All Candidates of a Generation - doing for each population
    for j in range(len(pop)):
        i = 0
        for cand in pop[j]:
            # Start output info of the solution
            outName = newDir + 'Gen' + str(num) + '_cand' + typePop[j] + str(i) + '.csv'
            with open(outName, 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(titles1)
                
                # All relations in a Candidate of a Generation
                for s, p in cand.getList():
                    row = s.get() + p.get()
                    spamwriter.writerow(row)
                spamwriter.writerow(" ")
                
                # Fitness information
                spamwriter.writerow([typePop[j], cand.getFitness()])
                spamwriter.writerow(" ")
                
                # Extracting all important info to analyse the quality of the solution
                info = extractInfo(cand, prof, subj)

                # Output extra information for analisys
                spamwriter.writerow(titles2)
                for row in info: spamwriter.writerow(row)
            
            # if(prt == 1): print("Created: " + outName + "in" + newDir + "...")
            csvfile.close()
            i = i + 1
    
    # Output all Fitness in a Generation
    outName = newDir + 'gen' +  str(num) + '.csv'
    with open(outName, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Candidate', 'Population', 'Fitness'])
        i = 0
        for cand in solutionsI.getList():
            spamwriter.writerow([i,'Infeasible', cand.getFitness()])
            i = i + 1
        
        i = 0
        for cand in solutionsF.getList():
            spamwriter.writerow([i,'Feasible', cand.getFitness()])
            i = i + 1
    # if(prt == 1): print("Created: " + outName + "in" + newDir + "...")
    csvfile.close()

    if(prt == 1): print("All Generation (Solutions) data Exported!")
    
#==============================================================================================================

def finalOutData(solutionsI, solutionsF, num, prof, subj, maxFeaIndex=[], config=[]):
    print("Exporting final data....", end='')
    
    # Main titles to output datas
    titles1 = ['sLevel', 'sCode', 'sName', 'sQuadri', 'sPeriod', 'sCampus', 'sCharge', 'sTimetableList','pName', 
                'pPeriod', 'pCharge', 'pQuadriSabbath', 'pPrefCampus', 'pPrefSubjQ1List', 'pPrefSubjQ2List', 
                'pPrefSubjQ3List', 'pPrefSubjLimList']
    titles2 = ['pName', 'numSubjects', 'notPref', 'notPeriod', 'isSabbath', 'notCampus', 'numI2', 'numI3', 'difCharge']
    titles3 = ['maxIter', 'numCand', 'numCandInit', 'randNewSol', 'convergDetect', 'stopFitValue', 'pctParentsCross', 
            'pctMut', 'pctElitism', 'w_alpha', 'w_beta', 'w_gamma', 'w_delta', 'w_omega', 'w_sigma', 'w_pi', 'w_rho']
    
    # Output Run-Config and Final best results (different of each other)
    outName = currFilePath + 'runConfigResult.csv'
    with open(outName, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        
        # All Config info
        spamwriter.writerow(titles3)
        spamwriter.writerow(config)
        spamwriter.writerow('')

        # If feasible solutions were found
        if(len(maxFeaIndex)!=0):
            # Lists of data of all different solutions with same max fit found
            maxCand, fitMaxData, maxData, resumeMaxData, maxInfo, info_alreadyShow = [], [], [], [], [], []
            # Every feasible solution with same max fit
            for m in range(len(maxFeaIndex)):
                # Getting the solution and its fitness
                maxCand.append(solutionsF.getList()[maxFeaIndex[m]])
                # Getting and recording its data
                fitMaxData.append(maxCand[m].getFitness())
                maxData.append([s.get() + p.get() for s, p in maxCand[m].getList()])
                maxInfo.append(extractInfo(maxCand[m], prof, subj))

                # Checks if is different from something that was already output
                if(info_alreadyShow.count(maxInfo[m]) == 0): 
                    # Adding to Lists
                    info_alreadyShow.append(maxInfo[m])
                    # Resuming the result to show only 'sName' and 'pName' of each relation
                    resumeMaxData.append([[row[2], row[8]] for row in maxData[m]])

                    # Best Feasible Solution info
                    if(m == 0): spamwriter.writerow(["Best solutions found:", maxFeaIndex])
                    spamwriter.writerow(["Index/Fit:", maxFeaIndex[m], fitMaxData[m]])
                    spamwriter.writerow('')
                    # sName + pName
                    spamwriter.writerow(['index', titles1[2], titles1[8]])
                    i = 1
                    for row in resumeMaxData[-1]:
                        spamwriter.writerow([i] + row)
                        i = i + 1
                    # Extracted Info of one of the best Solutions found
                    spamwriter.writerow('')
                    spamwriter.writerow(titles2)
                    i = 1
                    for row in maxInfo[m]:
                        spamwriter.writerow([i] + row)
                        i = i + 1
                    # All Details of same solution
                    spamwriter.writerow('')
                    spamwriter.writerow(titles1)
                    for row in maxData[m]:
                        spamwriter.writerow(row)
                    spamwriter.writerow('')    

        else: spamwriter.writerow("Do not found feasible solutions.")
    csvfile.close()

    # Showing important Info on terminal for user
    print("Final Data Exported!", '\n')
    
    return fitMaxData, resumeMaxData, maxInfo, titles1, titles2, titles3
        
#==============================================================================================================

# First print of a round
def printHead(prof, subj, curIter, maxIter, firstFeasSol, lastMaxIter):
    if(curIter == 0): print("\nStarting hard work...\n")
    print('Iteration:', curIter, 'of', maxIter, '/ Working with (Prof/Subj):', len(prof), '/', len(subj))
    if(firstFeasSol != -1): 
        print('First Feas Sol at (iter): ', firstFeasSol, '/ Cur Max Feas Sol at (iter): ', lastMaxIter, '/ Num Iter since last Max:', curIter - lastMaxIter)

#==============================================================================================================

# Last print of a round
def printTail(solutionsI, solutionsF, minInf, maxInf, avgInf, minFea, maxFea, avgFea):
    if(minInf != 0): print('Infeasibles (', len(solutionsI.getList()), ') Min:', minInf, 'Max:', maxInf, 'Avg:', avgInf)
    else: print('No Infeasibles Solutions!')
    if(minFea != 1): print('Feasibles (', len(solutionsF.getList()), ') Min:', minFea, 'Max:', maxFea, 'Avg:', avgFea)
    else: print('No Feasibles Solutions!')
    print("")

#==============================================================================================================

# Print (Config + First best solution found) Info
def printFinalResults(config, maxFeaIndex, fitMaxData, resumeMaxData, maxInfo, titles1, titles2, titles3):
    import pandas
    # Printing the Run-Config
    print("Run-Config values of the algorithm:")
    with pandas.option_context('display.max_rows', 999):
        print(pandas.DataFrame(data=[[titles3[i], config[i]] for i in range(len(config))], columns=['config', 'value'], index=None), '\n')
    
    # Printing one of the best solutions found
    if(len(maxFeaIndex)!=0):
        print("These are the best solutions found:", maxFeaIndex[0])
        print("Index/Fit:", maxFeaIndex[0], '/', fitMaxData[0])
        with pandas.option_context('display.max_rows', 999):
            print(pandas.DataFrame(data=resumeMaxData[0], index=None, columns=[titles1[2], titles1[8]]), '\n')
            print(pandas.DataFrame(data=maxInfo[0], index=None, columns=titles2), '\n')       

#==============================================================================================================

# Print all Obj data
def printObjDataList(objList):
    for i in objList: print(i.get())

#==============================================================================================================

# Print all Prof's Subj Preference
def printSubjPref(prof, subj, subjIsPref):
    for pIndex in range(len(prof)):
        # Getting data of current Prof
        pName, _, _, _, _, _, _, _, _ = prof[pIndex].get()
        # All Relations of one Prof
        for sIndex in range(len(subj)):
            # Getting data of current Subj
            _, _, sName, _, _, _, _, _ = subj[sIndex].get()
            if(subjIsPref[pIndex][sIndex]!=0): print(pName, sName, subjIsPref[pIndex][sIndex])

#==============================================================================================================
       
# Print all data of a Candidate (Professor-Subject Relations)
def printOneCand(candidate):
    i = 0
    for s, p in candidate.getList():
        print(i, s.get(), p.get())
        i = i + 1

#==============================================================================================================

# Print the data of all Candidates (Professor-Subject Relations) of a generation
def printAllCand(solutionsI=None, solutionsF=None):
    for cand in solutionsI.getList(): printOneCand(cand)
    for cand in solutionsF.getList(): printOneCand(cand)
    print("--------")
        
#==============================================================================================================

# Print MinMaxAvg Fitness of a generation
def printMMAFit(solutionsI=None, solutionsF=None):
    minInf, maxInf, avgInf = 0, -1, 0
    # Find Min/Max Fitness in the Infeasible Pop.
    for cand in solutionsI.getList():
        avgInf = avgInf + cand.getFitness()
        if(cand.getFitness() > maxInf): maxInf = cand.getFitness()
        if(cand.getFitness() < minInf): minInf = cand.getFitness()
    if(len(solutionsI.getList()) != 0): avgInf = avgInf / len(solutionsI.getList())
    
    minFea, maxFea, avgFea = 1, 0, 0
    # Find Min/Max Fitness in the Feasible Pop.
    for cand in solutionsF.getList():
        avgFea = avgFea + cand.getFitness()
        if(cand.getFitness() > maxFea):
            maxFea = cand.getFitness()
        if(cand.getFitness() < minFea):
            minFea = cand.getFitness()
    if(len(solutionsF.getList()) != 0): avgFea = avgFea / len(solutionsF.getList())
    
    if(minInf != 0): print('Infeasibles - Num:', len(solutionsI.getList()), 'Min:', minInf, 'Max:', maxInf, 'Avg:', avgInf)
    else: print('No Infeasibles Solutions!')
    if(minFea != 1): print('Feasibles - Num:', len(solutionsF.getList()), 'Min:', minFea, 'Max:', maxFea, 'Avg:', avgFea)
    else: print('No Feasibles Solutions!')

#==============================================================================================================

# Print the Fitness of all candidates in a population
def printAllPopFit(solutions, text=''):
    if(len(solutions.getList()) != 0):
        print(text)
        n = 0
        for cand in solutions.getList():
            print(str(n), ': ', str(cand.getFitness()), ',',)
            n = n + 1
    else: print('No Solutions in:' + text)

#==============================================================================================================