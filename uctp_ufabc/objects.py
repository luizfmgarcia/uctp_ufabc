# Objects used on UCTP algorithm

#==============================================================================================================

# Keep the data of a professor
class Prof:
    def __init__(self, name, period, charge, quadriSabbath, prefCampus, prefSubjQ1List, prefSubjQ2List, prefSubjQ3List, prefSubjLimList):
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
    
#==============================================================================================================

# Keep the data of a Candidate
class Candidate:
    def __init__(self):
        # Main Data
        self.listRelations = []
        self.fitness = 0.0
        
        # Useful Variables that carries more info about the Candidate
        # Each List contains, for each prof, lists of Subj Indexs
        self.prof_relations = []
        self.conflicts_i2 = []
        self.conflicts_i3 = []
        self.subjPref = []
        self.periodPref = []
        self.quadSabbNotPref = []
        self.campusPref = []
        self.difCharge = []
        
    def getFitness(self):
        return self.fitness
    
    def setFitness(self, fit):
        self.fitness = fit
    
    def getFeaVariables(self):
        return self.prof_relations, self.subjPref, self.periodPref, self.quadSabbNotPref, self.campusPref, self.difCharge
    
    def setFeaVariables(self, prof_relations, subjPref, periodPref, quadSabbNotPref, campusPref, difCharge):
        self.prof_relations = prof_relations
        self.subjPref = subjPref
        self.periodPref = periodPref
        self.quadSabbNotPref = quadSabbNotPref
        self.campusPref = campusPref
        self.difCharge = difCharge
    
    def getInfVariables(self):
        return  self.prof_relations, self.conflicts_i2, self.conflicts_i3
    
    def setInfVariables(self, prof_relations, conflicts_i2, conflicts_i3):
        self.prof_relations = prof_relations
        self.conflicts_i2 = conflicts_i2
        self.conflicts_i3 = conflicts_i3
    
    def getList(self):
        return self.listRelations
    
    def setList(self, List):
        self.listRelations = List
    
    def addRelation(self, Subject, Prof):
        relation = [Subject, Prof]
        self.listRelations.append(relation)
    
    def removeRelation(self, relation):
        self.listRelations.remove(relation)
    
#==============================================================================================================

# Keep all Candidates obtained during a run of the algorithm
class Solutions:
    def __init__(self):
        self.listCandidates = []
    
    def getList(self):
        return self.listCandidates
    
    def setList(self, List):
        self.listCandidates = List
    
    def resetList(self):
        self.listCandidates = []
    
    def addCand(self, candidate):
        self.listCandidates.append(candidate)
    
    def removeCand(self, candidate):
        self.listCandidates.remove(candidate)
    
#==============================================================================================================