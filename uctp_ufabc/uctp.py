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
    def twoPop(self, solutionsNoPop, solI, solF, prof, subj, weights):
        # Granting that the Lists will be empty to receive new Solutions
        solI.resetList()
        solF.resetList()
        
        for cand in solutionsNoPop.getList():
            # Classification by checking feasibility
            pop = self.checkFeasibility(cand, prof, subj, weights[0], weights[1], weights[2])
            if(pop=="feasible"):
                solF.addCand(cand)
            elif(pop=="infeasible"):
                solI.addCand(cand) 
                   
        solutionsNoPop.resetList()
        
#==============================================================================================================            
        
    # Detect the violation of a Restriction into a candidate
    def checkFeasibility(self, candidate, prof, subj, w_alpha, w_beta, w_gamma):
        # As part of the Candidate's Prof-Subj relations with both the Feasible and the Infeasible will be traversed to check his Feasibility here, 
        # instead of having to pass the entire Infeasible Candidate again in the 'calc_fitInfeas', the calculation of Infeasible Fitness
        # will already be done only one time here. Only the Feasible ones will have to pass through 'calc_fitFeas' later.
        
        # Restrictions to be verified:
        # i1: penalty to how many Professors does not have at least one relation with a Subject 
        # i2: penalty to how many Subjects, related to the same Professor, are teach in the same day, hour and quadri
        # i3: penalty to how many Subjects, related to the same Professor, are teach in the same day and quadri but in different campus
        
        # Auxiliary variables to main ones (i1, i2 and i3)
        p_p=0.0
        # List of the subjects that have a conflict between them - always the two conflicts are added, that is, there can be repetitions of subjects
        conflicts_n_n = []
        conflicts_s_s = []
        
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
                        # Variables that flags if a conflict was already detected (do not count 2 or more times same 2 subjects in conflict)
                        verified_n_n = False
                        verified_s_s = False
                        
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
                                            # if one 'frequency' is "QUINZENAL I" and the other is "QUINZENAL II" then DO NOT count
                                            if('SEMANAL' in i_frequency[i_day.index(a)] or 'SEMANAL' in inext_frequency[inext_day.index(a)]):
                                                if(verified_n_n == False):
                                                    conflicts_n_n.append(list_subj[i])
                                                    conflicts_n_n.append(list_subj[k])
                                                    verified_n_n = True
                                            elif('QUINZENAL I' in i_frequency[i_day.index(a)] and 'QUINZENAL I' in inext_frequency[inext_day.index(a)]):
                                                if(verified_n_n == False):
                                                    conflicts_n_n.append(list_subj[i])
                                                    conflicts_n_n.append(list_subj[k])
                                                    verified_n_n = True
                                            elif('QUINZENAL II' in i_frequency[i_day.index(a)] and'QUINZENAL II' in inext_frequency[inext_day.index(a)]):
                                                if(verified_n_n == False):
                                                    conflicts_n_n.append(list_subj[i])
                                                    conflicts_n_n.append(list_subj[k])
                                                    verified_n_n = True
                                        # There is, at least, two subjects teach in the same day and quadri, but in different campus
                                        if(campus_List[i]==campus_List[k]):
                                            # if one 'frequency' is "QUINZENAL I" and the other is "QUINZENAL II" then DO NOT count
                                            if('SEMANAL' in i_frequency[i_day.index(a)] or 'SEMANAL' in inext_frequency[inext_day.index(a)]):
                                                if(verified_s_s == False):
                                                    conflicts_s_s.append(list_subj[i])
                                                    conflicts_s_s.append(list_subj[k])
                                                    verified_s_s = True
                                            elif('QUINZENAL I' in i_frequency[i_day.index(a)] and 'QUINZENAL I' in inext_frequency[inext_day.index(a)]):
                                                if(verified_s_s == False):
                                                    conflicts_s_s.append(list_subj[i])
                                                    conflicts_s_s.append(list_subj[k])
                                                    verified_s_s = True
                                            elif('QUINZENAL II' in i_frequency[i_day.index(a)] and'QUINZENAL II' in inext_frequency[inext_day.index(a)]):
                                                if(verified_s_s == False):
                                                    conflicts_s_s.append(list_subj[i])
                                                    conflicts_s_s.append(list_subj[k])
                                                    verified_s_s = True
                        
                        # Going to the next Subject (k+1) to compare with the same, actual, main, Subject (i)
                        k = k+1    
                    
                    # Going to the next Subject (i+1) related to the same Professor   
                    i = i+1
        
        # Checking if occurred violations of restrictions on the Candidate
        if(prof_relations.count([])!=0 or len(conflicts_n_n)!=0 or len(conflicts_s_s)!=0):
            # Removing from 'conflicts_s_s' and 'conflicts_n_n' duplicates
            final_n_n = []
            final_s_s = []
            for n in conflicts_n_n:
                if(final_n_n.count(n)==0):
                    final_n_n.append(n)
            for s in conflicts_s_s:
                if(final_s_s.count(s)==0):
                    final_s_s.append(s)    
            
            # Calculating main variables
            i1 = p_p/(float(len(prof))-1.0)
            i2 = len(final_n_n)/float(len(subj))
            i3 = len(final_s_s)/float(len(subj))
            
            # Final Infeasible Function
            Fi = (-1.0)*(((w_alpha*i1)+(w_beta*i2)+(w_gamma*i3))/(w_alpha + w_beta + w_gamma))
            
            # Setting main variables of a Infeasible Candidate
            candidate.setFitness(Fi)
            candidate.setInfVariables(prof_relations, final_n_n, final_s_s)
            return "infeasible"
                    
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
        # List of the subjects that have a conflict between them - always the two conflicts are added, that is, there can be repetitions of subjects
        conflicts_n_n = []
        conflicts_s_s = []
        
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
                        # Variables that flags if a conflict was already detected (do not count 2 or more times same 2 subjects in conflict)
                        verified_n_n = False
                        verified_s_s = False
                        
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
                                            # if one 'frequency' is "QUINZENAL I" and the other is "QUINZENAL II" then DO NOT count
                                            if('SEMANAL' in i_frequency[i_day.index(a)] or 'SEMANAL' in inext_frequency[inext_day.index(a)]):
                                                if(verified_n_n == False):
                                                    conflicts_n_n.append(list_subj[i])
                                                    conflicts_n_n.append(list_subj[k])
                                                    verified_n_n = True
                                            elif('QUINZENAL I' in i_frequency[i_day.index(a)] and 'QUINZENAL I' in inext_frequency[inext_day.index(a)]):
                                                if(verified_n_n == False):
                                                    conflicts_n_n.append(list_subj[i])
                                                    conflicts_n_n.append(list_subj[k])
                                                    verified_n_n = True
                                            elif('QUINZENAL II' in i_frequency[i_day.index(a)] and'QUINZENAL II' in inext_frequency[inext_day.index(a)]):
                                                if(verified_n_n == False):
                                                    conflicts_n_n.append(list_subj[i])
                                                    conflicts_n_n.append(list_subj[k])
                                                    verified_n_n = True
                                        # There is, at least, two subjects teach in the same day and quadri, but in different campus
                                        if(campus_List[i]==campus_List[k]):
                                            # if one 'frequency' is "QUINZENAL I" and the other is "QUINZENAL II" then DO NOT count
                                            if('SEMANAL' in i_frequency[i_day.index(a)] or 'SEMANAL' in inext_frequency[inext_day.index(a)]):
                                                if(verified_s_s == False):
                                                    conflicts_s_s.append(list_subj[i])
                                                    conflicts_s_s.append(list_subj[k])
                                                    verified_s_s = True
                                            elif('QUINZENAL I' in i_frequency[i_day.index(a)] and 'QUINZENAL I' in inext_frequency[inext_day.index(a)]):
                                                if(verified_s_s == False):
                                                    conflicts_s_s.append(list_subj[i])
                                                    conflicts_s_s.append(list_subj[k])
                                                    verified_s_s = True
                                            elif('QUINZENAL II' in i_frequency[i_day.index(a)] and'QUINZENAL II' in inext_frequency[inext_day.index(a)]):
                                                if(verified_s_s == False):
                                                    conflicts_s_s.append(list_subj[i])
                                                    conflicts_s_s.append(list_subj[k])
                                                    verified_s_s = True
                        
                        # Going to the next Subject (k+1) to compare with the same, actual, main, Subject (i)
                        k = k+1    
                    
                    # Going to the next Subject (i+1) related to the same Professor   
                    i = i+1
        
        # Removing from 'conflicts_s_s' and 'conflicts_n_n' duplicates
        final_n_n = []
        final_s_s = []
        for n in conflicts_n_n:
            if(final_n_n.count(n)==0):
                final_n_n.append(n)
        for s in conflicts_s_s:
            if(final_s_s.count(s)==0):
                final_s_s.append(s)    
        
        # Calculating main variables
        i1 = p_p/(float(len(prof))-1.0)
        i2 = len(final_n_n)/float(len(subj))
        i3 = len(final_s_s)/float(len(subj))
        
        # Final Infeasible Function
        Fi = (-1.0)*(((w_alpha*i1)+(w_beta*i2)+(w_gamma*i3))/(w_alpha + w_beta + w_gamma))
        
        # Setting main variables of a Infeasible Candidate
        candidate.setInfVariables(prof_relations, final_n_n, final_s_s)
        
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
    def offspringI(self, solutionsNoPop, solutionsI, prof, subj):
        # Check if the Infeasible pop. is empty
        if(len(solutionsI.getList())!=0):
            # Make a Mutation for each candidate, trying to repair a restriction problem maker
            for cand in solutionsI.getList():
                newCand = self.mutationI(cand, prof, subj)
                # Adding the new Candidate generated by Mutation to 'solutionsNoPop'
                solutionsNoPop.addCand(newCand)
        
