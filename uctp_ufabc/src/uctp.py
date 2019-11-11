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

#-------------------------------------------------------

# Create new Candidate Full-Random
def newCandRand(subjList, profList):
    candidate = objects.Candidate()
    # Follow the subjects in 'subjList', in order, and for each one, choose a professor randomly
    for sub in subjList: candidate.addRelation(sub, profList[random.randrange(len(profList))])
    return candidate

#==============================================================================================================

# Extracts info about what Subj appears in which Prof PrefList
def extractSubjIsPref(subjList, profList):
    # Lists for each Prof, where it is '1' if Subj in respective index is on Prof List of Pref but not same Quadri
    # '2' if same quadri
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
def twoPop(solutionsNoPop, infPool, feaPool, profList, subjList, weightsList, numInfWeights):
    # Granting that the Lists will be empty to receive new Solutions
    infPool.resetCandList()
    feaPool.resetCandList()
    
    for cand in solutionsNoPop.getCandList():
        # Classification by checking feasibility
        pop = checkFeasibility(cand, profList, subjList, weightsList, numInfWeights)
        if(pop == "feasible"): feaPool.addCand(cand)
        elif(pop == "infeasible"): infPool.addCand(cand)
    
    # Granting that the List will be empty to next operations
    solutionsNoPop.resetCandList()
    
    if(printSteps == 1): print("Checked Feasibility (new Candidates)/", end='')

#==============================================================================================================

# Detect the violation of a Restriction into a candidate
def checkFeasibility(candidate, profList, subjList, weightsList, numInfWeights):
    # As part of the Candidate's Prof-Subj relations (with both Feasible and the Infeasible) will be traversed to check they Feasibility here,
    # instead of re-pass an entire Infeasible Candidate again in the 'calc_fitInfeas', the calculation of its Fitness will already be done
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
        i1 = float(prof_relationsList.count([]) / (len(profList) - 1.0))
        i2 = float(sum([len(i) for i in i2_conflictsList]) / len(subjList))
        i3 = float(sum([len(i) for i in i3_conflictsList]) / len(subjList))
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
    f1 = 1.0 - float(sum_chargesRelative / len(profList))
    f2 = float(sum_Satisfaction / len(profList))
    f3 = float(sum_quadSabbNotPref / len(subjList))
    f4 = float(sum_periodPref / len(subjList))
    f5 = float(sum_campusPref / len(subjList))
    f6 = 1.0 - float(sum_relationsRelative / len(profList))
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
    charges_EachProf = [profList[i].getCharge() for i in range(len(profList))]

    # Counting the occurrences, filling the vectors
    for i in range(len(prof_relationsList)):
        # Summing all chargers of all relations of this Prof
        charges_eachProfRelations[i] = sum([subjList[sIndex].getCharge() for sIndex in prof_relationsList[i]])
    
    # Difference of Prof Charge and the sum of all of its Subj-Relations
    difChargeList = [charges_EachProf[i] - charges_eachProfRelations[i] for i in range(len(profList))]

    # Relative weigh of excess or missing charge for each Prof - based on the absolute credit difference
    # between the credits requested by the Prof and the sum off all Subj related to it
    charges_relative = [float(abs(difChargeList[i]) / charges_EachProf[i]) for i in range(len(profList))]
    
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
                finalQX[i][prof_index] = float(finalQX[i][prof_index] / total_weight)
    
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

    # Relative value of quality of all relations for each Prof (2 is the max value of quality - same quadri of pref list)
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

# Generate new solutions from the current Feasible population
def offspringF(solutionsNoPop, solutionsF, profList, subjList, subjIsPrefList, maxNumCand_perPop, pctParentsCross, reposCross, twoPointsCross):
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
            # If have at most 1 solution (insufficient to make any crossover) - then all solutions will generate a child through a mutation
            for cand in solutionsF.getCandList(): solutionsNoPop.addCand(mutationF(cand, profList, subjList, subjIsPrefList))
        # If we have at least 2 solutions
        else:
            # Roulette Wheel to choose solutions to become Parents
            fitnessList = [cand.getFitness() for cand in solutionsF.getCandList()]
            parentsSolFeas, notParents_objectsList, _ = rouletteWheel(solutionsF.getCandList(), fitnessList, objectiveNum, reposCross)
            
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
                newCand1, newCand2 = crossover(parentsSolFeas[parent1], parentsSolFeas[parent2], twoPointsCross)

                # Removing used parents to make a new selection of Parents
                parent2 = parentsSolFeas[parent2]
                parentsSolFeas.remove(parentsSolFeas[parent1])
                parentsSolFeas.remove(parent2)
                
                # adding the new candidates generated to childSolFeas
                childSolFeas.append(newCand1)
                childSolFeas.append(newCand2)

            # Adding the child generated by crossover to 'solutionsNoPop'
            for cand in childSolFeas:
                solutionsNoPop.addCand(cand)

            # Make Mutation with all the candidates that were not chosen to be Parents right before
            for cand in notParents_objectsList:
                # Making a not random mutation
                newCand = mutationF(cand, profList, subjList, subjIsPrefList)
                # Adding the child not generated by crossover to 'solutionsNoPop'
                solutionsNoPop.addCand(newCand)

        if(printSteps == 1): print("Feas. Offspring/", end='')
        
