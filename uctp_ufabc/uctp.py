# UCTP Main Methods

import objects
import ioData
import random

# Set '1' to allow, during the run, the print on terminal of some steps
prt = 0

#==============================================================================================================

class UCTP:

#==============================================================================================================

    # Create the first generation of solutions
    def start(self, solutionsNoPop, subj, prof, init):
        if(prt == 1): print("Creating first generation...", end='')
        for _ in range(init): solutionsNoPop.addCand(self.newCandRand(subj, prof))
        if(prt == 1): print("Created first generation!")
        #printAllCand(solutions)

#==============================================================================================================

    # Create new Candidate Full-Random
    def newCandRand(self, subj, prof):
        candidate = objects.Candidate()
        # Follow the subjects in 'subj' list, in order, and for each one, choose a professor randomly
        for sub in subj: candidate.addRelation(sub, prof[random.randrange(len(prof))])
        return candidate

#==============================================================================================================

    # Extracts info about what Subj appears in which Prof (PrefList)
    def extractSubjIsPref(self, subj, prof):
        # Lists for each Prof, where it is '1' if Subj in respective index is on Prof List of Pref
        subjIsPref = [[0 for _ in range(len(subj))] for _ in range(len(prof))]

        # Counting the occurrences, filling the vectors
        for pIndex in range(len(prof)):
            # Getting data of current Prof
            _, _, _, _, _, pPrefSubjQ1List, pPrefSubjQ2List, pPrefSubjQ3List, pPrefSubjLimList = prof[pIndex].get()
            prefSubjLists = [pPrefSubjQ1List, pPrefSubjQ2List, pPrefSubjQ3List, pPrefSubjLimList]
            
            # All Relations of one Prof
            for sIndex in range(len(subj)):
                # Getting data of current Subj
                _, _, sName, sQuadri, _, _, _, _ = subj[sIndex].get()
                
                # For each quadri
                for i in range(3):
                    # Finding the Subject 'sName' in "pPrefSubjQXList+pPrefSubjLimList" list
                    sumList = prefSubjLists[i] + prefSubjLists[3]
                    # Checking if the List is not empty
                    if(len(sumList) > 0):
                        try: index_value = sumList.index(sName)
                        except ValueError: index_value = -1
                        # If the Subj name appears in the list
                        if(index_value != -1):
                            # Looking for only in the list of respective quadri of current Subject in analisys
                            if(str(i+1) in sQuadri):
                                # Informing that the Subj appears on respective Prof-QuadriPrefList
                                subjIsPref[pIndex][sIndex] = 2
                            # Informing that the Subj appears on other Prof-QuadriPrefList that is not same Quadri
                            else: subjIsPref[pIndex][sIndex] = 1
        
        return subjIsPref

#==============================================================================================================
    
    # Separation of solutions into 2 populations
    def twoPop(self, solutionsNoPop, solI, solF, prof, subj, weights):
        # Granting that the Lists will be empty to receive new Solutions
        solI.resetList()
        solF.resetList()
        
        for cand in solutionsNoPop.getList():
            # Classification by checking feasibility
            pop = self.checkFeasibility(cand, prof, subj, weights)
            if(pop == "feasible"): solF.addCand(cand)
            elif(pop == "infeasible"): solI.addCand(cand)
        
        # Granting that the List will be empty to next operations
        solutionsNoPop.resetList()
        
        if(prt == 1): print("Checked Feasibility (new Candidates)/", end='')

#==============================================================================================================
    
    # Detect the violation of a Restriction into a candidate
    def checkFeasibility(self, candidate, prof, subj, weights):
        # As part of the Candidate's Prof-Subj relations (with both Feasible and the Infeasible) will be traversed to check they Feasibility here,
        # instead of repass an entire Infeasible Candidate again in the 'calc_fitInfeas', the calculation of its Fitness will already be done
        # only one time here. Only the Feasible ones will have to pass through 'calc_fitFeas' later.
        fit = -1
        fit = self.calc_fitInfeas(candidate, prof, subj, weights[0], weights[1], weights[2])
        if(fit < 0):
            candidate.setFitness(fit)
            return "infeasible"
        return "feasible"

#==============================================================================================================
   
    # Calculate the Fitness of the candidate
    def calcFit(self, infeasibles, feasibles, prof, subj, weights):
        # All Infeasible Candidates - is here this code only for the representation of the default/original algorithm`s work
        # The Inf. Fitness calc was already done in 'checkFeasibility()' method
        # Check if the Infeasible pop. is empty
        if(len(infeasibles.getList()) != 0):
            for cand in infeasibles.getList():
                if(cand.getFitness() == 0.0):
                    # Setting the Fitness with the return of calc_fitInfeas() method
                    cand.setFitness(self.calc_fitInfeas(cand, prof, subj, weights[0], weights[1], weights[2]))
            if(prt == 1): print("Fitness of all Inf./", end='')
        
        # All Feasible Candidates
        # Check if the Feasible pop. is empty
        if(len(feasibles.getList()) != 0):
            for cand in feasibles.getList():
                if(cand.getFitness() == 0.0):
                    # Setting the Fitness with the return of calc_fitFeas() method
                    cand.setFitness(self.calc_fitFeas(cand, prof, subj, weights[3], weights[4], weights[5], weights[6], weights[7]))
            if(prt == 1): print("Fitness of all Feas./", end='')
        