#==============================================================================================================            
    
    # Make a mutation into a solution
    def mutationI(self, candidate, prof, subj):
        # (1) Prof without relations with Subjects in 'prof_relations'
        # (2) 2 or more Subjects (related to the same Prof) with same 'quadri', day and hour in 'final_n_n'
        # (3) 2 or more Subjects (related to the same Prof) with same 'day but different 'quadri' in 'final_s_s'
        
        # Getting data to work with
        relations = candidate.getList()
        prof_relations, final_n_n, final_s_s = candidate.getInfVariables()
        
        # This While ensures that 'errorType' will choose Randomly one 'restriction repair'
        flag_repair_done = False   
        while(flag_repair_done == False):
            # Choosing one type of restriction repair
            errorType =  randrange(1,4)
                   
            if(errorType==1):
                # Granting that the 'errorType' do not change good relations without restrictions to repair
                if(prof_relations.count([])!=0):
                    # Creating a list with only the index of Prof without Relations and an other one only with Prof with Relations
                    prof_No_Relations = []
                    prof_With_Relations = []
                    for p in prof_relations:
                        if(p==[]):
                            prof_No_Relations.append(prof_relations.index(p))
                        else:
                            prof_With_Relations.append(prof_relations.index(p))    
                    
                    # Choosing one Prof to be included in one relation        
                    change_index = randrange(len(prof_No_Relations))
                    change = prof_No_Relations[change_index]
                    newProf = prof[change]
                    
                    # Choosing the Prof will lose a Relation to the new one using a Roulette Wheel
                    # Creating a list of Weights based in the number of relations of each professor with relations
                    Weights = []
                    for p in prof_With_Relations:
                        Weights.append(float(len(prof_relations[p])))
                        
                    # Find the total Number of Relations of the population (has to be the same of number of Subjects
                    totalRelations = 0.0
                    for w in Weights:
                        totalRelations = totalRelations + w
                        
                    if(totalRelations != float(len(subj))):
                        print "ERRO! Numero de Relacoes diferente do numero de Disciplinas."    
                    
                    # Calculate the prob. of a selection for each prof
                    probList = []
                    for w in Weights:
                        p = w/totalRelations
                        probList.append(p) 
                    
                    # Calculate a cumulative prob. for each Professor
                    cumulative=0.0
                    cumulativeProbList = []
                    for q in probList:
                        qNew = q + cumulative
                        cumulativeProbList.append(qNew)
                        cumulative = qNew
                    
                    # Solutions selected by roullete and number of Solutions to be selected with the roulette
                    selectedProf_Index = []
                    objectiveNum = 1
                    # MAIN Roulette Selection process - do it until choose the 'objectiveNum' of Solutions
                    while(len(selectedProf_Index) < objectiveNum):    
                        # Previous Probability / Actual Prob. Index / Random Number to do one Roullete Round 
                        probPrev = 0.0
                        index = 0
                        r = float(randrange(100)/100.0)
                        
                        # Roullete round - find a unique solution in range 'probPrev' and 'q'
                        for q in cumulativeProbList:
                            if(probPrev < r and r <= q):
                                # Add the selected Solution to 'selectedProf_Index' list and finish this roullete round
                                selectedProf_Index.append(prof_With_Relations[index])
                                break
                            
                            # Go to next solution updating the main data
                            probPrev = q    
                            index = index + 1
                    
                    # Selecting a subject related with the Selected Prof to lose this Relation
                    relations_choosed = prof_relations[selectedProf_Index[0]]
                    index_relation_choosed = randrange(len(relations_choosed))
                    relation_will_change_index = relations_choosed[index_relation_choosed]
                    
                    # This line serves only to set the same 'subj' object to the new relation will be formed after
                    subj, oldProf = relations[relation_will_change_index]
                    
                    # Setting the flag to finish the while
                    flag_repair_done = True       
            
            elif(errorType==2):
                # Granting that the 'errorType' do not change good relations without restrictions to repair
                if(len(final_n_n)!=0):
                    # Choosing the relation to be modified
                    will_change_index = randrange(len(final_n_n))
                    relation_will_change_index = final_n_n[will_change_index]
                    
                    # Choosing new Prof to be in the relation with the Subj selected
                    subj, oldProf = relations[relation_will_change_index]
                    change = randrange(len(prof))
                    newProf = prof[change]
                    # Granting that the new Prof is different of the old one
                    while(oldProf==newProf):
                        change = randrange(len(prof))
                        newProf = prof[change]
                    
                    # Setting the flag to finish the while
                    flag_repair_done = True    
                
            elif(errorType==3):
                # Granting that the 'errorType' do not change good relations without restrictions to repair
                if(len(final_s_s)!=0):
                    # Choosing the relation to be modified
                    will_change_index = randrange(len(final_s_s))
                    relation_will_change_index = final_s_s[will_change_index]
                    
                    # Choosing new Prof to be in the relation with the Subj selected
                    subj, oldProf = relations[relation_will_change_index]
                    change = randrange(len(prof))
                    newProf = prof[change]
                    # Granting that the new Prof is different of the old one
                    while(oldProf==newProf):
                        change = randrange(len(prof))
                        newProf = prof[change]
                        
                    # Setting the flag to finish the while
                    flag_repair_done = True                
        
        # Setting the new relation, creating new Candidate and returning it
        relations[relation_will_change_index]=[subj,newProf]
        newCand = Candidate()
        newCand.setList(relations)
        
        return newCand
        