#==============================================================================================================

# Make a mutation into a infeasible candidate
def mutationI(candidate, profList, subjList, subjIsPrefList):
    # Getting data to work with
    relations = candidate.getRelationsList()[:]
    prof_relationsList, i2_conflictsList, i3_conflictsList = candidate.getInfVariables()

    # This While ensures that 'problemType' will choose Randomly one 'restriction repair'
    flag_work_done = False
    while(flag_work_done == False):
        # Choosing one type of restriction to repair
        problemType = random.randrange(0,4)
        
        # (0) No repair -> Random Change
        if(problemType == 0): flag_work_done, newCand = mutationRand(candidate, profList)
        # (1) Prof without relations (with no Subjects) in 'prof_relationsList'
        elif(problemType == 1):
            # Granting that the 'problemType' do not change good relations without restrictions to repair
            if(prof_relationsList.count([]) != 0):
                flag_work_done, newCand = mutationDeterm(profList, prof_relationsList, relations, subjIsPrefList, prof_relationsList)
        else:
            # (2) 2 or more Subjects (related to the same Prof) with same 'quadri', 'day' and 'hour' in 'i2_conflictsList'
            if(problemType == 2): iX_conflictsList = i2_conflictsList
            # (3) 2 or more Subjects (related to the same Prof) with same 'day' and 'quadri' but different 'campus' in 'i3_conflictsList'
            if(problemType == 3): iX_conflictsList = i3_conflictsList
            # Granting that the 'problemType' do not change good relations without restrictions to repair
            if(len(iX_conflictsList) != 0 and iX_conflictsList.count([]) != len(iX_conflictsList)):
                flag_work_done, newCand = mutationDeterm(profList, prof_relationsList, relations, subjIsPrefList, iX_conflictsList)
    return newCand

#==============================================================================================================

# Make a mutation into a feasible candidate
def mutationF(candidate, profList, subjList, subjIsPrefList):
    # Getting data to work with
    relations = candidate.getRelationsList()[:]
    prof_relationsList, _, periodPrefList, quadSabbNotPrefList, campPrefList, _ = candidate.getFeaVariables()
    
    # This While ensures that 'adjustType' will choose Randomly one 'Improvement work'
    flag_work_done = False
    while(flag_work_done == False):
        # Choosing one type of 'Improvement work'
        adjustType = random.randrange(0,6)
        
        # (0) No 'Improvement work' -> Random Change
        if(adjustType == 0): flag_work_done, newCand = mutationRand(candidate, profList)
        # (1) Improving number of Relations
        elif(adjustType == 1): flag_work_done, newCand = mutationDeterm(profList, prof_relationsList, relations, subjIsPrefList, prof_relationsList)
        # (2) Improving number of Subj Preferences
        elif(adjustType == 2):
            # Building a list with relations that is NOT Pref
            notPrefList = [[subjIndex for subjIndex in prof_relationsList[i] if subjIsPrefList[i][subjIndex] == 0] for i in range(len(prof_relationsList))]
            # Granting that the 'adjustType' do not change good relations without Problems to improve
            if(notPrefList.count([]) != len(notPrefList)):
                flag_work_done, newCand = mutationDeterm(profList, prof_relationsList, relations, subjIsPrefList, prof_relationsList)
        else:
            # (3) Improving number of Periods
            if(adjustType == 3): XPref = periodPrefList
            # (4) Improving number of QuadSabb
            if(adjustType == 4): XPref = quadSabbNotPrefList
            # (5) Improving number of Campus
            if(adjustType == 5): XPref = campPrefList
            
            if(len(XPref) != 0):
                # Building a list with relations that is NOT Pref
                notPrefList = [[subjIndex for subjIndex in prof_relationsList[i] if [i].count(subjIndex) == 0] for i in range(len(prof_relationsList))]
                # Granting that the 'adjustType' do not change good relations without Problems to improve
                if(notPrefList.count([]) != len(notPrefList)):
                    flag_work_done, newCand = mutationDeterm(profList, prof_relationsList, relations, subjIsPrefList, notPrefList)
    return newCand

#==============================================================================================================