#==============================================================================================================
    
    # Calculate Fitness of Infeasible Candidates
    def calc_fitInfeas(self, candidate, prof, subj, w_alpha, w_beta, w_gamma):
        # Getting information about the Candidate
        prof_relations = self.i1(candidate, prof, subj)
        conflicts_i2, conflicts_i3 = self.i2_i3(prof_relations, subj)
        
        # Setting found variables
        candidate.setInfVariables(prof_relations, conflicts_i2, conflicts_i3)

        # Checking if occurred violations of restrictions on the Candidate
        # If there are violated restrictions, this Cadidate is Infeasible and then will calculate and return a negative Fitness,
        # if not, is Feasible, will return 1.0 as Fitness
        if(prof_relations.count([]) != 0 or conflicts_i2.count([]) != len(conflicts_i2) or conflicts_i3.count([]) != len(conflicts_i3)):
            # Calculating main variables
            i1 = float(prof_relations.count([])) / (float(len(prof)) - 1.0)
            i2 = float(sum([len(i) for i in conflicts_i2])) / float(len(subj))
            i3 = float(sum([len(i) for i in conflicts_i3])) / float(len(subj))
            
            # Final Infeasible Function Fitness Calc
            Fi = (-1.0) * (((w_alpha * i1) + (w_beta * i2) + (w_gamma * i3)) / (w_alpha + w_beta + w_gamma))
            
            # Returning the calculated result
            return Fi

        # If all Relations Prof-Subj in this Candidate passed through the restrictions)
        return 1.0

    #-------------------------------------------------------
    
    # i1: penalty to how many Professors does not have at least one relation with a Subject
    def i1(self, candidate, prof, subj):
        # List of lists of Subjects that are related to the same Professor, where the position in this list is the same of the same professor in 'prof' list
        # Empty list in this list means that some Professor (p) does not exists on the Candidate
        prof_relations = [[] for _ in range(len(prof))]
        
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
        conflicts_i2, conflicts_i3 = [[] for _ in range(len(prof_relations))], [[] for _ in range(len(prof_relations))]
        
        # Searching, in each professor (one at a time), conflicts of schedules between subjects related to it
        for list_subj in prof_relations:
            # Current Prof in analisys
            profIndex = prof_relations.index(list_subj)

            # Check if the professor has more than 1 relation Prof-Subj to analyze
            if(len(list_subj) > 1):
                # Getting the data of all Subjects related to current Professor in analysis
                subj_Data = [subj[i].get() for i in list_subj]
                timetableList_List = [sTimetableList for _, _, _, _, _, _, _, sTimetableList in subj_Data]
                quadri_List = [sQuadri for _, _, _, sQuadri, _, _, _, _ in subj_Data]
                campus_List = [sCampus for _, _, _, _, _, sCampus, _, _ in subj_Data]
                period_List = [sPeriod for _, _, _, _, sPeriod, _, _, _ in subj_Data]
                
                # Comparing the data of one Subject (i) with all next subjects listed, and do the same with next ones
                i = 0
                for timeTable in timetableList_List:
                    # all [day/hour/frequency] of the Timetable of the Subject (i) in 'timetableList_List'
                    i_day = [j[0] for j in timeTable]
                    i_hour = [j[1] for j in timeTable]
                    i_frequency = [j[2] for j in timeTable]

                    # Now, comparing current (i) subject data with next ones (k), one at a time
                    k = i + 1
                    rest = timetableList_List[k:]
                    # repeat this 'len(rest)' times
                    for nextK in rest:
                        # Alredy check if both Subj (i, k) is on same Quadri
                        if(quadri_List[i] == quadri_List[k]):
                            # Variables that flags if a conflict was already detected (do not count 2 or more times same 2 subjects in conflict)
                            verified_i2, verified_i3 = False, False
                            # all [day/hour/frequency] of the Timetable of the Subject (k) in 'timetableList_List'
                            inext_day = [j[0] for j in nextK]
                            inext_hour = [j[1] for j in nextK]
                            inext_frequency = [j[2] for j in nextK]
                            
                            # Finally comparing one-to-one timetables - between i and k subjects
                            for a in i_day:
                                for b in inext_day:
                                    if(a == b):
                                        # There is, at least, two subjects teach in the same day and quadri, but in different campus
                                        if(campus_List[i] != campus_List[k]):
                                            if(verified_i3 == False):
                                                conflicts_i3[profIndex].append(list_subj[i])
                                                conflicts_i3[profIndex].append(list_subj[k])
                                                verified_i3 = True

                                        # There is, at least, two subjects teach in the same day, hour and quadri
                                        # First check if they have the same Period
                                        if(period_List[i] == period_List[k] and i_hour[i_day.index(a)] == inext_hour[inext_day.index(b)]):
                                            # if one 'frequency' is "QUINZENAL I" and the other is "QUINZENAL II" then DO NOT count
                                            if('SEMANAL' in i_frequency[i_day.index(a)] or 'SEMANAL' in inext_frequency[inext_day.index(b)]):
                                                if(verified_i2 == False):
                                                    conflicts_i2[profIndex].append(list_subj[i])
                                                    conflicts_i2[profIndex].append(list_subj[k])
                                                    #print(subj[list_subj[i]].get(), subj[list_subj[k]].get(), '\n')
                                                    verified_i2 = True
                                            elif('QUINZENAL I' in i_frequency[i_day.index(a)] and 'QUINZENAL I' in inext_frequency[inext_day.index(b)]):
                                                if(verified_i2 == False):
                                                    conflicts_i2[profIndex].append(list_subj[i])
                                                    conflicts_i2[profIndex].append(list_subj[k])
                                                    #print(subj[list_subj[i]].get(), subj[list_subj[k]].get(), '\n')
                                                    verified_i2 = True
                                            elif('QUINZENAL II' in i_frequency[i_day.index(a)] and 'QUINZENAL II' in inext_frequency[inext_day.index(b)]):
                                                if(verified_i2 == False):
                                                    conflicts_i2[profIndex].append(list_subj[i])
                                                    conflicts_i2[profIndex].append(list_subj[k])
                                                    #print(subj[list_subj[i]].get(), subj[list_subj[k]].get(), '\n')
                                                    verified_i2 = True
                        # Going to the next Subject (k+1) to compare with the same, current, main, Subject (i)
                        k = k + 1
                    # Going to the next Subject (i+1) related to the same Professor
                    i = i + 1
        
        # Removing from 'conflicts_i2' and 'conflicts_i3' duplicates
        final_i2 = [[] for _ in range(len(prof_relations))]
        final_i3 = [[] for _ in range(len(prof_relations))]
        for i in range(len(prof_relations)):
            for j in conflicts_i2[i]:
                if(final_i2[i].count(j) == 0): final_i2[i].append(j)
            for j in conflicts_i3[i]:
                if(final_i3.count(j) == 0): final_i3[i].append(j)
        
        return final_i2, final_i3

