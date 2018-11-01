# Import/Export Data Methods

from objects import *
import csv
import os
import sys
    
# Get all data to work
def getData(subj, prof): 
    # Read the data of professors and subjects and create the respective objects
    print "Getting datas of Professors...",
    with open('professors.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        print "Setting Professors...",
        for row in spamreader:
            datas = [row[0].upper(), row[1].upper(), row[2].upper(), row[3].upper()]
            if(not datas.__contains__('')):
                prof.append(Prof(datas[0], datas[1], datas[2], datas[3]))
                print datas
    csvfile.close() 
        
    print(" ")
    print "Getting datas of Subjects...",
    with open('subjects.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        print "Setting Subjects...",
        for row in spamreader:
            datas = [row[0].upper(), row[1].upper(), row[2].upper(), row[3].upper(), row[4].upper(), row[5].upper(), row[6].upper()]
            if(not datas.__contains__('') and row[0] == 'G' and ('MCTA' in row[1] or 'MCZA' in row[1])):
                subj.append(Subject(datas[0], datas[1], datas[2], datas[3], datas[4], datas[5], datas[6]))
                print datas       
    csvfile.close()
        
    print ("Data Obtained!")
    
    #this code starts the OUT CSV with the titles
    # get current directory and creating new 'generationsCSV' dir
    currentDir = os.getcwd()
    newDir = currentDir + os.sep + 'generationsCSV' + os.sep
    if not os.path.exists(newDir):
            os.makedirs(newDir)
    outName = newDir + 'totalMinMaxAvg.csv'
                    
    with open(outName, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['min', 'max', 'avg'])  
    # print("Created: " + outName + "in" + newDir + "...")
    csvfile.close()

def outDataMMM(solutionsI, solutionsF):
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
    for cand in solutionsI.get():             
        if(cand.getFitness() < min):
            min = cand.getFitness()
    
    for cand in solutionsF.get():             
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
    for cand in solutionsI.get():            
        outName = newDir + 'finalGen_candInf' +  str(i) + '.csv'
        with open(outName, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['sLevel', 'sCode', 'sName', 'sQuadri', 'sPeriod', 'sCharge', 'pName', 'pPeriod', 'pCharge', 'pQuadriSabbath'])
            # All relations in a Candidate of a Generation
            for s, p in cand.get():
                row = s.get() + p.get()
                spamwriter.writerow(row)
            spamwriter.writerow(" ")
            spamwriter.writerow(['Infeasible', cand.getFitness()])
        # print("Created: " + outName + "in" + newDir + "...")
        i = i + 1
        csvfile.close()
    
    # All Candidates of a Generation
    i = 0
    for cand in solutionsF.get():            
        outName = newDir + 'finalGen_candFea' +  str(i) + '.csv'
        with open(outName, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['sLevel', 'sCode', 'sName', 'sQuadri', 'sPeriod', 'sCharge', 'pName', 'pPeriod', 'pCharge', 'pQuadriSabbath'])
            # All relations in a Candidate of a Generation
            for s, p in cand.get():
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
        for cand in solutionsI.get():            
            spamwriter.writerow([i,'Infeasible', cand.getFitness()])
            i = i + 1
        
        i = 0
        for cand in solutionsF.get():            
            spamwriter.writerow([i,'Feasible', cand.getFitness()])
            i = i + 1            
    # print("Created: " + outName + "in" + newDir + "...")
    csvfile.close()
            
    print ("Data Exported!")   
    
def printOneCand(candidate):
    for s, p in candidate.get():
        print s.get(), p.get()

def printAllCand(solutionsI, solutionsF):
    for cand in solutionsI.get():
        self.printOneCand(cand)
    for cand in solutionsF.get():
        self.printOneCand(cand)    
        print ("--------")    

def printOneFit(candidate):
    print (': Infeasible, ', str(candidate.getFitness()), ' / ')
            
def printAllFit(solutionsI, solutionsF):
    n = 0
    for cand in solutionsI.get():
        print str(n), ': Infeasible, ', str(cand.getFitness()), ' / ',
        n = n + 1
    
    n = 0
    for cand in solutionsF.get():
        print str(n), ': Feasible, ', str(cand.getFitness()), ' / ',
        n = n + 1    
        