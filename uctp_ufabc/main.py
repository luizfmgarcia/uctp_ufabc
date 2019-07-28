# Main Class - Algorithm

import objects
import uctp
import ioData
import cProfile

"""
- Sempre procurar por:
    -Verificar se há variaveis/List importantes sendo modificadas quando n deveriam !
    -Erros nos comments - verificar com notepad++ ! melhorar comments
    -Nomes de variaveis ruins !
    -Rever uso de float()
    -Corrigir [1 for s in a if sName in s] ver se existe string em list of strings
    -   prof_data = [prof[i].get() for i in range(len(prof))]
        charges_EachProf = [int(pCharge) for _, _, pCharge, _, _, _, _, _, _ in prof_data]
    -uso de _, remover espa;os em branco....
    -rever roulettes (quais com reposicao ou nao, negative)

-melhorar:
    - f2 - rever a forma de obtencao das variaveis,
    - mutationI - refatorar e modificar(?)
    - gerar automaticamente os graficos que serão utilizados no trab

- Problemas e adiçoes:
    -SelectionF com uma parte elitista e outra com roleta? offspringF (100% mutation para quem nao é Parent)?
    -Reformular f2 para apenas contagem de materias de preferencia(sem levar em conta posicao no vetor)?
        -Ou adicionar mais um f6 com essa contagem....

    -havendo acumulo de disciplinas em poucos prof
    -rever mutationI erros 1,2,3 - escolher troca de disciplinas com aqueles prof com mais disciplinas, e/ou tirar materia de um
    que nao tem pref e dar pra qm tem pref
"""

#==============================================================================================================
# Run with <python -m cProfile -s cumtime main.py> to see the main time spent of the algorithm
# Debug <import pdb; pdb.set_trace()>

# main
class main:
    # Record Run Info Start
    pr = cProfile.Profile()
    pr.enable()

    #----------------------------------------------------------------------------------------------------------
    # CONFIGURATION

    # RUN CONFIG
    # Set '1' to allow, during the run, the print on terminal of some steps
    prt = 1
    # Max Number of iterations to get a solution
    maxIter = 7000
    # Number of candidates in a generation (same for each Pop Feas/Inf.)
    numCand = 130
    # Initial number of solutions generated randomly
    numCandInit = 100
    # Number of new solutions (created generated randomly) every round
    randNewSol = 10
    # Convergence Detector: num of iterations passed since last MaxFit found
    convergDetect = 0 # equal '0' to not consider this condition
    # Max Fitness value that must find to stop the run before reach 'maxIter'
    stopFitValue = 0.9 # equal '0' to not consider this condition
 
    # OPERATORS CONFIG (Must be between '0' and '100')
    # Percentage of candidates from Feasible Pop. that will be selected, to become Parents and make Crossovers, through a Roulette Wheel with Reposition
    pctParentsCross = 0 # The rest (to complete 100%) will pass through Mutation
    # Percentage of mutation that maybe each child generated through 'Crossover' process will suffer 
    pctMut = 30
    # Percentage of selection by elitism of feasible candidates, the rest of them will pass through a Roulette Wheel
    pctElitism = 100

    # WEIGHTS CONFIG (must be Float)
    w_alpha = 1.0   # i1 - Prof without Subj
    w_beta = 3.0    # i2 - Subjs (same Prof), same quadri and timetable conflicts
    w_gamma = 2.0   # i3 - Subjs (same Prof), same quadri and day but in different campus
    w_delta = 10.0   # f1 - Balance of distribution of Subjs between Profs
    w_omega = 7.7   # f2 - Profs preference Subjects
    w_sigma = 1.5   # f3 - Profs with Subjs in quadriSabbath
    w_pi = 1.0      # f4 - Profs with Subjs in Period
    w_rho = 1.3     # f5 - Profs with Subjs in Campus

    numInfWeights = 3 # Number of infeasible waights to divide properly 'weights' vector into some functions
    weights = [w_alpha, w_beta, w_gamma, w_delta, w_omega, w_sigma, w_pi, w_rho]

    # Gathering all variables
    config = [maxIter, numCand, numCandInit, randNewSol, convergDetect, stopFitValue, pctParentsCross, 
              pctMut, pctElitism] + weights
    
    #----------------------------------------------------------------------------------------------------------
    # MAIN VARIABLES

    # to access UCTP Main methods and creating Solutions (List of Candidates)
    uctp = uctp.UCTP()
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
    uctp.calcFit(solutionsI, solutionsF, prof, subj, weights, numInfWeights)

    # Print and export generated data
    if(prt == 1): ioData.printHead(prof, subj, curIter, maxIter, firstFeasSol, lastMaxIter)
    maxFeaIndex, _, _, _, _, maxFea, _ = ioData.outDataMMA(solutionsI, solutionsF, curIter)
    if(len(maxFeaIndex) != 0): lastMax = maxFea
    # Next iteration
    curIter = curIter + 1
    
    #----------------------------------------------------------------------------------------------------------
    # MAIN WORK - iterations of GA-Algorithm to find a solution
    
    # Verify the stop conditions occurence
    while(uctp.stop(curIter, maxIter, lastMaxIter, convergDetect, maxFea, stopFitValue)):
        # First print of each run
        if(prt == 1): ioData.printHead(prof, subj, curIter, maxIter, firstFeasSol, lastMaxIter)
        
        # Creating new Random Solutions
        for _ in range(randNewSol): solutionsNoPop.addCand(uctp.newCandRand(subj, prof))
        
        # Choosing Parents to generate children (put all new into 'solutionsNoPop')
        uctp.offspringI(solutionsNoPop, solutionsI, prof, subj)
        uctp.offspringF(solutionsNoPop, solutionsF, prof, subj, pctMut, pctParentsCross, numCand)
        
        # Classification and Fitness calculation of all new candidates
        uctp.twoPop(solutionsNoPop, infPool, feaPool, prof, subj, weights, numInfWeights)
        uctp.calcFit(infPool, feaPool, prof, subj, weights, numInfWeights)
        
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
    #ioData.outDataGeneration(solutionsI, solutionsF, curIter, prof, subj)
    fitMaxData, resumeMaxData, maxInfo = ioData.finalOutData(solutionsI, solutionsF, curIter, prof, subj, maxFeaIndex, config)
    if(prt == 1): ioData.printFinalResults(config, maxFeaIndex, fitMaxData, resumeMaxData, maxInfo)
    # Record Run Info End
    ioData.outRunData(pr)
    if(prt == 1): print("End of works")

#==============================================================================================================    