#==============================================================================================================

    # Calculate Fitness of Feasible Candidates
    def calc_fitFeas(self, candidate, prof, subj, w_delta, w_omega, w_sigma, w_pi, w_rho):
        
        prof_relations, _, _, _, _, _ = candidate.getFeaVariables()
        
        # Looking for good Relations into the Candidate using "Quality Amplifiers"
        # Getting information about the Candidate
        sum_chargesRelative, difCharge = self.f1(subj, prof, prof_relations)
        sum_Satisfaction, subjPref = self.f2(subj, prof, prof_relations)
        sum_quadSabbNotPref, quadSabbNotPref = self.f3(subj, prof, prof_relations)
        sum_periodPref, periodPref = self.f4(subj, prof, prof_relations)
        sum_campusPref, campusPref = self.f5(subj, prof, prof_relations)

        # Setting found variables
        candidate.setFeaVariables(prof_relations, subjPref, periodPref, quadSabbNotPref, campusPref, difCharge)
        
        # Calculating main variables
        f1 = 1.0 - (float(sum_chargesRelative) / float(len(prof)))
        f2 = float(sum_Satisfaction) / float(len(prof))
        f3 = float(sum_quadSabbNotPref) / float(len(subj))
        f4 = float(sum_periodPref) / float(len(subj))
        f5 = float(sum_campusPref) / float(len(subj))
        
        # Final Feasible Function Fitness Calc
        Ff = ((w_delta * f1) + (w_omega * f2) + (w_sigma * f3) + (w_pi * f4) + (w_rho * f5)) / (w_delta + w_omega + w_sigma + w_pi + w_rho)
        
        # Returning the result calculated
        return Ff
    
    #-------------------------------------------------------
    
    # f1: how balanced is the distribution of Subjects, considering the "Charge" of each Professor and its Subj related
    def f1(self, subj, prof, prof_relations):
        # List of all 'Effective Charges', that is, the sum of the charges of all the subjects related to the professor
        charges_eachProfRelations = [0 for _ in range(len(prof))]
        # List of requested charges of each professor
        prof_data = [prof[i].get() for i in range(len(prof))]
        charges_EachProf = [float(pCharge) for _, _, pCharge, _, _, _, _, _, _ in prof_data]

        # Counting the occurrences, filling the vectors
        for i in range(len(prof_relations)):
            # Getting data of current Subj related to this pIndex Prof
            subj_data = [subj[sIndex].get() for sIndex in prof_relations[i]]
            # Summing all chagers of all relations of this Prof
            charges_eachProfRelations[i] = sum([float(str(sCharge).replace(",",".")) for _, _, _, _, _, _, sCharge, _ in subj_data])
        
        # Difference of Prof Charge and the sum of all of its Subj-Relations
        difCharge = [charges_EachProf[i] - charges_eachProfRelations[i] for i in range(len(prof))]

        # Relative weigh of excess or missing charge for each Prof - based on the credit difference module
        # between the credits requested by the Prof and the sum off all Subj related to it
        charges_relative = [float(abs(difCharge[i])) / charges_EachProf[i] for i in range(len(prof))]
        
        # Making a simple adjust on the value
        charges_relativeFinal = [charge if charge < 1.0 else 1.0 for charge in charges_relative]
        
        # The sum of charge discrepancies of all professors
        sum_chargesRelative = sum([charge for charge in charges_relativeFinal])
        
        return sum_chargesRelative, difCharge

    #-------------------------------------------------------
    
    # f2: how many and which Subjects are the professors preference, considering "prefSubj..." Lists
    def f2(self, subj, prof, prof_relations):
        # These are Lists (each quadri - 3) of Lists (each professor) of Lists (each PrefList+LimList)
        # In each List (inside the List inside the List) we have 1 if the same index Subject (from same Quadri X Pref List + Lim Pref List) is related to Same Prof
        # or we have 0 if it is not related
        qX_relations = [[[] for _ in range(len(prof))] for _ in range(3)]

        # List with the number of subjects that are on respective Prof's List of Preferences
        subjPref = [0 for _ in range(len(prof))]

        # Initializing qX_relations Lists of Lists (in each one appends "pPrefSubjQXList" with "pPrefSubjLimList" to have the length of the subList)
        for relations in prof_relations:
            # Setting Index of current Prof
            pIndex = prof_relations.index(relations)
            
            # Getting data of current Prof
            _, _, _, _, _, pPrefSubjQ1List, pPrefSubjQ2List, pPrefSubjQ3List, pPrefSubjLimList = prof[pIndex].get()
            prefSubjLists = [pPrefSubjQ1List, pPrefSubjQ2List, pPrefSubjQ3List, pPrefSubjLimList]
            
            # For each Quadri - Filling QX Lists of current Prof
            for i in range(3):
                qX_relations[i][pIndex] = [0 for _ in range(len(prefSubjLists[i]) + len(prefSubjLists[3]))]
        
        # Counting the occurrences, filling the vectors
        for relations in prof_relations:
            # Setting Index of current Prof
            pIndex = prof_relations.index(relations)
            
            # Getting data of current Prof
            _, _, _, _, _, pPrefSubjQ1List, pPrefSubjQ2List, pPrefSubjQ3List, pPrefSubjLimList = prof[pIndex].get()
            prefSubjLists = [pPrefSubjQ1List, pPrefSubjQ2List, pPrefSubjQ3List, pPrefSubjLimList]
            
            # All Relations of one Prof
            for sIndex in relations:
                # Getting data of current Subj
                _, _, sName, sQuadri, _, _, _, _ = subj[sIndex].get()
                
                # For each quadri
                for i in range(3):
                    # Looking for only in the list of respective quadri of current Subject in analisys
                    if(str(i+1) in sQuadri):
                        # Finding the Subject 'sName' in "pPrefSubjQXList+pPrefSubjLimList" list
                        sumList = prefSubjLists[i] + prefSubjLists[3]
                        # Checking if the List is not empty
                        if(len(sumList) > 0):
                            try: index_value = sumList.index(sName)
                            except ValueError: index_value = -1
                            # If the Subj name appears in the list
                            if(index_value != -1):
                                # Putting '1' in same position found 'index_value' in the subList (which this one, is in same position of prof)
                                qX_relations[i][pIndex][index_value] = 1
                                # Adding the Subj that is on Prof Pref List
                                subjPref[pIndex] = subjPref[pIndex] + 1
            
        # Calculating intermediate variables
        # Lists of the calculation of "satisfaction" based on the order of Subjects choose by a Professor (index = 0 has more weight)
        finalQX = [[0.0 for _ in range(len(prof))] for _ in range(3)]
        
        # For each Qaudri
        for i in range(3):
            # Calculating the Satisfaction from QX relations for each Professor
            for list_choice_relation in qX_relations[i]:
                # Setting current Prof Index and current List Relations-Preference
                prof_index = qX_relations[i].index(list_choice_relation)
                len_current_list = len(list_choice_relation)
                
                # Initializing current position and total weight that will be calculated next
                total_weight = 0
                
                # Checking if the Relations-Preference List is empty
                if(len_current_list == 0): finalQX[i][prof_index] = 1.0
                # If is needed to be calculated (is not empty)
                else:
                    # QX Relations of each Professor
                    for h in list_choice_relation:
                        # Setting current Subject Preference Position
                        pref_index = list_choice_relation.index(h)
                        # Summing the Total Weight of this list of preferences to normalize later (+1 because first index is 0)
                        total_weight = total_weight + pref_index + 1
                        
                        # If the current Subj, in this specific position on the Preference List of current Prof, is related to it
                        if(h == 1):
                            # Summing the respective weight the Subj has in the Prof List of Preferences
                            finalQX[i][prof_index] = finalQX[i][prof_index] + (len_current_list - pref_index + 1)
                    
                    # Calculate the final value of "Satisfaction" normalized, after obtained and summed all weights from Subjects related to current professor
                    finalQX[i][prof_index] = float(finalQX[i][prof_index]) / float(total_weight)
        
        # Calculate the final value of a Prof "satisfaction" summing all 3 values (from finalQ1, finalQ2 and finalQ3 lists) and normalizing it
        final_Satisf = [float((finalQX[0][i] + finalQX[1][i] + finalQX[2][i]) / 3.0) for i in range(len(finalQX[0]))]
        
        # Finally, calculating all Professors Satisfaction summing all final values
        sum_Satisfaction = sum([value for value in final_Satisf])
        
        return sum_Satisfaction, subjPref
    
    #-------------------------------------------------------
    
    # f3: how many Subjects are teach in a "Quadri" that is not the same of Professors 'quadriSabbath'
    def f3(self, subj, prof, prof_relations):
        quadSabbNotPref = [0 for _ in range(len(prof))]

        # Counting the occurrences, filling the vector
        for i in range(len(prof_relations)):
            # Getting data of current Prof
            _, _, _, pQuadriSabbath, _, _, _, _, _ = prof[i].get()
            
            # All Relations of one Prof
            for sIndex in prof_relations[i]:
                # Getting data of current Subj
                _, _, _, sQuadri, _, _, _, _ = subj[sIndex].get()
                # Adding to count if the Subj is not in the same 'pQuadriSabbath' (if Prof choose 'nenhum' he does not have a 'pQuadriSabbath')
                if('NENHUM' in pQuadriSabbath or sQuadri != pQuadriSabbath): quadSabbNotPref[i] = quadSabbNotPref[i] + 1
            
        # Calculating intermediate variable
        sum_quadSabbNotPref = sum([value for value in quadSabbNotPref])

        return sum_quadSabbNotPref, quadSabbNotPref

    #-------------------------------------------------------
    
    # f4: how many Subjects are teach in the same "Period" of the Professor preference "pPeriod"
    def f4(self, subj, prof, prof_relations):
        periodPref = [0 for _ in range(len(prof))]

        # Counting the occurrences, filling the vector
        for i in range(len(prof_relations)):
            # Getting data of current Prof
            _, pPeriod, _, _, _, _, _, _, _ = prof[i].get()
            
            # All Relations of one Prof
            for sIndex in prof_relations[i]:
                # Getting data of current Subj
                _, _, _, _, sPeriod, _, _, _ = subj[sIndex].get()
                # Adding to count if the Subj is in the same 'pPeriod' or if Prof do not care about 'pPeriod' equal to 'NEGOCIAVEL'
                if('NEGOCI' in pPeriod or sPeriod == pPeriod): periodPref[i] = periodPref[i] + 1
            
        # Calculating intermediate variable
        sum_periodPref = sum([value for value in periodPref])
        
        return sum_periodPref, periodPref
    
    #-------------------------------------------------------
    
    # f5: how many Subjects are teach in the same "Campus" of the Professor preference "prefCampus"
    def f5(self, subj, prof, prof_relations):
        campusPref = [0 for _ in range(len(prof))]

        # Counting the occurrences, filling the vector
        for i in range(len(prof_relations)):
            # Getting data of current Prof
            _, _, _, _, pPrefCampus, _, _, _, _ = prof[i].get()
            
            # All Relations of one Prof
            for sIndex in prof_relations[i]:
                # Getting data of current Subj
                _, _, _, _, _, sCampus, _, _ = subj[sIndex].get()
                # Adding to count if the Subj is in the same 'pPrefCampus'
                if(sCampus == pPrefCampus): campusPref[i] = campusPref[i] + 1
        
        # Calculating intermediate variable
        sum_campusPref = sum([value for value in campusPref])

        return sum_campusPref, campusPref

