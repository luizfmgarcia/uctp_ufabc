# UCTP Main Methods

from objects import *
from ioData import *
from random import *

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
        # If there are violated restrictions, will return a negative Fitness, if not, will return 1.0
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
        p_p = prof_relations.count([])
        
        # Searching, in each professor (one at a time), conflicts of schedules between subjects related to it
        for list_subj in prof_relations:
            # Check if the professor has more than 1 relation Prof-Subj to analyze
            if(len(list_subj)>1):
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
                        for j in next:
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
                                        if(campus_List[i]!=campus_List[k]):
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
            i1 = float(p_p)/(float(len(prof))-1.0)
            i2 = float(len(final_n_n))/float(len(subj))
            i3 = float(len(final_s_s))/float(len(subj))
            # Final Infeasible Function
            Fi = (-1.0)*(((w_alpha*i1)+(w_beta*i2)+(w_gamma*i3))/(w_alpha + w_beta + w_gamma))

            # Setting main variables of a Infeasible Candidate
            candidate.setInfVariables(prof_relations, final_n_n, final_s_s)
            
            # Returning the result calculated
            return Fi

        # If all Relations Prof-Subj in this Candidate passed through the restrictions
        candidate.setFeaVariables(prof_relations)
        return 1.0
        
#==============================================================================================================            
    
    # Calculate Fitness of Feasible Candidates 
    def calc_fitFeas(self, candidate, prof, subj, w_delta, w_omega, w_sigma, w_pi, w_rho):
        # This method looks for good Relations into the Candidate
        # These are the "Quality Amplifiers"
        # f1: how balanced is the distribution of Subjects, considering the "Charge" of each Professor (count the "Charge" of all Subj related to that Prof)
        # f2: how many and which Subjects are the professors preference, considering "prefSubj..." Lists
        # f3: how many Subjects are teach in a "Quadri" that is not the same of Professors 'quadriSabbath'
        # f4: how many Subjects are teach in the same "Period" of the Professor
        # f5: how many Subjects are teach in the same "Campus" of the Professor preference "prefCampus"
        
        # Auxiliary variables to main ones (f1, f2,...,f5) they have the Index related to "prof" list index
        # Use to all of them
        prof_relations = []
        prof_relations = candidate.getFeaVariables()
        
        # Use to f1
        # List of all 'Effective Charges', that is, the sum of the charges of all the subjects related to the professor
        charges_AllRelations = []
        # List of requested charges of each professor
        charges_EachProf = []
        
        # Use to f2
        # These are Lists of Lists, each Index is the same of Prof index 
        # In each List (inside the List) we have 1 if the same index Subject (from same Quadri Pref List) is related to Same Prof
        # or we have 0 if it is not related 
        q1_relations = []
        q2_relations = []
        q3_relations = []
        
        # Use to f3
        num_NotSameQuadriSab = []
        
        # Use to f4
        num_SamePeriod = []
        
        # Use to f5
        num_sameCampus = []
        
        # Initializing vectors
        i=0
        for i in range(len(prof)):
            charges_AllRelations.append(0)
            num_NotSameQuadriSab.append(0)
            num_SamePeriod.append(0)
            num_sameCampus.append(0)
            q1_relations.append([])
            q2_relations.append([])
            q3_relations.append([])
        
        # Initializing qX_relations Lists of Lists (in each one appends "pPrefSubjQXList" with "pPrefSubjLimList" to have the length of the subList)
        for relations in prof_relations:
            # Setting Index of actual Prof
            pIndex = prof_relations.index(relations)
            # Getting data of actual Prof
            pName, pPeriod, pCharge, pQuadriSabbath, pPrefCampus, pPrefSubjQ1List, pPrefSubjQ2List, pPrefSubjQ3List, pPrefSubjLimList = prof[pIndex].get()
            # Filling Q1 List of actual Prof
            j=0
            for j in range(len(pPrefSubjQ1List)+len(pPrefSubjLimList)):
                q1_relations[pIndex].append(0)
            
            # Filling Q2 List of actual Prof
            j=0
            for j in range(len(pPrefSubjQ2List)+len(pPrefSubjLimList)):
                q2_relations[pIndex].append(0)    
            
            # Filling Q3 List of actual Prof
            j=0
            for j in range(len(pPrefSubjQ3List)+len(pPrefSubjLimList)):
                q3_relations[pIndex].append(0) 
                    
        # Counting every type of occurrence, filling the vectors
        for relations in prof_relations:
            # Setting Index of actual Prof
            pIndex = prof_relations.index(relations)
            
            # Getting data of actual Prof
            pName, pPeriod, pCharge, pQuadriSabbath, pPrefCampus, pPrefSubjQ1List, pPrefSubjQ2List, pPrefSubjQ3List, pPrefSubjLimList = prof[pIndex].get()
            
            # Collecting each Professors Charge 
            charges_EachProf.append(int(pCharge))
            
            # All Relations of one Prof
            for subj_related in relations:
                # Setting Index of actual Subj
                sIndex = relations.index(subj_related)
                
                # Getting data of actual Subj
                sLevel, sCode, sName, sQuadri, sPeriod, sCampus, sCharge, sTimetableList = subj[sIndex].get()
                
                # Collecting and summing Subjects Charges related to same Prof
                charges_AllRelations[sIndex] = charges_AllRelations[sIndex] + float(str(sCharge).replace(",","."))
                
                # Adding to count if the Subj is not in the same 'pQuadriSabbath' (if Prof choose 'nenhum' he does not have a 'pQuadriSabbath')
                if(sQuadri!=pQuadriSabbath):
                    num_NotSameQuadriSab[sIndex] = num_NotSameQuadriSab[sIndex] + 1
                
                # Adding to count if the Subj is in the same 'pPeriod' of if Prof do not care about 'pPeriod' equal to 'NEGOCIAVEL'
                if(sPeriod==pPeriod or 'NEGOC' in pPeriod):
                    num_SamePeriod[sIndex] = num_SamePeriod[sIndex] + 1
                
                # Adding to count if the Subj is in the same 'pPrefCampus'
                if(sCampus==pPrefCampus):    
                    num_sameCampus[sIndex] = num_sameCampus[sIndex] + 1
                
                # Finding the Subject 'sName' in "pPrefSubjQ1List+pPrefSubjLimList" list
                list = pPrefSubjQ1List+pPrefSubjLimList
                # Checking if the List is not empty
                if(len(list)>0):
                    try:
                        index_value = list.index(sName)
                    except ValueError:
                        index_value = -1
                    # If the Subj name appears in the list
                    if(index_value!=-1):
                        # Putting '1' in same position found 'index_value' in the subList (which this one, is in same position of prof) 
                        subList = q1_relations[pIndex]
                        subList[index_value] = 1
                        # Updating the subList in 'q1_relations' List 
                        q1_relations[pIndex] = subList
                
                # Finding the Subject 'sName' in "pPrefSubjQ2List+pPrefSubjLimList" list
                list = pPrefSubjQ2List+pPrefSubjLimList
                # Checking if the List is not empty
                if(len(list)>0):
                    try:
                        index_value = list.index(sName)
                    except ValueError:
                        index_value = -1
                    # If the Subj name appears in the list
                    if(index_value!=-1):
                        # Putting '1' in same position found 'index_value' in the subList (which this one, is in same position of prof) 
                        subList = q2_relations[pIndex]
                        subList[index_value] = 1
                        # Updating the subList in 'q2_relations' List 
                        q2_relations[pIndex] = subList
                
                # Finding the Subject 'sName' in "pPrefSubjQ3List+pPrefSubjLimList" list
                list = pPrefSubjQ3List+pPrefSubjLimList
                # Checking if the List is not empty
                if(len(list)>0):
                    try:
                        index_value = list.index(sName)
                    except ValueError:
                        index_value = -1
                    # If the Subj name appears in the list    
                    if(index_value!=-1):
                        # Putting '1' in same position found 'index_value' in the subList (which this one, is in same position of prof) 
                        subList = q3_relations[pIndex]
                        subList[index_value] = 1
                        # Updating the subList in 'q1_relations' List 
                        q3_relations[pIndex] = subList
                
        # Calculating intermediate variables
        
        # For f1
        # Relative weigh of excess or missing charge for each Prof
        charges_relative = []
        
        # Initializing vector
        for p in range(len(prof)):
            charges_relative.append(0.0)
            
        # Calculating and filling vector
        for pCharge in charges_EachProf:
            # Setting Index of actual Prof
            actual_index = charges_EachProf.index(pCharge)
            # Finding relative charge based on the credit difference module between the credits requested by the Prof and the sum off all Subj related to it
            charges_relative[actual_index] = abs(float(pCharge) - float(charges_AllRelations[actual_index]))/float(pCharge)
        
        # The arithmetic average of charge discrepancies of all professors;  
        u_u = 0.0
        # Calculating the value
        for charge in charges_relative:
            u_u = u_u + float(charge)
        
        # Normalizing value    
        u_u = u_u/float(len(prof))
             
        # For f2
        # Lists of the calculation of "satisfaction" based on the order of Subjects choose by a Professor (index = 0 has more weight)
        finalQ1 = []
        finalQ2 = []
        finalQ3 = []
        
        
        # Calculating the Satisfaction from Q1 relations for all Professors
        for list_choice_relation in q1_relations:
            # Setting actual Prof Index and actual List Relations-Preference
            prof_index = q1_relations.index(list_choice_relation)
            len_actual_list = len(list_choice_relation)
            
            # Initialing actual position and total weight that will be calculated next
            finalQ1.append(0.0)
            total_weight = 0
            
            # Checking if the Relations-Preference List is empty
            if(len_actual_list == 0):
                finalQ1[prof_index] = 1.0
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
                        finalQ1[prof_index] = finalQ1[prof_index] + (float(len_actual_list)-float(pref_index)+1.0)
                
                # Calculate the final value of "Satisfaction" normalized, after obtained and summed all weights from Subjects related to actual professor
                finalQ1[prof_index] = float(finalQ1[prof_index])/float(total_weight)        
        
        # Calculating the Satisfaction from Q2 relations for all Professors
        for list_choice_relation in q2_relations:
            # Setting actual Prof Index and actual List Relations-Preference
            prof_index = q2_relations.index(list_choice_relation)
            len_actual_list = len(list_choice_relation)
            
            # Initialing actual position and total weight that will be calculated next
            finalQ2.append(0.0)
            total_weight = 0
            
            # Checking if the Relations-Preference List is empty
            if(len_actual_list == 0):
                finalQ2[prof_index] = 1.0
            # It is needed to be calculate (is not empty)
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
                        finalQ2[prof_index] = finalQ2[prof_index] + (float(len_actual_list)-float(pref_index)+1.0)
                
                # Calculate the final value of "Satisfaction" normalized, after obtained and summed all weights from Subjects related to actual professor
                finalQ2[prof_index] = float(finalQ2[prof_index])/float(total_weight)
        
        # Calculating the Satisfaction from Q3 relations for all Professors
        for list_choice_relation in q3_relations:
            # Setting actual Prof Index and actual List Relations-Preference
            prof_index = q3_relations.index(list_choice_relation)
            len_actual_list = len(list_choice_relation)
            
            # Initialing actual position and total weight that will be calculated next
            finalQ3.append(0.0)
            total_weight = 0
            
            # Checking if the Relations-Preference List is empty
            if(len_actual_list == 0):
                finalQ3[prof_index] = 1.0
            # It is needed to be calculate (is not empty)
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
                        finalQ3[prof_index] = finalQ3[prof_index] + (float(len_actual_list)-float(pref_index)+1.0)
                
                # Calculate the final value of "Satisfaction" normalized, after obtained and summed all weights from Subjects related to actual professor
                finalQ3[prof_index] = float(finalQ3[prof_index])/float(total_weight)
        
        # Calculate the final value of a Prof "satisfaction" summing all 3 values (from finalQ1, finalQ2 and finalQ3 lists) and normalizing it
        final_Satisf = []
        for i in range(len(finalQ3)):
            final_Satisf.append((finalQ1[i]+finalQ2[i]+finalQ3[i])/3.0)
        
        # Finally, calculating all Professors Satisfaction summing all final values    
        m_m = 0.0
        for value in final_Satisf:
            m_m = m_m + value
        
        # For f3
        s_s = 0
        for value in num_NotSameQuadriSab:
            s_s = s_s + value
        
        # For f4
        t_t = 0
        for value in num_SamePeriod:
            t_t = t_t + value
            
        # For f5
        c_c = 0
        for value in num_sameCampus:
            c_c = c_c + value
            
        # Calculating main variables
        f1 = 1.0 - u_u
        f2 = float(m_m)/float(len(prof))
        f3 = float(s_s)/float(len(subj)) 
        f4 = float(t_t)/float(len(subj)) 
        f5 = float(c_c)/float(len(subj)) 
        
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
                
            if(prt==1): print("Inf. Offspring/", end='')
        
