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
    pr = ioData.startRunData()

    #----------------------------------------------------------------------------------------------------------
    # CONFIGURATION

    # RUN CONFIG
    # Set '1' to allow, during the run, the print on terminal of some steps
    prt = 1
    # Max Number of iterations to get a solution
    maxIter = 100
    # Number of candidates in a generation (same for each Pop Feas/Inf.)
    numCand = 30
    # Initial number of solutions generated randomly
    numCandInit = 100
    # Convergence Detector: num of iterations passed since last MaxFit found
    convergDetect = 500 # equal '0' to not consider this condition
    # Max Fitness value that must find to stop the run before reach 'maxIter'
    stopFitValue = 0.9 # equal '0' to not consider this condition
 
    # OPERATORS CONFIG (Must be between '0' and '100')
    # Percentage of candidates from Feasible Pop. that will be selected, to become Parents and make Crossovers, through a Roulette Wheel with Reposition
    pctParentsCross = 50 # The rest (to complete 100%) will pass through Mutation
    # Percentage of mutation that maybe each child generated through 'Crossover' process will suffer 
    pctMut = 70
    # Percentage of selection by elitism of feasible candidates, the rest of them will pass through a Roulette Wheel
    pctElitism = 5

    # WEIGHTS CONFIG (must be Float)
    w_alpha = 1.0   # i1 - Prof without Subj
    w_beta = 3.0    # i2 - Subjs (same Prof), same quadri and timetable conflicts
    w_gamma = 2.0   # i3 - Subjs (same Prof), same quadri and day but in different campus
    w_delta = 2.0   # f1 - Balance of distribution of Subjs between Profs with each pCharge
    w_omega = 2.0   # f2 - Profs preference Subjects
    w_sigma = 1.5   # f3 - Profs with Subjs in quadriSabbath
    w_pi = 1.0      # f4 - Profs with Subjs in Period
    w_rho = 1.3     # f5 - Profs with Subjs in Campus
    w_lambda = 3.0  # f6 - Balance of distribution of Subjs between Profs with an average
    w_theta = 5.0  # f7 - Quality of relations (subj (not) appears in some list of pref or/and same quadriList)

    numInfWeights = 3 # Number of infeasible waights to divide properly 'weights' vector into some functions

    # Gathering all variables
    weights = [w_alpha, w_beta, w_gamma, w_delta, w_omega, w_sigma, w_pi, w_rho, w_lambda, w_theta]
    config = [maxIter, numCand, numCandInit, convergDetect, stopFitValue, pctParentsCross, 
              pctMut, pctElitism] + weights
    
    #----------------------------------------------------------------------------------------------------------
    # MAIN VARIABLES

    # Main candidates of a generation
    solutionsI, solutionsF = objects.Solutions(), objects.Solutions()
    # Candidates without classification
    solutionsNoPop = objects.Solutions()
    # Candidates generated in a iteration (will be selected to be, or not, in the main List of Candidates)
    infPool, feaPool = objects.Solutions(), objects.Solutions()
    # Base Lists of Professors and Subjects - never modified through the run
    prof, subj = [], []
    # Other variables
    maxFeaIndex, minInf, maxInf, avgInf, minFea, maxFea, avgFea = [], 0, 0, 0, 0, 0, 0
    # Flag to mark when appears the first Feasible Solution during a run
    firstFeasSol = -1
    # Variables that records when current MaxFit Feas Sol appears and its Fit value
    lastMaxIter, lastMax = 0, 0
    # Initial Iteration value
    curIter = 0

    #----------------------------------------------------------------------------------------------------------
    # START OF THE WORK
    
    # Creating folders if is needed
    ioData.startOutFolders()
    
    # Getting data to work with
    ioData.getData(subj, prof)

    # Extracting basic info about Prof's Subj Preferences
    subjIsPref = uctp.extractSubjIsPref(subj, prof)
    
    # Creating the first 'numCand' candidates (First Generation)
    uctp.start(solutionsNoPop, subj, prof, numCandInit)

    # Classification and Fitness calc of the first candidates
    uctp.twoPop(solutionsNoPop, solutionsI, solutionsF, prof, subj, weights, numInfWeights)
    uctp.calcFit(solutionsI, solutionsF, prof, subj, weights, numInfWeights, subjIsPref)

    # Print and export generated data
    if(prt == 1): ioData.printHead(prof, subj, curIter, maxIter, firstFeasSol, lastMaxIter)
    maxFeaIndex, _, _, _, _, maxFea, _ = ioData.outDataMMA(solutionsI, solutionsF, curIter)
    if(len(maxFeaIndex) != 0): lastMax = maxFea
    # Next iteration
    curIter = curIter + 1
    
    #----------------------------------------------------------------------------------------------------------
    # MAIN WORK - iterations of GA-Algorithm to find a solution
    
    # Verify the stop conditions occurence
    while(not uctp.stop(curIter, maxIter, lastMaxIter, convergDetect, maxFea, stopFitValue)):
        # First print of each run
        if(prt == 1): ioData.printHead(prof, subj, curIter, maxIter, firstFeasSol, lastMaxIter)
        
        # Choosing Parents to generate children (put all new into 'solutionsNoPop')
        uctp.offspringI(solutionsNoPop, solutionsI, prof, subj, subjIsPref)
        uctp.offspringF(solutionsNoPop, solutionsF, prof, subj, pctMut, pctParentsCross, numCand, subjIsPref)
        
        # Classification and Fitness calculation of all new candidates
        uctp.twoPop(solutionsNoPop, infPool, feaPool, prof, subj, weights, numInfWeights)
        uctp.calcFit(infPool, feaPool, prof, subj, weights, numInfWeights, subjIsPref)
        
        # Selecting between parents (old generation) and children (new candidates) to create the next generation
        uctp.selectionI(infPool, solutionsI, numCand)
        uctp.selectionF(feaPool, solutionsF, numCand, pctElitism)
        
        # Print and export generated data
        maxFeaIndex, minInf, maxInf, avgInf, minFea, maxFea, avgFea = ioData.outDataMMA(solutionsI, solutionsF, curIter)
        
        # Last print of each run
        if(prt == 1): ioData.printTail(solutionsI, solutionsF, minInf, maxInf, avgInf, minFea, maxFea, avgFea)
    
        # Register of the 'Iteration' that appeared the first Feas Sol
        if(firstFeasSol == -1 and len(solutionsF.getList()) != 0): firstFeasSol = curIter
        
        # Register of the 'Iteration' that the Max Feas Sol changed
        if(firstFeasSol != -1 and lastMax != maxFea):
            lastMax = maxFea
            lastMaxIter = curIter

        # Next Iteration
        curIter = curIter + 1
    # End of While (Iterations) - Stop condition verified
    
    #----------------------------------------------------------------------------------------------------------
    # FINAL processing of the data
    
    # Export last generation of candidates and Config-Run Info
    #ioData.outDataGeneration(solutionsI, solutionsF, curIter, prof, subj, subjIsPref)
    fitMaxData, resumeMaxData, maxInfo = ioData.finalOutData(solutionsI, solutionsF, curIter, prof, subj, subjIsPref, maxFeaIndex, config)
    if(prt == 1): ioData.printFinalResults(config, maxFeaIndex, fitMaxData, resumeMaxData, maxInfo)
    # Record Run Info End
    ioData.outRunData(pr)
    if(prt == 1): print("End of works")

#==============================================================================================================    