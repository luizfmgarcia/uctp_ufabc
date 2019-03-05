# UCTP Main Methods

from objects import *
from ioData import *
from random import *
        
#==============================================================================================================            

#sLevel, sCode, sName, sQuadri, sPeriod, sCampus, sCharge, sTimetableList = s.get()
#pName, pPeriod, pCharge, pQuadriSabbath, pPrefCampus, pPrefSubjQ1List, pPrefSubjQ2List, pPrefSubjQ3List, pPrefSubjLimList = p.get()
class UCTP:
        
#==============================================================================================================            
        
    # Create the first generation of solutions
    def start(self, solutionsNoPop, subj, prof, init):        
        print "Creating first generation...",
        n = 0
        while(n!=init):
            candidate = Candidate()
            # Follow the subjects in 'subj' list, in order, and for each one, choose a professor randomly 
            for sub in subj:
                candidate.addRelation(sub, prof[randrange(len(prof))])
            solutionsNoPop.addCand(candidate)
            n = n+1
        print ("Created first generation!")    
        #printAllCand(solutions)
        
#==============================================================================================================            
    
    # Separation of solutions into 2 populations
    def twoPop(self, solutionsNoPop, solutionsI, solutionsF, prof, subj):
        for cand in solutionsNoPop.getList():
            # classification by checking feasibility
            pop = self.checkFeasibility(cand, prof, subj)
            if(pop=="feasible"):
                solutionsF.addCand(cand)
            elif(pop=="infeasible"):
                solutionsI.addCand(cand) 
                   
        solutionsNoPop.resetList()
        
#==============================================================================================================            
        
    # Detect the violation of a Restriction into a candidate
    def checkFeasibility(self, candidate, prof, subj):
        # List of lists of Subjects that are related to the same Professor, where the position in this list is the same of the same professor in 'prof' list 
        prof_relations = []
        
        # Initializing the list
        n=0
        for n in range(len(prof)):
            prof_relations.append([])
            n = n+1
        
        # Filling the list according to the candidate    
        for s, p in candidate.getList():            
            indexp = prof.index(p)
            indexs = subj.index(s)
            prof_relations[indexp].append(indexs)
        
        # Search a Professor that do not exists on the Candidate - empty list in the 'prof_relations' list   
        if(prof_relations.count([])!=0):
            return "infeasible"
        
        # Searching, in each professor (one at a time), conflicts of schedules between subjects related to it
        for list_subj in prof_relations:
            # Check if the professor has more than 1 relation Prof-Subj to analyze
            if(len(list_subj)!=1):
                # Getting the data of all Subjects related to actual Professor in analysis (the same position in all 3 lists it is from the same subj) 
                timetableList_List = []
                quadri_List = []
                campus_List = []
                for subj_index in list_subj:
                    sLevel, sCode, sName, sQuadri, sPeriod, sCampus, sCharge, sTimetableList = subj[subj_index].get()
                    timetableList_List.append(sTimetableList)
                    quadri_List.append(sQuadri)
                    campus_List.append(sCampus)
                
                # Comparing the data of one Subject (i) with all next subjects listed, and do the same with next ones
                i=0
                for timeTable in  timetableList_List:
                    # all [day/hour/frequency] of the Timetable of the Subject (i) in 'timetableList_List'
                    i_day = []
                    i_hour = []
                    i_frequency = []
                    for j in timeTable:
                        i_day.append(j[0])
                        i_hour.append(j[1])
                        i_frequency.append(j[2])
                    
                    # Now, comparing actual (i) subject data with next ones (k), one at a time
                    k = i+1
                    rest = timetableList_List[k:]
                    # repeat this 'len(rest)' times
                    for next in rest:
                        # all [day/hour/frequency] of the Timetable of the Subject (k) in 'timetableList_List'
                        inext_day = []
                        inext_hour = []
                        inext_frequency = []
                        for j in timeTable:
                            inext_day.append(j[0])
                            inext_hour.append(j[1])
                            inext_frequency.append(j[2])
                        
                        # Finally comparing one-to-one timetables - between i and k subjects
                        for a in i_day:
                            for b in inext_day:                                
                                if(a==b):
                                    if(quadri_List[i]==quadri_List[k]):
                                        # There is, at least, two subjects teach in the same day, hour and quadri
                                        if(i_hour[i_day.index(a)]==inext_hour[inext_day.index(b)]):
                                            return "infeasible" 
                                        # There is, at least, two subjects teach in the same day and quadri, but in different campus
                                        if(campus_List[i]==campus_List[k]):
                                            return "infeasible"
                        
                        #Going to the next Subject (k+1) to compare with the same, actual, main, Subject (i)
                        k = k+1    
                    
                    # Going to the next Subject (i+1) related to the same Professor   
                    i = i+1
                    
        # If all Relations Prof-Subj in this Candidate passed through the restrictions
        return "feasible"
         