#==============================================================================================================            
    
    # Make a mutation into a solution
    def mutationI(self, candidate, prof, subj):
        # (0) No repair
        # (1) Prof without relations with Subjects in 'prof_relations'
        # (2) 2 or more Subjects (related to the same Prof) with same 'quadri', 'day' and 'hour' in 'final_n_n'
        # (3) 2 or more Subjects (related to the same Prof) with same 'day' but different 'campus' in 'final_s_s'
        
        # Getting data to work with
        relations = candidate.getList()
        prof_relations, final_n_n, final_s_s = candidate.getInfVariables()
        
        # This While ensures that 'errorType' will choose Randomly one 'restriction repair'
        flag_repair_done = False   
        while(flag_repair_done == False):
            # Choosing one type of restriction repair
            errorType = randrange(1,4)
            
            if(errorType==0):
                # Do not granting that the 'errorType' do not change good relations without restrictions to repair
                # Choosing the relation to be modified
                relation_will_change_index = randrange(len(subj))
                
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

            elif(errorType==1):
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
                        
                    # Find the total Number of Relations of the population (has to be the same of the number of Subjects)
                    totalRelations = 0.0
                    for w in Weights:
                        totalRelations = totalRelations + w
                        
                    if(totalRelations != float(len(subj))):
                        print("Error! Number of relation different of number of Subjects.")   
                    
                    # Calculate the prob. of a selection for each prof
                    probList = []
                    for w in Weights:
                        p = float(w/totalRelations)
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
        
        #print(prof_relations.count([]),len(final_n_n), len(final_s_s))
        #print(final_n_n, final_s_s)

        return newCand
        