#==============================================================================================================            
                 
    # Generate new solutions from the current Feasible population
    def offspringF(self, solutionsNoPop, solutionsF, prof, subj, pctMut, pctRouletteCross, numCand):
        # Check if the Feasible pop. is empty
        if(len(solutionsF.getList())!=0):
            # 'objectiveNum': number of solutions to become parents - based on 'pctRouletteCross'
            objectiveNum = (pctRouletteCross*len(solutionsF)/100)
            
            # Turning 'objectiveNum' to Even if it is Odd -> summing +1 to it only if the new 'objectiveNum' is not bigger then len(solutionsF)
            if(objectiveNum % 2 != 0):
                if((objectiveNum+1)<=len(solutionsF)):
                    objectiveNum = objectiveNum + 1
                else:
                    objectiveNum = objectiveNum - 1
            
            # Granting that are solutions enough to became fathers (more than or equal 2)
            if(objectiveNum<2):
                # If do not have at least 2 solutions - all solutions will generate a child through mutation  
                for cand in solutionsF.getList():
                    newCand = self.mutationF(cand, prof)
                    solutionsNoPop.addCand(newCand)
                    
            # If we have at least 2 solutions, will have a Roulette Wheel with Reposition where the 'objectiveNum' of solutions will become Parents
            else:
                # Find the total fitness of the population
                totalFitFeas = 0.0
                for cand in solutionsF.getList():
                    totalFitFeas = totalFitFeas + cand.getFitness()
                
                # Calculate the prob. of a selection for each candidate
                probFeas = []
                for cand in solutionsF.getList():
                    p = cand.getFitness()/totalFitFeas
                    probFeas.append(p) 
                
                # Calculate a cumulative prob. for each candidate
                cumulativeProbFeas = []
                cumulative=0.0
                for q in probFeas:
                    qNew = q + cumulative
                    cumulativeProbFeas.append(qNew)
                    cumulative = qNew
                
                # Solutions selected by roullete to be parents
                parentsSolFeas = []
                # MAIN Roulette Selection process - do it until choose the 'objectiveNum' of Solutions
                while(len(parentsSolFeas) < objectiveNum):
                    # Previous Probability / Actual Prob. Index / Random Number to do one Roullete Round     
                    probPrev = 0.0
                    index = 0
                    r = float(randrange(100)/100.0)
                    
                    # Roullete round - find a unique solution in range 'probPrev' and 'q'
                    for q in cumulativeProbFeas:
                        if(probPrev < r and r <= q):
                            # Add the selected Solution to 'parentsSolFeas' list and finish this roullete round
                            parentsSolFeas.append(solutionsF.getList()[index])
                            break
                        
                        # Go to next solution updating the main data
                        probPrev = q    
                        index = index + 1        
                
                # Solutions 'children' created by crossover
                childSolFeas = []  
                # Make a Crossover (create two new candidates) for each pair of parents candidates randomly choose
                # Granting the number of children is equal of parents
                while(childSolFeas < objectiveNum):                    
                    # If there are only 2 parents, make a crossover between them
                    if(parentsSolFeas<=2):
                        parent1 = 0
                        parent2 = 1
                    
                    # If there are more, choosing the parents Randomly  
                    else:
                        parent1 = randrange(len(parentsSolFeas))
                        parent2 = randrange(len(parentsSolFeas))
                        # Granting the second parent is not the same of first one
                        while(parent1==parent2):
                            parent2 = randrange(len(parentsSolFeas))
                    
                    # Making the Crossover with the selected parents
                    newCand1, newCand2 = self.crossoverF(parentsSolFeas[parent1], parentsSolFeas[parent2])
                   
                    # Removing used parents to make a new selection of Parents
                    parentsSolFeas.pop(parent1)
                    parentsSolFeas.pop(parent2)
                    
                    # adding the new candidates generated to childSolFeas  
                    childSolFeas.append(newCand1)
                    childSolFeas.append(newCand2)
                
                # Make Mutations with 'pctMut' (mutation prob.) with all the children generated by Crossover right before
                for cand in childSolFeas:
                    # Generating a random value to validate the execution of a Mutation
                    r = float(randrange(100)/100.0)
                    if(r<=(pctMut/100.0)):
                        # Making a mutation process to the child
                        newCand = self.mutationF(cand, prof)
                        # Adding the generated by crossover and modified by mutation Candidate to 'solutionsNoPop'
                        solutionsNoPop.addCand(newCand)
                    else:
                        # Adding the generated by crossover Candidate to 'solutionsNoPop'
                        solutionsNoPop.addCand(cand)    
        