#==============================================================================================================

    # Generate new solutions from the current Infeasible population
    def offspringI(self, solutionsNoPop, solutionsI, prof, subj):
        # Check if the Infeasible pop. is empty
        if(len(solutionsI.getList()) != 0):
            # Make a Mutation for each candidate, trying to repair a restriction problem maker
            for cand in solutionsI.getList():
                newCand = self.mutationI(cand, prof, subj)
                # Adding the new Candidate generated by Mutation to 'solutionsNoPop'
                solutionsNoPop.addCand(newCand)

            if(prt == 1): print("Inf. Offspring/", end='')
    
#==============================================================================================================

    # Make a mutation into a solution
    def mutationI(self, candidate, prof, subj):
        # Getting data to work with
        relations = candidate.getList()
        prof_relations, conflicts_i2, conflicts_i3 = candidate.getInfVariables()
        
        # This While ensures that 'errorType' will choose Randomly one 'restriction repair'
        flag_repair_done = False
        while(flag_repair_done == False):
            # Choosing one type of restriction to repair
            errorType = random.randrange(0,4)
            #errorType = 0
            # (0) No repair -> Random Change
            if(errorType == 0):
                # Do NOT granting that the 'errorType' do not change good relations without restrictions to repair
                #newCand = self.mutationRand(candidate, prof)
                # Roulette Wheel - more relations -> more weight
                numRelationsList = [float(len(prof_relations[i])) for i in range(len(prof_relations))]
                selected, _, _ = self.rouletteWheel(prof_relations, numRelationsList, objectiveNum=1, repos=True, negative=False)
                will_change_index = random.randrange(len(selected[0]))
                relation_will_change_index = selected[0][will_change_index]
                
                # Choosing new Prof to be in the relation with the Subj selected
                subj, oldProf = relations[relation_will_change_index]

                # Granting that the new Prof is different of the old one
                newProf = oldProf
                while(oldProf == newProf):
                    # Finding randomly a new Prof
                    change = random.randrange(len(prof))
                    newProf = prof[change]
                
                # Setting the new relation, creating new Candidate and returning it
                relations[relation_will_change_index]=[subj,newProf]
                newCand = objects.Candidate()
                newCand.setList(relations)    
                # Setting the flag to finish the while
                flag_repair_done = True

            # (1) Prof without relations with Subjects in 'prof_relations'
            if(errorType == 1):
                # Granting that the 'errorType' do not change good relations without restrictions to repair
                if(prof_relations.count([]) != 0):
                    # Creating a list with only the index of Prof without Relations and an other one only with Prof with Relations
                    prof_Zero_Relations, prof_With_Relations = [], []

                    for p in prof_relations:
                        if(len(p) == 0): prof_Zero_Relations.append(prof_relations.index(p))
                        else: prof_With_Relations.append(prof_relations.index(p))
                    
                    # Roulette Wheel - more relations -> more weight 
                    numRelationsList = [float(len(prof_relations[p])) for p in prof_With_Relations]
                    selectedProf_Index, _, _ = self.rouletteWheel(prof_With_Relations, numRelationsList, objectiveNum=1, repos=True, negative=False)
                    
                    # Selecting a subject related with the Selected Prof to lose this Relation
                    relations_choosed = prof_relations[selectedProf_Index[0]]
                    index_relation_choosed = random.randrange(len(relations_choosed))
                    relation_will_change_index = relations_choosed[index_relation_choosed]
                    
                    # Choosing one Prof to be included in one relation
                    subj, oldProf = relations[relation_will_change_index]
                    change_index = random.randrange(len(prof_Zero_Relations))
                    change = prof_Zero_Relations[change_index]
                    newProf = prof[change]

                    # Setting the new relation, creating new Candidate and returning it
                    relations[relation_will_change_index]=[subj,newProf]
                    newCand = objects.Candidate()
                    newCand.setList(relations)

                    # Setting the flag to finish the while
                    flag_repair_done = True
            
            # (2) 2 or more Subjects (related to the same Prof) with same 'quadri', 'day' and 'hour' in 'conflicts_i2'
            if(errorType == 2):
                # Granting that the 'errorType' do not change good relations without restrictions to repair
                if(conflicts_i2.count([]) != len(conflicts_i2)):
                    # Choosing the relation to be modified
                    # Roulette Wheel - more relations -> more weight
                    numRelationsList = [float(len(prof_relations[i])) if len(conflicts_i2[i]) != 0 else 0 for i in range(len(prof_relations))]
                    selected_i2, _, _ = self.rouletteWheel(conflicts_i2, numRelationsList, objectiveNum=1, repos=True, negative=False)
                    will_change_index = random.randrange(len(selected_i2[0]))
                    relation_will_change_index = selected_i2[0][will_change_index]
                    
                    # Choosing new Prof to be in the relation with the Subj selected
                    subj, oldProf = relations[relation_will_change_index]

                    # Granting that the new Prof is different of the old one
                    newProf = oldProf
                    while(oldProf == newProf):
                        # Finding randomly a new Prof
                        change = random.randrange(len(prof))
                        newProf = prof[change]
                    
                    # Setting the new relation, creating new Candidate and returning it
                    relations[relation_will_change_index]=[subj,newProf]
                    newCand = objects.Candidate()
                    newCand.setList(relations)

                    # Setting the flag to finish the while
                    flag_repair_done = True

            # (3) 2 or more Subjects (related to the same Prof) with same 'day' and 'quadri' but different 'campus' in 'conflicts_i3'
            if(errorType == 3):
                # Granting that the 'errorType' do not change good relations without restrictions to repair
                if(conflicts_i3.count([]) != len(conflicts_i3)):
                    # Choosing the relation to be modified
                    # Roulette Wheel - more relations -> more weight
                    numRelationsList = [float(len(prof_relations[i])) if len(conflicts_i2[i]) != 0 else 0 for i in range(len(prof_relations))]
                    selected_i3, _, _ = self.rouletteWheel(conflicts_i2, numRelationsList, objectiveNum=1, repos=True, negative=False)
                    will_change_index = random.randrange(len(selected_i3[0]))
                    relation_will_change_index = selected_i3[0][will_change_index]

                    # Choosing new Prof to be in the relation with the Subj selected
                    subj, oldProf = relations[relation_will_change_index]

                    # Granting that the new Prof is different of the old one
                    newProf = oldProf
                    while(oldProf == newProf):
                        # Finding randomly a new Prof
                        change = random.randrange(len(prof))
                        newProf = prof[change]
                    
                    # Setting the new relation, creating new Candidate and returning it
                    relations[relation_will_change_index]=[subj,newProf]
                    newCand = objects.Candidate()
                    newCand.setList(relations)

                    # Setting the flag to finish the while
                    flag_repair_done = True

        return newCand

