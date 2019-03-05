from objects import *
from uctp import *
from ioData import *
        
#==============================================================================================================            
## LOOK TO QUINZENAL
            
# main
class main:
    # to access UCTP Main methods and creating Solutions (List of Candidates)
    uctp = UCTP()
    # Main candidates of a generation
    solutionsI = Solutions()
    solutionsF = Solutions()
    # Candidates without classification 
    solutionsNoPop = Solutions()
    # Candidates generated in a iteration (will be selected to be, or not, in the main List of Candidates)
    infPool = Solutions()
    feaPool = Solutions()
    
    # Base Lists of Professors and Subjects - never modified through the run
    prof = []
    subj = []
    
    # Max Number of iterations to get a solution
    iterations = 2
    # number of candidates in a generation (same for each Feas/Inf.)
    numCand = 100
    # Percentage of candidates from Feasible Pop. that will be selected through a Roulette to make after, a Crossover
    pctRouletteCross = 50
    # Percentage of mutation that maybe each offspring will suffer 
    pctMut = 15
    
    # Weights (!!!must be float!!!)
    w_alpha = 1.0
    w_beta = 1.0
    w_gamma = 1.0
    w_delta = 1.0
    w_omega = 1.0
    w_sigma = 1.0
    w_pi = 1.0
    w_rho = 1.0
    weights = [w_alpha, w_beta, w_gamma, w_delta, w_omega, w_sigma, w_pi, w_rho]
    
    # Start of the works
    # Getting data
    getData(subj, prof)
    
    # Creating the first 'numCand' candidates (First Generation)
    uctp.start(solutionsNoPop, subj, prof, numCand)
    # Classification and calculating this first candidates
    uctp.twoPop(solutionsNoPop, solutionsI, solutionsF, prof, subj)
    uctp.calcFit(solutionsI, solutionsF, prof, subj, weights)
    # Print and export generated data
    outDataMMA(solutionsI, solutionsF)
    
    # Main work - iterations of GA-Algorithm to find a solution
    print(" ")
    print("Starting hard work...")
    t = 0;
    while(uctp.stop(t, iterations, solutionsI, solutionsF)):
        print 'Iteration:', t+1
        # Choosing Parents to generate children (solutionsNoPop) 
        uctp.offspringI(solutionsNoPop, solutionsI, prof) 
        uctp.offspringF(solutionsNoPop, solutionsF, prof, pctMut, pctRouletteCross, numCand)
        # Classification and calculating this new candidates 
        uctp.twoPop(solutionsNoPop, infPool, feaPool, prof, subj)
        uctp.calcFit(infPool, feaPool, prof, subj, weights)
        # Selecting between parents (old generation) and children (new candidates) to create the new generation
        uctp.selectionI(infPool, solutionsI, numCand)
        uctp.selectionF(feaPool, solutionsF, numCand)
        # Print and export generated data
        outDataMMA(solutionsI, solutionsF)
        if((t/10) % 2 == 0):
            printAllFit(solutionsI, solutionsF)
        print(" ")
        
        # Next Iteration
        t = t+1
    # End While (Iterations) - Stop condition verified
     
    # Export last generation of candidates (with a Solution)  
    outData(solutionsI, solutionsF, t)        
    print("FIM")
            
#==============================================================================================================