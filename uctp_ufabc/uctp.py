# UCTP Main Methods

import objects
import ioData
import random

# Set '1' to allow, during the run, the print on terminal of some steps
printSteps = 0

#==============================================================================================================

# Create the first generation of solutions
def start(solutionsNoPop, subjList, profList, init):
    if(printSteps == 1): print("Creating first generation...", end='')
    for _ in range(init): solutionsNoPop.addCand(newCandRand(subjList, profList))
    if(printSteps == 1): print("Created first generation!")

#==============================================================================================================

# Create new Candidate Full-Random
def newCandRand(subjList, profList):
    candidate = objects.Candidate()
    # Follow the subjects in 'subjList', in order, and for each one, choose a professor randomly
    for sub in subjList: candidate.addRelation(sub, profList[random.randrange(len(profList))])
    return candidate

#==============================================================================================================

# Extracts info about what Subj appears in which Prof (PrefList)
def extractSubjIsPref(subjList, profList):
    # Lists for each Prof, where it is '1' if Subj in respective index is on Prof List of Pref
    subjIsPrefList = [[0 for _ in range(len(subjList))] for _ in range(len(profList))]

    # Counting the occurrences, filling the vectors
    for pIndex in range(len(profList)):
        # Getting data of current Prof
        prefSubjLists = [i for i in profList[pIndex].getPrefSubjLists()]
        
        # All Relations of one Prof
        for sIndex in range(len(subjList)):
            # Getting data of current Subj
            sName = subjList[sIndex].getName()
            sQuadri = subjList[sIndex].getQuadri()
            
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
                        # If current Subject in analysis is on current Quadri 
                        if(str(i+1) in sQuadri):
                            # Informing that the Subj appears on respective Prof-QuadriPrefList
                            subjIsPrefList[pIndex][sIndex] = 2
                        # Informing that the Subj appears on other Prof-QuadriPrefList that is not same Quadri
                        else:
                            # Granting that do not decrease a value 2 already set
                            if(subjIsPrefList[pIndex][sIndex] == 0): subjIsPrefList[pIndex][sIndex] = 1
    
    return subjIsPrefList

#==============================================================================================================

# Separation of solutions into 2 populations
def twoPop(solutionsNoPop, solI, solF, profList, subjList, weightsList, numInfWeights):
    # Granting that the Lists will be empty to receive new Solutions
    solI.resetCandList()
    solF.resetCandList()
    
    for cand in solutionsNoPop.getCandList():
        # Classification by checking feasibility
        pop = checkFeasibility(cand, profList, subjList, weightsList, numInfWeights)
        if(pop == "feasible"): solF.addCand(cand)
        elif(pop == "infeasible"): solI.addCand(cand)
    
    # Granting that the List will be empty to next operations
    solutionsNoPop.resetCandList()
    
    if(printSteps == 1): print("Checked Feasibility (new Candidates)/", end='')

#==============================================================================================================

# Detect the violation of a Restriction into a candidate
def checkFeasibility(candidate, profList, subjList, weightsList, numInfWeights):
    # As part of the Candidate's Prof-Subj relations (with both Feasible and the Infeasible) will be traversed to check they Feasibility here,
    # instead of repass an entire Infeasible Candidate again in the 'calc_fitInfeas', the calculation of its Fitness will already be done
    # only one time here. Only the Feasible ones will have to pass through 'calc_fitFeas' later.
    fit = -1
    fit = calc_fitInfeas(candidate, profList, subjList, weightsList[:numInfWeights])
    if(fit < 0):
        candidate.setFitness(fit)
        return "infeasible"
    return "feasible"

#==============================================================================================================

# Calculate the Fitness of the candidate
def calcFit(infeasibles, feasibles, profList, subjList, weightsList, numInfWeights, subjIsPrefList):
    # All Infeasible Candidates - is here this code only for the representation of the default/original algorithm`s work
    # The Inf. Fitness calc was already done in 'checkFeasibility()' method
    # Check if the Infeasible pop. is empty
    if(len(infeasibles.getCandList()) != 0):
        for cand in infeasibles.getCandList():
            if(cand.getFitness() == 0.0):
                # Setting the Fitness with the return of calc_fitInfeas() method
                cand.setFitness(calc_fitInfeas(cand, profList, subjList, weightsList[:numInfWeights]))
        if(printSteps == 1): print("Fitness of all Inf./", end='')
    
    # All Feasible Candidates
    # Check if the Feasible pop. is empty
    if(len(feasibles.getCandList()) != 0):
        for cand in feasibles.getCandList():
            if(cand.getFitness() == 0.0):
                # Setting the Fitness with the return of calc_fitFeas() method
                cand.setFitness(calc_fitFeas(cand, profList, subjList, weightsList[numInfWeights:], subjIsPrefList))
        if(printSteps == 1): print("Fitness of all Feas./", end='')
    
#==============================================================================================================

# Calculate Fitness of Infeasible Candidates
def calc_fitInfeas(candidate, profList, subjList, weightsList):
    # Getting information about the Candidate
    prof_relationsList = calc_i1(candidate, profList, subjList)
    i2_conflictsList, i3_conflictsList = calc_i2_i3(prof_relationsList, subjList)
    
    # Setting found variables
    candidate.setInfVariables(prof_relationsList, i2_conflictsList, i3_conflictsList)

    # Checking if occurred violations of restrictions on the Candidate
    # If there are violated restrictions, this Candidate is Infeasible and then will calculate and return a negative Fitness,
    # if not, is Feasible, will return 1.0 as Fitness
    if(prof_relationsList.count([]) != 0 or i2_conflictsList.count([]) != len(i2_conflictsList) or i3_conflictsList.count([]) != len(i3_conflictsList)):
        # Calculating main variables
        i1 = float(prof_relationsList.count([])) / (float(len(profList)) - 1.0)
        i2 = float(sum([len(i) for i in i2_conflictsList])) / float(len(subjList))
        i3 = float(sum([len(i) for i in i3_conflictsList])) / float(len(subjList))
        i = [i1, i2, i3]

        # Final Infeasible Function Fitness Calc
        Fi = -1.0 * sum([i[j] * weightsList[j] for j in range(len(i))]) / sum([w for w in weightsList])
        
        # Returning the calculated result
        return Fi

    # If all Relations Prof-Subj in this Candidate passed through the restrictions)
    return 1.0

