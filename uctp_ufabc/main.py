# Main Class - Algorithm

import objects
import uctp
import ioData

"""
-Verificar se há variaveis/List importantes sendo modificadas quando n deveriam !
-Erros nos comments - verificar com notepad++ !
-Nomes de variaveis ruins !
-Corrigir [1 for s in a if sName in s] ver se existe string em list of strings
-uso de _, remover espa;os em branco....

-PErmitir maior variacao de individuos feasible?
    -Reformular SelectionF para ter uma parte elitista e outra com roleta?
-Reformular f2 para apenas contagem de meterias de preferencia(sem levar em conta posicao no vetor)?
-Ou adicionar mais um f6 com essa contagem....

-havendo acumulo de disciplinas em poucos prof
-muitas materias n sao de pref
    -Criar X funcoes novas totalmente aleatorias toda rodada?
    -rever mutationI erros 1,2,3 - escolher troca de disciplinas com aqueles prof com mais disciplinas, e/ou tirar materia de um
        que nao tem pref e dar pra qm tem pref

-Contador de iteracoes que finaliza o algoritmo qundo nao acha solucao melhor dps de um tempo?
-Ou a possibilidade de uma tecla para finalizar o algoritmo e ainda assim apresentar um resultado?
"""

#==============================================================================================================
# Run with <python -m cProfile -s cumtime main.py> to see the main time spent of the algorithm
# Debug <import pdb; pdb.set_trace()>

# main
class main:
    #----------------------------------------------------------------------------------------------------------
    # CONFIGURATION

    # Set '1' to allow, during the run, the print on terminal of some steps
    prt = 1

    # Max Number of iterations to get a solution
    maxIter = 2000
    # Number of candidates in a generation (same for each Feas/Inf.)
    numCand = 30

    # Percentage of candidates from Feasible Pop. that will be selected, to become Parents and make Crossovers, through a Roulette Wheel with Reposition
    pctParentsCross = 75 # Must be between '0' and '100'
    # Percentage of mutation that maybe each child generated through 'offspringF' process will suffer 
    pctMut = 80 # Must be between '0' and '100'
    # pctElitism
    pctElitism = 100

    # Weights (must be float)
    w_alpha = 1.0   # i1 - Prof without Subj
    w_beta = 3.0    # i2 - Subjs (same Prof), same quadri and timetable conflicts
    w_gamma = 2.0   # i3 - Subjs (same Prof), same quadri and day but in different campus
    w_delta = 1.0   # f1 - Balance of distribution of Subjs between Profs
    w_omega = 1.0   # f2 - Profs preference Subjects
    w_sigma = 1.0   # f3 - Profs with Subjs in quadriSabbath
    w_pi = 1.0      # f4 - Profs with Subjs in Period
    w_rho = 1.0     # f5 - Profs with Subjs in Campus
    weights = [w_alpha, w_beta, w_gamma, w_delta, w_omega, w_sigma, w_pi, w_rho]
    
    #----------------------------------------------------------------------------------------------------------
    # CREATION OF MAIN VARIABLES

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

    #----------------------------------------------------------------------------------------------------------
    # START OF THE WORK
    
    # Getting data to work with
    ioData.getData(subj, prof)
    ioData.startOutFolders()

    # Creating the first 'numCand' candidates (First Generation)
    uctp.start(solutionsNoPop, subj, prof, numCand)
    
    # Extracting basic info about Prof's Subj Pref
    subjIsPref = uctp.extractSubjIsPref(subj, prof)
    if(prt == 1):
        for pIndex in range(len(prof)):
                # Getting data of current Prof
                pName, _, _, _, _, _, _, _, _ = prof[pIndex].get()
                # All Relations of one Prof
                for sIndex in range(len(subj)):
                    # Getting data of current Subj
                    _, _, sName, sQuadri, _, _, _, _ = subj[sIndex].get()
                    if(subjIsPref[pIndex][sIndex]!=0): print(pName, sName, subjIsPref[pIndex][sIndex])
        print("")

    # Classification and Fitness calc of the first candidates
    uctp.twoPop(solutionsNoPop, solutionsI, solutionsF, prof, subj, weights)
    uctp.calcFit(solutionsI, solutionsF, prof, subj, weights)

    # Print and export generated data
    if(prt == 1): print('Iteration: 0')
    maxFeaIndex, _, _, _, _, _, _ = ioData.outDataMMA(solutionsI, solutionsF, 0)

    #----------------------------------------------------------------------------------------------------------
    # MAIN WORK - iterations of GA-Algorithm to find a solution
    
    if(prt == 1): print("\nStarting hard work...\n")
    
    # Flag to mark when appears the first Feasible Solution during a run
    firstFeasSol = -1
    
    curIter = 1
    while(uctp.stop(curIter, maxIter, solutionsI, solutionsF)):
        # Important Info to output and follow on terminal during the run
        if(prt == 1):
            print('Iteration:', curIter, 'of', maxIter, '/ Working with (Prof/Subj):', len(prof), '/', len(subj))
            if(firstFeasSol != -1): print('First Feasible Sol. at (iteration): ', firstFeasSol)

        for _ in range(int(numCand*30/100)): solutionsNoPop.addCand(uctp.newCandRand(subj, prof))
        
        # Choosing Parents to generate children (put all new into 'solutionsNoPop')
        uctp.offspringI(solutionsNoPop, solutionsI, prof, subj)
        uctp.offspringF(solutionsNoPop, solutionsF, prof, subj, pctMut, pctParentsCross, numCand)
        
        # Classification and Fitness calculation of all new candidates
        uctp.twoPop(solutionsNoPop, infPool, feaPool, prof, subj, weights)
        uctp.calcFit(infPool, feaPool, prof, subj, weights)
        
        # Selecting between parents (old generation) and children (new candidates) to create the next generation
        uctp.selectionI(infPool, solutionsI, numCand)
        uctp.selectionF(feaPool, solutionsF, numCand, pctElitism)
        
        # Print and export generated data
        maxFeaIndex, minInf, maxInf, avgInf, minFea, maxFea, avgFea = ioData.outDataMMA(solutionsI, solutionsF, curIter)
        
        # Register of the 'Iteration' that appeared the first Feas Sol
        if(firstFeasSol == -1 and len(solutionsF.getList()) != 0): firstFeasSol = curIter
        
        # Next Iteration
        curIter = curIter + 1

        # Important Info to output and follow on terminal during the run
        if(prt == 1):
            if(minInf != 0): print('Infeasibles (', len(solutionsI.getList()), ') Min:', minInf, 'Max:', maxInf, 'Avg:', avgInf)
            else: print('No Infeasibles Solutions!')
            if(minFea != 1): print('Feasibles (', len(solutionsF.getList()), ') Min:', minFea, 'Max:', maxFea, 'Avg:', avgFea)
            else: print('No Feasibles Solutions!')
            print("")
    # End of While (Iterations) - Stop condition verified
    
    #----------------------------------------------------------------------------------------------------------
    
    # Final - last processing of the data
    # Export last generation of candidates and Config-Run Info
    config = [maxIter, numCand, pctParentsCross, pctMut, w_alpha, w_beta, w_gamma, w_delta, w_omega, w_sigma, w_pi, w_rho]
    #ioData.outDataGeneration(solutionsI, solutionsF, curIter, prof, subj)
    ioData.finalOutData(solutionsI, solutionsF, curIter, prof, subj, maxFeaIndex, config)
    if(prt == 1): print("End of works")
    
#==============================================================================================================