#==============================================================================================================

    # Generate new solutions from the current Feasible population
    def offspringF(self, solutionsNoPop, solutionsF, prof, subj, pctMut, pctParentsCross, numCand):
        # Check if the Feasible pop. is empty
        if(len(solutionsF.getList()) != 0):
            # 'objectiveNum': number of solutions to become parents - based on 'pctParentsCross'
            objectiveNum = int(pctParentsCross * len(solutionsF.getList()) / 100)
            
            # Turning 'objectiveNum' to Even if it is Odd -> summing +1 to it only if the new 'objectiveNum' is not bigger then len(solutionsF)
            if(objectiveNum % 2 != 0):
                if((objectiveNum + 1) <= len(solutionsF.getList())): objectiveNum = objectiveNum + 1
                else: objectiveNum = objectiveNum - 1
            
            # Granting that are solutions enough to became fathers (more than or equal 2)
            if(objectiveNum < 2):
                # If have at most 2 solutions - each solution will generate a child through random mutation
                for cand in solutionsF.getList(): solutionsNoPop.addCand(self.mutationRand(cand, prof))   
            # If we have at least 2 solutions
            else:
                # Roulette Wheel with Reposition to choose solutions to become Parents
                fitnessList = [cand.getFitness() for cand in solutionsF.getList()]
                parentsSolFeas, notParents_objectsList, _ = self.rouletteWheel(solutionsF.getList(), fitnessList, objectiveNum, repos=True, negative=False)
                
                # Solutions 'children' created by crossover
                childSolFeas = []
                # Make a Crossover (create two new candidates) for each pair of parents candidates randomly choose
                # Granting the number of children is equal of parents
                while(len(childSolFeas) != objectiveNum):
                    # If there are only 2 parents, make a crossover between them
                    if(len(parentsSolFeas) <= 2): parent1, parent2 = 0, 1
                    # If there are more then 2, choosing the parents Randomly
                    else:
                        parent1, parent2 = random.randrange(len(parentsSolFeas)), random.randrange(len(parentsSolFeas))
                        # Granting the second parent is not the same of first one
                        while(parent1 == parent2): parent2 = random.randrange(len(parentsSolFeas))
                    
                    # Making the Crossover with the selected parents
                    newCand1, newCand2 = self.crossover(parentsSolFeas[parent1], parentsSolFeas[parent2])

                    # Removing used parents to make a new selection of Parents
                    parent2 = parentsSolFeas[parent2]
                    parentsSolFeas.remove(parentsSolFeas[parent1])
                    parentsSolFeas.remove(parent2)
                    
                    # adding the new candidates generated to childSolFeas
                    childSolFeas.append(newCand1)
                    childSolFeas.append(newCand2)
                
                # Make Mutations with 'pctMut' (mutation prob.) with all the children generated by Crossover right before
                for cand in childSolFeas:
                    # Will pass through random mutation process
                    if((float(pctMut / 100.0)) >= float(random.randrange(100) / 100.0)):
                        # Modifying the child making a rand mutation
                        cand = self.mutationRand(cand, prof)
                    # Adding the child generated by crossover to 'solutionsNoPop'
                    solutionsNoPop.addCand(cand)

                # Make Mutation with all the candidates that were not choosen to be Parents right before
                for cand in notParents_objectsList:
                    # Making a rand mutation
                    cand = self.mutationRand(cand, prof)
                    # Adding the child generated by crossover to 'solutionsNoPop'
                    solutionsNoPop.addCand(cand)

            if(prt == 1): print("Feas. Offspring/", end='')

