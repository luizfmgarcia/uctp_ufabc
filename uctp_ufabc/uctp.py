# UCTP Main Methods

from objects import *
from ioData import *
from random import *

# Set '1' to allow, during the run, the output of some steps
prt = 1

#==============================================================================================================            

class UCTP:

#==============================================================================================================            
        
    # Create the first generation of solutions
    def start(self, solutionsNoPop, subj, prof, init):        
        if(prt==1): print("Creating first generation...", end='')
        n = 0
        while(n!=init):
            candidate = Candidate()
            # Follow the subjects in 'subj' list, in order, and for each one, choose a professor randomly 
            for sub in subj:
                candidate.addRelation(sub, prof[randrange(len(prof))])
            solutionsNoPop.addCand(candidate)
            n = n+1
        if(prt==1): print("Created first generation!")    
        #printAllCand(solutions)
        
#==============================================================================================================            
    
    # Separation of solutions into 2 populations
    def twoPop(self, solutionsNoPop, solI, solF, prof, subj, weights):
        # Granting that the Lists will be empty to receive new Solutions
        solI.resetList()
        solF.resetList()
        
        for cand in solutionsNoPop.getList():
            # Classification by checking feasibility
            pop = self.checkFeasibility(cand, prof, subj, weights)
            if(pop=="feasible"):
                solF.addCand(cand)
            elif(pop=="infeasible"):
                solI.addCand(cand) 
        
        # Granting that the List will be empty to next operations          
        solutionsNoPop.resetList()
        
        if(prt==1): print("Checked Feasibility (new Candidates)/", end='')
        
#==============================================================================================================            
        
    # Detect the violation of a Restriction into a candidate
    def checkFeasibility(self, candidate, prof, subj, weights):
        # As part of the Candidate's Prof-Subj relations (with both Feasible and the Infeasible) will be traversed to check they Feasibility here, 
        # instead of repass an entire Infeasible Candidate again in the 'calc_fitInfeas', the calculation of its Fitness will already be done
        # only one time here. Only the Feasible ones will have to pass through 'calc_fitFeas' later.
        fit = -1
        fit = self.calc_fitInfeas(candidate, prof, subj, weights[0], weights[1], weights[2])
        if(fit<0):
            candidate.setFitness(fit)
            return "infeasible"
            
        return "feasible"
         
#==============================================================================================================            
   
    # Calculate the Fitness of the candidate
    def calcFit(self, infeasibles, feasibles, prof, subj, weights):
        # All Infeasible Candidates - is here this code only for the representation of the default/original algorithm`s work
        # The Inf. Fitness calc was already done in 'checkFeasibility()' method
        # Check if the Infeasible pop. is empty
        if(len(infeasibles.getList())!=0):
            for cand in infeasibles.getList():
                if(cand.getFitness() == 0.0):
                    # Setting the Fitness with the return of calc_fitInfeas() method
                    cand.setFitness(self.calc_fitInfeas(cand, prof, subj, weights[0], weights[1], weights[2]))
            if(prt==1): print("Fitness of all Inf./", end='')
        
        # All Feasible Candidates
        # Check if the Feasible pop. is empty
        if(len(feasibles.getList())!=0):
            for cand in feasibles.getList():
                if(cand.getFitness() == 0.0):
                    # Setting the Fitness with the return of calc_fitFeas() method
                    cand.setFitness(self.calc_fitFeas(cand, prof, subj, weights[3], weights[4], weights[5], weights[6], weights[7]))
            if(prt==1): print("Fitness of all Feas./", end='')
        
