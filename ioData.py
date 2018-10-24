# Import/Export Data Methods

from objects import *
import csv
import os
import sys
    
# Get all data to work
def getData(subj, prof):
    # Remove accents of datas
    #from unicodedata import normalize 
    #def remove_accent(txt):
    #    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
    
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
    return subj, prof

# Export Candidates in differents generations into CSV files
def outData(solutions, num):
    print "Exporting data....",
    
    # get current directory and creating new 'generationsCSV' dir
    currentDir = os.getcwd()
    newDir = currentDir + os.sep + 'generationsCSV' + os.sep
    if not os.path.exists(newDir):
            os.makedirs(newDir)
    
    # In 'generationsCSV' dir, create new 'gen' dir
    newDir = newDir + 'gen' + str(num) + os.sep
    if not os.path.exists(newDir):
        os.makedirs(newDir)
    
    # All Candidates of a Generation
    i = 0
    for cand in solutions.get():            
        outName = newDir + 'gen' +  str(num) + '_cand' +  str(i) + '.csv'
        with open(outName, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['sLevel', 'sCode', 'sName', 'sQuadri', 'sPeriod', 'sCharge', 'pName', 'pPeriod', 'pCharge', 'pQuadriSabbath'])
            # All relations in a Candidate of a Generation
            for s, p in cand.get():
                row = s.get() + p.get()
                spamwriter.writerow(row)
            spamwriter.writerow(" ")
            if cand.getIF() is 'f':
                spamwriter.writerow(['Feasible', cand.getFitness()])
            elif cand.getIF() is 'i':
                spamwriter.writerow(['Infeasible', cand.getFitness()])
            else:
                spamwriter.writerow(['Error', cand.getFitness()])   
        # print("Created: " + outName + "in" + newDir + "...")
        i = i + 1
        csvfile.close()
        
    # All Fitness in a Generation
    outName = newDir + 'gen' +  str(num) + '.csv'
    with open(outName, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Candidate', 'Population', 'Fitness'])
        i = 0
        for cand in solutions.get():            
            if cand.getIF() is 'f':
                spamwriter.writerow([i,'Feasible', cand.getFitness()])
            elif cand.getIF() is 'i':
                spamwriter.writerow([i,'Infeasible', cand.getFitness()])
            else:
                spamwriter.writerow([i,'Error', cand.getFitness()])
            i = i + 1       
    # print("Created: " + outName + "in" + newDir + "...")
    csvfile.close()
            
    print ("Data Exported!")    
    
def printOneCand(candidate):
    for s, p in candidate.get():
        print s.get(), p.get()

def printAllCand(solutions):
    for cand in solutions.get():
        self.printOneCand(cand)
        print ("--------")

def printOneFit(cand):
    if cand.getIF() is 'f':
       print (': Feasible, ', str(cand.getFitness()))
    elif cand.getIF() is 'i':
        print (': Infeasible, ', str(cand.getFitness()))
    else:
        print (': Error, ', str(cand.getFitness()))     
        
def printAllFit(solutions):
    n = 1
    for cand in solutions.get():
        if cand.getIF() is 'f':
           print str(n), ': Feasible, ', str(cand.getFitness()), ' / ',
        elif cand.getIF() is 'i':
            print str(n), ': Infeasible, ', str(cand.getFitness()), ' / ',
        else:
            print str(n), ': Error, ', str(cand.getFitness()), ' / ',       
        n = n + 1
        