#==============================================================================================================            
                    
    # Make a mutation into a solution
    def mutationF(self, candidate, prof):
        # Getting all relations from Candidate
        relations = candidate.getList()
        
        # Choosing randomly a relation to be modified
        original = randrange(len(relations))
        # Recording the Original Relation
        subj, oldProf = relations[original]
        
        # Finding randomly a new Prof
        change = randrange(len(prof))
        newProf = prof[change]
        
        # Granting that the 'newProf' is different from the 'oldProf'
        while(oldProf==newProf):
            change = randrange(len(prof))
            newProf = prof[change]
        
        # Setting the new Relation modified, creating and setting a new Candidate
        relations[original]=[subj,newProf]
        newCand = Candidate()
        newCand.setList(relations)
        
        # Returning the new Candidate generated
        return newCand
        
#==============================================================================================================            
    
    # Make a crossover between two solutions    
    def crossoverF(self, cand1, cand2):
        # Getting all relations from Candidates
        relations1 = cand1.getList()
        relations2 = cand2.getList()
        
        # Generating, Randomly two number to create a patch - can be a single modification (when p1==p2)
        point1 = randrange(len(relations1))
        point2 = randrange(len(relations1))
        
        # Granting that 'point2' is bigger than 'point1'
        if(point2<point1):
            p = point1
            point1 = point2
            point2 = p
        
        # Passing through the relations between 'point1' and 'point2'    
        while (point1<=point2):
            # Recording the originals relations
            s1, p1 = relations1[point1]
            s2, p2 = relations2[point1]
            
            # Making the exchange of relations
            relations1[point1] = s2, p2 
            relations2[point1] = s1, p1
            
            # Next relation
            point1 = point1 + 1
               
        # Creating and setting the two new Candidates
        newCand1 = Candidate()
        newCand2 = Candidate()
        newCand1.setList(relations1)
        newCand2.setList(relations2)
        
        # Returning the new Candidates
        return newCand1, newCand2 
        