#==============================================================================================================            
    
    # Calculate Fitness of Infeasible Candidates 
    def calc_fitInfeas(self, candidate, prof, subj, w_alpha, w_beta, w_gamma):
        # Getting information about the Candidate
        prof_relations = self.i1(candidate, prof, subj)
        conflicts_n_n, conflicts_s_s = self.i2_i3(prof_relations, subj)
        
        # Checking if occurred violations of restrictions on the Candidate
        # If there are violated restrictions, this Cadidate is Infeasible and then will calculate and return a negative Fitness, 
        # if not, is Feasible, will return 1.0 as Fitness
        if(prof_relations.count([])!=0 or len(conflicts_n_n)!=0 or len(conflicts_s_s)!=0):            
            # Calculating main variables
            i1 = float(prof_relations.count([]))/(float(len(prof))-1.0)
            i2 = float(len(conflicts_n_n))/float(len(subj))
            i3 = float(len(conflicts_s_s))/float(len(subj))
            
            # Final Infeasible Function Fitness Calc
            Fi = (-1.0)*(((w_alpha*i1)+(w_beta*i2)+(w_gamma*i3))/(w_alpha + w_beta + w_gamma))

            # Setting main variables of a Infeasible Candidate
            candidate.setInfVariables(prof_relations, conflicts_n_n, conflicts_s_s)
            
            # Returning the calculated result 
            return Fi

        # If all Relations Prof-Subj in this Candidate passed through the restrictions
        candidate.setFeaVariables(prof_relations)
        return 1.0

    #-------------------------------------------------------
    
    # i1: penalty to how many Professors does not have at least one relation with a Subject
    def i1(self, candidate, prof, subj):
        # List of lists of Subjects that are related to the same Professor, where the position in this list is the same of the same professor in 'prof' list 
        # Empty list in this list means that some Professor (p) does not exists on the Candidate
        prof_relations = [[] for i in range(len(prof))]
        
        # Filling the list according to the candidate    
        for s, p in candidate.getList():            
            indexp = prof.index(p)
            indexs = subj.index(s)
            prof_relations[indexp].append(indexs)
        
        return prof_relations        
    
    #-------------------------------------------------------

    # i2: penalty to how many Subjects, related to the same Professor, are teach in the same day, hour and quadri
    # i3: penalty to how many Subjects, related to the same Professor, are teach in the same day and quadri but in different campus
    def i2_i3(self, prof_relations, subj):
        # List of the subjects that have a conflict between them - always the two conflicts are added, that is, 
        # there can be repetitions of subjects
        conflicts_n_n = []
        conflicts_s_s = []
        
        # Searching, in each professor (one at a time), conflicts of schedules between subjects related to it
        for list_subj in prof_relations:
            # Check if the professor has more than 1 relation Prof-Subj to analyze
            if(len(list_subj)>1):
                # Getting the data of all Subjects related to actual Professor in analysis
                timetableList_List = []
                quadri_List = []
                campus_List = []
                period_List = []
                for subj_index in list_subj:
                    _, _, _, sQuadri, sPeriod, sCampus, _, sTimetableList = subj[subj_index].get()
                    timetableList_List.append(sTimetableList)
                    quadri_List.append(sQuadri)
                    campus_List.append(sCampus)
                    period_List.append(sPeriod)
                
                # Comparing the data of one Subject (i) with all next subjects listed, and do the same with next ones
                i=0
                for timeTable in timetableList_List:
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
                    for nextK in rest:
                        # Alredy check if both Subj (i, k) is on same Quadri
                        if(quadri_List[i]==quadri_List[k]):
                            # Variables that flags if a conflict was already detected (do not count 2 or more times same 2 subjects in conflict)
                            verified_n_n = False
                            verified_s_s = False
                            
                            # all [day/hour/frequency] of the Timetable of the Subject (k) in 'timetableList_List'
                            inext_day = []
                            inext_hour = []
                            inext_frequency = []
                            for j in nextK:
                                inext_day.append(j[0])
                                inext_hour.append(j[1])
                                inext_frequency.append(j[2])
                            
                            # Finally comparing one-to-one timetables - between i and k subjects
                            for a in i_day:
                                for b in inext_day:                                
                                    if(a==b):
                                        # There is, at least, two subjects teach in the same day and quadri, but in different campus
                                        if(campus_List[i]!=campus_List[k]):
                                            if(verified_s_s == False):
                                                conflicts_s_s.append(list_subj[i])
                                                conflicts_s_s.append(list_subj[k])
                                                verified_s_s = True

                                        # There is, at least, two subjects teach in the same day, hour and quadri
                                        # First check if they have the same Period
                                        if(period_List[i]==period_List[k] and i_hour[i_day.index(a)]==inext_hour[inext_day.index(b)]):
                                            # if one 'frequency' is "QUINZENAL I" and the other is "QUINZENAL II" then DO NOT count
                                            if('SEMANAL' in i_frequency[i_day.index(a)] or 'SEMANAL' in inext_frequency[inext_day.index(b)]):
                                                if(verified_n_n == False):
                                                    conflicts_n_n.append(list_subj[i])
                                                    conflicts_n_n.append(list_subj[k])
                                                    #print(subj[list_subj[i]].get(), subj[list_subj[k]].get(), '\n')
                                                    verified_n_n = True
                                            elif('QUINZENAL I' in i_frequency[i_day.index(a)] and 'QUINZENAL I' in inext_frequency[inext_day.index(b)]):
                                                if(verified_n_n == False):
                                                    conflicts_n_n.append(list_subj[i])
                                                    conflicts_n_n.append(list_subj[k])
                                                    #print(subj[list_subj[i]].get(), subj[list_subj[k]].get(), '\n')
                                                    verified_n_n = True
                                            elif('QUINZENAL II' in i_frequency[i_day.index(a)] and'QUINZENAL II' in inext_frequency[inext_day.index(b)]):
                                                if(verified_n_n == False):
                                                    conflicts_n_n.append(list_subj[i])
                                                    conflicts_n_n.append(list_subj[k])
                                                    #print(subj[list_subj[i]].get(), subj[list_subj[k]].get(), '\n')
                                                    verified_n_n = True
                        
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

        return final_n_n, final_s_s
        
