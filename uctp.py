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
    def two_pop(self, solutionsNoPop, solutionsI, solutionsF, prof, subj):
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
            if(('NEGOCI' not in pPeriod) and (pPeriod != sPeriod)):
                return "infeasible"
            # ?? Subject is on a Quadri where the Prof chosed to be your Sabbath Quadri
            elif(pQuadriSabbath == sQuadri):
                return "infeasible"
            
            # Searchs a Prof that dont exists on the Candidate
            index = prof.index(p)
            prof_total_exist[index] = 1
            # ?? Sera que a distribuicao balanceada de materias eh uma resticao??
            prof_total_charge[index] = (prof_total_charge[index]+ float(sCharge.replace(",", ".")))

        # Count how many Prof doesnt has a Subject
        if(prof_total_exist.count(0)!=0):
            return "infeasible"
        
        # ??
        n=0
        for n in range(len(prof)):
            pName, pPeriod, pCharge, pQuadriSabbath = prof[n].get()
            if(pCharge < prof_total_charge[n]):
                return "infeasible"
            n = n+1
                        
        return "feasible"
    
    # Calculate the Fitness of the candidate
    def calc_fit(self, solutionsI, solutionsF, prof, subj):
        for cand in solutionsI.getList():
            cand.setFitness(self.calc_fitInfeas(cand, prof, subj))
        for cand in solutionsF.getList():
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
            
    # Generate new solutions from the actual Infeasible population
    def offspringI(solutionsNoPop, solutionsI, prof):
        i=0
        currentMutNum = 0
        objectiveMutNum = (pctMut*numCand/100)
        while(currentMutNum < objectiveMutNum):
            list = solutionsF.getList()
            if(len(list)!=0):
                newCand = self.mutation(list[randrange(len(list))], prof)
                solutionsNoPop.addCand(newCand)
                currentMutNum = currentMutNum + 1
                
            list = solutionsI.getList()
            if(len(list)!=0):
                newCand = self.mutation(list[randrange(len(list))], prof)
                solutionsNoPop.addCand(newCand)
                currentMutNum = currentMutNum + 1
            
        i=0
        currentCrosNum = 0
        objectiveCrosNum = (pctCross*numCand/100)
        while(currentCrosNum < objectiveCrosNum):
            list = solutionsF.getList()
            if(len(list)!=0):
                newCand1, newCand2 = self.crossover(list[randrange(len(list))], list[randrange(len(list))])  
                solutionsNoPop.addCand(newCand1)
                solutionsNoPop.addCand(newCand2)
                currentCrosNum = currentCrosNum + 2
            
            list = solutionsI.getList()
            if(len(list)!=0):
                newCand1, newCand2 = self.crossover(list[randrange(len(list))], list[randrange(len(list))])  
                solutionsNoPop.addCand(newCand1)
                solutionsNoPop.addCand(newCand2)
                currentCrosNum = currentCrosNum + 2
                 
    # Generate new solutions from the actual Feasible population
    def offspringF(self, solutionsNoPop, solutionsF, prof, pctMut, pctCross, numCand):
        
        i=0
        currentMutNum = 0
        objectiveMutNum = (pctMut*numCand/100)
        while(currentMutNum < objectiveMutNum):
            list = solutionsF.getList()
            if(len(list)!=0):
                newCand = self.mutation(list[randrange(len(list))], prof)
                solutionsNoPop.addCand(newCand)
                currentMutNum = currentMutNum + 1
                
            list = solutionsI.getList()
            if(len(list)!=0):
                newCand = self.mutation(list[randrange(len(list))], prof)
                solutionsNoPop.addCand(newCand)
                currentMutNum = currentMutNum + 1
            
        i=0
        currentCrosNum = 0
        objectiveCrosNum = (pctCross*numCand/100)
        while(currentCrosNum < objectiveCrosNum):
            list = solutionsF.getList()
            if(len(list)!=0):
                newCand1, newCand2 = self.crossover(list[randrange(len(list))], list[randrange(len(list))])  
                solutionsNoPop.addCand(newCand1)
                solutionsNoPop.addCand(newCand2)
                currentCrosNum = currentCrosNum + 2
            
            list = solutionsI.getList()
            if(len(list)!=0):
                newCand1, newCand2 = self.crossover(list[randrange(len(list))], list[randrange(len(list))])  
                solutionsNoPop.addCand(newCand1)
                solutionsNoPop.addCand(newCand2)
                currentCrosNum = currentCrosNum + 2
                
    # Make a mutation into a solution
    def mutation(self, candidate, prof):
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
    def crossover(self, cand1, cand2):
        relations1 = cand1.getList()
        relations2 = cand2.getList()
        
        originalRand1 = randrange(len(relations1))
        originalRand2 = randrange(len(relations2))
        rel1 = relations1[originalRand1]
        rel2 = relations2[originalRand2]
        
        relations1[originalRand1] = rel2
        relations2[originalRand2] = rel1
        
        newCand1 = Candidate()
        newCand2 = Candidate()
        newCand1.setList(relations1)
        newCand2.setList(relations2)
        
        return newCand1, newCand2 
        
    # Make a Roulette Wheel selection of the solutions from Infeasible Pop.
    def selectionI(self, solutionsI, numCand):
        newSolInf = []
        newSolFea = []
        totalFitInf = 0.0
        totalFitFea = 0.0
        probInf = []
        profFea = []
        
        # Elitismo - escolher quantidade predefinida de feasibles e/ou os maiores fitness pra cada valor fixo tipo = 3 e não é excluido da roleta
        
        # Find the total fitness of the population
        for cand in solutionsI.getList():
            totalFitInf = totalFitInf + cand.getFitness()
        for cand in solutionsF.getList():
            totalFitFea = totalFitFea + cand.getFitness()
        
        # Calculate the prob. of a selection for each candidate
        for cand in solutionsI.getList():
            p = cand.getFitness()/totalFitInf
            probInf.append(p) 
        for cand in solutionsF.getList():
            p = cand.getFitness()/totalFitFea
            profFea.append(p)
        
        # Calculate a cumulative prob. for each candidate
        comulative=0.0
        index = 0
        for q in probInf:
            qNew = q + comulative
            probInf[index] = qNew
            index = index+1
            comulative = qNew
        
        comulative=0.0
        index = 0     
        for q in profFea:
            qNew = q + comulative
            profFea[index] = qNew
            index = index + 1
            comulative = qNew
        
        # MAIN Selection process
        currentSelNum = len(newSolInf)+len(newSolFea)
        objectiveSelNum = (pctSelect*numCand/100)
        while(currentSelNum < objectiveSelNum):    
            probPrev = 0.0
            index = 0
            for q in probInf:
                r = float(randrange(100)/100.0)
                if(probPrev < r and r <= q):
                    newSolInf.append(solutionsI.getList()[index])
                probPrev = q    
                index = index + 1
            
            probPrev = 0.0
            index = 0
            for q in profFea:
                r = float(randrange(100)/100.0)
                if(probPrev < r and r <= q):
                    newSolFea.append(solutionsF.getList()[index])
                probPrev = q    
                index = index + 1
            
            currentSelNum = len(newSolInf)+len(newSolFea)        

        solutionsI.setList(newSolInf)
        solutionsF.setList(newSolFea)
    
    # Make a Selection of the best solutions from Feasible Pop.
    def selectionF(self, solutionsF, numCand):
        newSolFea = []
        totalFitFea = 0.0
        profFea = []
        
        # Find the total fitness of the population
        for cand in solutionsF.getList():
            totalFitFea = totalFitFea + cand.getFitness()
        
        # Calculate the prob. of a selection for each candidate
        for cand in solutionsI.getList():
            p = cand.getFitness()/totalFitInf
            probInf.append(p) 
        for cand in solutionsF.getList():
            p = cand.getFitness()/totalFitFea
            profFea.append(p)
        
        # Calculate a cumulative prob. for each candidate
        comulative=0.0
        index = 0
        for q in probInf:
            qNew = q + comulative
            probInf[index] = qNew
            index = index+1
            comulative = qNew
        
        comulative=0.0
        index = 0     
        for q in profFea:
            qNew = q + comulative
            profFea[index] = qNew
            index = index + 1
            comulative = qNew
        
        # MAIN Selection process
        currentSelNum = len(newSolInf)+len(newSolFea)
        objectiveSelNum = (pctSelect*numCand/100)
        while(currentSelNum < objectiveSelNum):    
            probPrev = 0.0
            index = 0
            for q in probInf:
                r = float(randrange(100)/100.0)
                if(probPrev < r and r <= q):
                    newSolInf.append(solutionsI.getList()[index])
                probPrev = q    
                index = index + 1
            
            probPrev = 0.0
            index = 0
            for q in profFea:
                r = float(randrange(100)/100.0)
                if(probPrev < r and r <= q):
                    newSolFea.append(solutionsF.getList()[index])
                probPrev = q    
                index = index + 1
            
            currentSelNum = len(newSolInf)+len(newSolFea)        

        solutionsI.setList(newSolInf)
        solutionsF.setList(newSolFea)
                
    # Detect the stop condition
    def stop(self, iteration, total, solutionsI, solutionsF):
        for cand in solutionsF.getList():
            if cand.getFitness() >= 0.999:
                return False
        if(iteration == total):
            return False
        else:
            return True
    