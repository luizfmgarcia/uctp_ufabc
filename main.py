#OPERADORES!!! de crossover e mutation
# 2.Cuidar das conexoes como numeros (e procurar nas listas), ponteiro, copia dos objetos? - trabalha sempre com ponteiros o python
# 3.Cuidar para ter todos os professores logo na primeira populacao? Pode acontecer de um nao entrar por ser randomico? - nao a mutacao resolve
# 4.Colocar tmb no calculo de Fitness se ha ou nao todos os professores (deve haver todos)!!!!!!

# filter subjects graduation and computing only;
# So....level = 'G' and code = {'MCTA', 'MCZA'} 'BCM'?, 'MCTB'?;
# Code where 2 first letters (period 'D' or 'N', class 'A' or 'B' etc);
# and maybe one number before the code itself of subjects;
# Example: DA1MCTA0001;
# Every professor must have name, period and charge -> error if not;
# Every subject must have level, code, name, quadri, period, campus and charge -> error if not;
# Transform every letter to Uppercase; - nao se importar

# Um excel onde a cada geracao e salva uma nova linha contendo (o fitness minimo - maximo - medio) - para plotar o grafico;
# E gerar apenas no excel a melhor solucao final


from objects import *
from uctp import *
from ioData import *
            
# main
class main:
    # to access UCTP Main methods and creating Solutions (List of Candidates)
    uctp = UCTP()
    solutionsI = Solutions()
    solutionsF = Solutions()
    solutionsNoPop = Solutions()
    # Base Lists of Professors and Subjects
    prof = []
    subj = []
    
    # Max Number of iterations to get a solution
    total = 100
    # number of initial candidates (first generation)
    num = 50
    # Min and Max number of candidates in a generation
    min = 50
    max = 100
    # Number of Mutations and Crossover
    nMut = 10
    nCross = 10
    
    # Start of the works
    getData(subj, prof)
    
    # First generation
    uctp.start(solutionsNoPop, subj, prof, num)
    uctp.two_pop(solutionsNoPop, solutionsI, solutionsF, prof)
    uctp.calc_fit(solutionsI, solutionsF)
    outDataMMM(solutionsI, solutionsF)
    printAllFit(solutionsI, solutionsF)
    
    # Main work - iterations to find a solution
    print(" ")
    print("Starting hard work...")
    t = 0;
    while(uctp.stop(t, total, solutionsI, solutionsF)):
        print 'Iteration:', t+1
        
        uctp.new_generation(solutionsI, solutionsF, prof, nMut, nCross) 
        uctp.resetPop(solutionsNoPop, solutionsI, solutionsF)
        uctp.two_pop(solutionsNoPop, solutionsI, solutionsF, prof)
        uctp.calc_fit(solutionsI, solutionsF)
        uctp.selection(solutionsI, solutionsF, min, max)
        
        outDataMMM(solutionsI, solutionsF)
        printAllFit(solutionsI, solutionsF)
        print(" ")
        t = t+1
        
    outData(solutionsI, solutionsF, t)        
    print("FIM")
    
