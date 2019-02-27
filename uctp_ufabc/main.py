from objects import *
from uctp import *
from ioData import *
            
# main
class main:
    # to access UCTP Main methods and creating Solutions (List of Candidates)
    uctp = UCTP()
    solutionsI = Solutions()
    solutionsF = Solutions()
    solutionsNoPop = Solutions()
    infPool = Solutions()
    feaPool = Solutions()
    
    # Base Lists of Professors and Subjects
    prof = []
    subj = []
    
    # Max Number of iterations to get a solution
    iterations = 10
    # number of candidates in a generation (same for each Feas/Inf.)
    numCand = 100
    # Percentage of candidates from Feasible Pop. that will pass through Roullete (Crossover) -> Mutation
    pctMut = 15
    pctRouletteCross = 50
    
    # Weights
    w_alpha = 1
    w_beta = 1
    w_gamma = 1
    w_delta = 1
    w_omega = 1
    w_sigma = 1
    w_pi = 1
    w_rho = 1
    weights = [w_alpha, w_beta, w_gamma, w_delta, w_omega, w_sigma, w_pi, w_rho]
    
    # Start of the works
    getData(subj, prof)
    
    # First generation
    uctp.start(solutionsNoPop, subj, prof, numCand)
    uctp.twoPop(solutionsNoPop, solutionsI, solutionsF, prof, subj)
    uctp.calcFit(solutionsI, solutionsF, prof, subj, weights)
    outDataMMA(solutionsI, solutionsF)
    printMMAFit(solutionsI, solutionsF)
    printAllFit(solutionsI, solutionsF)
    
    # Main work - iterations to find a solution
    print(" ")
    print("Starting hard work...")
    t = 0;
    while(uctp.stop(t, iterations, solutionsI, solutionsF)):
        print 'Iteration:', t+1

        uctp.offspringI(solutionsNoPop, solutionsI, prof) 
        uctp.offspringF(solutionsNoPop, solutionsF, prof, pctMut, pctRouletteCross, numCand) 
        #uctp.resetPop(solutionsNoPop, solutionsI, solutionsF)
        uctp.twoPop(solutionsNoPop, infPool, feaPool, prof, subj)
        uctp.calcFit(infPool, feaPool, prof, subj, weights)
        uctp.selectionI(infPool, solutionsI, numCand)
        uctp.selectionF(feaPool, solutionsF, numCand)
        
        outDataMMA(solutionsI, solutionsF)
        printMMAFit(solutionsI, solutionsF)
        printAllFit(solutionsI, solutionsF)
        print(" ")
        t = t+1
        
    outData(solutionsI, solutionsF, t)        
    print("FIM")
    
