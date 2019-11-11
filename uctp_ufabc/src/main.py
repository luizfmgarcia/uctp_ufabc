# Main Class - Algorithm

import objects
import uctp
import ioData
import time

#==============================================================================================================
# Install Pandas, Python 3 and PIP
# To see the main time spent of the algorithm on cmd (on the end of the run), run with:
#   python -m cProfile -s cumtime main.py
# To not use the default configurations (in ioData.py file), run with (e.g.):
#   python main.py 1 0 10000 20 50 1000 0 90 15 5 1.0 1.0 1.0 0.05 0.05 0.05 0.05 0.05 0.05 0.05
# To Debug:
#   import pdb
#   pdb.set_trace()
#==============================================================================================================

class main():
    # Get CONFIG var values
    printSteps, asks, maxNum_Iter, maxNumCand_perPop, convergDetect, pctParentsCross, pctElitism, twoPointsCross, reposCross, reposSelInf, reposSelFea, w_alpha, w_beta, w_gamma, w_delta, w_omega, w_sigma, w_pi, w_rho, w_lambda, w_theta = ioData.getConfig()

    #----------------------------------------------------------------------------------------------------------
    # MAIN VARIABLES

    numInfWeights = 3 # Number of infeasible weights to divide properly 'weightsList' vector into some functions

    # Gathering all CONFIG variables
    weightsList = [w_alpha, w_beta, w_gamma, w_delta, w_omega, w_sigma, w_pi, w_rho, w_lambda, w_theta]
    configVarList = [maxNum_Iter, maxNumCand_perPop, convergDetect, pctParentsCross, pctElitism, twoPointsCross,
                    reposCross, reposSelInf, reposSelFea] + weightsList

    profList, subjList = [], [] # Base Lists of Professors and Subjects - never modified through the run

    solutionsI, solutionsF = objects.Solutions(), objects.Solutions() # Main candidates of a generation
    solutionsNoPop = objects.Solutions() # Candidates without classification
    # 'Children' Candidates generated in a iteration (will be selected to be, or not, in the main List of Candidates)
    infPool, feaPool = objects.Solutions(), objects.Solutions()

    maxFitIndexes, minFitInf, maxFitInf, avgFitInf, minFitFea, maxFitFea, avgFitFea = [], 0, 0, 0, 0, 0, 0 # Variables to inform important Fitness Values
    lastMaxFit_Iter, lastMaxFit = 0, -1 # Variables that records when current MaxFit Sol appears and its Fit value
    firstFeasSol_Iter = -1 # Flag to mark when appears the first Feasible Solution during a run
    recordNumIter = 0 # Record number of iterations occurred where MaxFit did not change
    curr_Iter = 1 # Initial Iteration value

    #----------------------------------------------------------------------------------------------------------
    # START OF THE WORK

    ioData.startOutputDirs(asks) # Creating folders if is needed
    start_time = time.time() # Recording duration of the run
    #runProfile = ioData.startRunData() # Start Record Run Info with cProfile
    
    subjList, profList = ioData.getData() # Getting data to work with
    subjIsPrefList = uctp.extractSubjIsPref(subjList, profList) # Extracting basic info about Prof's Subj Preferences
    uctp.start(solutionsNoPop, subjList, profList, maxNumCand_perPop)  # Creating the first 'maxNumCand_perPop' candidates (First Generation)

    #----------------------------------------------------------------------------------------------------------
    # MAIN WORK - iterations of GA-Algorithm to find an optimal solution
    
    stopReturn = False
    while(not stopReturn):
        # Choosing Parents to generate children (put all new into 'solutionsNoPop')
        uctp.offspringI(solutionsNoPop, solutionsI, profList, subjList, subjIsPrefList)
        uctp.offspringF(solutionsNoPop, solutionsF, profList, subjList, subjIsPrefList, maxNumCand_perPop, pctParentsCross, reposCross, twoPointsCross)

        # Classification and Fitness calculation of all new candidates
        uctp.twoPop(solutionsNoPop, infPool, feaPool, profList, subjList, weightsList, numInfWeights)
        uctp.calcFit(infPool, feaPool, profList, subjList, weightsList, numInfWeights, subjIsPrefList)

        # Selecting between parents (old generation) and children (new candidates) to create the next generation
        uctp.selectionI(infPool, solutionsI, maxNumCand_perPop, reposSelInf)
        uctp.selectionF(feaPool, solutionsF, maxNumCand_perPop, pctElitism, reposSelFea)

        # Get, print and export generated data of current iteration
        maxFitIndexes, minFitInf, maxFitInf, avgFitInf, minFitFea, maxFitFea, avgFitFea = ioData.getDataMMA(solutionsI, solutionsF)
        ioData.outDataMMA(minFitInf, maxFitInf, avgFitInf, minFitFea, maxFitFea, avgFitFea, curr_Iter)

        # Register of the 'Iteration' that appeared the first Feas Sol
        if(firstFeasSol_Iter == -1 and len(solutionsF.getCandList()) != 0): firstFeasSol_Iter = curr_Iter
        # Register of the 'Iteration' that the Max Sol changed
        if(len(solutionsF.getCandList()) != 0): maxFit_toCheck = maxFitFea # If already there is Feasible Solutions
        else: maxFit_toCheck = maxFitInf # There is only Infeasible Solutions
        if(lastMaxFit != maxFit_toCheck):
            lastMaxFit = maxFit_toCheck
            diff = curr_Iter - lastMaxFit_Iter
            if(diff > recordNumIter): recordNumIter = diff
            lastMaxFit_Iter = curr_Iter

        # Important print of each run
        if(printSteps == 1):
            ioData.printHead(profList, subjList, curr_Iter, maxNum_Iter, firstFeasSol_Iter, lastMaxFit_Iter, recordNumIter)
            ioData.printTail(solutionsI, solutionsF, minFitInf, maxFitInf, avgFitInf, minFitFea, maxFitFea, avgFitFea)

        # Verify the stop conditions occurrence
        stopReturn = uctp.stop(asks, curr_Iter, maxNum_Iter, lastMaxFit_Iter, convergDetect, maxFitFea)
        if(stopReturn != False and stopReturn !=  True): # If returned a number (more iterations to do)
            maxNum_Iter = maxNum_Iter + stopReturn
            stopReturn = False

        # Next Iteration
        if(stopReturn == False): curr_Iter = curr_Iter + 1
    # End of While (Iterations) - Stop condition verified

    #----------------------------------------------------------------------------------------------------------
    # FINAL process on the data

    # Export last generation of candidates and Config-Run Info
    final_time = time.time() - start_time
    bestSol_FitList, bestSol_ResumRelatList, bestSol_extractInfoList = ioData.finalOutData(solutionsI, solutionsF, profList, subjList, subjIsPrefList, curr_Iter, firstFeasSol_Iter, lastMaxFit_Iter, recordNumIter, final_time, maxFitIndexes, configVarList)
    if(printSteps == 1): ioData.printFinalResults(configVarList, maxFitIndexes, bestSol_FitList, bestSol_ResumRelatList, bestSol_extractInfoList, final_time)
    #ioData.outRunData(runProfile) # Record Run Info End
    if(printSteps == 1): print("End of works")

#==============================================================================================================