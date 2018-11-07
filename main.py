#OPERADORES!!! de crossover e mutation, elitismo...

# filter subjects graduation and computing only;
# So....level = 'G' and code = {'MCTA', 'MCZA'} 'BCM'?, 'MCTB'?;
# Code where 2 first letters (period 'D' or 'N', class 'A' or 'B' etc);
# and maybe one number before the code itself of subjects;
# Example: DA1MCTA0001;


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
    # Base Lists of Professors and Subjects
    prof = []
    subj = []
    
    # Max Number of iterations to get a solution
    iterations = 10
    # number of candidates in a generation (for each Feas/Inf.)
    numCand = 100
    # Percentage of candidates from Feasible Pop. that will pass through Roullete (Crossover) -> Mutation
    pctMut = 15
    pctCross = 50
    
    # Start of the works
    getData(subj, prof)
    
    # First generation
    uctp.start(solutionsNoPop, subj, prof, numCand)
    uctp.two_pop(solutionsNoPop, solutionsI, solutionsF, prof, subj)
    uctp.calc_fit(solutionsI, solutionsF, prof, subj)
    outDataMMA(solutionsI, solutionsF)
    printAllFit(solutionsI, solutionsF)
    
    # Main work - iterations to find a solution
    print(" ")
    print("Starting hard work...")
    t = 0;
    while(uctp.stop(t, iterations, solutionsI, solutionsF)):
        print 'Iteration:', t+1

        uctp.offspringI(solutionsNoPop, solutionsI, prof) 
        uctp.offspringF(solutionsNoPop, solutionsF, prof, pctMut, pctCross, numCand) 
        #uctp.resetPop(solutionsNoPop, solutionsI, solutionsF)
        uctp.two_pop(solutionsNoPop, solutionsI, solutionsF, prof, subj)
        uctp.calc_fit(solutionsI, solutionsF, prof, subj)
        uctp.selectionI(solutionsI, numCand)
        uctp.selectionF(solutionsF, numCand)
        
        outDataMMA(solutionsI, solutionsF)
        printAllFit(solutionsI, solutionsF)
        print(" ")
        t = t+1
        
    outData(solutionsI, solutionsF, t)        
    print("FIM")
    