#==============================================================================================================            
   
    # Calculate the Fitness of the candidate
    def calcFit(self, infeasibles, feasibles, prof, subj, weights):
        # All Infeasible Candidates
        for cand in infeasibles.getList():
            if(cand.getFitness() == 0.0):
                # Setting the Fitness with the return of calc_fitInfeas() method
                cand.setFitness(self.calc_fitInfeas(cand, prof, subj, weights[0], weights[1], weights[2]))
        # All Feasible Candidates
        for cand in feasibles.getList():
            if(cand.getFitness() == 0.0):
                # Setting the Fitness with the return of calc_fitFeas() method
                cand.setFitness(self.calc_fitFeas(cand, prof, subj, weights[3], weights[4], weights[5], weights[6], weights[7]))
        
#==============================================================================================================            
   
    # Calculate Fitness of Infeasible Candidates 
    def calc_fitInfeas(self, candidate, prof, subj, w_alpha, w_beta, w_gamma):
        # It is similar to 'checkFeasibility' method, checking same restrictions, but counting the number of occurrences of each violated restriction
        # i1: penalty to how many Professors does not have at least one relation with a Subject 
        # i2: penalty to how many Subjects, related to the same Professor, are teach in the same day, hour and quadri
        # i3: penalty to how many Subjects, related to the same Professor, are teach in the same day and quadri but in different campus
        
        # Auxiliary variables to main ones (i1, i2 and i3)
        p_p=0.0
        n_n=0.0
        s_s=0.0
        
        # List of lists of Subjects that are related to the same Professor, where the position in this list is the same of the same professor in 'prof' list 
        prof_relations = []
        
        # Initializing the list
        n=0
        for n in range(len(prof)):
            prof_relations.append([])
            n = n+1
        
        # Filling the list according to the candidate    
        for s, p in candidate.getList():            
            indexp = prof.index(p)
            indexs = subj.index(s)
            prof_relations[indexp].append(indexs)
        
        # Search (p) Professors that does not exists on the Candidate - empty list in the 'prof_relations' list   
        p_p = float(prof_relations.count([]))
        
        # Searching, in each professor (one at a time), conflicts of schedules between subjects related to it
        for list_subj in prof_relations:
            # Check if the professor has more than 1 relation Prof-Subj to analyze
            if(len(list_subj)!=1):
                # Getting the data of all Subjects related to actual Professor in analysis (the same position in all 3 lists it is from the same subj) 
                timetableList_List = []
                quadri_List = []
                campus_List = []
                for subj_index in list_subj:
                    sLevel, sCode, sName, sQuadri, sPeriod, sCampus, sCharge, sTimetableList = subj[subj_index].get()
                    timetableList_List.append(sTimetableList)
                    quadri_List.append(sQuadri)
                    campus_List.append(sCampus)
                
                # Comparing the data of one Subject (i) with all next subjects listed, and do the same with next ones
                i=0
                for timeTable in  timetableList_List:
                    # all [day/hour/frequency] of the Timetable of the Subject (i) in 'timetableList_List'
                    i_day = []
                    i_hour = []
                    i_frequency = []
                    for j in timeTable:
                        i_day.append(j[0])
                        i_hour.append(j[1])
                        i_frequency.append(j[2])
                    
                    # Now, comparing actual (i) subject data with next ones (k), one at a time
                    k = i+1
                    rest = timetableList_List[k:]
                    # repeat this 'len(rest)' times
                    for next in rest:
                        # all [day/hour/frequency] of the Timetable of the Subject (k) in 'timetableList_List'
                        inext_day = []
                        inext_hour = []
                        inext_frequency = []
                        for j in timeTable:
                            inext_day.append(j[0])
                            inext_hour.append(j[1])
                            inext_frequency.append(j[2])
                        
                        # Finally comparing one-to-one timetables - between i and k subjects
                        for a in i_day:
                            for b in inext_day:                                
                                if(a==b):
                                    if(quadri_List[i]==quadri_List[k]):
                                        # There is, at least, two subjects teach in the same day, hour and quadri
                                        if(i_hour[i_day.index(a)]==inext_hour[inext_day.index(b)]):
                                            n_n = n_n + 1.0 
                                        # There is, at least, two subjects teach in the same day and quadri, but in different campus
                                        if(campus_List[i]==campus_List[k]):
                                            s_s = s_s + 1.0
                        
                        #Going to the next Subject (k+1) to compare with the same, actual, main, Subject (i)
                        k = k+1    
                    
                    # Going to the next Subject (i+1) related to the same Professor   
                    i = i+1
        
        # Calculating main variables
        i1 = p_p/(float(len(prof))-1.0)
        i2 = n_n/float(len(subj))
        i3 = s_s/float(len(subj))
        
        # Final Infeasible Function
        Fi = (-1.0)*(((w_alpha*i1)+(w_beta*i2)+(w_gamma*i3))/(w_alpha + w_beta + w_gamma))
        
        # Returning the result calculated
        return Fi
        
