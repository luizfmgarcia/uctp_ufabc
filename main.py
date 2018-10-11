# PERGUNTAS:
# 1.Podem haver materias repetidas? Devo tratalas?
# 2.Cuidar das conexoes como numeros (e procurar nas listas) ou ponteiro?
# 3.Cuidar para ter todos os professores? Pode acontecer de um nao entrar?

# filter subjects graduation and computing only;
# So....level = 'G' and code = {'MCTA', 'MCZA'} 'BCM'?, 'MCTB'?;
# Code where 2 first letters (period 'D' or 'N', class 'A' or 'B' etc);
# and maybe one number before the code itself of subjects;
# Example: DA1MCTA0001;
# Every professor must have name, period and charge -> error if not;
# Every subject must have level, code, name, quadri, period, campus and charge -> error if not;
# Transform every letter to Uppercase;
from random import Random
from random import randrange
# Keep the details of a professor
class Prof:
    def __init__(self, name, period, charge):
        self.name = name
        self.period = period
        #self.prefSubject = prefSubject
        #self.research = research
        #self.quadriSabbath = quadriSabbath
        self.charge = charge

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

# Keep the details of a Candidate
class Candidate:
    def __init__(self):
        self.listRelations = []
        self.pop = None
    
    def isFeas(self):
        self._pop = 'f'

    def isInfeas(self):
        self._pop = 'i'
    
    def resetPop(self):
        self._pop = None
        
    def insert(self, Subject, Prof):
        relation = [Subject, Prof]
        self.listRelations.append(relation)
        
    def remove(self, relation):
        self.listRelations.remove(relation)    
                
# Keep all Candidates obtained during a run of the algorithm
class Solutions:
    def __init__(self):
        self.listCandidates = []
    
    def insert(self, candidate):
        self.listCandidates.append(candidate)
        
    def remove(self, candidate):
        self.listCandidates.remove(candidate)        

class UCTP:
    # Get all data to work
    def getData(self, subj, prof):
        # Remove accents of datas
        #from unicodedata import normalize 
        #def remove_accent(txt):
        #    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
        
        # Read the data of professors and subjects and create the respective objects
        import csv
        print("Getting datas of Professors...")
        with open('professors.csv') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            print("Setting Professors...")
            for row in spamreader:
                datas = [row[0].upper(), row[1].upper(), row[2].upper()]
                if(not datas.__contains__('')):
                    prof.append(Prof(datas[0], datas[1], datas[2]))
                    print datas
        
        print(" ")
        print("Getting datas of Subjects...")
        with open('subjects.csv') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            print("Setting Subjects...")
            for row in spamreader:
                datas = [row[0].upper(), row[1].upper(), row[2].upper(), row[3].upper(), row[4].upper(), row[5].upper(), row[6].upper()]
                if(not datas.__contains__('') and row[0] == 'G' and ('MCTA' in row[1] or 'MCZA' in row[1])):
                    subj.append(Subject(datas[0], datas[1], datas[2], datas[3], datas[4], datas[5], datas[6]))
                    print datas       
                
        return subj, prof
    
    # Create the first generation of solutions
    def start(self, solutions, subj, prof):
        # number of initial candidates
        num = 50
        
        n = 0
        while(n!=num):
            candidate = Candidate()
            for sub in subj:
                candidate.insert(sub, prof[randrange(len(prof))])
            solutions.insert(candidate)
            n = n+1
            print solutions
        return solutions

    # Separation of solutions into 2 populations
    def two_pop(self, solutions):
        pass
    
    # Detect the violation of a restriction into a solution
    def in_feasible():
        pass
    
    # Calculate the Fitness of the solution
    def calc_fit():
        pass
    
    # Generate new solutions from the actual population
    def new_generation():
        pass
    
    # Make a random selection into the solutions
    def selection():
        pass
        
    # Make a mutation into a solution
    def mutation():
        pass
    
    # Make a crossover between two solutions    
    def crossover():
        pass
    
    # Detect the stop condition
    def stop():
        pass
    
# main
class main:
    # to access methods
    uctp = UCTP()
    # Random operator
    rand = Random()
    randrange(10)
    # Number of iterations to get a solution
    t = 0;
    # Base Lists of Professors and Subjects
    prof = []
    subj = []
    # Start of the works
    subj, prof = uctp.getData(subj, prof)
    solutions = Solutions()
    solutions = uctp.start(solutions, subj, prof)
    
    # Main work - iterations to find a solution
    print(" ")
    print("Starting hard work...")
    while(t!=100):
             
         t = t+1
         print "Iteration:", t
    print("FIM")
    
