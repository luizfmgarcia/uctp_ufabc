# Process to execute automatically many instances/configs of the algorithm sequentially
# Before run: dont forget that this will erase all '.\results\run_x\' folders
# You have to copy the 'fitInstances.csv' - this specific file will be overwritten

import os
import csv
import shutil
import itertools

search_fit = 'Fit' # All
search_time = 'Time (sec)' # All
search_first = 'First Feas Sol at (iter)' # Infeas.
search_last = 'Last Iter' # NumCand
search_record = 'Record Num Iter No New Max' # NumCand
#-------------------------------------------------------

def getFitTime(i):
    folderName = 'results/run_' + str(i)
    fileName = folderName + '/runConfigResult_' + str(i) + '.csv'
    with open(fileName, encoding='unicode_escape') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            if(len(row) > 0):
                if(search_fit in str(row[0])): fit = row[2]
                if(search_time in str(row[0])): time = row[1]
                if(search_first in str(row[0])): first = row[1]
                if(search_last in str(row[0])): last = row[1]
                if(search_record in str(row[0])): record = row[1]
    csvfile.close()
    return fit, time, first, last, record

#-------------------------------------------------------

def outFitTime(i, fit, time, first, last, record):
    outFile = 'fitInstances.csv'
    # First instance - Verify and delete file if already exists
    if(i == 1 and os.path.exists(outFile)): os.remove(outFile)
    
    with open(outFile, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        if(i == 1): spamwriter.writerow(['Inst', search_fit, search_time, 'First Feas (at Iter)', search_last, search_record])
        spamwriter.writerow([i, fit, time, first, last, record])
    csvfile.close()

#-------------------------------------------------------

# Run sequentially different configurations
def runSeq(initialNum=1, repeatRunNum=10):
    # Repetitions of the run
    for currRun in range(initialNum, repeatRunNum + 1):
        # Deleting old results
        if os.path.exists('results'): shutil.rmtree('results')
        # Creating a new folder
        os.makedirs('results')

        with open("manyInstances.csv", encoding='unicode_escape') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            next(spamreader, None)  # Skip the headers
            i = 1 # Each instance
            
            # Execute the algorithm for each instance
            for row in spamreader:
                print("Executing the alg. with config:" + str(i))
                executeString = "src" + os.sep + "main.py"
                # Gathering config values to execute (cmd) the algorithm with params
                for r in row: executeString = executeString + " " + str(r)
                os.system(executeString) # Executing
                fit, time, first, last, record = getFitTime(i) # Get fitTime obtained of curr instance
                outFitTime(i, fit, time, first, last, record) # Output fit, Time and others
                i = i + 1 # Next instance
        csvfile.close()

        # Renaming folders to next run
        newName = ['fitInstances' + str(currRun) + '.csv', 'results' + str(currRun)]
        # Deleting old results
        for name in newName:
            if os.path.exists(name): shutil.rmtree(name)
        os.rename('fitInstances.csv', newName[0])
        os.rename('results', newName[1])

#-------------------------------------------------------

# Generate Cartesian Product of all different values for each config
def genConfig():
    # Num Cand: [1, 2, 5, 10, 15, 20, 30, 50, 70, 100]
    # Elitism
    #   Indv: 0, 1, 5, 10, 15, 20
    #   %: [0, 5, 25, 50, 75, 100]
    # Crossover
    #   Indv: 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20
    #   %: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    # twoPointsCross = [0, 1, -1]
    # Reposition: [0, 1]
    # Weights
    #   Complete: [0.05, 0.25, 0.5, 0.75, 1.0]
    #   Partial: [0.05, 0.5, 0.75]
    printSteps = [1]
    asks = [0]
    maxNum_Iter = [10000]
    maxNumCand_perPop = [20]
    convergDetect = [500]
    pctParentsCross = [80]
    pctElitism = [25]
    twoPointsCross = [1]
    reposCross = [0]
    reposSelInf = [0]
    reposSelFea = [1]
    w_alpha = [0.75]
    w_beta = [0.75]
    w_gamma = [0.75]
    w_delta = [0.05, 0.5, 0.75]
    w_omega = [0.05, 0.5, 0.75]
    w_sigma = [0.05, 0.5, 0.75]
    w_pi = [0.05, 0.5, 0.75]
    w_rho = [0.05, 0.5, 0.75]
    w_lambda = [0.05, 0.5, 0.75]
    w_theta = [0.05, 0.5, 0.75]

    # Getting the product of all possibilities
    result = itertools.product(printSteps, asks, maxNum_Iter, maxNumCand_perPop, convergDetect, pctParentsCross, pctElitism, twoPointsCross, 
    reposCross, reposSelInf, reposSelFea, w_alpha, w_beta, w_gamma, w_delta, w_omega, w_sigma, w_pi, w_rho, w_lambda, w_theta)
    
    # Transforming the Product to list of configs
    result = str(list(result))[2:-2]
    result = result.replace(', ',';')[:]
    result = result.split(");(")[:]
    
    # Recording Configs
    with open('manyInstances.csv', 'w') as f:
        f.write("printSteps;asks;maxNum_Iter;maxNumCand_perPop;convergDetect;pctParentsCross;pctElitism;twoPointsCross;reposCross;reposSelInf;reposSelFea;w_alpha;w_beta;w_gamma;w_delta;w_omega;w_sigma;w_pi;w_rho;w_lambda;w_theta" + '\n')
        for line in result: f.write(line + '\n')

#-------------------------------------------------------

#genConfig()
runSeq()