#-------------------------------------------------------

# i1: penalty to how many Professors does not have at least one relation with a Subject
def calc_i1(candidate, profList, subjList):
    # List of lists of Subjects that are related to the same Professor, where the position in this list is the same of the same professor in 'profList' list
    # Empty list in this list means that some Professor (p) does not exists on the Candidate
    prof_relationsList = [[] for _ in range(len(profList))]
    
    # Filling the list according to the candidate
    for s, p in candidate.getRelationsList():
        indexp = profList.index(p)
        indexs = subjList.index(s)
        prof_relationsList[indexp].append(indexs)
    
    return prof_relationsList

#-------------------------------------------------------

# i2: penalty to how many Subjects, related to the same Professor, are teach in the same day, hour and quadri
# i3: penalty to how many Subjects, related to the same Professor, are teach in the same day and quadri but in different campus
def calc_i2_i3(prof_relationsList, subjList):
    # List of the subjects that have a conflict between them - always the two conflicts are added, that is,
    # there can be repetitions of subjects
    i2_conflictsList, i3_conflictsList = [[] for _ in range(len(prof_relationsList))], [[] for _ in range(len(prof_relationsList))]
    
    # Searching, in each professor (one at a time), conflicts of schedules between subjects related to it
    for list_subj in prof_relationsList:
        # Current Prof in analysis
        profIndex = prof_relationsList.index(list_subj)

        # Check if the professor has more than 1 relation Prof-Subj to analyze
        if(len(list_subj) > 1):
            # Getting the data of all Subjects related to current Professor in analysis
            timetableList_List = [subjList[i].getTimeTableList() for i in list_subj]
            quadri_List = [subjList[i].getQuadri() for i in list_subj]
            campus_List = [subjList[i].getCampus() for i in list_subj]
            period_List = [subjList[i].getPeriod() for i in list_subj]

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
                    # Already check if both Subj (i, k) is on same Quadri
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
                                            i3_conflictsList[profIndex].append(list_subj[i])
                                            i3_conflictsList[profIndex].append(list_subj[k])
                                            verified_i3 = True

                                    # There is, at least, two subjects teach in the same day, hour and quadri
                                    # First check if they have the same Period
                                    if(period_List[i] == period_List[k] and i_hour[i_day.index(a)] == inext_hour[inext_day.index(b)]):
                                        # if one 'frequency' is "QUINZENAL I" and the other is "QUINZENAL II" then DO NOT count
                                        if('SEMANAL' in i_frequency[i_day.index(a)] or 'SEMANAL' in inext_frequency[inext_day.index(b)]):
                                            if(verified_i2 == False):
                                                i2_conflictsList[profIndex].append(list_subj[i])
                                                i2_conflictsList[profIndex].append(list_subj[k])
                                                #print(subjList[list_subj[i]].get(), subjList[list_subj[k]].get(), '\n')
                                                verified_i2 = True
                                        elif('QUINZENAL I' in i_frequency[i_day.index(a)] and 'QUINZENAL I' in inext_frequency[inext_day.index(b)]):
                                            if(verified_i2 == False):
                                                i2_conflictsList[profIndex].append(list_subj[i])
                                                i2_conflictsList[profIndex].append(list_subj[k])
                                                #print(subjList[list_subj[i]].get(), subjList[list_subj[k]].get(), '\n')
                                                verified_i2 = True
                                        elif('QUINZENAL II' in i_frequency[i_day.index(a)] and 'QUINZENAL II' in inext_frequency[inext_day.index(b)]):
                                            if(verified_i2 == False):
                                                i2_conflictsList[profIndex].append(list_subj[i])
                                                i2_conflictsList[profIndex].append(list_subj[k])
                                                #print(subjList[list_subj[i]].get(), subjList[list_subj[k]].get(), '\n')
                                                verified_i2 = True
                    # Going to the next Subject (k+1) to compare with the same, current, main, Subject (i)
                    k = k + 1
                # Going to the next Subject (i+1) related to the same Professor
                i = i + 1
    
    # Removing from 'i2_conflictsList' and 'i3_conflictsList' duplicates
    final_i2 = [[] for _ in range(len(prof_relationsList))]
    final_i3 = [[] for _ in range(len(prof_relationsList))]
    for i in range(len(prof_relationsList)):
        for j in i2_conflictsList[i]:
            if(final_i2[i].count(j) == 0): final_i2[i].append(j)
        for j in i3_conflictsList[i]:
            if(final_i3.count(j) == 0): final_i3[i].append(j)
    
    return final_i2, final_i3

#==============================================================================================================

# Calculate Fitness of Feasible Candidates
def calc_fitFeas(candidate, profList, subjList, weightsList, subjIsPrefList):
    
    prof_relationsList, _, _, _, _, _ = candidate.getFeaVariables()

    # Looking for good Relations into the Candidate using "Quality Amplifiers"
    # Getting information about the Candidate
    sum_chargesRelative, difChargeList = calc_f1(subjList, profList, prof_relationsList)
    sum_Satisfaction, numSubjPrefList = calc_f2(subjList, profList, prof_relationsList, subjIsPrefList)
    sum_quadSabbNotPref, quadSabbNotPrefList = calc_f3(subjList, profList, prof_relationsList)
    sum_periodPref, periodPrefList = calc_f4(subjList, profList, prof_relationsList)
    sum_campusPref, campPrefList = calc_f5(subjList, profList, prof_relationsList)
    sum_relationsRelative, _ = calc_f6(subjList, profList, prof_relationsList)
    sum_qualityRelative, _ = calc_f7(subjList, profList, prof_relationsList, subjIsPrefList)

    # Setting found variables
    candidate.setFeaVariables(prof_relationsList, numSubjPrefList, periodPrefList, quadSabbNotPrefList, campPrefList, difChargeList)
    
    # Calculating main variables
    f1 = 1.0 - (float(sum_chargesRelative / len(profList)))
    f2 = float(sum_Satisfaction / len(profList))
    f3 = float(sum_quadSabbNotPref / len(subjList))
    f4 = float(sum_periodPref / len(subjList))
    f5 = float(sum_campusPref / len(subjList))
    f6 = 1.0 - (float(sum_relationsRelative / len(profList)))
    f7 = float(sum_qualityRelative / len(profList))
    f = [f1, f2, f3, f4, f5, f6, f7]

    # Final Feasible Function Fitness Calc
    Ff = sum([f[j] * weightsList[j] for j in range(len(f))]) / sum([w for w in weightsList])
    
    # Returning the result calculated
    return Ff

