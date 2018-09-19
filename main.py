# Keep the details of a professor
class Prof:
    def __init__(self, name, local, research, charge):
        self.name = name
        self.local = local
        #self._research = research
        self.charge = charge

# Keep the details of a subject
class Subject:
    def __init__(self, daysHours, local, charge):
        self.daysHours = daysHours
        self.local = local
        self.charge = charge

# Keep the details of a Candidate
class Candidate:
    def __init__(self):
        self.candidate = []
        self.relation = []

    def __insert__(self, Prof, Subject):
        self.relation.add(Prof, Subject)
        self.candidate.add(self._relation)
                
# Keep all Candidates obtained during a run of the algorithm
class Solutions:
    def __init__(self):
        self.listCandidates = []
        self.pop = None
    
    def __feas__(self):
        self._pop = 'f'

    def __infeas__(self):
        self._pop = 'i'
    
    def __resetPop__(self):
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
    def start():
        # Read the data of professors and subjects
        return
    
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
    def main():
        # Random operator
        from random import Random
        rand = Random()
        # Count of iterations of work
        t = 0;
        # Base List of Professors and Subjects
        prof = list()
        subj = list()
        # Start of the works
        self.start()
        # Main work - iterations to find a solution
        while(t!=100):
             t = t+1
        print("FIM")
    