#==============================================================================================================            
    
    # Calculate Fitness of Feasible Candidates 
    def calc_fitFeas(self, candidate, prof, subj, w_delta, w_omega, w_sigma, w_pi, w_rho):
        
        prof_relations = candidate.getFeaVariables()
        
        # Looking for good Relations into the Candidate using "Quality Amplifiers"
        # Getting information about the Candidate
        calcF1 = self.f1(subj, prof, prof_relations)
        calcF2 = self.f2(subj, prof, prof_relations)
        calcF3 = self.f3(subj, prof, prof_relations)
        calcF4 = self.f4(subj, prof, prof_relations)
        calcF5 = self.f5(subj, prof, prof_relations)

        # Calculating main variables
        f1 = 1.0 - float(calcF1)/float(len(prof))
        f2 = float(calcF2)/float(len(prof))
        f3 = float(calcF3)/float(len(subj)) 
        f4 = float(calcF4)/float(len(subj)) 
        f5 = float(calcF5)/float(len(subj)) 
        
        # Final Feasible Function Fitness Calc
        Ff = ((w_delta*f1)+(w_omega*f2)+(w_sigma*f3)+(w_pi*f4)+(w_rho*f5))/(w_delta + w_omega + w_sigma + w_pi + w_rho)
        
        # Returning the result calculated
        return Ff
    
    #-------------------------------------------------------
    
    # f1: how balanced is the distribution of Subjects, considering the "Charge" of each Professor (count the "Charge" of all Subj related to that Prof)
    def f1(self, subj, prof, prof_relations):
        # List of all 'Effective Charges', that is, the sum of the charges of all the subjects related to the professor
        charges_AllRelations = [0 for i in range(len(prof))]
        # List of requested charges of each professor
        charges_EachProf = []

        # Counting the occurrences, filling the vectors
        for relations in prof_relations:
            # Setting Index of actual Prof
            pIndex = prof_relations.index(relations)
            # Getting data of actual Prof
            _, _, pCharge, _, _, _, _, _, _ = prof[pIndex].get()
            
            # Collecting each Professors Charge 
            charges_EachProf.append(int(pCharge))
            
            # All Relations of one Prof
            for sIndex in relations:
                # Getting data of actual Subj
                _, _, _, _, _, _, sCharge, _ = subj[sIndex].get()
                # Collecting and summing Subjects Charges related to same Prof
                charges_AllRelations[pIndex] = charges_AllRelations[pIndex] + float(str(sCharge).replace(",","."))
                
        # Calculating intermediate variable
        
        # Relative weigh of excess or missing charge for each Prof
        charges_relative = [0.0 for i in range(len(prof))]

        # Calculating and filling vector
        for pCharge in charges_EachProf:
            # Setting Index of actual Prof
            actual_index = charges_EachProf.index(pCharge)
            # Finding relative charge based on the credit difference module between the credits requested by the Prof and the sum off all Subj related to it
            res = abs(float(pCharge) - float(charges_AllRelations[actual_index]))/float(pCharge)
            if(res>1.0): charges_relative[actual_index] = 1.0
            else: charges_relative[actual_index] = res    
        
        # The arithmetic average of charge discrepancies of all professors;  
        sum_chargesRelative = 0.0
        # Calculating the value
        for charge in charges_relative:
            sum_chargesRelative = sum_chargesRelative + float(charge)
        
        return sum_chargesRelative

    #-------------------------------------------------------
    
    # f2: how many and which Subjects are the professors preference, considering "prefSubj..." Lists
    def f2(self, subj, prof, prof_relations):
        # These are Lists (each quadri - 3) of Lists (each professor) of Lists (each PrefList+LimList)
        # In each List (inside the List inside the List) we have 1 if the same index Subject (from same Quadri X Pref List + Lim Pref List) is related to Same Prof
        # or we have 0 if it is not related 
        qX_relations = [[[] for i in range(len(prof))] for j in range(3)]

        # Initializing qX_relations Lists of Lists (in each one appends "pPrefSubjQXList" with "pPrefSubjLimList" to have the length of the subList)
        for relations in prof_relations:
            # Setting Index of actual Prof
            pIndex = prof_relations.index(relations)
            
            # Getting data of actual Prof
            _, _, _, _, _, pPrefSubjQ1List, pPrefSubjQ2List, pPrefSubjQ3List, pPrefSubjLimList = prof[pIndex].get()
            prefSubjLists = [pPrefSubjQ1List, pPrefSubjQ2List, pPrefSubjQ3List, pPrefSubjLimList]
            
            # For each Quadri - Filling QX Lists of actual Prof
            for i in range(3):
                qX_relations[i][pIndex] = [0 for j in range(len(prefSubjLists[i])+len(prefSubjLists[3]))]   
            
        # Counting the occurrences, filling the vectors
        for relations in prof_relations:
            # Setting Index of actual Prof
            pIndex = prof_relations.index(relations)
            
            # Getting data of actual Prof
            _, _, _, _, _, pPrefSubjQ1List, pPrefSubjQ2List, pPrefSubjQ3List, pPrefSubjLimList = prof[pIndex].get()
            prefSubjLists = [pPrefSubjQ1List, pPrefSubjQ2List, pPrefSubjQ3List, pPrefSubjLimList]
            
            # All Relations of one Prof
            for sIndex in relations:
                # Getting data of actual Subj
                _, _, sName, _, _, _, _, _ = subj[sIndex].get()
                
                # For each Quadri
                for i in range(3):
                    # Finding the Subject 'sName' in "pPrefSubjQXList+pPrefSubjLimList" list
                    sumList = prefSubjLists[i]+prefSubjLists[3]
                    # Checking if the List is not empty
                    if(len(sumList)>0):
                        try:
                            index_value = sumList.index(sName)
                        except ValueError:
                            index_value = -1
                        # If the Subj name appears in the list
                        if(index_value!=-1):
                            # Putting '1' in same position found 'index_value' in the subList (which this one, is in same position of prof) 
                            qX_relations[i][pIndex][index_value] = 1
        
        # Calculating intermediate variables
        # Lists of the calculation of "satisfaction" based on the order of Subjects choose by a Professor (index = 0 has more weight)
        finalQX = [[] for i in range(3)]
        
        # For each Qaudri
        for i in range(3):
            # Calculating the Satisfaction from QX relations for each Professor
            for list_choice_relation in qX_relations[i]:
                # Setting actual Prof Index and actual List Relations-Preference
                prof_index = qX_relations[i].index(list_choice_relation)
                len_actual_list = len(list_choice_relation)
                
                # Initializing actual position and total weight that will be calculated next
                finalQX[i].append(0.0)
                total_weight = 0
                
                # Checking if the Relations-Preference List is empty
                if(len_actual_list == 0):
                    finalQX[i][prof_index] = 1.0
                # If is needed to be calculated (is not empty)
                else:
                    # Q1 Relations of each Professor
                    for h in list_choice_relation:
                        # Setting actual Subject Preference Position
                        pref_index = list_choice_relation.index(h)
                        # Summing the Total Weight of this list of preferences to normalize later (+1 because first index is 0)
                        total_weight = total_weight + pref_index + 1
                        
                        # If the actual Subj, in this specific position on the Preference List of actual Prof, is related to it
                        if(h==1):
                            # Summing the respective weight the Subj has in the Prof List of Preferences
                            finalQX[i][prof_index] = finalQX[i][prof_index] + (len_actual_list - pref_index + 1)
                    
                    # Calculate the final value of "Satisfaction" normalized, after obtained and summed all weights from Subjects related to actual professor
                    finalQX[i][prof_index] = float(finalQX[i][prof_index])/float(total_weight)        
        
        # Calculate the final value of a Prof "satisfaction" summing all 3 values (from finalQ1, finalQ2 and finalQ3 lists) and normalizing it
        final_Satisf = [float((finalQX[0][i]+finalQX[1][i]+finalQX[2][i])/3.0) for i in range(len(finalQX[0]))]
                
        # Finally, calculating all Professors Satisfaction summing all final values    
        sum_Satisfaction = 0.0
        for value in final_Satisf:
            sum_Satisfaction = sum_Satisfaction + value
        
        return sum_Satisfaction
        
    #-------------------------------------------------------
    
    # f3: how many Subjects are teach in a "Quadri" that is not the same of Professors 'quadriSabbath'
    def f3(self, subj, prof, prof_relations):
        num_NotSameQuadriSab = [0 for i in range(len(prof))]

        # Counting the occurrences, filling the vector
        for relations in prof_relations:
            # Setting Index of actual Prof
            pIndex = prof_relations.index(relations)
            # Getting data of actual Prof
            _, _, _, pQuadriSabbath, _, _, _, _, _ = prof[pIndex].get()
            
            # All Relations of one Prof
            for sIndex in relations:                
                # Getting data of actual Subj
                _, _, _, sQuadri, _, _, _, _ = subj[sIndex].get()
                # Adding to count if the Subj is not in the same 'pQuadriSabbath' (if Prof choose 'nenhum' he does not have a 'pQuadriSabbath')
                if(sQuadri!=pQuadriSabbath or 'NENHUM' in pQuadriSabbath):
                    num_NotSameQuadriSab[pIndex] = num_NotSameQuadriSab[pIndex] + 1
                
        # Calculating intermediate variable
        sum_NotSameQuadriSab = 0
        for value in num_NotSameQuadriSab:
            sum_NotSameQuadriSab = sum_NotSameQuadriSab + value

        return sum_NotSameQuadriSab

    #-------------------------------------------------------
    
    # f4: how many Subjects are teach in the same "Period" of the Professor preference "pPeriod"
    def f4(self, subj, prof, prof_relations):
        num_SamePeriod = [0 for i in range(len(prof))]

        # Counting the occurrences, filling the vector
        for relations in prof_relations:
            # Setting Index of actual Prof
            pIndex = prof_relations.index(relations)
            # Getting data of actual Prof
            _, pPeriod, _, _, _, _, _, _, _ = prof[pIndex].get()
            
            # All Relations of one Prof
            for sIndex in relations:
                # Getting data of actual Subj
                _, _, _, _, sPeriod, _, _, _ = subj[sIndex].get()
                # Adding to count if the Subj is in the same 'pPeriod' or if Prof do not care about 'pPeriod' equal to 'NEGOCIAVEL'
                if(sPeriod==pPeriod or 'NEGOCI' in pPeriod):
                    num_SamePeriod[pIndex] = num_SamePeriod[pIndex] + 1
                
        # Calculating intermediate variable
        sum_SamePeriod = 0
        for value in num_SamePeriod:
            sum_SamePeriod = sum_SamePeriod + value
        
        return sum_SamePeriod
        
    #-------------------------------------------------------
    
    # f5: how many Subjects are teach in the same "Campus" of the Professor preference "prefCampus"
    def f5(self, subj, prof, prof_relations):
        num_sameCampus = [0 for i in range(len(prof))]

        # Counting the occurrences, filling the vector
        for relations in prof_relations:
            # Setting Index of actual Prof
            pIndex = prof_relations.index(relations)
            # Getting data of actual Prof
            _, _, _, _, pPrefCampus, _, _, _, _ = prof[pIndex].get()
            
            # All Relations of one Prof
            for sIndex in relations:
                # Getting data of actual Subj
                _, _, _, _, _, sCampus, _, _ = subj[sIndex].get()
                # Adding to count if the Subj is in the same 'pPrefCampus'
                if(sCampus==pPrefCampus):    
                    num_sameCampus[pIndex] = num_sameCampus[pIndex] + 1
                
        # Calculating intermediate variable
        sum_sameCampus = 0
        for value in num_sameCampus:
            sum_sameCampus = sum_sameCampus + value

        return sum_sameCampus

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
  
            if(prt==1): print("Inf. Offspring/", end='')
        