#==============================================================================================================            
     
    # Calculate Fitness of Feasible Candidates 
    def calc_fitFeas(self, cand, prof, subj, w_delta, w_omega, w_sigma, w_pi, w_rho):
        
        # Calculating main variables
        f1=0
        f2=0
        f3=0
        f4=0
        f5=0
        
        # Final Feasible Function
        Ff = ((w_delta*f1)+(w_omega*f2)+(w_sigma*f3)+(w_pi*f4)+(w_rho*f5))/(w_delta + w_omega + w_sigma + w_pi + w_rho)
        
        # Returning the result calculated
        return Ff
         
#==============================================================================================================            
           
    # Generate new solutions from the current Infeasible population
    def offspringI(self, solutionsNoPop, solutionsI, prof):
        if(len(solutionsI.getList())!=0):
            # Make a Mutation for each candidate, trying to repair a restriction problem maker
            for cand in solutionsI.getList():
                newCand = self.mutationI(cand, prof)
                solutionsNoPop.addCand(newCand)
        
#==============================================================================================================            
    
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
        
#==============================================================================================================            
                 
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
        
#==============================================================================================================            
                    
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
        
#==============================================================================================================            
    
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
        
#==============================================================================================================            
        
    # Make a Roulette Wheel selection of the solutions from Infeasible Pop.
    def selectionI(self, infPool, solutionsI, numCand):
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
        
#==============================================================================================================            
    
    # Make a Selection of the best solutions from Feasible Pop.
    def selectionF(self, feaPool, solutionsF, numCand):
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
        
#==============================================================================================================            
                
    # Detect the stop condition
    def stop(self, iteration, total, solutionsI, solutionsF):
        for cand in solutionsF.getList():
            if cand.getFitness() >= 0.999:
                return False
        if(iteration == total):
            return False
        else:
            return True
        
#==============================================================================================================    