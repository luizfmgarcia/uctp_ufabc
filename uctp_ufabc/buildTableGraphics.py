# -*- coding: utf-8 -*-
"""
describe()
count: conta a quantidade de linhas envolvidas
mean: calcula a média dos elementos da coluna
std: calcula o desvio padrão dos elementos da coluna
min: menor elemento da coluna (0% dos elementos são menores do que ele)
25%: primeiro quartil da coluna (25% dos elementos são menores do que ele)
50%: segundo quartil da coluna, equivalente à mediana (50% dos elementos são menores do que ele)
75%: terceiro quartil da coluna (75% dos elementos são menores do que ele)
max: maior elemento da coluna (100% dos elementos são menores do que ele)
------------------------------------------
-when you want an inline plot
    %matplotlib inline
-when you want graphs in a separate window and
    %matplotlib qt
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib qt
sns.set(style="darkgrid")

def mma():
    j=5
    x_title = "Iter"
    hue_title = "MMA"
    mmaInfo = pd.read_csv("totalMinMaxAvg_"+str(j)+".csv", sep=";")
    y_title = ["Inf","Fea"]
    mmaInfo = [mmaInfo[mmaInfo["Pop"]=="Inf"], mmaInfo[mmaInfo["Pop"]=="Fea"]]
    mmaInfo = [pd.melt(mmaInfo[0], id_vars=["Pop", "Iter"], var_name="MMA", value_name="Fit"), pd.melt(mmaInfo[1], id_vars=["Pop", "Iter"], var_name="MMA", value_name="Fit")]
    # Plotting
    for i in range(len(y_title)):
        otherInfoMMA = mmaInfo[i].describe()
        otherInfoMMA.to_csv("otherInfoMMA_"+y_title[i]+"_"+str(j)+".csv", sep=";")
        fig = sns.relplot(x=x_title, y="Fit", hue=hue_title, data=mmaInfo[i], kind="line", aspect=2)
        fig.savefig(x_title+"_"+hue_title+"_"+y_title[i]+"_"+str(j)+"_line.png", dpi=120)
        
#----------------------------------------------------------------------------        

def instances():
    num = 10
    x_title = "twoPointsCross"
    hue_title = "reposCross"
    
    configs = pd.read_csv("manyInstances.csv", sep=";")
    for i in range(1,num+1):
        #table = pd.read_csv("fitInstances"+str(i)+".csv", sep=";")
        table = pd.read_csv("occurrSum"+str(i)+".csv", sep=";")
        y_title = list(table)[1:]
        table1 = pd.DataFrame(table[list(table)[0]]) 
        table2 = pd.DataFrame(table, columns=y_title)
        table = pd.concat([table1, configs, table2], axis=1, join='inner')
        
        if(i==1):
            finalSumAvg = table
            finalAppend = table
        else:
            finalSumAvg = finalSumAvg + table
            finalAppend = finalAppend.append(table) 
    
    finalSumAvg = finalSumAvg/num
    finalSumAvg.to_csv(x_title+"_finalSumAvg.csv", sep=";")
    finalAppend.to_csv(x_title+"_finalAppend.csv", sep=";")
    
    # Other infos
    otherInfoT = finalSumAvg.describe()
    otherInfoA = finalAppend.describe()
    otherInfoT.to_csv(x_title+"_otherInfoSumAvg.csv", sep=";")
    otherInfoA.to_csv(x_title+"_otherInfoAppend.csv", sep=";")
    
    # Plotting
    final = pd.read_csv(x_title+"_finalAppend.csv", sep=";")
    #These lines concat all the weights  - when needed
    #final["infWeights"] = final['w_alpha'].astype(str)+","+final['w_beta'].astype(str)+","+final['w_gamma'].astype(str)
    #final["feaWeights"] = final['w_delta'].astype(str)+","+final['w_omega'].astype(str)+","+final['w_sigma'].astype(str)+","+final['w_pi'].astype(str)+","+final['w_rho'].astype(str)+","+final['w_lambda'].astype(str)+","+final['w_theta'].astype(str)
    
    for i in y_title:
        if(hue_title != ''):
            fig = sns.catplot(x=x_title, y=i, hue=hue_title, data=final, kind="box", aspect=2)
            fig.set_xticklabels(rotation=80)
            fig.savefig(x_title+"_"+hue_title+"_"+i+"_box.png", dpi=120)
            fig = sns.relplot(x=x_title, y=i, hue=hue_title, data=final, marker="o", kind="line", aspect=2)
            fig.set_xticklabels(rotation=80)
            fig.savefig(x_title+"_"+hue_title+"_"+i+"_line.png", dpi=120)
        else:
            fig = sns.catplot(x=x_title, y=i, data=final, kind="box", aspect=2)
            fig.set_xticklabels(rotation=80)
            plt.tight_layout()
            fig.savefig(x_title+"_"+i+"_box.png", dpi=120)
            fig = sns.relplot(x=x_title, y=i, data=final, marker="o", kind="line", aspect=2)
            fig.set_xticklabels(rotation=80)
            #plt.tight_layout()
            #fig.savefig(x_title+"_"+i+"_marker_line.png", dpi=120)
            #fig = sns.relplot(x=x_title, y=i, data=final, kind="line", aspect=2)
            #fig.set_xticklabels(rotation=80)
            plt.tight_layout()
            fig.savefig(x_title+"_"+i+"_line.png", dpi=120)
