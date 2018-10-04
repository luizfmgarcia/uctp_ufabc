# filter subjects graduation and computing only;
# So....level = 'G' and code = {'MCTA', 'MCZA'} 'BCM'?, 'MCTB'?;
# Code where 2 first letters (period 'D' or 'N', class 'A' or 'B' etc);
# and maybe one number before the code itself of subjects;
# Example: DA1MCTA0001;
# Every professor must have name, period and charge -> error if not;
# Every subject must have level, code, name, quadri, period, campus and charge -> error if not;
# Transform every letter to Uppercase;

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
        self.candidate = []
        self.relation = []

    def insert(self, Prof, Subject):
        self.relation.add(Prof, Subject)
        self.candidate.add(self._relation)
                
# Keep all Candidates obtained during a run of the algorithm
class Solutions:
    def __init__(self):
        self.listCandidates = []
        self.pop = None
    
    def isFeas(self):
        self._pop = 'f'

    def isInfeas(self):
        self._pop = 'i'
    
    def resetPop(self):
        self._pop = None

class UCTP:
    # Get all data to work
    def getData(self, prof, subj):
        # Remove accents of datas
        from unicodedata import normalize 
        def remove_accent(txt):
            return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
        
        # Read the data of professors and subjects and create the respective objects
        import csv
        print("Getting datas of Professors...")
        with open('professors.csv') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            print("Setting Professors...")
            for row in spamreader:
                datas = [remove_accent(row[0].upper()), remove_accent(row[1].upper()), remove_accent(row[2].upper())]
                if(not datas.__contains__('')):
                    prof.append(Prof(row[0], row[1], row[2]))
                    print datas
        
        print(" ")
        print("Getting datas of Subjects...")
        with open('subjects.csv') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            print("Setting Subjects...")
            for row in spamreader:
                datas = [row[0].upper(), row[1].upper(), row[2].upper(), row[3].upper(), row[4].upper(), row[5].upper(), row[6].upper()]
                if(not datas.__contains__('') and row[0] == 'G' and ('MCTA' in row[1] or 'MCZA' in row[1])):
                    subj.append(Subject(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
                    print datas       
                
        return prof, subj
    
    # Create the first generation of solutions
    def start(self, prof, subj):
        pass

    # Separation of solutions into 2 populations
    def two_pop():
        pass
    
    # Detect the violation of a restriction into a solution
    def in_feasible():
        pass
    
    # Calculate the Fitness of the solution
    def calc_fit():
        pass
    
    # Make a random selection into the solutions
    def selection():
        pass
    
    # Generate new solutions from the actual population
    def new_generation():
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
    from random import Random
    rand = Random()
    # Number of iterations to get a solution
    t = 0;
    # Base Lists of Professors and Subjects
    prof = []
    subj = []
    # Start of the works
    prof, subj = uctp.getData(prof, subj)
    # Main work - iterations to find a solution
    print(" ")
    print("Starting hard work...")
    while(t!=100):
         
         t = t+1
         print "Iteration:", t
    print("FIM")
    
