# UCTP Main Methods

from objects import *
from ioData import *
from random import *
from unicodedata import numeric
from _ast import Num

class UCTP:
        
    # Create the first generation of solutions
    def start(self, solutionsNoPop, subj, prof, init):        
        print "Creating first generation...",
        n = 0
        while(n!=init):
            candidate = Candidate()
            for sub in subj:
                candidate.add(sub, prof[randrange(len(prof))])
            solutionsNoPop.add(candidate)
            n = n+1
        print ("Created first generation!")    
        #printAllCand(solutions)
    
    # Reset Populations Separation to allow new separation
    def resetPop(self, solutionsNoPop, solutionsI, solutionsF):
        for cand in solutionsI.get():
            solutionsNoPop.add(cand)
        for cand in solutionsF.get():
            solutionsNoPop.add(cand)
            
        solutionsI.reset()
        solutionsF.reset()
            
    # Separation of solutions into 2 populations
    def two_pop(self, solutionsNoPop, solutionsI, solutionsF, prof):
        for cand in solutionsNoPop.get():
            pop = self.in_feasible(cand, prof)
            if(pop=="feasible"):
                solutionsF.add(cand)
            elif(pop=="infeasible"):
                solutionsI.add(cand) 
                   
        solutionsNoPop.reset()
        
    # Detect the violation of a Restriction into a candidate
    def in_feasible(self, candidate, prof):
        # Lists used to relate with the position of Professors in 'prof' list 
        prof_total_charge = []
        prof_total_exist = []
        
        # Initializing the lists 
        n=0
        for n in range(len(prof)):
            prof_total_charge.append(0)
            prof_total_exist.append(0)
            n = n+1
            
        for s, p in candidate.get():
            sLevel, sCode, sName, sQuadri, sPeriod, sCharge = s.get()
            pName, pPeriod, pCharge, pQuadriSabbath = p.get()
            # Period chosed by a Prof is not equal of a Subject
            if(('NEGOCI' not in pPeriod) and (pPeriod != sPeriod)):
                return "infeasible"
            # Subject is on a Quadri where the Prof chosed to be your Sabbath Quadri
            elif(pQuadriSabbath == sQuadri):
                return "infeasible"
            
            # Searchs a Prof that dont exists on the Candidate
            index = prof.index(p)
            prof_total_exist[index] = 1
            # Sera que a distribuicao balanceada de materias eh uma resticao?? 
            prof_total_charge[index] = (prof_total_charge[index]+ int(sCharge))
        
        # Count how many Prof doesnt has a Subject
        if(prof_total_exist.count(0)!=0):
            return "infeasible"
        
        n=0
        for n in range(len(prof)):
            pName, pPeriod, pCharge, pQuadriSabbath = prof[n].get()
            if(pCharge < prof_total_charge[n]):
                return "infeasible"
            n = n+1
                        
        return "feasible"
    
    # Calculate the Fitness of the candidate
    def calc_fit(self, solutionsI, solutionsF):
        for cand in solutionsI.get():
            cand.setFitness(self.calc_fitInfeas(cand))
        for cand in solutionsF.get():
            cand.setFitness(self.calc_fitFeas(cand))
    
    # quao balanceada esta a dispribuicao de materias para cada Prof (levando em consideracao a carga escolhida por cada)
    # quantas materias sao da preferencia do prof
    # Tirar o quadriSabath como uma restricao?? e usar aqui? - minimizar a quantidade de materias no quadriSabath
    def calc_fitFeas(self, cand):
        result = 1
        return result
    
    # materia turno por professor (a) - quantos ferem 
    # ??quadrimestre sabatico por prof (b) - quantos possuem materias no periodo sabatico
    # ha todos os prof com materias (c) - quantos faltam
    # quantas materias(no mesmo quadri) (1)ha no mesmo dia/mesmo horario, (2)mesmo dia/horario diferente/mesmo periodo/Campus diferentes 
    def calc_fitInfeas(self, cand):
        result = 1
        return ((-1)*result)
        
    
    # Make a Roulette Wheel selection of the solutions
    def selection(self, solutionsI, solutionsF, pctSelect, numCand):
        newSolInf = []
        newSolFea = []
        totalFitInf = 0
        totalFitFea = 0
        probInf = []
        profFea = []
        
        # Find the total fitness of the population
        for cand in solutionsI.get():
            totalFitInf = totalFitInf + cand.getFitness()
        for cand in solutionsF.get():
            totalFitFea = totalFitFea + cand.getFitness()
        
        # Calculate the prob. of a selection for each candidate
        for cand in solutionsI.get():
            p = cand.getFitness()/totalFitInf
            probInf.append(p) 
        for cand in solutionsF.get():
            p = cand.getFitness()/totalFitFea
            profFea.append(p)
        
        # Calculate a cumulative prob. for each candidate
        comulative=0
        index = 0
        for q in probInf:
            qNew = q + comulative
            probInf[index] = qNew
            index = index+1
            comulative = qNew
        
        comulative=0
        index = 0     
        for q in profFea:
            qNew = q + comulative
            profFea[index] = qNew
            index = index + 1
            comulative = qNew
        
        # MAIN Selection process
        currentSelNum = len(newSolInf)+len(newSolFea)
        objectiveSelNum = (pctSelect/100)*numCand
        while(currentSelNum < objectiveSelNum):    
            probPrev = 0
            index = 0
            for q in probInf:
                r = uniform(1)
                if(probPrev < r and r <= q):
                    newSolInf.append(solutionsI.get()[index])
                probPrev = q    
                index = index + 1
            
            probPrev = 0
            index = 0
            for q in profFea:
                r = uniform(1)
                if(probPrev < r and r <= q):
                    newSolFea.append(solutionsF.get()[index])
                probPrev = q    
                index = index + 1    
        
        solutionsI.reset()
        solutionsI.set(newSolInf)
        solutionsF.reset()
        solutionsF.set(newSolFea)
            
    # Generate new solutions from the actual population
    def offspring(self, solutionsI, solutionsF, prof, nMut, nCross):
        newCandInf = []
        newCandFea = []
        
        i=0
        for i in range(nMut):
            list = solutionsI.get()
            if(len(list)!=0):
                newCand = self.mutation(list[randrange(len(list))], prof)
                newSolI.add(newCand)
            
            list = solutionsF.get()
            if(len(list)!=0):
                newCand = self.mutation(list[randrange(len(list))], prof)
                newSolF.add(newCand)
            
        i=0
        for i in range(nCross):
            list = solutionsI.get()
            if(len(list)!=0):
                newCand1, newCand2 = self.crossover(list[randrange(len(list))], list[randrange(len(list))])  
                newSolI.add(newCand1)
                newSolI.add(newCand2)
            
            list = solutionsF.get()
            if(len(list)!=0):
                newCand1, newCand2 = self.crossover(list[randrange(len(list))], list[randrange(len(list))])  
                newSolF.add(newCand1)
                newSolF.add(newCand2)
        
        for newCand in newSolI.get():
            solutionsI.add(newCand)
        for newCand in newSolF.get():
            solutionsF.add(newCand)
                
    # Make a mutation into a solution - pegar um prof aleatorio da lista original!!!
    def mutation(self, candidate, prof):
        relations = candidate.get()
        
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
        relation1 = cand1.get()
        relation2 = cand2.get()
        return cand1, cand2 
    
    # Detect the stop condition
    def stop(self, iteration, total, solutionsI, solutionsF):
        for cand in solutionsF.get():
            if cand.getFitness() >= 10:
                return False
        if(iteration == total):
            return False
        else:
            return True
    