#==============================================================================================================            
                 
    # Generate new solutions from the current Feasible population
    def offspringF(self, solutionsNoPop, solutionsF, prof, subj, pctMut, pctRouletteCross, numCand):
        # Check if the Feasible pop. is empty
        if(len(solutionsF.getList())!=0):
            # 'objectiveNum': number of solutions to become parents - based on 'pctRouletteCross'
            objectiveNum = (pctRouletteCross*len(solutionsF.getList())/100)
            
            # Turning 'objectiveNum' to Even if it is Odd -> summing +1 to it only if the new 'objectiveNum' is not bigger then len(solutionsF)
            if(objectiveNum % 2 != 0):
                if((objectiveNum+1)<=len(solutionsF.getList())):
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
                while(len(parentsSolFeas) != objectiveNum):
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
                while(len(childSolFeas) != objectiveNum):                    
                    # If there are only 2 parents, make a crossover between them
                    if(len(parentsSolFeas)<=2):
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
        if(len(solutionsI.getList())!=0):
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
                
            if(prt==1): print("Inf. Selection/", end='')
               
#==============================================================================================================            
    
    # Make a Selection of the best solutions from Feasible Pop.
    def selectionF(self, feaPool, solutionsF, numCand):
        # Check if the Feasible pop. is empty
        if(len(solutionsF.getList())!=0):
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
