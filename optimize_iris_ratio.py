# -*- coding: utf-8 -*-
import pandas as pd 
import numpy as np
#FUNCTION
#=============================================================================
def find_optimum_freq(freq_list):
    '''
    This function finds the smallest deviation of final resonant frequency 
    from 400.8 MHz 
    
    Input -> List of frequencies from each sheet
    Output -> final resonant frequency closest to 400.8 MHz 
    '''
    diff_list = []
    for i in freq_list:
        diff = abs(400.8 - i)  # calculate the difference 
        diff_list.append(diff)  # append the difference value to the list
        
    final_freq_location = diff_list.index(min(diff_list))
    final_freq = freq_list[final_freq_location]
    
    return float(final_freq)
#=============================================================================
# MAIN SCRIPT (Optimum dome ratio = 0.74)

df_sheet = pd.read_excel(r'C:\LANL\Examples\CavityTuning\EllipticalCavity\Output_Excel.xlsx',sheetname='Dome_0.74')
# Each sheet -> 4 columns, extract optimum values from here 
freq_list = list(df_sheet['Final Resonant Frequency'])
E_list = list(df_sheet['Peak Electric Field on cavity surface'])
H_list = list(df_sheet['Peak Magnetic Field on cavity surface'])
Q_list = list(df_sheet['Quality Factor'])

# define benchmark values
freq_benchmark = find_optimum_freq(freq_list) 
E_benchmark = float(min(E_list))
H_benchmark = float(min(H_list))
Q_benchmark = max(Q_list)

print('#{}\n  opt_freq:{}\n  E_min:{}\n  H_min:{}\n  Q_max:{}'.format('Dome_0.74',freq_benchmark,E_benchmark,H_benchmark,Q_benchmark))
print('#########################################################\n')

freq_score=[] ; E_score=[] ; H_score=[] ; Q_score=[]
for i in range(len(freq_list)): # Loop every single element in the lists 
    # calculate the score points for each element in the lists 
    # highest score point is the optimum value 
    freq_i = freq_list[i] / freq_benchmark
    E_i = E_benchmark / E_list[i]
    H_i = H_benchmark / H_list[i]
    Q_i = float(Q_list[i] / Q_benchmark)
    
    # Store the score points in the list for each element 
    freq_score.append(freq_i)
    E_score.append(E_i)
    H_score.append(H_i)
    Q_score.append(Q_i)
    
# Check if the dome lists have the same length 
if len(freq_score) == len(E_score) == len(H_score) == len(Q_score):
    print('freq_score, E_score, H_score, Q_score have same length --> {}\n'.format(len(freq_score)))
    pass # do nothing when the length of all the appended lists are the sae
else:
     print('freq_score, E_score, H_score, Q_score do not have same length!!\n')
#-----------------------------------------------------------------------------
score_list = [] 
for i in range(len(freq_score)): # since the length is same, just take the length of freq_score 
    # Sum all the score points for each dome ratio and store in score_list
    # Max score for each dome ratio is 4
    score_list.append(freq_score[i] + E_score[i] + H_score[i] + Q_score[i])

print('Maximum score point:4')
highest_score = max(score_list)  # find the highest score point
print('Highest score point calculated:{}'.format(highest_score))
# Locate the dome ration actual value 
optimum_iris_ratio = (score_list.index(max(score_list))+50)/100
print('Optimum iris ratio:{}\n'.format(optimum_iris_ratio))


 

    





    
    
    