#-------------------------------------------------------

# f1: how balanced is the distribution of Subjects, considering the "Charge" of each Professor and its Subj related
def calc_f1(subjList, profList, prof_relationsList):
    # List of all 'Effective Charges', that is, the sum of the charges of all the subjects related to the professor
    charges_eachProfRelations = [0 for _ in range(len(profList))]
    # List of requested charges of each professor
    charges_EachProf = [float(profList[i].getCharge()) for i in range(len(profList))]

    # Counting the occurrences, filling the vectors
    for i in range(len(prof_relationsList)):
        # Summing all chargers of all relations of this Prof
        charges_eachProfRelations[i] = sum([float(str(subjList[sIndex].getCharge()).replace(",",".")) for sIndex in prof_relationsList[i]])
    
    # Difference of Prof Charge and the sum of all of its Subj-Relations
    difChargeList = [charges_EachProf[i] - charges_eachProfRelations[i] for i in range(len(profList))]

    # Relative weigh of excess or missing charge for each Prof - based on the absolute credit difference
    # between the credits requested by the Prof and the sum off all Subj related to it
    charges_relative = [float(abs(difChargeList[i])) / charges_EachProf[i] for i in range(len(profList))]
    
    # Making a simple adjust on the value
    charges_relativeFinal = [charge if charge < 1.0 else 1.0 for charge in charges_relative]
    
    # The sum of charge discrepancies of all professors
    sum_chargesRelative = sum([charge for charge in charges_relativeFinal])
    
    return sum_chargesRelative, difChargeList

#-------------------------------------------------------

# f2: how many and which Subjects are the professors preference, considering "prefSubj..." Lists
def calc_f2(subjList, profList, prof_relationsList, subjIsPrefList):
    # These are Lists (each quadri - 3) of Lists (each professor) of Lists (each PrefList+LimList)
    # In each List (inside the List inside the List) we have 1 if the same index Subject (from same Quadri X Pref List + Lim Pref List) is related to Same Prof
    # or we have 0 if it is not related
    qX_relations = [[[] for _ in range(len(profList))] for _ in range(3)]

    # List with the number of subjects that are on respective Prof's List of Preferences
    numSubjPrefList = [0 for _ in range(len(profList))]
    
    # Counting the occurrences, filling the vectors
    for relations in prof_relationsList:
        # Setting Index of current Prof
        pIndex = prof_relationsList.index(relations)
        
        # Getting data of current Prof
        prefSubjLists = [i for i in profList[pIndex].getPrefSubjLists()]
        
        # For each Quadri - Filling QX Lists of current Prof
        # in each one appends "pPrefSubjQXList" with "pPrefSubjLimList" to have the length of the subList
        for i in range(3):
            qX_relations[i][pIndex] = [0 for _ in range(len(prefSubjLists[i]) + len(prefSubjLists[3]))]

        # All Relations of one Prof
        for sIndex in relations:
            # Getting data of current Subj
            sName = subjList[sIndex].getName()
            sQuadri = subjList[sIndex].getQuadri()

            # For each quadri
            for i in range(3):
                # Looking for only in the list of respective quadri of current Subject in analysis
                if(str(i+1) in sQuadri):
                    # Finding the Subject 'sName' in "pPrefSubjQXList+pPrefSubjLimList" list
                    sumList = prefSubjLists[i] + prefSubjLists[3]
                    # Checking if the List is not empty
                    if(len(sumList) > 0):
                        try: index_value = sumList.index(sName)
                        except ValueError: index_value = -1
                        # If the Subj name appears in the list
                        if(index_value != -1):
                            # Putting '1' in same position found 'index_value' in the subList (which this one, is in same position of profList)
                            qX_relations[i][pIndex][index_value] = 1
                            # Adding the Subj that is on Prof Pref List
                            numSubjPrefList[pIndex] = numSubjPrefList[pIndex] + 1
        
    # Calculating intermediate variables
    # Lists of the calculation of "satisfaction" based on the order of Subjects choose by a Professor (index = 0 has more weight)
    finalQX = [[0.0 for _ in range(len(profList))] for _ in range(3)]
    
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
    
    return sum_Satisfaction, numSubjPrefList

#-------------------------------------------------------

# f3: how many Subjects are teach in a "Quadri" that is not the same of Professors 'quadriSabbath'
def calc_f3(subjList, profList, prof_relationsList):
    # List of Subjs related to a Prof that is on different Quadri of prof's QuadSabb
    quadSabbNotPrefList = [[] for _ in range(len(profList))]

    # Getting the occurrences, filling the vector
    for i in range(len(prof_relationsList)):
        # Getting data of current Prof
        pQuadriSabbath = profList[i].getQuadriSabbath()

        # All Relations of one Prof
        for sIndex in prof_relationsList[i]:
            # Getting data of current Subj
            sQuadri = subjList[sIndex].getQuadri()

            # Adding to count if the Subj is not in the same 'pQuadriSabbath' (if Prof choose 'nenhum' he does not have a 'pQuadriSabbath')
            if('NENHUM' in pQuadriSabbath or sQuadri != pQuadriSabbath): quadSabbNotPrefList[i].append(sIndex)
        
    # Calculating intermediate variable
    sum_quadSabbNotPref = sum([len(listSubj) for listSubj in quadSabbNotPrefList])

    return sum_quadSabbNotPref, quadSabbNotPrefList

#-------------------------------------------------------

# f4: how many Subjects are teach in the same "Period" of the Professor preference "pPeriod"
def calc_f4(subjList, profList, prof_relationsList):
    # List of Subjs related to a Prof that is on same Period of prof's Period
    periodPrefList = [[] for _ in range(len(profList))]

    # Getting the occurrences, filling the vector
    for i in range(len(prof_relationsList)):
        # Getting data of current Prof
        pPeriod = profList[i].getPeriod()

        # All Relations of one Prof
        for sIndex in prof_relationsList[i]:
            # Getting data of current Subj
            sPeriod = subjList[sIndex].getPeriod()

            # Adding to count if the Subj is in the same 'pPeriod' or if Prof do not care about 'pPeriod' equal to 'NEGOCIAVEL'
            if('NEGOCI' in pPeriod or sPeriod == pPeriod): periodPrefList[i].append(sIndex)
        
    # Calculating intermediate variable
    sum_periodPref = sum([len(listSubj) for listSubj in periodPrefList])
    
    return sum_periodPref, periodPrefList