#==============================================================================================================

    # Make a selection of the solutions from all Infeasible Pop.('infPool' and 'solutionsI')
    def selectionI(self, infPool, solutionsI, numCand):
        # Check if the Infeasible pop. is empty
        if(len(solutionsI.getList()) != 0 or len(infPool.getList()) != 0):
            # Gathering both lists (infPool and solutionsI)
            infeasibles_List = solutionsI.getList() + infPool.getList()
            
            # Check if is needed to make a selection process
            if(len(infeasibles_List) > numCand):
                # Roulette Wheel Selection
                fitnessList = [cand.getFitness() for cand in infeasibles_List] # Negative values
                infeasibles_List, _, _ = self.rouletteWheel(infeasibles_List, fitnessList, numCand, repos=False, negative=True)
                
            # Updating the (new) 'solutionsI' list to the next generation
            solutionsI.setList(infeasibles_List)
                
            if(prt == 1): print("Inf. Selection/", end='')
            
#==============================================================================================================

    # Make a Selection of the best solutions from Feasible Pop.
    def selectionF(self, feaPool, solutionsF, numCand, pctElitism=100):
        # Check if the Feasible pop. is empty
        if(len(solutionsF.getList()) != 0 or len(feaPool.getList()) != 0):
            # Gathering both lists (feaPool and solutions)
            feasibles_List = solutionsF.getList() + feaPool.getList()
            
            # Check if is needed to make a selection process
            if(len(feasibles_List) > numCand):
                # Gathering all Fitness
                listFit = [cand.getFitness() for cand in feasibles_List]
                
                # Defining the division of number of candidates between selections process
                elitismNum = int(numCand * pctElitism / 100.0)
                if(elitismNum == 0): elitismNum = 1
                roulNum = numCand - elitismNum

                # Elitism and Roulette Selection
                maxFeasibles_List, rest_objectsList, rest_valuesList = self.elitismSelection(feasibles_List, listFit, elitismNum)
                selectedObj, _, _ = self.rouletteWheel(rest_objectsList, rest_valuesList, roulNum, repos=False, negative=False)
                feasibles_List = maxFeasibles_List + selectedObj
            
            # Updating the (new) 'solutionsF' list to the next generation
            solutionsF.setList(feasibles_List)
            
            if(prt == 1): print("Feas. Selection/", end='')

