# Main Class - Algorithm

import objects
import uctp
import ioData

#==============================================================================================================
# Run with <python -m cProfile -s cumtime main.py> to see the main time spent of the algorithm
# Debug <import pdb; pdb.set_trace()>

# main
class main:
    # Start Record Run Info with cProfile 
    runProfile = ioData.startRunData()

    #----------------------------------------------------------------------------------------------------------
    # CONFIGURATION

    # RUN CONFIG
    # Set '1' to allow, during the run, the print on terminal of some steps
    printSteps = 1
    # Max Number of iterations to get a solution
    maxNum_Iter = 10000
    # Number of candidates in a generation (same for each Pop Feas./Inf.)
    maxNumCand_perPop = 100
    # Initial number of solutions generated randomly
    numCandInit = 200
    # Convergence Detector: num of iterations passed since last MaxFit found
    convergDetect = 1000 # equal '0' to not consider this condition
    # Max Fitness value that must find to stop the run before reach 'maxNum_Iter'
    stopFitValue = 0.9 # equal '0' to not consider this condition
 
    # OPERATORS CONFIG (Must be between '0' and '100')
    # Percentage of candidates from Feasible Pop. that will be selected, to become Parents and make Crossovers, through a Roulette Wheel with Reposition
    pctParentsCross = 70 # The rest (to complete 100%) will pass through Mutation
    # Percentage of mutation that maybe each child generated through 'Crossover' process will suffer 
    pctMut_childCross = 70
    # Percentage of selection by elitism of feasible candidates, the rest of them will pass through a Roulette Wheel
    pctElitism = 5

    # WEIGHTS CONFIG (must be Float)
    w_alpha = 1.0   # i1 - Prof without Subj
    w_beta = 1.0    # i2 - Subjs (same Prof), same quadri and timetable conflicts
    w_gamma = 1.0   # i3 - Subjs (same Prof), same quadri and day but in different campus
    
    w_delta = 1.0   # f1 - Balance of distribution of Subjs between Profs with each pCharge
    w_omega = 1.0   # f2 - Profs preference Subjects
    w_sigma = 1.0   # f3 - Profs with Subjs in quadriSabbath
    w_pi = 1.0      # f4 - Profs with Subjs in Period
    w_rho = 1.0     # f5 - Profs with Subjs in Campus
    w_lambda = 1.0  # f6 - Balance of distribution of Subjs between Profs with an average
    w_theta = 1.0   # f7 - Quality of relations (subj (not) appears in some list of pref or/and same quadriList)

    numInfWeights = 3 # Number of infeasible weights to divide properly 'weightsList' vector into some functions

    # Gathering all variables
    weightsList = [w_alpha, w_beta, w_gamma, w_delta, w_omega, w_sigma, w_pi, w_rho, w_lambda, w_theta]
    configVarList = [maxNum_Iter, maxNumCand_perPop, numCandInit, convergDetect, stopFitValue, pctParentsCross, 
              pctMut_childCross, pctElitism] + weightsList
    
    #----------------------------------------------------------------------------------------------------------
    # MAIN VARIABLES

    # Main candidates of a generation
    solutionsI, solutionsF = objects.Solutions(), objects.Solutions()
    # Candidates without classification
    solutionsNoPop = objects.Solutions()
    # Candidates generated in a iteration (will be selected to be, or not, in the main List of Candidates)
    infPool, feaPool = objects.Solutions(), objects.Solutions()
    # Base Lists of Professors and Subjects - never modified through the run
    profList, subjList = [], []
    # Other variables
    maxFitFeaIndex, minFitInf, maxFitInf, avgFitInf, minFitFea, maxFitFea, avgFitFea = [], 0, 0, 0, 0, 0, 0
    # Flag to mark when appears the first Feasible Solution during a run
    firstFeasSol_Iter = -1
    # Variables that records when current MaxFit Feas Sol appears and its Fit value
    lastMaxFitFea_Iter, lastMaxFitFea = 0, 0
    # Initial Iteration value
    curr_Iter = 0

    #----------------------------------------------------------------------------------------------------------
    # START OF THE WORK
    
    # Creating folders if is needed
    ioData.startOutputDirs()
    
    # Getting data to work with
    ioData.getData(subjList, profList)

    # Extracting basic info about Prof's Subj Preferences
    subjIsPrefList = uctp.extractSubjIsPref(subjList, profList)
    
    # Creating the first 'maxNumCand_perPop' candidates (First Generation)
    uctp.start(solutionsNoPop, subjList, profList, numCandInit)

    # Classification and Fitness calc of the first candidates
    uctp.twoPop(solutionsNoPop, solutionsI, solutionsF, profList, subjList, weightsList, numInfWeights)
    uctp.calcFit(solutionsI, solutionsF, profList, subjList, weightsList, numInfWeights, subjIsPrefList)

    # Print and export generated data
    if(printSteps == 1): ioData.printHead(profList, subjList, curr_Iter, maxNum_Iter, firstFeasSol_Iter, lastMaxFitFea_Iter)
    maxFitFeaIndex, _, _, _, _, maxFitFea, _ = ioData.outDataMMA(solutionsI, solutionsF, curr_Iter)
    if(len(maxFitFeaIndex) != 0): lastMaxFitFea = maxFitFea
    # Next iteration
    curr_Iter = curr_Iter + 1
    
    #----------------------------------------------------------------------------------------------------------
    # MAIN WORK - iterations of GA-Algorithm to find a solution
    
    # Verify the stop conditions occurrence
    while(not uctp.stop(curr_Iter, maxNum_Iter, lastMaxFitFea_Iter, convergDetect, maxFitFea, stopFitValue)):
        # First print of each run
        if(printSteps == 1): ioData.printHead(profList, subjList, curr_Iter, maxNum_Iter, firstFeasSol_Iter, lastMaxFitFea_Iter)
        
        # Choosing Parents to generate children (put all new into 'solutionsNoPop')
        uctp.offspringI(solutionsNoPop, solutionsI, profList, subjList, subjIsPrefList)
        uctp.offspringF(solutionsNoPop, solutionsF, profList, subjList, pctMut_childCross, pctParentsCross, maxNumCand_perPop, subjIsPrefList)
        
        # Classification and Fitness calculation of all new candidates
        uctp.twoPop(solutionsNoPop, infPool, feaPool, profList, subjList, weightsList, numInfWeights)
        uctp.calcFit(infPool, feaPool, profList, subjList, weightsList, numInfWeights, subjIsPrefList)
        
        # Selecting between parents (old generation) and children (new candidates) to create the next generation
        uctp.selectionI(infPool, solutionsI, maxNumCand_perPop)
        uctp.selectionF(feaPool, solutionsF, maxNumCand_perPop, pctElitism)
        
        # Print and export generated data
        maxFitFeaIndex, minFitInf, maxFitInf, avgFitInf, minFitFea, maxFitFea, avgFitFea = ioData.outDataMMA(solutionsI, solutionsF, curr_Iter)
        
        # Last print of each run
        if(printSteps == 1): ioData.printTail(solutionsI, solutionsF, minFitInf, maxFitInf, avgFitInf, minFitFea, maxFitFea, avgFitFea)
    
        # Register of the 'Iteration' that appeared the first Feas Sol
        if(firstFeasSol_Iter == -1 and len(solutionsF.getCandList()) != 0): firstFeasSol_Iter = curr_Iter
        
        # Register of the 'Iteration' that the Max Feas Sol changed
        if(firstFeasSol_Iter != -1 and lastMaxFitFea != maxFitFea):
            lastMaxFitFea = maxFitFea
            lastMaxFitFea_Iter = curr_Iter

        # Next Iteration
        curr_Iter = curr_Iter + 1
    # End of While (Iterations) - Stop condition verified
    
    #----------------------------------------------------------------------------------------------------------
    # FINAL processing of the data
    
    # Export last generation of candidates and Config-Run Info
    #ioData.outDataGeneration(solutionsI, solutionsF, curr_Iter, profList, subjList, subjIsPrefList)
    fitMaxData, resumeMaxData, maxInfo = ioData.finalOutData(solutionsI, solutionsF, curr_Iter, profList, subjList, subjIsPrefList, maxFitFeaIndex, configVarList)
    if(printSteps == 1): ioData.printFinalResults(configVarList, maxFitFeaIndex, fitMaxData, resumeMaxData, maxInfo)
    # Record Run Info End
    ioData.outRunData(runProfile)
    if(printSteps == 1): print("End of works")

#==============================================================================================================    