#-------------------------------------------------------

# f5: how many Subjects are teach in the same "Campus" of the Professor preference "prefCampus"
def calc_f5(subjList, profList, prof_relationsList):
    # List of Subjs related to a Prof that is on same Campus of prof's Campus
    campPrefList = [[] for _ in range(len(profList))]

    # Getting the occurrences, filling the vector
    for i in range(len(prof_relationsList)):
        # Getting data of current Prof
        pPrefCampus = profList[i].getPrefCampus()
        
        # All Relations of one Prof
        for sIndex in prof_relationsList[i]:
            # Getting data of current Subj
            sCampus = subjList[sIndex].getCampus()
            # Adding to count if the Subj is in the same 'pPrefCampus'
            if(sCampus == pPrefCampus): campPrefList[i].append(sIndex)
    
    # Calculating intermediate variable
    sum_campusPref = sum([len(listSubj) for listSubj in campPrefList])

    return sum_campusPref, campPrefList

#-------------------------------------------------------

# f6: average of relations between profs
def calc_f6(subjList, profList, prof_relationsList):
    # Number of Subjs ideal for each professor
    avgSubjperProf = float(len(subjList)/len(profList))

    # Difference between num of relations of each prof and the average
    difNumRel = [len(relations) - avgSubjperProf for relations in prof_relationsList]

    # Relative weigh of excess or missing relations for each Prof - based on the absolute relations difference
    relations_relative = [float(abs(difNumRel[i]) / avgSubjperProf) for i in range(len(prof_relationsList))]
    
    # Making a simple adjust on the values
    relations_relativeFinal = [value if value < 1.0 else 1.0 for value in relations_relative]
    
    # The sum of relations discrepancies of all professors
    sum_relationsRelative = sum([charge for charge in relations_relativeFinal])
    
    return sum_relationsRelative, difNumRel 

#-------------------------------------------------------

# f7: quality of relations (subj appears in some list of pref or/and same quadri)
def calc_f7(subjList, profList, prof_relationsList, subjIsPrefList):
    # Summing, for each professor, its relations qualities
    sumRelationsQuality = [sum([subjIsPrefList[i][pos] for pos in prof_relationsList[i]]) for i in range(len(prof_relationsList))]

    # Relative value of quality of all relations for each Prof (2 is the max value of quality)
    qualityRelative = [float(sumRelationsQuality[i] / (2 * len(prof_relationsList[i]))) for i in range(len(prof_relationsList))]

    # The sum of relative qualities of all professors
    sum_qualityRelative = sum([value for value in qualityRelative])

    return sum_qualityRelative, qualityRelative

#==============================================================================================================

# Generate new solutions from the current Infeasible population
def offspringI(solutionsNoPop, solutionsI, profList, subjList, subjIsPrefList):
    # Check if the Infeasible pop. is empty
    if(len(solutionsI.getCandList()) != 0):
        # Make a Mutation for each candidate, trying to repair a restriction problem maker
        for cand in solutionsI.getCandList():
            newCand = mutationI(cand, profList, subjList, subjIsPrefList)
            # Adding the new Candidate generated by Mutation to 'solutionsNoPop'
            solutionsNoPop.addCand(newCand)

        if(printSteps == 1): print("Inf. Offspring/", end='')

#==============================================================================================================

# Make a mutation into a infeasible candidate
def mutationI(candidate, profList, subjList, subjIsPrefList):
    # Getting data to work with
    relations = candidate.getRelationsList()
    prof_relationsList, i2_conflictsList, i3_conflictsList = candidate.getInfVariables()
    
    # This While ensures that 'errorType' will choose Randomly one 'restriction repair'
    flag_repair_done = False
    while(flag_repair_done == False):
        # Choosing one type of restriction to repair
        errorType = random.randrange(0,4)
        
        # (0) No repair -> Random Change
        if(errorType == 0):
            # Getting a new candidate (modified) 
            newCand = mutationRand(candidate, profList)
            # Setting the flag to finish the while
            flag_repair_done = True
        # (1) Prof without relations with Subjects in 'prof_relationsList'
        if(errorType == 1):
            flag_repair_done, newCand = errorTypeI1(profList, prof_relationsList, relations, subjIsPrefList)
        # (2) 2 or more Subjects (related to the same Prof) with same 'quadri', 'day' and 'hour' in 'i2_conflictsList'
        if(errorType == 2):
            flag_repair_done, newCand = errorTypeI23(profList, prof_relationsList, relations, i2_conflictsList, subjIsPrefList)
        # (3) 2 or more Subjects (related to the same Prof) with same 'day' and 'quadri' but different 'campus' in 'i3_conflictsList'
        if(errorType == 3):
            flag_repair_done, newCand = errorTypeI23(profList, prof_relationsList, relations, i3_conflictsList, subjIsPrefList)

    return newCand

#-------------------------------------------------------