#==============================================================================================================

    # Make a rand mutation into a solution
    def mutationRand(self, candidate, prof):
        # Getting all relations from Candidate
        relations = candidate.getList().copy()
        
        # Choosing randomly a relation to be modified
        original = random.randrange(len(relations))
        # Recording the Original Relation
        subj, oldProf = relations[original]
        
        # Granting that the 'newProf' is different from the 'oldProf'
        newProf = oldProf
        while(oldProf == newProf):
            # Finding randomly a new Prof
            change = random.randrange(len(prof))
            newProf = prof[change]
        
        # Setting the new Relation modified, creating and setting a new Candidate
        relations[original]=[subj,newProf]
        newCand = objects.Candidate()
        newCand.setList(relations)
        
        # Returning the new Candidate generated
        return newCand
        
#==============================================================================================================

    # Make a crossover between two solutions
    def crossover(self, cand1, cand2, twoPoints=None, firstHalf=None, notEqualParent=None):
        # The number of changes between parents will always be equal (same crossover segment size), never same size of Num of Parents Relations
        # twoPoints = False -> its chosen only one point, will have changes from the point till the rest of the relations
        # firstHalf = True -> changes from the beginning till the one point choosed
        # notEqualParent = True -> avoid occurrence of childs equal to his parents
        
        # What is equal 'None' will be a random choice
        if(twoPoints == None): twoPoints = random.choice([True, False])
        if(firstHalf == None): twoPoints = random.choice([True, False])
        if(notEqualParent == None): notEqualParent = random.choice([True, False])
        
        # Getting all relations from Candidates to work with
        relations1, relations2 = cand1.getList(), cand2.getList()
        
        # OnePoint type:
        if(twoPoints == False):
            # Priorizing change of relations on first half of the candidates
            if(firstHalf == True):
                point1 = 0 # Default point in 'firstHalf' mode
                point2 = random.randrange(len(relations1)) # Randomly choosing other point that can be equal to 'point1'
                # Granting that not occur only a copy of parents - the chosen point is not the last relation
                if(notEqualParent == True):
                    while(point2 == len(relations1)-1): point2 = random.randrange(len(relations1))
            
            # Priorizing change of relations on second half of the candidates
            else:
                point2 = len(relations1)-1 # Default point in 'secondHalf' mode
                point1 = random.randrange(len(relations1)) # Randomly choosing other point that can be equal to 'point2'
                # Granting that not occur only a copy of parents - the chosen point is not the last relation
                if(notEqualParent == True):
                    while(point1 == 0): point1 = random.randrange(len(relations1))
        
        # TwoPoints Type
        else:
            # Generating, randomly two numbers to create a patch - can be a single modification (when p1==p2)
            point1, point2 = random.randrange(len(relations1)), random.randrange(len(relations1))
            # Granting that 'point2' is bigger than 'point1'
            if(point2 < point1):
                p = point1
                point1 = point2
                point2 = p

            # Granting that the crossover do not only copy all relations of one Cand to the another
            while(notEqualParent == True and point2 - point1 == len(relations1) - 1):
                # Generating, randomly two numbers to create a patch - can be a single modification (when p1==p2)
                point1, point2 = random.randrange(len(relations1)), random.randrange(len(relations1))
                # Granting that 'point2' is bigger than 'point1'
                if(point2 < point1):
                    p = point1
                    point1 = point2
                    point2 = p

        # Passing through the relations between Parents making all changes
        while (point1 <= point2):
            # Recording the original relations
            s1, p1 = relations1[point1]
            s2, p2 = relations2[point1]
            
            # Making the exchange of relations (changing only professors)
            relations1[point1] = s1, p2
            relations2[point1] = s2, p1
            
            # Next relation
            point1 = point1 + 1
        
        # Creating and setting the two new Candidates
        newCand1, newCand2 = objects.Candidate(), objects.Candidate()
        newCand1.setList(relations1)
        newCand2.setList(relations2)
        
        # Returning the new Candidates
        return newCand1, newCand2

