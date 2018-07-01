# Keep the details of a professor
class Prof:
        def __init__(self, name, local, research, charge):
                self._name = name
                self._local = local
                self._research = research
                self._charge = charge

# Keep the details of a subject
class Subject:
        def __init__(self, daysHours, local, charge):
                self._daysHours = name
                self._local = local
                self._charge = charge

# Keep the details of a Candidate
class Candidate:
        def __init__(self):
                self._list = list()
                self._relation = list()

        def __insert__(self, Prof, Subject):
                self._relation.add(Prof, Subject)
                self._list.add(self._relation)
                
# Keep all Candidates obtained during a run of the algorithm
class Solutions:
        def __init__(self):
                self._listCandidates = list()
                self._pop = None

        def __feas__(self):
                self._pop = 'f'

        def __infeas__(self):
                self._pop = 'i'
                
### Assign the type Feasible for a solution and gives an especific function
##class Feasible(solution):
##        def __init__(self):
##                self._pop = "f"
##
### Assign the type Infeasible for a solution and gives an especific function
##class Infeasible(solution):
##        def __init__(self):
##                self._pop = "i"


# Create the first generation of solutions
def start:

# Separation of solutions into 2 populations
def 2pop:

# Detect the violation of a restriction into a solution
def in_feasible:
    
# Calculate de Fitness of the solution
def calc_fit:

# Make a random selection into the solutions
def selection:

# Generate new solutions from the actual population
def new_generation:

# Make a mutation into a solution
def mutation:

# Make a crossover between two solutions    
def crossover:

# Detect the stop condition
def stop:
    
# main
from random import Random
rand = Random() 

