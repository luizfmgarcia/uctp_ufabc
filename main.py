# PERGUNTAS:
# 1.Podem haver materias repetidas vindas do arquivo? Devo tratalas? Removelas?
# 2.Cuidar das conexoes como numeros (e procurar nas listas), ponteiro, copia dos objetos?
# 3.Cuidar para ter todos os professores logo na primeira populacao? Pode acontecer de um nao entrar por ser randomico?
# 4.Colocar tmb no calculo de Fitness se ha ou nao todos os professores (deve haver todos)

# filter subjects graduation and computing only;
# So....level = 'G' and code = {'MCTA', 'MCZA'} 'BCM'?, 'MCTB'?;
# Code where 2 first letters (period 'D' or 'N', class 'A' or 'B' etc);
# and maybe one number before the code itself of subjects;
# Example: DA1MCTA0001;
# Every professor must have name, period and charge -> error if not;
# Every subject must have level, code, name, quadri, period, campus and charge -> error if not;
# Transform every letter to Uppercase;

from objects import *
from uctp import *
from ioData import *
            
# main
class main:
    # to access UCTP Main methods and creating Solutions (List of Candidates)
    uctp = UCTP()
    solutions = Solutions()
    
    # Max Number of iterations to get a solution
    total = 100;
    # number of initial candidates (first generation)
    num = 50
    # Min and Max number of candidates in a generation
    min = 50
    max = 100
    # Number of Mutations and Crossover
    nMut = 10
    nCross = 10
    
    # Base Lists of Professors and Subjects
    prof = []
    subj = []
    
    # Start of the works
    subj, prof = getData(subj, prof)
    
    # First generation
    solutions = uctp.start(solutions, subj, prof, num)
    solutions = uctp.two_pop(solutions, prof)
    solutions = uctp.calc_fit(solutions)
    #outData(solutions, 0)
    printAllFit(solutions)
    
    # Main work - iterations to find a solution
    print(" ")
    print("Starting hard work...")
    t = 0;
    while(uctp.stop(t, total, solutions)):
        print 'Iteration:', t+1
        solutions = uctp.new_generation(solutions, nMut, nCross)
        solutions = uctp.selection(solutions, min, max) 
        solutions = uctp.resetPop(solutions)
        solutions = uctp.two_pop(solutions, prof)
        solutions = uctp.calc_fit(solutions)     
        #outData(solutions, t)
        printAllFit(solutions)
        print(" ")
        t = t+1
            
    print("FIM")
    