# (1) Prof without relations (with no Subjects) in 'prof_relationsList'
def errorTypeI1(profList, prof_relationsList, relations, subjIsPrefList):
    # Granting that the 'errorType' do not change good relations without restrictions to repair
    if(prof_relationsList.count([]) == 0):
        newCand = objects.Candidate()
        newCand.setRelationsList(relations)
        # Setting the flag to NOT finish the while
        flag_repair_done = False
    else:
        # Choosing a professor to lose a relation
        # Roulette Wheel - more relations -> more weight 
        numRelationsList = [len(i) for i in prof_relationsList]
        profRelList_Selected, _, _ = rouletteWheel(prof_relationsList, numRelationsList, objectiveNum=1, repos=True, negative=False)
        
        # Choosing the relation to be modified
        # Roulette Wheel - less preference -> more weight
        profLost_Index = prof_relationsList.index(profRelList_Selected[0])
        lessPrefValue = [2 - subjIsPrefList[profLost_Index][subjIndex] for subjIndex in prof_relationsList[profLost_Index]]
        will_change_index, _, _ = rouletteWheel(profRelList_Selected[0], lessPrefValue, objectiveNum=1, repos=True, negative=False)
        relation_will_change_index = will_change_index[0]
        
        # Recording original relation that will be modified
        subjList, _ = relations[relation_will_change_index]
        
        # Choosing one Prof with Zero relations to get the relation
        profZeroRelIndex = [i for i in range(len(prof_relationsList)) if len(prof_relationsList[i]) == 0]
        # Roulette Wheel - more preference -> more weight
        morePrefValue = [subjIsPrefList[profIndex][relation_will_change_index] for profIndex in profZeroRelIndex]
        newProfIndex, _, _ = rouletteWheel(profZeroRelIndex, morePrefValue, objectiveNum=1, repos=True, negative=False)
        newProf = profList[newProfIndex[0]]

        # Setting the new relation, creating new Candidate and returning it
        relations[relation_will_change_index]=[subjList,newProf]
        newCand = objects.Candidate()
        newCand.setRelationsList(relations)

        # Setting the flag to finish the while
        flag_repair_done = True

    return flag_repair_done, newCand

#-------------------------------------------------------

# (2) 2 or more Subjects (related to the same Prof) with same 'quadri', 'day' and 'hour' in 'i2_conflictsList'
# (3) 2 or more Subjects (related to the same Prof) with same 'day' and 'quadri' but different 'campus' in 'i3_conflictsList'
def errorTypeI23(profList, prof_relationsList, relations, conflicts_iX, subjIsPrefList):
    # Granting that the 'errorType' do not change good relations without restrictions to repair
    if(conflicts_iX.count([]) == len(conflicts_iX)):
        newCand = objects.Candidate()
        newCand.setRelationsList(relations)
        # Setting the flag to NOT finish the while
        flag_repair_done = False
    else:
        # Choosing a professor with 'iX' conflicts to lose a relation
        # Roulette Wheel - more conflicts -> more weight
        weightList = [len(conflicts_iX[i]) for i in range(len(prof_relationsList))]
        selected_iX, _, _ = rouletteWheel(conflicts_iX, weightList, objectiveNum=1, repos=True, negative=False)
        profLost_Index = conflicts_iX.index(selected_iX[0])
        
        # Choosing the relation to be modified
        # Roulette Wheel - less preference -> more weight
        lessPrefValue = [2 - subjIsPrefList[profLost_Index][subjIndex] for subjIndex in conflicts_iX[profLost_Index]]
        will_change_index, _, _ = rouletteWheel(selected_iX[0], lessPrefValue, objectiveNum=1, repos=True, negative=False)
        relation_will_change_index = will_change_index[0]

        # Recording original relation that will be modified
        subjList, oldProf = relations[relation_will_change_index]

        # Choosing new Prof to be in the relation with the Subj selected
        # Granting that the new Prof is different of the old one
        newProf = oldProf
        while(oldProf == newProf):
            # Roulette Wheel - more preference AND less relations -> more weight
            SubjPrefValuesList = [subjIsPrefList[relation_will_change_index] for subjIsPrefList in subjIsPrefList]
            # Removing possible Zeros to make the division
            prof_relations_final = [len(i) if len(i) != 0 else 0.5 for i in prof_relationsList]
            # Getting the values
            morePrefValueList = [float(SubjPrefValuesList[i] / prof_relations_final[i]) for i in range(len(profList))]
            # If there is only one Prof with value != 0.0
            if(morePrefValueList.count(0.0) == len(morePrefValueList) - 1):
                indexNotZero = [i for i in range(len(profList)) if morePrefValueList != 0.0]
                # If is the same of the old one
                if(oldProf == profList[indexNotZero[0]]): newProf = profList[random.randrange(len(profList))]
                # If not
                else: newProf = profList[indexNotZero[0]]
            # If there are more then 1 Prof to chose
            else: 
                newProf, _, _ = rouletteWheel(profList, morePrefValueList, objectiveNum=1, repos=True, negative=False)
                newProf = newProf[0]
        
        # Setting the new relation, creating new Candidate and returning it
        relations[relation_will_change_index]=[subjList,newProf]
        newCand = objects.Candidate()
        newCand.setRelationsList(relations)

        # Setting the flag to finish the while
        flag_repair_done = True

    return flag_repair_done, newCand

#==============================================================================================================

# Generate new solutions from the current Feasible population
def offspringF(solutionsNoPop, solutionsF, profList, subjList, pctMut_childCross, pctParentsCross, maxNumCand_perPop, subjIsPrefList):
    # Check if the Feasible pop. is empty
    if(len(solutionsF.getCandList()) != 0):
        # 'objectiveNum': number of solutions to become parents - based on 'pctParentsCross'
        objectiveNum = int(pctParentsCross * len(solutionsF.getCandList()) / 100)
        
        # Turning 'objectiveNum' to Even if it is Odd -> summing +1 to it only if the new 'objectiveNum' is not bigger then len(solutionsF)
        if(objectiveNum % 2 != 0):
            if((objectiveNum + 1) <= len(solutionsF.getCandList())): objectiveNum = objectiveNum + 1
            else: objectiveNum = objectiveNum - 1
        
        # Granting that are solutions enough to became fathers (more than or equal 2)
        if(objectiveNum < 2):
            # If have at most 2 solutions - each solution will generate a child through a mutation
            for cand in solutionsF.getCandList(): solutionsNoPop.addCand(mutationF(cand, profList, subjList, subjIsPrefList))
        # If we have at least 2 solutions
        else:
            # Roulette Wheel with Reposition to choose solutions to become Parents
            fitnessList = [cand.getFitness() for cand in solutionsF.getCandList()]
            parentsSolFeas, notParents_objectsList, _ = rouletteWheel(solutionsF.getCandList(), fitnessList, objectiveNum, repos=True, negative=False)
            
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
                newCand1, newCand2 = crossover(parentsSolFeas[parent1], parentsSolFeas[parent2])

                # Removing used parents to make a new selection of Parents
                parent2 = parentsSolFeas[parent2]
                parentsSolFeas.remove(parentsSolFeas[parent1])
                parentsSolFeas.remove(parent2)
                
                # adding the new candidates generated to childSolFeas
                childSolFeas.append(newCand1)
                childSolFeas.append(newCand2)
            
            # Make Mutations with 'pctMut_childCross' (mutation prob.) with all the children generated by Crossover right before
            for cand in childSolFeas:
                # Will pass through a mutation process
                if((float(pctMut_childCross / 100.0)) >= float(random.randrange(101) / 100.0)):
                    # Getting information about the Candidate to be able to make some of the repairs on "mutationF"
                    prof_relationsList = calc_i1(cand, profList, subjList)
                    # Setting found variables
                    cand.setInfVariables(prof_relationsList, [], [])
                    
                    # Modifying the child making a mutation
                    cand = mutationF(cand, profList, subjList, subjIsPrefList)
                # Adding the child generated by crossover to 'solutionsNoPop'
                solutionsNoPop.addCand(cand)

            # Make Mutation with all the candidates that were not chosen to be Parents right before
            for cand in notParents_objectsList:
                # Making a rand mutation
                cand = mutationF(cand, profList, subjList, subjIsPrefList)
                # Adding the child generated by crossover to 'solutionsNoPop'
                solutionsNoPop.addCand(cand)

        if(printSteps == 1): print("Feas. Offspring/", end='')
