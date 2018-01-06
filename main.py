# -*- coding: utf-8 -*-

from subprocess import Popen,PIPE
import time
import os
import numpy as np
import modules
import pandas as pd
#=============================================================================
# THIS RUNS 82BE.ell iteratively and collect all the required files & data 

ell_2 = "C:\LANL\Examples\CavityTuning\EllipticalCavity\82BE.ell"
exe_path = r'C:\LANL\ELLFISH.EXE'
output = modules.launch_program(exe_path,ell_2)
print('The program is successfully run:{}'.format(output))

#right_dome_ratio = np.arange(0.5,1.01,0.01) # Define a numpy array from 0.5 - 1.0 with 0.01 interval
#right_iris_ratio = np.arange(0.5,1.01,0.01)

#Testing... Dome ratio (0.731-0.750)
# AIM - Increase the data points between 0.73 and 0.75 to verify the peak dome ratio at 0.74
right_dome_ratio = np.arange(0.731,0.751,0.001) # Define a numpy array from 0.5 - 1.0 with 0.01 interval
right_iris_ratio = np.arange(0.5,1.01,0.01)

count_run = 0
count_run_success = 0   

# create a list for each data extracted 
freq_list = [] 
Q_list = []
maxH_list = []
maxE_list = []

list_dfs = [] # create a list to store dataframes

for i in range(len(right_dome_ratio)): # loop through every interval for right_dome_ratio
    dome_ratio = str(round(right_dome_ratio[i],3))
    modules.write_ell_file('RIGHT_DOME_A/B',dome_ratio) # update the .ell file with new dome ratio
    
    freq_list = [] ; Q_list = [] ; maxH_list = [] ; maxE_list = [] # Empty the lists for another dome ratio
    
    for j in range(len(right_iris_ratio)):  # loop through every interval for right_iris_ratio
        iris_ratio = str(round(right_iris_ratio[j],2))
        print('dome ratio:{} , iris ratio:{}'.format(dome_ratio,iris_ratio))
        modules.write_ell_file('RIGHT_IRIS_A/B',iris_ratio) # update the .ell file with new iris ratio
        # launch the program here
        output = modules.launch_program(exe_path,ell_2)  
        count_run = count_run + 1 # check number of runs
        print('#RUN:{} , Output of program:{}\n'.format(count_run,output))
        
        # program failed to run
        if output == False:
            continue # go to the next inner loop in j 
#-----------------------------------------------------------------------------            
        # program ran successfully 
        else: 
            count_run_success = count_run_success + 1 # count successful run

            # extract the required data from .SFO file, data in float
            freq,Q,maxH,maxE = modules.extract_SFO_FileData() 

            freq_list.append(freq)
            Q_list.append(Q)
            maxH_list.append(maxH)
            maxE_list.append(maxE)
#//////////////////////////////////////////////////////////////////////////////
            #Store the extracted data in pandas 
            if j == 50:   # Original j == 50  
                # once the last element of the RIGHT_IRIS_A/B is reached
                dic_storage = {'Final Resonant Frequency':freq_list,
                               'Quality Factor':Q_list,
                               'Peak Magnetic Field on cavity surface':maxH_list,
                               'Peak Electric Field on cavity surface':maxE_list}
                
                df = pd.DataFrame(dic_storage)  # Make a dataframe using Pandas
                list_dfs.append(df)
                print('Length of list_dfs:{}'.format(len(list_dfs)))
                print('list_dfs = {}\n'.format(list_dfs))
#//////////////////////////////////////////////////////////////////////////////
            # make a directory for the path
            folder_store_output_files = ((r"C:\LANL\Examples\CavityTuning\Elliptical Cavity (Collected Output Files)(Dome Ratio 0.731-0.750)\folder_%s_%s") % (i,j))
            os.mkdir(folder_store_output_files)  
                
            # Move the output files to another folder for each iteration 
            modules.move_files(folder_store_output_files)
            time.sleep(1.5)
            Popen(r"C:\LANL\Examples\CavityTuning\CLR_TC.BAT") # Clear the remaining files
#----------------------------------------------------------------------------- 
modules.save_excel(list_dfs,'Output_Excel(Dome ratio 0.731-0.750).xlsx') # Once the list of dataframes is compiled
                                                 # Write all the dataframes to an excel file with different sheets
print('Total number of successful run:{}'.format(count_run_success))

#=============================================================================