#==============================================================================================================            

    # Make a selection of the solutions from all Infeasible Pop.('infPool' and 'solutionsI')
    def selectionI(self, infPool, solutionsI, numCand):
        # New list with both lists (infPool and solutionsI)
        infeasibles_List = []
        infeasibles_List = solutionsI.getList()+infPool.getList()
        
        # Check if there are more or less Candidates then it is possible to have into a generation
        if(len(infeasibles_List)<=numCand):            
            # Is not needed to make the whole process
            # Setting the new 'solutionsI' list to go to the next generation
            solutionsI.setList(infeasibles_List)
        
        # Is needed to make the selection process with Roulette Wheel without Reposition
        else:
            # List whit the selected Solutions
            newSolInf = []
            
            # Updating the data for the next Roullete Round without the solution that was recent selected and added to 'newSolInf' on the past round 
            while(len(newSolInf) < numCand):         
                
                # Find the total fitness of the population
                totalFitInf = 0.0
                for cand in infeasibles_List:
                    # Since the value of Fitness is in the range of '-1' and '0' it is needed to be modified
                    # Modifying the values to put it into a range of '0' and '1'
                    newFit = 1.0 + cand.getFitness()
                    totalFitInf = totalFitInf + newFit
                
                # Calculate the prob. of a selection for each candidate
                probInf = []
                for cand in infeasibles_List:
                    # Since the value of Fitness is in the range of '-1' and '0' it is needed to be modified
                    # Modifying the values to put it into a range of '0' and '1'
                    newFit = 1.0 + cand.getFitness()
                    p = newFit/totalFitInf
                    probInf.append(p) 
                
                # Calculate a cumulative prob. for each candidate
                cumulativeProbInf = []
                cumulative=0.0
                for q in probInf:
                    qNew = q + cumulative
                    cumulativeProbInf.append(qNew)
                    cumulative = qNew
                
                # MAIN Roulette Wheel Selection process (no Reposition)    
                probPrev = 0.0
                index = 0
                r = float(randrange(100)/100.0)
                for q in cumulativeProbInf:
                    if(probPrev < r and r <= q):
                        # Adding the selected solution to 'newSolInf'
                        newSolInf.append(infeasibles_List[index])
                        # Removing the selected solution from 'infeasibles_List'
                        infeasibles_List.pop(index)
                        break
                    
                    probPrev = q    
                    index = index + 1   
            
            # Setting the new 'solutionsI' list to go to the next generation    
            solutionsI.setList(newSolInf)
            