#==============================================================================================================

    # Selection by elitism
    def elitismSelection(self, objectsList, valuesList, objectiveNum):
        selectedObj = [] # List with the selected Objects

        # Getting the maximal Value Solutions
        while(len(selectedObj) < objectiveNum):
            # Finding the maximal value in the list and its respective index
            maxValue = max(valuesList)
            maxIndex = valuesList.index(maxValue)

            # Adding selected object to list
            selectedObj.append(objectsList[maxIndex])

            # Removing maximal Value/Object to next selection
            valuesList.pop(maxIndex)
            objectsList.pop(maxIndex)
        
        return  selectedObj, objectsList, valuesList

#==============================================================================================================

    # Make selection of objects by Roulette Wheel
    def rouletteWheel(self, objectsList, valuesList, objectiveNum, repos=True, negative=False):
        # objectiveNum: Num of objects will be selected
        # repos: Type of wheel (with reposition)
        # Since the value of Fitness is in the range of '-1' and '0' it is needed to be modified
        # Modifying the values to put it into a range of '0' and '1'
        # negative = True -> modify de range of values

        # List with the selected Objects
        selectedObj = []
        # Flag tha allows to make all important calcs at least one time when the Roulette is donfig to have Reposition
        reCalc = True

        while(len(selectedObj) < objectiveNum):
            # Allow the Updating of the data for the next Roullete Round without the object that was recent selected on past round
            if(reCalc == True):
                # When the Roulette process does have reposition of objects
                if(repos == True): reCalc = False
                
                # Find the total Value of the Objects
                totalValue = sum([value if negative == False else 1.0 + value for value in valuesList])
                
                # Calculate the prob. of a selection for each object
                probObj = [float(value / totalValue) if negative == False else float((1.0 + value) / totalValue) for value in valuesList]
                
                # Calculate a cumulative prob. for each object
                cumulative = 0.0
                cumulativeProbObj = []
                for q in probObj:
                    qNew = q + cumulative
                    cumulativeProbObj.append(qNew)
                    cumulative = qNew
            
            # MAIN Roulette Wheel Selection process (one round)
            probPrev = 0.0
            r = float(random.randrange(100) / 100.0)
            for i in range(len(cumulativeProbObj)):
                if(probPrev < r and r <= cumulativeProbObj[i]):
                    # Adding the selected Object to 'selectedObj'
                    selectedObj.append(objectsList[i])
                    if(repos == False):
                        # Removing the selected object/value from 'valuesList' to do next roulette process
                        valuesList.pop(i)
                        objectsList.pop(i)
                    break
                probPrev = cumulativeProbObj[i]

        return  selectedObj, objectsList, valuesList

#==============================================================================================================
    
    # Detect the stop condition
    def stop(self, curIter, maxIter, lastMaxIter, convergDetect, maxFea, stopFitValue):
        #import pdb; pdb.set_trace()
        if(curIter > maxIter): return False # Reached max num of iterations
        if(stopFitValue != 0 and maxFea >= stopFitValue): return False # Reached max fit value
        if(convergDetect != 0 and curIter - lastMaxIter > convergDetect): return False # Reached convergence num of iterations
        return True # Continues the run with same num of iterations
    
    # Ask to user if wants to continue the run with more iterations
    def ask(self, value):
        ask1 = 'a'
        while(ask1 != "y" and ask1 != ""): ask1 = input("Need more iterations? Yes('y')/No('Enter'): ")
        if(ask1 == "y"):
            notPosNumber = False
            while(not notPosNumber): 
                ask2 = input("How much? (positive number): ")
                try: 
                    if(int(ask2) >= 0): notPosNumber = True
                except ValueError: notPosNumber = False
            return True # Continue with more iterations
        return False # Stop

#==============================================================================================================