#==============================================================================================================            
    
    # Make a mutation into a solution
    def mutationI(self, candidate, prof, subj):
        # Getting data to work with
        relations = candidate.getList()
        prof_relations, final_n_n, final_s_s = candidate.getInfVariables()
        
        # This While ensures that 'errorType' will choose Randomly one 'restriction repair'
        flag_repair_done = False   
        while(flag_repair_done == False):
            # Choosing one type of restriction repair
            errorType = randrange(1,4)
            
            # (0) No repair -> Random Change
            if(errorType==0):
                # Do not granting that the 'errorType' do not change good relations without restrictions to repair
                # Choosing the relation to be modified
                relation_will_change_index = randrange(len(subj))
                    
                # Setting the flag to finish the while
                flag_repair_done = True

            # (1) Prof without relations with Subjects in 'prof_relations'
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
                    
                    # Roulette Wheel
                    numRelationsList = [float(len(prof_relations[p])) for p in prof_With_Relations]
                    selectedProf_Index = self.rouletteWheel(prof_With_Relations, numRelationsList, objectiveNum=1, repos=True, negative=False)
                    
                    # Selecting a subject related with the Selected Prof to lose this Relation
                    relations_choosed = prof_relations[selectedProf_Index[0]]
                    index_relation_choosed = randrange(len(relations_choosed))
                    relation_will_change_index = relations_choosed[index_relation_choosed]
                    
                    # Setting the flag to finish the while
                    flag_repair_done = True       
            
            # (2) 2 or more Subjects (related to the same Prof) with same 'quadri', 'day' and 'hour' in 'final_n_n'
            if(errorType==2):
                # Granting that the 'errorType' do not change good relations without restrictions to repair
                if(len(final_n_n)!=0):
                    # Choosing the relation to be modified
                    will_change_index = randrange(len(final_n_n))
                    relation_will_change_index = final_n_n[will_change_index]
                    
                    # Setting the flag to finish the while
                    flag_repair_done = True    

            # (3) 2 or more Subjects (related to the same Prof) with same 'day' but different 'campus' in 'final_s_s'    
            if(errorType==3):
                # Granting that the 'errorType' do not change good relations without restrictions to repair
                if(len(final_s_s)!=0):
                    # Choosing the relation to be modified
                    will_change_index = randrange(len(final_s_s))
                    relation_will_change_index = final_s_s[will_change_index]
                        
                    # Setting the flag to finish the while
                    flag_repair_done = True                
        
        # Choosing new Prof to be in the relation with the Subj selected
        subj, oldProf = relations[relation_will_change_index]
        change = randrange(len(prof))
        newProf = prof[change]
        # Granting that the new Prof is different of the old one
        while(oldProf==newProf):
            change = randrange(len(prof))
            newProf = prof[change]

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
            objectiveNum = int(pctRouletteCross*len(solutionsF.getList())/100)
            
            # Turning 'objectiveNum' to Even if it is Odd -> summing +1 to it only if the new 'objectiveNum' is not bigger then len(solutionsF)
            if(objectiveNum % 2 != 0):
                if((objectiveNum+1)<=len(solutionsF.getList())):
                    objectiveNum = objectiveNum + 1
                else:
                    objectiveNum = objectiveNum - 1

            # Granting that are solutions enough to became fathers (more than or equal 2)
            if(objectiveNum<2):
                # If have at most 2 solutions - all solutions will generate a child through mutation  
                for cand in solutionsF.getList():
                    newCand = self.mutationF(cand, prof)
                    solutionsNoPop.addCand(newCand)
                    
            # If we have at least 2 solutions, will have a Roulette Wheel with Reposition where the 'objectiveNum' of solutions will become Parents
            else:
                # Roulette Wheel
                fitnessList = [cand.getFitness() for cand in solutionsF.getList()]
                parentsSolFeas = self.rouletteWheel(solutionsF.getList(), fitnessList, objectiveNum, repos=True, negative=False)
                
                # Solutions 'children' created by crossover
                childSolFeas = []  
                # Make a Crossover (create two new candidates) for each pair of parents candidates randomly choose
                # Granting the number of children is equal of parents
                while(len(childSolFeas) != objectiveNum):                    
                    # If there are only 2 parents, make a crossover between them
                    if(len(parentsSolFeas)<=2):
                        parent1 = 0
                        parent2 = 1
                    
                    # If there are more then 2, choosing the parents Randomly  
                    else:
                        parent1 = randrange(len(parentsSolFeas))
                        parent2 = randrange(len(parentsSolFeas))
                        # Granting the second parent is not the same of first one
                        while(parent1==parent2):
                            parent2 = randrange(len(parentsSolFeas))
                    
                    # Making the Crossover with the selected parents
                    newCand1, newCand2 = self.crossoverF(parentsSolFeas[parent1], parentsSolFeas[parent2])
                   
                    # Removing used parents to make a new selection of Parents
                    parent2 = parentsSolFeas[parent2]
                    parentsSolFeas.remove(parentsSolFeas[parent1])
                    parentsSolFeas.remove(parent2)
                    
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
  
            if(prt==1): print("Feas. Offspring/", end='')
                        
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
        # Check if the Infeasible pop. is empty
        if(len(solutionsI.getList())!=0 or len(infPool.getList())!=0):
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
                # Roulette Wheel
                fitnessList = [cand.getFitness() for cand in infeasibles_List]
                newSolInf = self.rouletteWheel(infeasibles_List, fitnessList, numCand, repos=False, negative=True)  
                
                # Setting the new 'solutionsI' list to go to the next generation    
                solutionsI.setList(newSolInf)
                
            if(prt==1): print("Inf. Selection/", end='')
               