# Make a selection of the solutions from all Infeasible Pop.('infPool' and 'solutionsI')
def selectionI(infPool, solutionsI, maxNumCand_perPop, reposSelInf):
    # Check if the Infeasible pop. is empty
    if(len(solutionsI.getCandList()) != 0 or len(infPool.getCandList()) != 0):
        # Gathering both lists (infPool and solutionsI)
        infeasibles_List = solutionsI.getCandList() + infPool.getCandList()
        
        # Check if is needed to make a selection process
        if(len(infeasibles_List) > maxNumCand_perPop):
            # Roulette Wheel Selection
            # Since the value of Fitness is in the range of '-1' and '0' it is needed to be modified to a range of '0' and '1'
            fitnessList = [1.0 + cand.getFitness() for cand in infeasibles_List]
            infeasibles_List, _, _ = rouletteWheel(infeasibles_List, fitnessList, maxNumCand_perPop, reposSelInf)
            
        # Updating the (new) 'solutionsI' list to the next generation
        solutionsI.setCandList(infeasibles_List)
            
        if(printSteps == 1): print("Inf. Selection/", end='')
        
#==============================================================================================================

# Make a Selection of the best solutions from Feasible Pop.
def selectionF(feaPool, solutionsF, maxNumCand_perPop, pctElitism, reposSelFea):
    # Check if the Feasible pop. is empty
    if(len(solutionsF.getCandList()) != 0 or len(feaPool.getCandList()) != 0):
        # Gathering both lists (feaPool and solutions)
        feasibles_List = solutionsF.getCandList() + feaPool.getCandList()
        
        # Check if is needed to make a selection process
        if(len(feasibles_List) > maxNumCand_perPop):
            # Defining the division of number of candidates between selections process
            elitismNum = maxNumCand_perPop * pctElitism / 100.0
            if(elitismNum > 0.0 and elitismNum < 1.0): elitismNum = 1
            else: elitismNum = int(elitismNum)
            roulNum = maxNumCand_perPop - elitismNum

            # Elitism and Roulette Selection
            listFit = [cand.getFitness() for cand in feasibles_List]
            maxFeasibles_List, rest_objectsList, rest_valuesList = elitismSelection(feasibles_List, listFit, elitismNum)
            selectedObj, _, _ = rouletteWheel(rest_objectsList, rest_valuesList, roulNum, reposSelFea)
            feasibles_List = maxFeasibles_List + selectedObj
        
        # Updating the (new) 'solutionsF' list to the next generation
        solutionsF.setCandList(feasibles_List)
        
        if(printSteps == 1): print("Feas. Selection/", end='')

#==============================================================================================================

# Make a rand mutation into a solution
def mutationRand(candidate, profList):
    # Getting all relations from Candidate
    relations = candidate.getRelationsList()[:]
    
    # Choosing randomly a relation to be modified
    original = random.randrange(len(relations))
    # Recording the Original Relation
    subj, oldProf = relations[original]
    
    # Granting that the 'newProf' is different from the 'oldProf'
    newProf = oldProf
    while(oldProf == newProf):
        # Finding randomly a new Prof
        change = random.randrange(len(profList))
        newProf = profList[change]
    
    # Setting the new Relation modified, creating and setting a new Candidate
    relations[original]=[subj,newProf]
    newCand = objects.Candidate()
    newCand.setRelationsList(relations)
    
    # Setting the flag to finish the while
    flag_work_done = True

    # Returning the new Candidate generated
    return flag_work_done, newCand

#==============================================================================================================

# Make some deterministic type of adjustment changing some 'bad' relation
def mutationDeterm(profList, prof_relationsList, relations, subjIsPrefList, problemList):
    # Choosing a professor to lose a relation
    # Roulette Wheel - more 'bad' relations -> more weight
    weightList = [len(i) for i in problemList]
    problemSubList_selected, _, _ = rouletteWheel(problemList, weightList, objectiveNum=1, repos=0)
    profLost_Index = problemList.index(problemSubList_selected[0])

    # Choosing the relation to be modified
    # Roulette Wheel - less preference -> more weight
    lessPrefValue = [2 - subjIsPrefList[profLost_Index][subjIndex] for subjIndex in problemList[profLost_Index]]
    will_change_index, _, _ = rouletteWheel(problemSubList_selected[0], lessPrefValue, objectiveNum=1, repos=0)
    relation_will_change_index = will_change_index[0]

    # Recording original relation that will be modified
    subjList, oldProf = relations[relation_will_change_index]

    # Choosing new Prof to be in the selected relation
    # Granting that the new Prof is different from the old one
    newProf = oldProf
    while(oldProf == newProf):
        # Roulette Wheel - more preference AND less relations -> more weight
        SubjPrefValuesList = [subjIsPref_subList[relation_will_change_index] for subjIsPref_subList in subjIsPrefList]
        # Removing possible Zeros to make the division
        prof_relations_final = [len(i) if len(i) != 0 else 0.5 for i in prof_relationsList]
        # Getting the weights values
        morePrefValueList = [float(SubjPrefValuesList[i] / prof_relations_final[i]) for i in range(len(profList))]
        # If there is only one Prof with value != 0.0
        if(morePrefValueList.count(0.0) == len(morePrefValueList) - 1):
            indexNotZero = [i for i in range(len(profList)) if morePrefValueList[i] != 0.0]
            # If is the same of the old one - random choice
            if(oldProf == profList[indexNotZero[0]]): newProf = profList[random.randrange(len(profList))]
            # If not
            else: newProf = profList[indexNotZero[0]]
        # If there are more then 1 Prof to chose
        else: 
            newProf, _, _ = rouletteWheel(profList, morePrefValueList, objectiveNum=1, repos=0)
            newProf = newProf[0]

    # Setting the new relation, creating new Candidate and returning it
    relations[relation_will_change_index]=[subjList, newProf]

    # Setting the flag to finish the while
    flag_work_done = True

    # Generating a new candidate
    newCand = objects.Candidate()
    newCand.setRelationsList(relations)

    return flag_work_done, newCand