#==============================================================================================================

# Make a mutation into a feasible candidate
def mutationF(candidate, profList, subjList, subjIsPrefList):
    # Getting data to work with
    relations = candidate.getRelationsList()
    prof_relationsList, _, periodPrefList, quadSabbNotPrefList, campPrefList, _ = candidate.getFeaVariables()
    
    # This While ensures that 'errorType' will choose Randomly one 'restriction repair'
    flag_repair_done = False
    while(flag_repair_done == False):
        # Choosing one type of restriction to repair
        errorType = random.randrange(0,6)
        
        # (0) No repair -> Random Change
        if(errorType == 0):
            # Getting a new candidate (modified) 
            newCand = mutationRand(candidate, profList)
            # Setting the flag to finish the while
            flag_repair_done = True
        # (1) Fixing number of Relations
        if(errorType == 1):
            flag_repair_done, newCand = errorTypeF1(profList, prof_relationsList, relations, subjIsPrefList)
        # (2) Fixing number of Subj Preferences
        if(errorType == 2): 
            flag_repair_done, newCand = errorTypeF2(profList, prof_relationsList, relations, subjIsPrefList)
        # (3) Fixing number of Periods
        if(errorType == 3):
            flag_repair_done, newCand = errorTypeF345(profList, prof_relationsList, relations, periodPrefList, subjIsPrefList)
        # (4) Fixing number of QuadSabb
        if(errorType == 4):
            flag_repair_done, newCand = errorTypeF345(profList, prof_relationsList, relations, quadSabbNotPrefList, subjIsPrefList)
        # (5) Fixing number of Campus
        if(errorType == 5):
            flag_repair_done, newCand = errorTypeF345(profList, prof_relationsList, relations, campPrefList, subjIsPrefList)

    return newCand

#-------------------------------------------------------

# (1) Fixing number of Relations
def errorTypeF1(profList, prof_relationsList, relations, subjIsPrefList):
    # Choosing a professor to lose a relation
    # Roulette Wheel - more relations -> more weight
    numRelationsList = [len(i) for i in prof_relationsList]
    profRelList_Selected, _, _ = rouletteWheel(prof_relationsList, numRelationsList, objectiveNum=1, repos=True, negative=False)
    profLost_Index = prof_relationsList.index(profRelList_Selected[0])
    
    # Choosing a relation to be modified
    # Roulette Wheel - less preference -> more weight
    lessPrefValue = [2 - subjIsPrefList[profLost_Index][subjIndex] for subjIndex in prof_relationsList[profLost_Index]]
    will_change_index, _, _ = rouletteWheel(profRelList_Selected[0], lessPrefValue, objectiveNum=1, repos=True, negative=False)
    relation_will_change_index = will_change_index[0]
    
    # Recording original relation that will be modified
    subjList, oldProf = relations[relation_will_change_index]

    # Choosing new Prof to be in the relation with the Subj selected
    # Granting that the new Prof is different of the old one
    newProf = oldProf
    while(oldProf == newProf):
        # Roulette Wheel - more preference AND less relations -> more weight
        SubjPrefValuesList = [subjIsPrefList[relation_will_change_index] for subjIsPrefList in subjIsPrefList]
        # Removing possible Zeros to make the division
        prof_relations_final = [len(i) if len(i) != 0 else 0.5 for i in prof_relationsList]
        # Getting the values
        morePrefValueList = [float(SubjPrefValuesList[i] / prof_relations_final[i]) for i in range(len(profList))]
        # If there is only one Prof with value != 0.0
        if(morePrefValueList.count(0.0) == len(morePrefValueList) - 1):
            indexNotZero = [i for i in range(len(profList)) if morePrefValueList != 0.0]
            # If is the same of the old one
            if(oldProf == profList[indexNotZero[0]]): newProf = profList[random.randrange(len(profList))]
            # If not
            else: newProf = profList[indexNotZero[0]]
        # If there are more then 1 Prof to chose
        else: 
            newProf, _, _ = rouletteWheel(profList, morePrefValueList, objectiveNum=1, repos=True, negative=False)
            newProf = newProf[0]

    # Setting the new relation, creating new Candidate and returning it
    relations[relation_will_change_index]=[subjList,newProf]
    newCand = objects.Candidate()
    newCand.setRelationsList(relations)

    # Setting the flag to finish the while
    flag_repair_done = True

    return flag_repair_done, newCand

#-------------------------------------------------------

