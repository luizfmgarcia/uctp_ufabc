# UCTP Main Methods

from objects import *
from ioData import *
from random import randrange

class UCTP:
        
    # Create the first generation of solutions
    def start(self, solutionsNoPop, subj, prof, num):        
        print "Creating first generation...",
        n = 0
        while(n!=num):
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
        # List used to relate with the position of Professors in 'prof' list 
        prof_total_charge = []
        n=0
        for n in range(len(prof)):
            prof_total_charge.append(0)
            n = n+1
            
        for s, p in candidate.get():
            sLevel, sCode, sName, sQuadri, sPeriod, sCharge = s.get()
            pName, pPeriod, pCharge, pQuadriSabbath = p.get()
            if(('NEGOCI' not in pPeriod) and (pPeriod != sPeriod)):
                return "infeasible"
            elif(pQuadriSabbath == sQuadri):
                return "infeasible"
            index = prof.index(p)
            prof_total_charge[index] = (prof_total_charge[index]+ float(sCharge))
        
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
    
    def calc_fitFeas(self, cand):
        
        return 1
    
    def calc_fitInfeas(self, cand):
        return -1
        # normalizacao materia turno por professor alfa
        # quadrimestre sabatico por prof beta
    
    # Generate new solutions from the actual population
    def new_generation(self, solutionsI, solutionsF, prof, nMut, nCross):
        newSolI = Solutions()
        newSolF = Solutions()
        
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
    
    # Make a random selection into the solutions
    def selection(self, solutionsI, solutionsF, min, max):
        originalSize = len(solutionsI.get())
        while(originalSize > max):
            list = solutionsI.get()
            cand = list[randrange(len(list))]
            solutionsI.remove(cand)
            originalSize = originalSize-1
            print "Candidate removed by Selection...."
            printOneFit(cand)
            
        originalSize = len(solutionsF.get())
        while(originalSize > max):
            list = solutionsF.get()
            cand = list[randrange(len(list))]
            solutionsF.remove(cand)
            originalSize = originalSize-1
            print "Candidate removed by Selection...."
            printOneFit(cand)    
    
    # Detect the stop condition
    def stop(self, iteration, total, solutionsI, solutionsF):
        for cand in solutionsF.get():
            if cand.getFitness() >= 10:
                return False
        if(iteration == total):
            return False
        else:
            return True
    