#==============================================================================================================            
    
    # Make a Selection of the best solutions from Feasible Pop.
    def selectionF(self, feaPool, solutionsF, numCand):
        # New list with both lists (feaPool and solutions)
        feasibles_List = []
        feasibles_List = solutionsF.getList()+feaPool.getList()
        
        # Check if there are more or less Candidates then it is possible to have into a generation
        if(len(feasibles_List)<=numCand):            
            # Is not needed to make the whole process
            # Setting the new 'solutionsF' list to go to the next generation
            solutionsF.setList(feasibles_List)
        
        # Is needed to make the selection process with only the best ones
        else:            
            # Gathering all Fitness
            listFit = []
            for cand in feasibles_List:
                listFit.append(cand.getFitness())
            
            # Removing the minimal Fitness Solutions
            while(len(feasibles_List)>numCand):
                # Finding the minimal value in the list and its respective index
                minValue = min(listFit)
                minIndex = listFit.index(minValue)
                
                # Removing from main lists this minimal Fitness Solution 
                listFit.pop(minIndex)
                feasibles_List.pop(minIndex)
            
            # Setting the new 'solutionsF' list to go to the next generation        
            solutionsF.setList(feasibles_List)        
        
#==============================================================================================================            
                
    # Detect the stop condition
    def stop(self, iteration, total, solutionsI, solutionsF):
        for cand in solutionsF.getList():
            if cand.getFitness() >= 0.999:
                return False
        if(iteration > total):
            return False
        else:
            return True
        
#==============================================================================================================    