# Fixing number of Subj Preferences
def errorTypeF2(profList, prof_relationsList, relations, subjIsPrefList):
    # Choosing the professor to lose a relation
    # Roulette Wheel - less Preferences -> more weight 
    prefValuesList = [sum([subjIsPrefList[i][subjIndex] for subjIndex in prof_relationsList[i]]) for i in range(len(prof_relationsList))]
    # Resolving the values = Zero
    prefValuesList_Partial = [float(1.0 / value) if value != 0 else 1.0 for value in prefValuesList]
    # Resolving the Prof without relations (can not be selected)
    prefValuesList_Final = [prefValuesList_Partial[i] if len(prof_relationsList[i]) != 0 else 0.0 for i in range(len(prefValuesList_Partial))]
    profRelList_Selected, _, _ = rouletteWheel(prof_relationsList, prefValuesList_Final, objectiveNum=1, repos=True, negative=False)
    profLost_Index = prof_relationsList.index(profRelList_Selected[0])
    
    # Choosing a relation to be modified
    # Roulette Wheel - less preference -> more weight
    lessPrefValue = [2 - subjIsPrefList[profLost_Index][subjIndex] for subjIndex in prof_relationsList[profLost_Index]]
    will_change_index, _, _ = rouletteWheel(profRelList_Selected[0], lessPrefValue, objectiveNum=1, repos=True, negative=False)
    relation_will_change_index = will_change_index[0]
    
    # Recording original relation that will be modified
    subjList, oldProf = relations[relation_will_change_index]

    # Choosing new Prof to be in the relation with the Subj selected
    # Granting that the new Prof is different of the old one
    newProf = oldProf
    while(oldProf == newProf):
        # Roulette Wheel - more preference AND less relations -> more weight
        SubjPrefValuesList = [subjIsPrefList[relation_will_change_index] for subjIsPrefList in subjIsPrefList]
        # Removing possible Zeros to make the division
        prof_relations_final = [len(i) if len(i) != 0 else 0.5 for i in prof_relationsList]
        # Getting the values
        morePrefValueList = [float(SubjPrefValuesList[i] / prof_relations_final[i]) for i in range(len(profList))]
        # If there is only one Prof with value != 0.0
        if(morePrefValueList.count(0.0) == len(morePrefValueList) - 1):
            indexNotZero = [i for i in range(len(profList)) if morePrefValueList != 0.0]
            # If is the same of the old one
            if(oldProf == profList[indexNotZero[0]]): newProf = profList[random.randrange(len(profList))]
            # If not
            else: newProf = profList[indexNotZero[0]]
        # If there are more then 1 Prof to chose
        else: 
            newProf, _, _ = rouletteWheel(profList, morePrefValueList, objectiveNum=1, repos=True, negative=False)
            newProf = newProf[0]

    # Setting the new relation, creating new Candidate and returning it
    relations[relation_will_change_index]=[subjList,newProf]
    newCand = objects.Candidate()
    newCand.setRelationsList(relations)

    # Setting the flag to finish the while
    flag_repair_done = True

    return flag_repair_done, newCand

#-------------------------------------------------------

# (3) Fixing number of Periods
# (4) Fixing number of QuadSabb
# (5) Fixing number of Campus
def errorTypeF345(profList, prof_relationsList, relations, XPref, subjIsPrefList):
    # Checking if there are problems to fix
    if(len(XPref) == 0):
        newCand = objects.Candidate()
        newCand.setRelationsList(relations)
        # Setting the flag to NOT finish the while
        flag_repair_done = False
    else:
        # Granting that the 'errorType' do not change good relations without Problems to repair
        notGoodList = [1 if len(prof_relationsList[i]) != len(XPref[i]) else 0 for i in range(len(prof_relationsList))]
        if(notGoodList.count(1) == 0):
            newCand = objects.Candidate()
            newCand.setRelationsList(relations)
            # Setting the flag to NOT finish the while
            flag_repair_done = False
        else:
            # Choosing the professor to lose a relation
            # Roulette Wheel - less XPref -> more weight
            conflictsList = [[subjIndex for subjIndex in prof_relationsList[i] if XPref[i].count(subjIndex) == 0] for i in range(len(prof_relationsList))] 
            prefValuesList = [len(i) for i in conflictsList]
            profRelList_Selected, _, _ = rouletteWheel(conflictsList, prefValuesList, objectiveNum=1, repos=True, negative=False)
            profLost_Index = conflictsList.index(profRelList_Selected[0])
            
            # Choosing the relation to be modified
            # Roulette Wheel - less preference -> more weight
            lessPrefValue = [2 - subjIsPrefList[profLost_Index][subjIndex] for subjIndex in conflictsList[profLost_Index]]
            will_change_index, _, _ = rouletteWheel(profRelList_Selected[0], lessPrefValue, objectiveNum=1, repos=True, negative=False)
            relation_will_change_index = will_change_index[0]
            
            # Recording original relation that will be modified
            subjList, oldProf = relations[relation_will_change_index]

            # Choosing new Prof to be in the relation with the Subj selected
            # Granting that the new Prof is different of the old one
            newProf = oldProf
            while(oldProf == newProf):
                # Roulette Wheel - more preference AND less relations -> more weight
                SubjPrefValuesList = [subjIsPrefList[relation_will_change_index] for subjIsPrefList in subjIsPrefList]
                # Removing possible Zeros to make the division
                prof_relations_final = [len(i) if len(i) != 0 else 0.5 for i in prof_relationsList]
                # Getting the values
                morePrefValueList = [float(SubjPrefValuesList[i] / prof_relations_final[i]) for i in range(len(profList))]
                # If there is only one Prof with value != 0.0
                if(morePrefValueList.count(0.0) == len(morePrefValueList) - 1):
                    indexNotZero = [i for i in range(len(profList)) if morePrefValueList != 0.0]
                    # If is the same of the old one
                    if(oldProf == profList[indexNotZero[0]]): newProf = profList[random.randrange(len(profList))]
                    # If not
                    else: newProf = profList[indexNotZero[0]]
                # If there are more then 1 Prof to chose
                else: 
                    newProf, _, _ = rouletteWheel(profList, morePrefValueList, objectiveNum=1, repos=True, negative=False)
                    newProf = newProf[0]

            # Setting the new relation, creating new Candidate and returning it
            relations[relation_will_change_index]=[subjList,newProf]
            newCand = objects.Candidate()
            newCand.setRelationsList(relations)

            # Setting the flag to finish the while
            flag_repair_done = True

    return flag_repair_done, newCand

#==============================================================================================================

