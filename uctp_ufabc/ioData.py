# Import/Export Data Methods

from objects import *
import csv
import os
import sys
import shutil
from string import split
    
# Get all data to work
def getData(subj, prof): 
    # Read the data of professors and create the respective objects
    print "Getting data of Professors...",
    with open('professors.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        print "Setting Professors..."
        for row in spamreader:
            # Transform every letter to upper case to impose a pattern
            datas = [row[0].upper(), row[1].upper(), row[2].upper(), row[3].upper(), row[4].upper(), row[5].upper(), row[6].upper(), row[7].upper(), row[8].upper()]
            # Verify if exist some important blank data (datas 0 to 4) 
            if(not datas[0]=='' and not datas[1]=='' and not datas[2]=='' and not datas[3]=='' and not datas[4]==''):
                # Separating the Subjects Pref., transforming into lists (datas 5 to 8)
                datas[5] = split(datas[5], '/')
                datas[6] = split(datas[6], '/')
                datas[7] = split(datas[7], '/')
                datas[8] = split(datas[8], '/')
                # Creating and saving a new Prof.
                prof.append(Prof(datas[0], datas[1], datas[2], datas[3], datas[4], datas[5], datas[6], datas[7], datas[8]))
                print datas
            else:
                print "This professor register has some missing data! It will not be used."
                print datas    
    csvfile.close() 
    
    # Read the data of subjects and create the respective objects    
    print(" ")
    print "Getting datas of Subjects...",
    with open('subjects.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        print "Setting Subjects..."
        for row in spamreader:
            # Transform every letter to upper case to impose a pattern
            datas = [row[0].upper(), row[1].upper(), row[2].upper(), row[3].upper(), row[4].upper(), row[5].upper(), row[6].upper(), row[7].upper(), row[8].upper()]
            # Verify if exist some important blank data (rows 0 to 8) 
            if(not datas[0]=='' and not datas[1]=='' and not datas[2]=='' and not datas[3]=='' and not datas[4]=='' and not datas[5]=='' and not datas[6]=='' and not datas[7]=='#N/D' and not datas[8]=='#N/D'):
                # Choose some specifics subjects
                if(datas[0]=='G' and ('MCTA' in datas[1] or 'MCZA' in datas[1])):
                    # Separating the Timetables of Subj. and transforming into lists of lists: day/hour/frequency - (data 7 and 8)
                    t0 = []
                    if(not datas[7]=='0'):
                        t1 = split(datas[7], '/')   
                        for r in t1:
                            day_rest = split(r, ' DAS ')
                            hour_room_freq = split(day_rest[1], ', ')
                            # Take only: day, hour and freq.
                            if(' E ' in hour_room_freq[2]): 
                                final = [day_rest[0], hour_room_freq[0], 'SEMANAL']
                            else:
                                final = [day_rest[0], hour_room_freq[0], hour_room_freq[2]]    
                            t0.append(final)
                    if(not datas[8]=='0'):    
                        t2 = split(datas[8], '/')
                        for r in t2:
                            day_rest = split(r, ' DAS ')
                            hour_room_freq = split(day_rest[1], ', ')
                            # Take only: day, hour and freq. 
                            if(' E ' in hour_room_freq[2]): 
                                final = [day_rest[0], hour_room_freq[0], 'SEMANAL']
                            else:
                                final = [day_rest[0], hour_room_freq[0], hour_room_freq[2]]  
                            t0.append(final)
                    
                    datas[7] = t0
                    datas.pop(8)
                    # Creating and saving a new Subj.
                    subj.append(Subject(datas[0], datas[1], datas[2], datas[3], datas[4], datas[5], datas[6], datas[7]))
                    print datas
            else:
                print "This subject register has some missing data! It will not be used."
                #print datas            
    csvfile.close()
        
    print ("Data Obtained!")
    startOutFolders()
    
# get current directory and (re)create new 'generationsCSV' directory - delete everything was there
def startOutFolders():    
    currentDir = os.getcwd()
    newDir = currentDir + os.sep + 'generationsCSV' + os.sep
    if not os.path.exists(newDir):
        os.makedirs(newDir)
    else:
        shutil.rmtree(newDir)
        os.makedirs(newDir)
    outName = newDir + 'totalMinMaxAvg.csv'
    
    # this code starts the MAIN OUT CSV with the titles                
    with open(outName, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['min', 'max', 'avg'])  
    # print("Created: " + outName + "in" + newDir + "...")
    csvfile.close()

# Put out on 'totalMinMaxAvg.csv' the current generation Min/Max/Avg Fitness
def outDataMMA(solutionsI, solutionsF):
    print "Exporting data....",
    
    # get current directory and creating new 'generationsCSV' dir
    currentDir = os.getcwd()
    newDir = currentDir + os.sep + 'generationsCSV' + os.sep
    if not os.path.exists(newDir):
            os.makedirs(newDir)
    outName = newDir + 'totalMinMaxAvg.csv'
    
    # All Candidates of a Generation
    min = 0
    max = 0
    for cand in solutionsI.getList():             
        if(cand.getFitness() < min):
            min = cand.getFitness()
    
    for cand in solutionsF.getList():             
        if(cand.getFitness() > max):
            max = cand.getFitness()
                    
    with open(outName, 'ab') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([min, max, ((min+max)/2)])  
    # print("Created: " + outName + "in" + newDir + "...")
    csvfile.close()
            
    print ("Data Exported!")
    
# Export Candidates in differents generations into CSV files
def outData(solutionsI, solutionsF, num):
    print "Exporting data....",
    
    # get current directory and creating new 'generationsCSV' dir
    currentDir = os.getcwd()
    newDir = currentDir + os.sep + 'generationsCSV' + os.sep
    if not os.path.exists(newDir):
            os.makedirs(newDir)
    
    # In 'generationsCSV' dir, create new 'gen' dir
    newDir = newDir + 'finalGen' + os.sep
    if not os.path.exists(newDir):
        os.makedirs(newDir)
    
    # All Candidates of a Generation
    i = 0
    for cand in solutionsI.getList():            
        outName = newDir + 'finalGen_candInf' +  str(i) + '.csv'
        with open(outName, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['sLevel', 'sCode', 'sName', 'sQuadri', 'sPeriod', 'sCampus', 'sCharge', 'sTimetableList','pName', 'pPeriod', 'pCharge', 'pQuadriSabbath', 'pPrefCampus', 'pPrefSubjQ1List', 'pPrefSubjQ2List', 'pPrefSubjQ3List', 'pPrefSubjLimList'])
            # All relations in a Candidate of a Generation
            for s, p in cand.getList():
                row = s.get() + p.get()
                spamwriter.writerow(row)
            spamwriter.writerow(" ")
            spamwriter.writerow(['Infeasible', cand.getFitness()])
        # print("Created: " + outName + "in" + newDir + "...")
        i = i + 1
        csvfile.close()
    
    # All Candidates of a Generation
    i = 0
    for cand in solutionsF.getList():            
        outName = newDir + 'finalGen_candFea' +  str(i) + '.csv'
        with open(outName, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['sLevel', 'sCode', 'sName', 'sQuadri', 'sPeriod', 'sCampus', 'sCharge', 'sTimetableList','pName', 'pPeriod', 'pCharge', 'pQuadriSabbath', 'pPrefCampus', 'pPrefSubjQ1List', 'pPrefSubjQ2List', 'pPrefSubjQ3List', 'pPrefSubjLimList'])
            # All relations in a Candidate of a Generation
            for s, p in cand.getList():
                row = s.get() + p.get()
                spamwriter.writerow(row)
            spamwriter.writerow(" ")
            spamwriter.writerow(['Feasible', cand.getFitness()])
        # print("Created: " + outName + "in" + newDir + "...")
        i = i + 1
        csvfile.close()
            
    # All Fitness in a Generation
    outName = newDir + 'gen' +  str(num) + '.csv'
    with open(outName, 'wb') as csvfile:
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
    # print("Created: " + outName + "in" + newDir + "...")
    csvfile.close()
            
    print ("Data Exported!")   
    
def printOneCand(candidate):
    for s, p in candidate.getList():
        print s.get(), p.get()

def printAllCand(solutionsI, solutionsF):
    for cand in solutionsI.getList():
        self.printOneCand(cand)
    for cand in solutionsF.getList():
        self.printOneCand(cand)    
        print ("--------")    

def printOneFit(candidate):
    print (': Infeasible, ', str(candidate.getFitness()), ' / ')

def printMMAFit(solutionsI, solutionsF):
    min = 0
    max = 0
    for cand in solutionsI.getList():             
        if(cand.getFitness() < min):
            min = cand.getFitness()
    
    for cand in solutionsF.getList():             
        if(cand.getFitness() > max):
            max = cand.getFitness()
    
    print 'Min:', min, 'Max:', max, 'Med:', (min+max)/2
                            
def printAllFit(solutionsI, solutionsF):
    n = 0
    for cand in solutionsI.getList():
        print str(n), ': Infeasible, ', str(cand.getFitness()), ' / ',
        n = n + 1
    
    n = 0
    for cand in solutionsF.getList():
        print str(n), ': Feasible, ', str(cand.getFitness()), ' / ',
        n = n + 1    
        