#==============================================================================================================            
    
    # Make a Selection of the best solutions from Feasible Pop.
    def selectionF(self, feaPool, solutionsF, numCand):
        # Check if the Feasible pop. is empty
        if(len(solutionsF.getList())!=0 or len(feaPool.getList())!=0):
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
            
            if(prt==1): print("Feas. Selection/", end='')

#==============================================================================================================            
           
    # Make selection of objects by Roulette Wheel
    def rouletteWheel(self, objectsList, valuesList, objectiveNum, repos=True, negative=False):
        # Num of objects will be selected: objectiveNum
        # Type of wheel (with reposition): repos
        # Since the value of Fitness is in the range of '-1' and '0' it is needed to be modified
        # Modifying the values to put it into a range of '0' and '1'
        # negative = True - modify de range of values

        # List with the selected Objects
        selectedObj = []
        # Flag tha allows to make all important calcs at least one time when the Roulette is with Reposition
        oneCalc = True

        while(len(selectedObj) < objectiveNum):         
            # Allow the Updating of the data for the next Roullete Round without the object that was recent selected on past round
            if(repos==False or oneCalc==True):
                # When the Roulette process does have reposition of objects 
                if(repos==True): oneCalc = False
                
                # Find the total Value of the Objects
                totalValue = 0.0
                for value in valuesList:
                    newValue = (1.0 if negative==True else 0.0) + value
                    totalValue = totalValue + newValue
                
                # Calculate the prob. of a selection for each object
                probObj = []
                for value in valuesList:
                    newValue = (1.0 if negative==True else 0.0) + value
                    p = float(newValue/totalValue)
                    probObj.append(p) 
                
                # Calculate a cumulative prob. for each object
                cumulative = 0.0
                cumulativeProbObj = []
                for q in probObj:
                    qNew = q + cumulative
                    cumulativeProbObj.append(qNew)
                    cumulative = qNew
            
            # MAIN Roulette Wheel Selection process (one round)    
            probPrev = 0.0
            index = 0
            r = float(randrange(100)/100.0)
            for q in cumulativeProbObj:
                if(probPrev < r and r <= q):
                    # Adding the selected Object to 'selectedObj'
                    selectedObj.append(objectsList[index])
                    if(repos==False):
                        # Removing the selected solution from 'valuesList'
                        valuesList.pop(index)
                    break
                probPrev = q    
                index = index + 1

        return  selectedObj
            
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