# Make a selection of the solutions from all Infeasible Pop.('infPool' and 'solutionsI')
def selectionI(infPool, solutionsI, maxNumCand_perPop):
    # Check if the Infeasible pop. is empty
    if(len(solutionsI.getCandList()) != 0 or len(infPool.getCandList()) != 0):
        # Gathering both lists (infPool and solutionsI)
        infeasibles_List = solutionsI.getCandList() + infPool.getCandList()
        
        # Check if is needed to make a selection process
        if(len(infeasibles_List) > maxNumCand_perPop):
            # Roulette Wheel Selection
            fitnessList = [cand.getFitness() for cand in infeasibles_List] # Negative values
            infeasibles_List, _, _ = rouletteWheel(infeasibles_List, fitnessList, maxNumCand_perPop, repos=False, negative=True)
            
        # Updating the (new) 'solutionsI' list to the next generation
        solutionsI.setCandList(infeasibles_List)
            
        if(printSteps == 1): print("Inf. Selection/", end='')
        
#==============================================================================================================

# Make a Selection of the best solutions from Feasible Pop.
def selectionF(feaPool, solutionsF, maxNumCand_perPop, pctElitism=100):
    # Check if the Feasible pop. is empty
    if(len(solutionsF.getCandList()) != 0 or len(feaPool.getCandList()) != 0):
        # Gathering both lists (feaPool and solutions)
        feasibles_List = solutionsF.getCandList() + feaPool.getCandList()
        
        # Check if is needed to make a selection process
        if(len(feasibles_List) > maxNumCand_perPop):
            # Gathering all Fitness
            listFit = [cand.getFitness() for cand in feasibles_List]
            
            # Defining the division of number of candidates between selections process
            elitismNum = maxNumCand_perPop * pctElitism / 100.0
            if(elitismNum > 0.0 and elitismNum < 1.0): elitismNum = 1
            elitismNum = int(elitismNum)
            roulNum = maxNumCand_perPop - elitismNum

            # Elitism and Roulette Selection
            maxFeasibles_List, rest_objectsList, rest_valuesList = elitismSelection(feasibles_List, listFit, elitismNum)
            selectedObj, _, _ = rouletteWheel(rest_objectsList, rest_valuesList, roulNum, repos=False, negative=False)
            feasibles_List = maxFeasibles_List + selectedObj
        
        # Updating the (new) 'solutionsF' list to the next generation
        solutionsF.setCandList(feasibles_List)
        
        if(printSteps == 1): print("Feas. Selection/", end='')

#==============================================================================================================

# Make a rand mutation into a solution
def mutationRand(candidate, profList):
    # Getting all relations from Candidate
    relations = candidate.getRelationsList().copy()
    
    # Choosing randomly a relation to be modified
    original = random.randrange(len(relations))
    # Recording the Original Relation
    subjList, oldProf = relations[original]
    
    # Granting that the 'newProf' is different from the 'oldProf'
    newProf = oldProf
    while(oldProf == newProf):
        # Finding randomly a new Prof
        change = random.randrange(len(profList))
        newProf = profList[change]
    
    # Setting the new Relation modified, creating and setting a new Candidate
    relations[original]=[subjList,newProf]
    newCand = objects.Candidate()
    newCand.setRelationsList(relations)
    
    # Returning the new Candidate generated
    return newCand
    
#==============================================================================================================

# Make a crossover between two solutions
def crossover(cand1, cand2, twoPoints=None, firstHalf=None, notEqualParent=None):
    # The number of changes between parents will always be equal (same crossover segment size), never same size of Num of Parents Relations
    # twoPoints = False -> its chosen only one point, will have changes from the point till the rest of the relations
    # firstHalf = True -> changes from the beginning till the one point choose
    # notEqualParent = True -> avoid the occurrence of children equal to his parents
    
    # What is equal 'None' will be a random choice
    if(twoPoints == None): twoPoints = random.choice([True, False])
    if(firstHalf == None): twoPoints = random.choice([True, False])
    if(notEqualParent == None): notEqualParent = random.choice([True, False])
    
    # Getting all relations from Candidates to work with
    relations1, relations2 = cand1.getRelationsList(), cand2.getRelationsList()
    
    # OnePoint type:
    if(twoPoints == False):
        # Prioritizing change of relations on first half of the candidates
        if(firstHalf == True):
            point1 = 0 # Default point in 'firstHalf' mode
            point2 = random.randrange(len(relations1)) # Randomly choosing other point that can be equal to 'point1'
            # Granting that not occur only a copy of parents - the chosen point is not the last relation
            if(notEqualParent == True):
                while(point2 == len(relations1)-1): point2 = random.randrange(len(relations1))
        
        # Prioritizing change of relations on second half of the candidates
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
    newCand1.setRelationsList(relations1)
    newCand2.setRelationsList(relations2)
    
    # Returning the new Candidates
    return newCand1, newCand2

#==============================================================================================================

# Selection by elitism
def elitismSelection(objectsList, valuesList, objectiveNum):
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
def rouletteWheel(objectsList, valuesList, objectiveNum, repos=True, negative=False):
    # objectiveNum: Num of objects will be selected
    # repos: Type of wheel (with reposition)
    # negative = True -> modify the range of values
    #   Since the value of Fitness is in the range of '-1' and '0' it is needed to be modified
    #   Modifying the values to put it into a range of '0' and '1'

    # List with the selected Objects
    selectedObj = []
    # Flag that allows to make all important calcs at least one time when the Roulette is configured to have Reposition
    reCalc = True

    while(len(selectedObj) < objectiveNum):
        # Allow the Updating of the data for the next Roulette Round without the object that was recent selected on past round
        if(reCalc == True):
            # When the Roulette process does have reposition of objects
            if(repos == True): reCalc = False
            
            # Find the total Value of the Objects
            totalValue = sum([float(value) if negative == False else 1.0 + float(value) for value in valuesList])
            
            # If all values are Zero
            if(totalValue == 0.0):
                valuesList = [1.0 for _ in valuesList]
                totalValue = float(len(valuesList))

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
        r = float(random.randrange(101) / 100.0)
        #r = float(random.randrange(0, 1, 0.001))
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
def stop(curr_Iter, maxNum_Iter, lastMaxFitFea_Iter, convergDetect, maxFitFea, stopFitValue):
    #import pdb; pdb.set_trace()
    if(curr_Iter > maxNum_Iter): return True # Reached max num of iterations
    if(stopFitValue != 0 and maxFitFea >= stopFitValue): return True # Reached max fit value
    if(convergDetect != 0 and curr_Iter - lastMaxFitFea_Iter > convergDetect): return True # Reached convergence num of iterations
    return False # Continues the run with same num of iterations

# Ask to user if wants to continue the run with more iterations
def ask(value):
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
