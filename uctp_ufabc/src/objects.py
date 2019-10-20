# Objects used on UCTP algorithm

#==============================================================================================================

# Keep the data of a professor
class Prof:
    def __init__(self, name, period, charge, quadriSabbath, prefCampus, prefSubjQ1List, prefSubjQ2List, 
                 prefSubjQ3List, prefSubjLimList):
        self.name = name
        self.period = period
        self.charge = charge
        self.quadriSabbath = quadriSabbath
        self.prefCampus = prefCampus
        self.prefSubjQ1List = prefSubjQ1List
        self.prefSubjQ2List = prefSubjQ2List
        self.prefSubjQ3List = prefSubjQ3List
        self.prefSubjLimList = prefSubjLimList
    
    def get(self):
        return self.name, self.period, self.charge, self.quadriSabbath, self.prefCampus, self.prefSubjQ1List, self.prefSubjQ2List, self.prefSubjQ3List, self.prefSubjLimList
    
    def getPrefSubjLists(self): return self.prefSubjQ1List, self.prefSubjQ2List, self.prefSubjQ3List, self.prefSubjLimList

    def getName(self): return self.name

    def getPeriod(self): return self.period

    def getCharge(self): return self.charge

    def getQuadriSabbath(self): return self.quadriSabbath

    def getPrefCampus(self): return self.prefCampus

#==============================================================================================================

# Keep the data of a subject
class Subject:
    def __init__(self, level, code, name, quadri, period, campus, charge, timetableList):
        self.level = level
        self.code = code
        self.name = name
        self.quadri = quadri
        self.period = period
        self.campus = campus
        self.charge = charge
        self.timetableList = timetableList

    def get(self):
        return self.level, self.code, self.name, self.quadri, self.period, self.campus, self.charge, self.timetableList

    def getLevel(self): return self.level

    def getCode(self): return self.code

    def getName(self): return self.name

    def getQuadri(self): return self.quadri

    def getPeriod(self): return self.period

    def getCampus(self): return self.campus

    def getCharge(self): return self.charge

    def getTimeTableList(self): return self.timetableList

#==============================================================================================================

# Keep the data of a Candidate
class Candidate:
    def __init__(self):
        # Main Data
        self.relationsList = []
        self.fitness = 0.0
        
        # Useful (for some functions) Variables that carries more info about the Candidate
        # Each List contains, for each prof, lists of Subj Indexes related to a characteristic
        self.prof_relationsList = []
        self.i2_conflictsList = []
        self.i3_conflictsList = []
        self.numSubjPrefList = []
        self.periodPrefList = []
        self.quadSabbNotPrefList = []
        self.campPrefList = []
        self.difChargeList = []
    
    def addRelation(self, Subject, Prof):
        relation = [Subject, Prof]
        self.relationsList.append(relation)
    
    def setRelationsList(self, List): self.relationsList = List
    
    def getRelationsList(self): return self.relationsList

    def setFitness(self, fit): self.fitness = fit

    def getFitness(self): return self.fitness
    
    def setInfVariables(self, prof_relationsList, i2_conflictsList, i3_conflictsList):
        self.prof_relationsList = prof_relationsList
        self.i2_conflictsList = i2_conflictsList
        self.i3_conflictsList = i3_conflictsList
    
    def getInfVariables(self):
        return  self.prof_relationsList, self.i2_conflictsList, self.i3_conflictsList
    
    def setFeaVariables(self, prof_relationsList, numSubjPrefList, periodPrefList, quadSabbNotPrefList, campPrefList, difChargeList):
        self.prof_relationsList = prof_relationsList
        self.numSubjPrefList = numSubjPrefList
        self.periodPrefList = periodPrefList
        self.quadSabbNotPrefList = quadSabbNotPrefList
        self.campPrefList = campPrefList
        self.difChargeList = difChargeList

    def getFeaVariables(self):
        return self.prof_relationsList, self.numSubjPrefList, self.periodPrefList, self.quadSabbNotPrefList, self.campPrefList, self.difChargeList

#==============================================================================================================

# Keep all Candidates obtained during a run of the algorithm
class Solutions:
    def __init__(self): self.candidatesList = []

    def addCand(self, candidate): self.candidatesList.append(candidate)

    def setCandList(self, List): self.candidatesList = List

    def getCandList(self): return self.candidatesList

    def resetCandList(self): self.candidatesList = []

#==============================================================================================================