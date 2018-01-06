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
# MAIN SCRIPT
#df1 = pd.read_excel(r'C:\LANL\Examples\CavityTuning\EllipticalCavity\Output_Excel.xlsx',sheetname='Dome_0.50')

# Create lists to append the optimum values from each sheet (dome ratio)
dome_freq = []
dome_E_min = []
dome_H_min = []
dome_Q_max = []

#original path - r'C:\LANL\Examples\CavityTuning\EllipticalCavity\Output_Excel.xlsx'
df = pd.ExcelFile(r'C:\LANL\Examples\CavityTuning\EllipticalCavity\Output_Excel(Dome ratio 0.731-0.750).xlsx')
sheet_list = df.sheet_names

for i in sheet_list: # loop every sheet (dome ratio)
    df_sheet = pd.read_excel(r'C:\LANL\Examples\CavityTuning\EllipticalCavity\Output_Excel(Dome ratio 0.731-0.750).xlsx',sheetname=i)
    # Each sheet -> 4 columns, extract optimum values from here 
    freq_list = list(df_sheet['Final Resonant Frequency'])
    opt_freq = find_optimum_freq(freq_list) 
    
    E_min= float(min(list(df_sheet['Peak Electric Field on cavity surface'])))
    H_min = float(min(list(df_sheet['Peak Magnetic Field on cavity surface'])))
    Q_max = max(list(df_sheet['Quality Factor']))
    
    print('#{}\n  opt_freq:{}\n  E_min:{}\n  H_min:{}\n  Q_max:{}'.format(i,opt_freq,E_min,H_min,Q_max))
    print('#########################################################\n')
    # # Append the optimum values from each sheet (dome ratio) in these lists
    dome_freq.append(opt_freq)
    dome_E_min.append(E_min)
    dome_H_min.append(H_min)
    dome_Q_max.append(Q_max)
 
# Check if the dome lists have the same length 
if len(dome_freq) == len(dome_E_min) == len(dome_H_min) == len(dome_Q_max):
    print('dome_freq, dome_E_min, dome_H_min, dome_Q_max have same length --> {}\n'.format(len(dome_freq)))
    pass # do nothing when the length of all the appended lists are the sae
else:
     print('dome_freq, dome_E_min, dome_H_min, dome_Q_max do not have same length!!\n')
#-----------------------------------------------------------------------------
# Give benchmark values for optimum output values 
freq_benchmark = 400.8
E_benchmark = min(dome_E_min)
H_benchmark = min(dome_H_min)
Q_benchmark = max(dome_Q_max)

freq_score=[] ; E_score=[] ; H_score=[] ; Q_score=[]

for i in range(len(dome_freq)): # Loop every single element in the lists 
    # calculate the score points for each element in the lists 
    # highest score point is the optimum value 
    freq_i = dome_freq[i] / freq_benchmark
    E_i = E_benchmark / dome_E_min[i]
    H_i = H_benchmark / dome_H_min[i]
    Q_i = float(dome_Q_max[i] / Q_benchmark)
    
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
#original - optimum_dome_ratio = (score_list.index(max(score_list))+50)/100
optimum_dome_ratio = score_list.index(max(score_list))
#original - print('Optimum dome ratio:{}\n'.format(optimum_dome_ratio))
print('Optimum dome ratio index number:{}\n'.format(optimum_dome_ratio))
#-----------------------------------------------------------------------------
# Write the output lists to an excel file 
dic_storage = {'Dome Ratio':np.arange(0.731,0.751,0.001), #original - 'Dome Ratio':np.arange(0.5,1.21,0.01)
               'Final Resonant Frequency':dome_freq,
               'Peak Electric Field on cavity surface':dome_E_min,
               'Peak Magnetic Field on cavity surface':dome_H_min,
               'Quality Factor':dome_Q_max}

df1 = pd.DataFrame(dic_storage)
#original - writer = pd.ExcelWriter(r'C:\LANL\Examples\CavityTuning\EllipticalCavity\Filtered_Output_Excel_1(Dome ratio 0.731-0.750).xlsx')
writer = pd.ExcelWriter(r'C:\LANL\Examples\CavityTuning\EllipticalCavity\Filtered_Output_Excel_1(Dome ratio 0.731-0.750).xlsx')
df1.to_excel(writer,index=False)
writer.save

    
    

 

    





    
    
    