# UCTP Main Methods

from objects import *
from ioData import *
from random import *

class UCTP:
        
    # Create the first generation of solutions
    def start(self, solutionsNoPop, subj, prof, init):        
        print "Creating first generation...",
        n = 0
        while(n!=init):
            candidate = Candidate()
            for sub in subj:
                candidate.addRelation(sub, prof[randrange(len(prof))])
            solutionsNoPop.addCand(candidate)
            n = n+1
        print ("Created first generation!")    
        #printAllCand(solutions)
    
    # Reset Populations Separation to allow new separation
    def resetPop(self, solutionsNoPop, solutionsI, solutionsF):
        for cand in solutionsI.getList():
            solutionsNoPop.addCand(cand)
        for cand in solutionsF.getList():
            solutionsNoPop.addCand(cand)
            
        solutionsI.resetList()
        solutionsF.resetList()
            
    # Separation of solutions into 2 populations
    def twoPop(self, solutionsNoPop, solutionsI, solutionsF, prof, subj):
        for cand in solutionsNoPop.getList():
            pop = self.in_feasible(cand, prof, subj)
            if(pop=="feasible"):
                solutionsF.addCand(cand)
            elif(pop=="infeasible"):
                solutionsI.addCand(cand) 
                   
        solutionsNoPop.resetList()
        
    # Detect the violation of a Restriction into a candidate
    def in_feasible(self, candidate, prof, subj):
        # Lists used to relate with the position of Professors in 'prof' list 
        prof_total_charge = []
        prof_total_exist = []
        
        # Initializing the lists 
        n=0
        for n in range(len(prof)):
            prof_total_charge.append(0.0)
            prof_total_exist.append(0.0)
            n = n+1
            
        for s, p in candidate.getList():
            sLevel, sCode, sName, sQuadri, sPeriod, sCharge = s.get()
            pName, pPeriod, pCharge, pQuadriSabbath = p.get()
            # Period chosed by a Prof is not equal of a Subject
            #if(('NEGOCI' not in pPeriod) and (pPeriod != sPeriod)):
            #    return "infeasible"
            # ?? Subject is on a Quadri where the Prof chosed to be your Sabbath Quadri
            #elif(pQuadriSabbath == sQuadri):
            #    return "infeasible"
            
            # Searchs a Prof that dont exists on the Candidate
            index = prof.index(p)
            prof_total_exist[index] = 1
            # ?? Sera que a distribuicao balanceada de materias eh uma resticao??
            #prof_total_charge[index] = (prof_total_charge[index]+ float(sCharge.replace(",", ".")))

        # Count how many Prof doesnt has a Subject
        if(prof_total_exist.count(0)!=0):
            return "infeasible"
        
        # ??
        #n=0
        #for n in range(len(prof)):
        #    pName, pPeriod, pCharge, pQuadriSabbath = prof[n].get()
        #    if(pCharge < prof_total_charge[n]):
        #        return "infeasible"
        #    n = n+1
                        
        return "feasible"
    
    # Calculate the Fitness of the candidate
    def calcFit(self, solutionsI, solutionsF, prof, subj):
        for cand in solutionsI.getList():
            if(cand.getFitness() == 0.0):
                cand.setFitness(self.calc_fitInfeas(cand, prof, subj))
        for cand in solutionsF.getList():
            if(cand.getFitness() == 0.0):
                cand.setFitness(self.calc_fitFeas(cand, prof, subj))
    
    # Calculate Fitness of Feasible Candidates 
    def calc_fitFeas(self, cand, prof, subj):
        # quao balanceada esta a dispribuicao de materias para cada Prof (levando em consideracao a carga escolhida por cada) calcular variancia
        # quantas materias sao da preferencia do prof
        # QuadriSabath - minimizar a quantidade de materias no quadriSabath
        # materia turno por professor (a) - quantos ferem 
        # Preferencia de campus do prof
        result = 1.0
        return result
    
    # Calculate Fitness of Infeasible Candidates 
    def calc_fitInfeas(self, cand, prof, subj):
        # ha todos os prof com materias (c) - quantos faltam
        # quantas materias(no mesmo quadri) (1)ha no mesmo dia/mesmo horario, (2)mesmo dia/Campus diferentes
        result = 1.0
        return ((-1)*result)
            
    # Generate new solutions from the current Infeasible population
    def offspringI(self, solutionsNoPop, solutionsI, prof):
        if(len(solutionsI.getList())!=0):
            # Make a Mutation for each candidate, trying to repair a restriction problem maker
            for cand in solutionsI.getList():
                newCand = self.mutationI(cand, prof)
                solutionsNoPop.addCand(newCand)
    
    # Make a mutation into a solution
    def mutationI(self, candidate, prof):
        # (1) faltam prof com materias
        # (2) quantas materias(no mesmo quadri) ha no mesmo dia/mesmo horario, 
        # (3) mesmo dia/Campus diferentes
        errorType =  randrange(1,4)
        relations = candidate.getList()
        
        original = randrange(len(relations))
        s, oldProf = relations[original]
        change = randrange(len(prof))
        newProf = prof[change]
        while(oldProf==newProf):
            change = randrange(len(prof))
            newProf = prof[change]
        
        relations[original]=[s,newProf]
        newCand = Candidate()
        newCand.setList(relations)
        
        return newCand
                 
    # Generate new solutions from the current Feasible population
    def offspringF(self, solutionsNoPop, solutionsF, prof, pctMut, pctRouletteCross, numCand):
        if(len(solutionsF.getList())!=0):
            # Make a Roulette of 50% in Feasibles Pop. to become Parents
            parentsSolFeas = []
            childSolFeas = []
            newSolFeas = []
            totalFitFeas = 0.0
            probFeas = []
            cumulativeProbFeas = []
            
            # Find the total fitness of the population
            for cand in solutionsF.getList():
                totalFitFeas = totalFitFeas + cand.getFitness()
            
            # Calculate the prob. of a selection for each candidate
            for cand in solutionsF.getList():
                p = cand.getFitness()/totalFitFeas
                probFeas.append(p) 
            
            # Calculate a cumulative prob. for each candidate
            cumulative=0.0
            for q in probFeas:
                qNew = q + cumulative
                cumulativeProbFeas.append(qNew)
                cumulative = qNew
            
            # MAIN Roulette Selection process
            objectiveNum = (pctRouletteCross*len(solutionsF)/100.0)
            while(len(parentsSolFeas) < objectiveNum):    
                probPrev = 0.0
                index = 0
                r = float(randrange(100)/100.0)
                for q in cumulativeProbFeas:
                    if(probPrev < r and r <= q):
                        parentsSolFeas.append(solutionsF.getList()[index])
                        break
                    probPrev = q    
                    index = index + 1        
               
            # Make a Crossover (two new candidates) for each pair of parents candidates
            i=0
            objectiveNum = (pctRouletteCross*len(solutionsF)/100.0)
            while(childSolFeas < objectiveCrosNum):
                i1 = i
                i2 = len(parentsSolFeas)-1-i
                newCand1, newCand2 = self.crossoverF(list[r1], list[r2])  
                childSolFeas.append(newCand1)
                childSolFeas.append(newCand2)
                i = i+2
            
            #Make Mutations with Pm (mutation prob.) only childs (generated by crossover before)
            for cand in newSolFeas:
                r = float(randrange(100)/100.0)
                if(r<=(pctMut/100.0)):
                    newCand = self.mutationF(cand, prof)
                    solutionsNoPop.addCand(newCand)
                else:
                    solutionsNoPop.addCand(cand)    
                    
    # Make a mutation into a solution
    def mutationF(self, candidate, prof):
        relations = candidate.getList()
        
        original = randrange(len(relations))
        s, oldProf = relations[original]
        change = randrange(len(prof))
        newProf = prof[change]
        while(oldProf==newProf):
            change = randrange(len(prof))
            newProf = prof[change]
        
        relations[original]=[s,newProf]
        newCand = Candidate()
        newCand.setList(relations)
        
        return newCand
    
    # Make a crossover between two solutions    
    def crossoverF(self, cand1, cand2):
        relations1 = cand1.getList()
        relations2 = cand2.getList()
        
        originalRand1 = randrange(len(relations1))
        originalRand2 = randrange(len(relations2))
        rel1 = relations1[originalRand1]
        rel2 = relations2[originalRand2]
        
        s1, p1 = rel1
        s2, p2 = rel2
        
        while(originalRand1==originalRand2 and p1==p2):
            originalRand2 = randrange(len(relations2))
            rel2 = relations2[originalRand2]
            s2, p2 = rel2
            
        relations1[originalRand1] = rel2
        relations2[originalRand2] = rel1
        
        newCand1 = Candidate()
        newCand2 = Candidate()
        newCand1.setList(relations1)
        newCand2.setList(relations2)
        
        return newCand1, newCand2 
        
    # Make a Roulette Wheel selection of the solutions from Infeasible Pop.
    def selectionI(self, solutionsI, numCand):
        if(len(solutionsI.getList())>numCand):
            newSolInf = []
            totalFitInf = 0.0
            probInf = []
            cumulativeProbInf = []
            
            # Find the total fitness of the population
            for cand in solutionsI.getList():
                totalFitInf = totalFitInf + cand.getFitness()
            
            # Calculate the prob. of a selection for each candidate
            for cand in solutionsI.getList():
                p = cand.getFitness()/totalFitInf
                probInf.append(p) 
            
            # Calculate a cumulative prob. for each candidate
            cumulative=0.0
            for q in probInf:
                qNew = q + cumulative
                cumulativeProbInf.append(qNew)
                cumulative = qNew
            
            # MAIN Roulette Selection process
            while(len(newSolInf) < numCand):    
                probPrev = 0.0
                index = 0
                r = float(randrange(100)/100.0)
                for q in cumulativeProbInf:
                    if(probPrev < r and r <= q):
                        newSolInf.append(solutionsI.getList()[index])
                        break
                    probPrev = q    
                    index = index + 1
            
            solutionsI.setList(newSolInf)            
    
    # Make a Selection of the best solutions from Feasible Pop.
    def selectionF(self, solutionsF, numCand):
        if(len(solutionsF.getList())>numCand):
            bestFeas = []
            listFit = []
            for cand in solutionsF.getList():
                listFit.append(cand.getFitness())
            
            while(listFit.count(-10.0)<(len(solutionsF)-numCand)):
                minValue = min(listFit)
                minIndex = listFit.index(minValue)
                listFit[minIndex] = -10.0
            
            for i in range(numCand):
                if(listFit[i]!=-10.0):
                    bestFeas.append(solutionsF.getList()[i])
                    
            solutionsF.setList(bestFeas)        
                
    # Detect the stop condition
    def stop(self, iteration, total, solutionsI, solutionsF):
        for cand in solutionsF.getList():
            if cand.getFitness() >= 0.999:
                return False
        if(iteration == total):
            return False
        else:
            return True
    