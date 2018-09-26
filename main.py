# creditos defaul anual = 18
# filtrar disciplinas graduação e computação apenas
# Keep the details of a professor
class Prof:
    def __init__(self, name, shift, charge):
        self.name = name
        self. shift = shift
        #self._research = research
        self.charge = charge

# Keep the details of a subject
class Subject:
    def __init__(self, name, shift, campus, charge):
        self.name = name
        self.shift = shift
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
    
    def feas(self):
        self._pop = 'f'

    def infeas(self):
        self._pop = 'i'
    
    def resetPop(self):
        self._pop = None
                
### Assign the type Feasible for a solution and gives an especific function
##class Feasible(solution):
##        def __init__(self):
##                self._pop = "f"
##
### Assign the type Infeasible for a solution and gives an especific function
##class Infeasible(solution):
##        def __init__(self):
##                self._pop = "i"

class UCTP:
    # Create the first generation of solutions
    def start(self, prof, subj):
        # Read the data of professors and subjects
        return prof, subj
    
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
    prof, subj = uctp.start(prof, subj)
    # Main work - iterations to find a solution
    print("Starting hard work...")
    while(t!=100):
         
         t = t+1
         print "Iteration:", t
    print("FIM")
    
