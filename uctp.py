# UCTP Main Methods

from objects import *
from ioData import *
from random import randrange

class UCTP:
        
    # Create the first generation of solutions
    def start(self, solutions, subj, prof, num):        
        print "Creating first generation...",
        n = 0
        while(n!=num):
            candidate = Candidate()
            for sub in subj:
                candidate.add(sub, prof[randrange(len(prof))])
            solutions.add(candidate)
            n = n+1
        print ("Created first generation!")    
        #printAllCand(solutions)
           
        return solutions
    
    # Reset Populations Separation to allow new separation
    def resetPop(self, solutions):
        newSol = Solutions()
        for cand in solutions.get():
            newCand = cand
            newCand.resetPop()
            newSol.add(newCand)      
        return newSol
    
    # Separation of solutions into 2 populations
    def two_pop(self, solutions, prof):
        newSol = Solutions()
        for cand in solutions.get():
            newCand = self.in_feasible(cand, prof)
            newSol.add(cand)
        return newSol
    
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
                candidate.setInfeas()
                return candidate
            elif(pQuadriSabbath == sQuadri):
                candidate.setInfeas()
                return candidate
            index = prof.index(p)
            prof_total_charge[index] = (prof_total_charge[index]+ int(sCharge))
        
        n=0
        for n in range(len(prof)):
            pName, pPeriod, pCharge, pQuadriSabbath = prof[n].get()
            if(pCharge < prof_total_charge[n]):
                candidate.setInfeas()
                return candidate
            n = n+1
            
        candidate.setFeas()            
        return candidate
    
    # Calculate the Fitness of the candidate
    def calc_fit(self, solutions):
        newSol = Solutions()
        for cand in solutions.get():
            newCand = cand
            if newCand.getIF() is 'f':
                newCand.setFitness(self.calc_fitFeas(newCand))
            elif newCand.getIF() is 'i':
                newCand.setFitness(self.calc_fitInfeas(newCand))
            else:
                print "ERROR: no Fitness, solution is not in a population!"
            newSol.add(newCand)
        return newSol
    
    def calc_fitFeas(self, candidate):
        return 1
    
    def calc_fitInfeas(self, candidate):
        return -1
    
    # Generate new solutions from the actual population
    def new_generation(self, solutions, nMut, nCross):
        newSol = Solutions()
        i=0
        for i in range(nMut):
            list = solutions.get()
            newCand = self.mutation(list[randrange(len(list))])
            newSol.add(newCand)
            
        i=0
        for i in range(nCross):
            list = solutions.get()
            newCand1, newCand2 = self.crossover(list[randrange(len(list))], list[randrange(len(list))])  
            newSol.add(newCand1)
            newSol.add(newCand2)
        
        for newCand in newSol.get():
            solutions.add(newCand)
            
        return solutions
            
    # Make a mutation into a solution
    def mutation(self, candidate):
        relations = candidate.get()
        return candidate
    
    # Make a crossover between two solutions    
    def crossover(self, cand1, cand2):
        relation1 = cand1.get()
        relation2 = cand2.get()
        return cand1, cand2
    
    # Make a random selection into the solutions
    def selection(self, solutions, min, max):
        originalSize = len(solutions.get())
        while(originalSize > max):
            list = solutions.get()
            cand = list[randrange(len(list))]
            solutions.remove(cand)
            originalSize = originalSize-1
            print "Candidate removed by Selection...."
            printOneFit(cand)
        return solutions
    
    # Detect the stop condition
    def stop(self, iteration, total, solutions):
        for cand in solutions.get():
            if cand.getFitness() >= 100:
                return False
        if(iteration == total):
            return False
        else:
            return True
    