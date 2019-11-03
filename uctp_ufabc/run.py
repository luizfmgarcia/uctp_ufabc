# Process to execute automatically many instances/configs of the algorithm sequentially
# Before run: dont forget that this will erase all '.\results\run_x\' folders
# You have to copy the 'fitInstances.csv' - this specific file will be overwritten

import os
import csv
import shutil
import itertools

#-------------------------------------------------------

def getFit(instance):
    folderName = 'results/run_' + str(instance)
    fileName = folderName + '/runConfigResult_' + str(instance) + '.csv'
    lineToSearch = 'Index/Fit:'

    with open(fileName, encoding='unicode_escape') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            if(len(row) > 0 and lineToSearch in str(row[0])):
                instance = row[2]
                break
        csvfile.close()
    return instance

#-------------------------------------------------------

def outFit(i, fit):
    outFile = 'fitInstances.csv'
    # First instance - Verify and delete file if already exists
    if(i == 0 and os.path.exists(outFile)): os.remove(outFile)
    
    with open(outFile, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        if(i == 0): spamwriter.writerow(['Inst', 'Fit'])
        spamwriter.writerow([i, fit])
    csvfile.close()

#-------------------------------------------------------

# Run sequentially different configurations
if(1):
    # Deleting old results
    shutil.rmtree('results')
    os.makedirs('results')

    with open("manyInstances.csv", encoding='unicode_escape') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        next(spamreader, None)  # Skip the headers
        i = 0 # Each instance
        
        # Execute the algorithm for each instance
        for row in spamreader:
            print("Executing the alg. with config:" + str(i))
            executeString = "src\main.py"
            # Gathering config values to execute (cmd) the algorithm with params
            for r in row: executeString = executeString + " " + str(r)
            os.system(executeString) # Executing
            fit = getFit(i) # Get fit obtained of curr instance
            outFit(i, fit) # Output Fit
            i = i + 1 # Next instance

# Generate Cartesian Product of all different values for each config
else:
    printSteps = [1]
    asks = [0]
    maxNum_Iter = [10000]
    maxNumCand_perPop = [20]
    numCandInit = [50]
    convergDetect = [1000]
    stopFitValue = [0.9]
    pctParentsCross = [90]
    pctMut_childCross = [15]
    pctElitism = [5]
    w_alpha = [1.0]
    w_beta = [1.0]
    w_gamma = [1.0]
    w_delta = [0.05, 0.25, 0.5, 0.75, 1.0]
    w_omega = [0.05, 0.25, 0.5, 0.75, 1.0]
    w_sigma = [0.05, 0.25, 0.5, 0.75, 1.0]
    w_pi = [0.05, 0.25, 0.5, 0.75, 1.0]
    w_rho = [0.05, 0.25, 0.5, 0.75, 1.0]
    w_lambda = [0.05, 0.25, 0.5, 0.75, 1.0]
    w_theta = [0.05, 0.25, 0.5, 0.75, 1.0]

    result = itertools.product(printSteps, asks, maxNum_Iter, maxNumCand_perPop, numCandInit, convergDetect, stopFitValue, pctParentsCross, pctMut_childCross, pctElitism, w_alpha, w_beta, w_gamma, w_delta, w_omega, w_sigma, w_pi, w_rho, w_lambda, w_theta)

    with open('mxt.txt', 'w+') as f: f.write(str(list(result)))