#==============================================================================================================

# Make a crossover between two solutions
def crossover(cand1, cand2, twoPointsCross=-1):
    # The number of changes between parents will always be equal (same crossover segment size), never same size of Num of Parents Relations
    # twoPointsCross = False -> its chosen only one point, will have changes from the 0 relation till the chosed point
    
    # What is equal '-1' will be a random choice
    if(twoPointsCross == -1): twoPointsCross = random.choice([True, False])
    
    # Getting all relations from Candidates to work with
    relations1 = cand1.getRelationsList()[:]
    relations2 = cand2.getRelationsList()[:]

    # OnePoint type:
    if(not twoPointsCross):
        point1 = 0 # Default initial point ('first-half') - if we make changes on 'second-half' the result woud be the same
        point2 = random.randrange(len(relations1)) # Randomly choosing other point that can be equal to 'point1'
        # Granting that not occur only a copy of parents - the chosen point is not the last relation
        while(point2 == len(relations1)-1): point2 = random.randrange(len(relations1))
    
    # twoPointsCross Type
    else:
        # Generating, randomly two numbers to create a patch - can be a single modification (when p1=p2)
        point1, point2 = random.randrange(len(relations1)), random.randrange(len(relations1))
        # Granting that 'point2' is bigger than 'point1'
        if(point2 < point1):
            p = point1
            point1 = point2
            point2 = p

        # Granting that the crossover do not only copy all relations of one Cand to the another
        while(point2 - point1 == len(relations1) - 1):
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
    objectsList = objectsList[:]
    valuesList = valuesList[:]

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
def rouletteWheel(objectsList, valuesList, objectiveNum, repos=0):
    # objectiveNum: Num of objects will be selected
    # repos: Type of wheel (with reposition)
    
    # Making a copy of the original lists to work with
    objectsList = objectsList[:]
    valuesList = valuesList[:]

    # List with the selected Objects
    selectedObj = []
    # Flag that allows to make all important calcs at least one time when the Roulette is configured to have Reposition
    reCalc = True

    while(len(selectedObj) < objectiveNum):
        # Allow the Updating of the data for the next Roulette Round without the object that was recent selected on past round
        if(reCalc):
            # When the Roulette process does have reposition of objects
            if(repos): reCalc = False
            
            # Find the total Value of the Objects
            totalValue = sum([value for value in valuesList])
            
            # If all values are Zero
            if(totalValue == 0.0):
                valuesList = [1.0 for _ in valuesList]
                totalValue = len(valuesList)

            # Calculate the prob. of a selection for each object
            probObj = [float(value / totalValue) for value in valuesList]
            
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
                if(not repos):
                    # Removing the selected object/value from 'valuesList' to do next roulette process
                    valuesList.pop(i)
                    objectsList.pop(i)
                break
            probPrev = cumulativeProbObj[i]

    # Removing from 'objectsList' the selected objects (not removed before because of the reposition)
    # If there are repeated objects, (objectsList + selectedObj) will be larger then original objectsList size
    if(repos):
        for i in selectedObj:
            try:
                index = objectsList.index(i)
                objectsList.pop(index)
                valuesList.pop(index)
            except ValueError: index = -1

    return  selectedObj, objectsList, valuesList

#==============================================================================================================

# Detect the stop condition
def stop(asks, curr_Iter, maxNum_Iter, lastMaxFit_Iter, convergDetect, maxFitFea):
    if(curr_Iter == maxNum_Iter): return (True if asks == 0 else ioData.askStop()) # Reached max num of iterations
    if(convergDetect != 0 and curr_Iter - lastMaxFit_Iter == convergDetect): return (True if asks == 0 else ioData.askStop()) # Reached convergence num of iterations
    return False # Continues the run with same num of iterations

#==============================================================================================================
