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
    with open('professors.csv') as csvfile:
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
    with open('subjects.csv') as csvfile:
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
    # Find Min/Max Fitness in the Feasible Pop.    
    for cand in solutionsF.getList():
        avgFea = avgFea + cand.getFitness()
        if(cand.getFitness() > maxFea):
            maxFea = cand.getFitness()        
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
        
#==============================================================================================================                
    
# Export all Candidates in a generation into CSV files
# Create a CSV File for each Candidate and one CSV for all Fitness of the Candidates: 
def outData(solutionsI, solutionsF, num):
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
    
    # All  Infeasible Candidates of a Generation
    i = 0
    for cand in solutionsI.getList():            
        outName = newDir + 'Gen' + str(num) + '_candInf' +  str(i) + '.csv'
        with open(outName, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['sLevel', 'sCode', 'sName', 'sQuadri', 'sPeriod', 'sCampus', 'sCharge', 'sTimetableList','pName', 'pPeriod', 'pCharge', 'pQuadriSabbath', 'pPrefCampus', 'pPrefSubjQ1List', 'pPrefSubjQ2List', 'pPrefSubjQ3List', 'pPrefSubjLimList'])
            # All relations in a Candidate of a Generation
            for s, p in cand.getList():
                row = s.get() + p.get()
                spamwriter.writerow(row)
            spamwriter.writerow(" ")
            spamwriter.writerow(['Infeasible', cand.getFitness()])
        # if(prt == 1): print("Created: " + outName + "in" + newDir + "...")
        i = i + 1
        csvfile.close()
    
    # All Feasible Candidates of a Generation
    i = 0
    for cand in solutionsF.getList():            
        outName = newDir + 'Gen' + str(num) + '_candFea' +  str(i) + '.csv'
        with open(outName, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['sLevel', 'sCode', 'sName', 'sQuadri', 'sPeriod', 'sCampus', 'sCharge', 'sTimetableList','pName', 'pPeriod', 'pCharge', 'pQuadriSabbath', 'pPrefCampus', 'pPrefSubjQ1List', 'pPrefSubjQ2List', 'pPrefSubjQ3List', 'pPrefSubjLimList'])
            # All relations in a Candidate of a Generation
            for s, p in cand.getList():
                row = s.get() + p.get()
                spamwriter.writerow(row)
            spamwriter.writerow(" ")
            spamwriter.writerow(['Feasible', cand.getFitness()])
        # if(prt == 1): print("Created: " + outName + "in" + newDir + "...")
        i = i + 1
        csvfile.close()
            
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
            
    if(prt == 1): print("Data Exported!")   
        
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
        self.printOneCand(cand)
    for cand in solutionsF.getList():
        self.printOneCand(cand)    
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
