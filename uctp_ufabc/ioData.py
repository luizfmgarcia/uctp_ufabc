# Import/Export Data Methods

from objects import *
import csv
import os
import sys
import shutil

# Set '1' to allow, during the run, the output of some steps
prt = 1

#==============================================================================================================            
    
# Get all data to work
def getData(subj, prof): 
    # Read the data of Professors and create the respective objects
    if(prt == 1): print("Getting data of Professors...", end='')
    with open('professors.csv', encoding = 'unicode_escape') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        if(prt == 1): print("Setting Professors...")
        for row in spamreader:
            # Transform every letter to upper case to impose a pattern
            datas = [row[0].upper(), row[1].upper(), row[2].upper(), row[3].upper(), row[4].upper(), row[5].upper(), row[6].upper(), row[7].upper(), row[8].upper()]
            # Verify if exist some important blank data (data 0 to 4) 
            if(not datas[0]=='' and not datas[1]=='' and not datas[2]=='' and not datas[3]=='' and not datas[4]==''):
                # Separating the Subjects Pref., transforming into lists (data 5 to 8)
                datas[5] = datas[5].split('/')
                datas[6] = datas[6].split('/')
                datas[7] = datas[7].split('/')
                datas[8] = datas[8].split('/')
                # Creating and saving a new Prof.
                prof.append(Prof(datas[0], datas[1], datas[2], datas[3], datas[4], datas[5], datas[6], datas[7], datas[8]))
                if(prt == 1): print(datas)
            else:
                if(prt == 1):
                    print("This professor register has some missing data! It will not be used.")
                    print(datas)   
    csvfile.close() 
    
    # Read the data of Subjects and create the respective objects    
    if(prt == 1):
        print(" ")
        print("Getting datas of Subjects...", end='')
    with open('subjects.csv', encoding = 'unicode_escape') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        if(prt == 1): print("Setting Subjects...")
        for row in spamreader:
            # Transform every letter to upper case to impose a pattern
            datas = [row[0].upper(), row[1].upper(), row[2].upper(), row[3].upper(), row[4].upper(), row[5].upper(), row[6].upper(), row[7].upper(), row[8].upper()]
            # Verify if exist some important blank data (rows 0 to 8) 
            if(not datas[0]=='' and not datas[1]=='' and not datas[2]=='' and not datas[3]=='' and not datas[4]=='' and not datas[5]=='' and not datas[6]=='' and not datas[7]=='#N/D' and not datas[8]=='#N/D'):
                # Choose some specifics subjects
                if(datas[0]=='G' and ('MCTA' in datas[1] or 'MCZA' in datas[1])):
                    # Separating the Timetables of Subj. and transforming into lists of lists: [...,[day/hour/frequency],...] - (data 7 and 8)
                    t0 = []
                    # Theory classes
                    if(not datas[7]=='0'):
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
                    if(not datas[8]=='0'):    
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
                    subj.append(Subject(datas[0], datas[1], datas[2], datas[3], datas[4], datas[5], datas[6], datas[7]))
                    if(prt == 1): print(datas)
            else:
                if(prt == 1): print("This subject register has some missing data! It will not be used.")
                #if(prt == 1): print(datas)            
    csvfile.close()
       
    if(prt == 1): print("Data Obtained!")
    startOutFolders()
        
#==============================================================================================================            
    
