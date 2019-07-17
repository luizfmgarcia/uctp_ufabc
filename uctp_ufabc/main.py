# Main Class - Algorithm

from objects import *
from uctp import *
from ioData import *

"""
-Reformulado Crossover para não gerar 2 filhos iguais aos pais (que na maioria das vezes sao iguais)

-Melhorar saida apresentando tmb a config do algoritmo
-Reformular funcao de Roulette Wheel padrao: opcao de escolher os piores valores?
-Criar funcoes mutation, crossover mais gerais para reutilizacao de codigo?
-Criar X funcoes novas totalmente aleatorias toda rodada? 
-Reformular SelectionF para ter uma parte elitista e outra com roleta? Exp. de codigo:
----------------------------------------------------------------------
    maxFeasible = [feasibles_List[listFit.index(max(listFit))]]
    listFit.pop(listFit.index(max(listFit)))
    feasibles_List.pop(listFit.index(max(listFit)))

    # Roulette Wheel
    newSolFea = self.rouletteWheel(feasibles_List, listFit, numCand-1, repos=True, negative=False)  
    
    # Setting the new 'solutionsF' list to go to the next generation        
    solutionsF.setList(maxFeasible + newSolFea)
----------------------------------------------------------------------

-havendo acumulo de disciplinas em poucos prof
-muitas materias n sao de pref
    -rever mutationI erros 1,2,3 - escolher troca de disciplinas com aqueles prof com mais disciplinas, e/ou tirar materia de um
        que nao tem pref e dar pra qm tem pref
"""

#==============================================================================================================            
# Run with <python -m cProfile -s cumtime main.py> to see the main time spent of the algorithm
# Debug <import pdb; pdb.set_trace()>

# main
class main:     
    #----------------------------------------------------------------------------------------------------------
    # CONFIGURATION

    # Set '1' to allow, during the run, the output of some steps
    prt = 1

    # Max Number of iterations to get a solution
    iterations = 1000
    # Number of candidates in a generation (same for each Feas/Inf.)
    numCand = 300

    # Percentage of candidates from Feasible Pop. that will be selected, to become Parents and make Crossovers, through a Roulette Wheel with Reposition
    pctRouletteCross = 45 # Must be between '0' and '100'
    # Percentage of mutation that maybe each child generated through 'offspringF' process will suffer 
    pctMut = 80 # Must be between '0' and '100'

    # Weights (must be float)
    w_alpha = 2.0   # Prof without Subj
    w_beta = 3.0   # Subjs (same Prof), same quadri and timetable conflicts
    w_gamma = 1.0   # Subjs (same Prof), same quadri and day but in different campus
    w_delta = 20.0   # Balance of distribution of Subjs between Profs
    w_omega = 30.0   # Profs preference Subjects
    w_sigma = 1.0   # Profs with Subjs in quadriSabbath
    w_pi = 1.0      # Profs with Subjs in Period
    w_rho = 1.0     # Profs with Subjs in Campus
    weights = [w_alpha, w_beta, w_gamma, w_delta, w_omega, w_sigma, w_pi, w_rho]
    
    #----------------------------------------------------------------------------------------------------------
    # CREATION OF MAIN VARIABLES
    
    # to access UCTP Main methods and creating Solutions (List of Candidates)
    uctp = UCTP()
    # Main candidates of a generation
    solutionsI, solutionsF = Solutions(), Solutions()
    # Candidates without classification 
    solutionsNoPop = Solutions()
    # Candidates generated in a iteration (will be selected to be, or not, in the main List of Candidates)
    infPool, feaPool = Solutions(), Solutions()
    # Base Lists of Professors and Subjects - never modified through the run
    prof, subj = [], []

    #----------------------------------------------------------------------------------------------------------
    # START OF THE WORK
    
    # Getting data to work with
    getData(subj, prof)

    # Creating the first 'numCand' candidates (First Generation)
    uctp.start(solutionsNoPop, subj, prof, numCand)

    # Classification and Fitness calc of the first candidates
    uctp.twoPop(solutionsNoPop, solutionsI, solutionsF, prof, subj, weights)
    uctp.calcFit(solutionsI, solutionsF, prof, subj, weights)

    # Print and export generated data
    if(prt == 1): print('Iteration: 0')
    maxFeaIndex = outDataMMA(solutionsI, solutionsF, 0)

    #----------------------------------------------------------------------------------------------------------
    # MAIN WORK - iterations of GA-Algorithm to find a solution
    
    if(prt == 1): print("\nStarting hard work...\n")
    
    # Flag to mark when appears the first Feasible Solution during a run
    firstFeasSol = -1
    
    t = 1
    while(uctp.stop(t, iterations, solutionsI, solutionsF)):
        # Some good information to follow during the run
        if(prt == 1): 
            print('Iteration:', t, 'of', iterations, '/ Working with (Prof/Subj):', len(prof), '/', len(subj))
            if(firstFeasSol != -1): print('First Feasible Sol. at (iteration): ', firstFeasSol)
        
        # Choosing Parents to generate children (put all new into 'solutionsNoPop') 
        uctp.offspringI(solutionsNoPop, solutionsI, prof, subj) 
        uctp.offspringF(solutionsNoPop, solutionsF, prof, subj, pctMut, pctRouletteCross, numCand)
        
        # Classification and Fitness calculation of all new candidates  
        uctp.twoPop(solutionsNoPop, infPool, feaPool, prof, subj, weights)
        uctp.calcFit(infPool, feaPool, prof, subj, weights)
        
        # Selecting between parents (old generation) and children (new candidates) to create the next generation
        uctp.selectionI(infPool, solutionsI, numCand)
        uctp.selectionF(feaPool, solutionsF, numCand)
        
        # Print and export generated data
        maxFeaIndex = outDataMMA(solutionsI, solutionsF, t)
        
        # Register of the 'Iteration' that appeared the first Feas Sol
        if(firstFeasSol == -1 and len(solutionsF.getList()) != 0): firstFeasSol = t

        # Next Iteration
        t = t + 1
        if(prt == 1): print("\n")
    # End of While (Iterations) - Stop condition verified
    
    #----------------------------------------------------------------------------------------------------------
    # Final - last processing of the data

    # Export last generation of candidates  
    outData(solutionsI, solutionsF, t, maxFeaIndex)      
    if(prt == 1): print("End of works") 
          
#==============================================================================================================
