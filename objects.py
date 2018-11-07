# Objects used on UCTP algorithm

# Keep the details of a professor
class Prof:
    def __init__(self, name, period, charge, quadriSabbath):
        self.name = name
        self.period = period
        self.charge = charge
        self.quadriSabbath = quadriSabbath
        #self.prefSubject = prefSubject
     
    def get(self):
        return self.name, self.period, self.charge, self.quadriSabbath

# Keep the details of a subject
class Subject:
    def __init__(self, level, code, name, quadri, period, campus, charge):
        self.level = level
        self.code = code
        self.name = name
        self.quadri = quadri
        self.period = period
        self.campus = campus
        self.charge = charge
        #self.daysList = daysList
        #self.hoursList = hoursList
    
    def get(self):
        return self.level, self.code, self.name, self.quadri, self.period, self.charge    

# Keep the details of a Candidate
class Candidate:
    def __init__(self):
        self.listRelations = []
        self.fitness = 0.0
        
    def getFitness(self): 
        return self.fitness
            
    def setFitness(self, fit): 
        self.fitness = fit   
    
    def getList(self):
        return self.listRelations
    
    def setList(self, list):
        self.listRelations = list
            
    def addRelation(self, Subject, Prof):
        relation = [Subject, Prof]
        self.listRelations.append(relation)
        
    def removeRelation(self, relation):
        self.listRelations.remove(relation)       
                
# Keep all Candidates obtained during a run of the algorithm
class Solutions:
    def __init__(self):
        self.listCandidates = []
    
    def getList(self):
        return self.listCandidates
    
    def setList(self, list):
        self.listCandidates = list 
            
    def resetList(self):
        self.listCandidates = []
            
    def addCand(self, candidate):
        self.listCandidates.append(candidate)
        
    def removeCand(self, candidate):
        self.listCandidates.remove(candidate) 
        