# Get current directory and (re)create new 'generationsCSV' directory - delete past runs' data
def startOutFolders():    
    currentDir = os.getcwd()
    newDir = currentDir + os.sep + 'generationsCSV' + os.sep
    if not os.path.exists(newDir):
        os.makedirs(newDir)
    else:
        shutil.rmtree(newDir)
        os.makedirs(newDir)
    
    # this code starts the MAIN OUT CSV with the titles (MinMaxAvg)
    outName = newDir + 'totalMinMaxAvg.csv'                
    with open(outName, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Pop', 'Iter','Min', 'Max', 'Avg'])  
    # if(prt == 1): print("Created: " + outName + "in" + newDir + "...")
    csvfile.close()
        
#==============================================================================================================            

# Put out on 'totalMinMaxAvg.csv' the current generation Min/Max/Avg Fitness
def outDataMMA(solutionsI, solutionsF, iter):
    if(prt == 1): print("Exporting data....")
    
    minInf = 0
    maxInf = -1
    avgInf = 0
    # Find Min/Max Fitness in the Infeasible Pop.          
    for cand in solutionsI.getList():
        avgInf = avgInf + cand.getFitness()
        if(cand.getFitness() > maxInf):
            maxInf = cand.getFitness()             
        if(cand.getFitness() < minInf):
            minInf = cand.getFitness()
    if(len(solutionsI.getList())!=0): avgInf = avgInf/len(solutionsI.getList())
    
    minFea = 1
    maxFea = 0
    avgFea = 0
    maxFeaIndex = [] # Recording the best solutions found
    # Find Min/Max Fitness in the Feasible Pop.    
    for cand in solutionsF.getList():
        avgFea = avgFea + cand.getFitness()
        if(cand.getFitness() == maxFea):
            maxFeaIndex.append(solutionsF.getList().index(cand))
        if(cand.getFitness() > maxFea):
            maxFea = cand.getFitness()
            maxFeaIndex = [solutionsF.getList().index(cand)]        
        if(cand.getFitness() < minFea):
            minFea = cand.getFitness()
    if(len(solutionsF.getList())!=0): avgFea = avgFea/len(solutionsF.getList())
    
    # get current directory, 'generationsCSV' dir., and CSV file to be modified with current generation Min/Max Fitness
    currentDir = os.getcwd()
    newDir = currentDir + os.sep + 'generationsCSV' + os.sep
    outName = newDir + 'totalMinMaxAvg.csv'                
    with open(outName, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        if(minInf!=0):
            spamwriter.writerow(['Inf', iter, minInf, maxInf, avgInf])
        if(minFea!=1):
            spamwriter.writerow(['Fea', iter, minFea, maxFea, avgFea])
    csvfile.close()

    if(prt == 1):
        if(minInf!=0): print('Infeasibles (', len(solutionsI.getList()), ') Min:', minInf, 'Max:', maxInf, 'Avg:', avgInf)
        else: print('No Infeasibles Solutions!')
        if(minFea!=1): print('Feasibles (', len(solutionsF.getList()), ') Min:', minFea, 'Max:', maxFea, 'Avg:', avgFea)
        else: print('No Feasibles Solutions!')        
        print("Data Exported!")
    
    return maxFeaIndex        
        
#==============================================================================================================                

# Extract information - auxiliar function to "outData" function
def extractInfo(datas):
    # Collecting Profs names in 'prof' and putting Subj index related to same Prof in same index of 'indexs' list
    prof, indexs = [], []
    for data in range(len(datas)):
        _, _, sName, sQuadri, sPeriod, sCampus, sCharge, _, pName, pPeriod, pCharge, pQuadriSabbath, pPrefCampus, pPrefSubjQ1List, pPrefSubjQ2List, pPrefSubjQ3List, pPrefSubjLimList = datas[data]
        try:
            i = prof.index(pName)
        except ValueError:
            i = -1
        if(i!=-1): indexs[i].append(data)
        else:
            prof.append(pName)
            indexs.append([data])
    
    # Initializing 'info' List
    info = [[] for i in range(len(prof))]
    
    # Extracting the number of each occurence
    # info = [profName, numSubjs, numSubjNotPrefered, numPeriodNotPrefered, numQuadriSabbathPrefered, numCampusNotPrefered, SubtractProfCharge(SumSubjCharges)]
    for i in range(len(prof)):
        info[i] = info[i]+[prof[i], len(indexs[i]), 0, 0, 0, 0, 0]
        k=0
        for j in indexs[i]:
            _, _, sName, sQuadri, sPeriod, sCampus, sCharge, _, pName, pPeriod, pCharge, pQuadriSabbath, pPrefCampus, pPrefSubjQ1List, pPrefSubjQ2List, pPrefSubjQ3List, pPrefSubjLimList = datas[j]    
            if('1' in sQuadri):
                if(pPrefSubjQ1List.count(sName)==0 and pPrefSubjLimList.count(sName)==0):
                    info[i][2] = info[i][2]+1
            elif('2' in sQuadri):
                if(pPrefSubjQ2List.count(sName)==0 and pPrefSubjLimList.count(sName)==0):
                    info[i][2] = info[i][2]+1
            elif('3' in sQuadri):
                if(pPrefSubjQ3List.count(sName)==0 and pPrefSubjLimList.count(sName)==0):
                    info[i][2] = info[i][2]+1                
            if('NEGOCI' not in pPeriod and sPeriod!=pPeriod):
                info[i][3] = info[i][3]+1
            if('NENHUM' not in pQuadriSabbath and sQuadri==pQuadriSabbath):
                info[i][4] = info[i][4]+1 
            if(sCampus!=pPrefCampus):
                info[i][5] = info[i][5]+1
            if(',' in pCharge): pCharge = pCharge.replace(",", ".")
            if(',' in sCharge): sCharge = sCharge.replace(",", ".")
            if(k==0): info[i][6] = float(pCharge)-float(sCharge)
            else: info[i][6] = info[i][6]-float(sCharge)
            k=k+1

    # Last line sums total data
    total = ['Total', 0, 0, 0, 0, 0, 0]
    for i in info:
        for j in range(1,7):
            total[j] = total[j] + i[j]
    info.append(total)

    return  info

#-------------------------------------------------------

# Export all Candidates in a generation into CSV files
# Create a CSV File for each Candidate and one CSV for all Fitness of the Candidates: 
def outData(solutionsI, solutionsF, num, maxFeaIndex=[]):
    if(prt == 1): print("Exporting data....", end='')

    # get current directory and create, if necessary, new 'generationsCSV' dir
    currentDir = os.getcwd()
    newDir = currentDir + os.sep + 'generationsCSV' + os.sep
    if not os.path.exists(newDir):
            os.makedirs(newDir)
    
    # In 'generationsCSV' dir, create new 'gen' dir
    newDir = newDir + 'Gen' + str(num) + os.sep
    if not os.path.exists(newDir):
        os.makedirs(newDir)
    
    # Main titles to output datas 
    titles1 = ['sLevel', 'sCode', 'sName', 'sQuadri', 'sPeriod', 'sCampus', 'sCharge', 'sTimetableList','pName', 'pPeriod', 'pCharge', 'pQuadriSabbath', 'pPrefCampus', 'pPrefSubjQ1List', 'pPrefSubjQ2List', 'pPrefSubjQ3List', 'pPrefSubjLimList']
    titles2 = ['pName', 'numSubjects', 'notPref', 'notPeriod', 'isSabbath', 'notCampus', 'difCharge']
        
    # All  Infeasible Candidates of a Generation
    i = 0
    for cand in solutionsI.getList():      
        datas = []  
        # Start output info of the solution
        outName = newDir + 'Gen' + str(num) + '_candInf' +  str(i) + '.csv'
        with open(outName, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(titles1)
            
            # All relations in a Candidate of a Generation
            for s, p in cand.getList():
                row = s.get() + p.get()
                datas.append(row)
                spamwriter.writerow(row)
            spamwriter.writerow(" ")
            
            # Fitness information
            spamwriter.writerow(['Infeasible', cand.getFitness()])
            spamwriter.writerow(" ")
            
            # Extracting some good info to analyse the quality of the solution           
            info = extractInfo(datas)

            # Output extra information for analisys
            spamwriter.writerow(titles2)
            for row in info:
                spamwriter.writerow(row)       
        
        # if(prt == 1): print("Created: " + outName + "in" + newDir + "...")
        csvfile.close()
        i = i + 1
    
    # All Feasible Candidates of a Generation
    i = 0
    for cand in solutionsF.getList():
        datas = []
        # Start output info of the solution            
        outName = newDir + 'Gen' + str(num) + '_candFea' +  str(i) + '.csv'
        with open(outName, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(titles1)
            
            # All relations in a Candidate of a Generation
            for s, p in cand.getList():
                row = s.get() + p.get()
                datas.append(row)
                spamwriter.writerow(row)
            spamwriter.writerow(" ")
            
            # Fitness information
            spamwriter.writerow(['Feasible', cand.getFitness()])
            spamwriter.writerow(" ")
            
            # Extracting some good info to analyse the quality of the solution           
            info = extractInfo(datas)

            # Output extra information for analisys
            spamwriter.writerow(titles2)
            for row in info:
                spamwriter.writerow(row)
        
        # if(prt == 1): print("Created: " + outName + "in" + newDir + "...")
        csvfile.close()
        
        # If we are on the last iteration of the algorithm
        if(len(maxFeaIndex)!=0):
            if(maxFeaIndex[0]==i):
                maxData = datas
                maxInfo = info
        i = i + 1
            
    # All Fitness in a Generation
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
            
    if(prt == 1):
        print("Data Exported!")
        # Printing one of the best solutions found
        if(len(maxFeaIndex)!=0):
            print("")
            print("These are the best solutions found:", maxFeaIndex)
            print("This is the first of them:")
            import pandas
            newData=[]
            for row in maxData:
                newData.append([row[2],row[8]])
            with pandas.option_context('display.max_rows', 999):   
                print(pandas.DataFrame(data=newData, index=None, columns=[titles1[2], titles1[8]]), '\n')
                
                print(pandas.DataFrame(data=maxInfo, index=None, columns=titles2), '\n')
        
#==============================================================================================================            

# Print all data of a Candidate (Professor-Subject Relations)    
def printOneCand(candidate):
    i=0
    for s, p in candidate.getList():
        print(i, s.get(), p.get())
        i=i+1
        
#==============================================================================================================            

# Print the data of all Candidates (Professor-Subject Relations) of a generation
def printAllCand(solutionsI, solutionsF):
    for cand in solutionsI.getList():
        printOneCand(cand)
    for cand in solutionsF.getList():
        printOneCand(cand)    
        print("--------")    
        
#==============================================================================================================            

# Print MinMaxAvg Fitness of a generation
def printMMAFit(solutionsI, solutionsF):

    minInf = 0
    maxInf = -1
    avgInf = 0
    # Find Min/Max Fitness in the Infeasible Pop.          
    for cand in solutionsI.getList():
        avgInf = avgInf + cand.getFitness()
        if(cand.getFitness() > maxInf):
            maxInf = cand.getFitness()             
        if(cand.getFitness() < minInf):
            minInf = cand.getFitness()
    if(len(solutionsI.getList())!=0): avgInf = avgInf/len(solutionsI.getList())
    
    minFea = 1
    maxFea = 0
    avgFea = 0
    # Find Min/Max Fitness in the Feasible Pop.    
    for cand in solutionsF.getList():
        avgFea = avgFea + cand.getFitness()
        if(cand.getFitness() > maxFea):
            maxFea = cand.getFitness()        
        if(cand.getFitness() < minFea):
            minFea = cand.getFitness()
    if(len(solutionsF.getList())!=0): avgFea = avgFea/len(solutionsF.getList())

    if(minInf!=0): print('Infeasibles - Num:', len(solutionsI.getList()), 'Min:', minInf, 'Max:', maxInf, 'Avg:', avgInf)
    else: print('No Infeasibles Solutions!')
    if(minFea!=1): print('Feasibles - Num:', len(solutionsF.getList()), 'Min:', minFea, 'Max:', maxFea, 'Avg:', avgFea)
    else: print('No Feasibles Solutions!')
        
#==============================================================================================================            

# Print the Fitness of all candidates in a generation                
def printAllFit(solutionsI, solutionsF):
    # Infeasible ones
    if(len(solutionsI.getList())!=0):
        print('Infeasibles Solutions:')
        n = 0
        for cand in solutionsI.getList():
            print(str(n), ': ', str(cand.getFitness()), ',',)
            n = n + 1
        print(" ")
    else:
        print('No Infeasibles Solutions!')
    
    # Feasible ones        
    if(len(solutionsF.getList())!=0):
        print('Feasibles Solutions:')
        n = 0
        for cand in solutionsF.getList():
            print(str(n), ': ', str(cand.getFitness()), ',',)
            n = n + 1    
        print(" ")
    else:
        print('No Feasibles Solutions!')        
#==============================================================================================================        
