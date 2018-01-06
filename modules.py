from subprocess import Popen,PIPE
import time
import os
import win32gui
import numpy as np
import shutil
import pandas as pd
#=============================================================================
def launch_program(exe_path,ell_file):
    '''
    This function launches program file assigned 
    
    IMPORTANT: MAKE SURE TO MOVE OUTPUT FILES TO SEPARATE FOLDER FOR EACH 
    ITERATION TO AVOID REPLACEMENT OF FILES AUTOMATICALLY 
    
    Input -> (execution path,ell_file path)
    Output -> Boolean success (True or False)
    '''
    output = Popen("%s %s" % (exe_path, ell_file),stdout=PIPE,stderr=PIPE)
    
    time.sleep(1.5)
    window = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(window) # Collect the title of the pop-up window
        if title == 'Warning' or 'Error':
        print('title is:{}'.format(title)) 
        output.terminate()
    if title == 'ELLfish 7.17 --- Elliptical cavity tuning code': # Program is running correctly
        output = Popen("%s %s" % (exe_path, ell_file),stdout=PIPE,stderr=PIPE) # Re-run the program
        time.sleep(0.5)
        #Minimize = win32gui.GetForegroundWindow() 
        Minimize = win32gui.FindWindow(None,'ELLfish 7.17 --- Elliptical cavity tuning code')
        title_updated = win32gui.GetWindowText(Minimize)
        win32gui.ShowWindow(Minimize, 6) # Miniize the current window
        print('Minimize the current window:{}'.format(title_updated))
        
        output.wait() # Wait until the program is finished running
    success = True # Run successfully
    
    if (os.path.isfile('82BE1.SFO') == True) and (os.path.getsize('82BE1.SFO') > 0):
        # If 82BE1.SFO exists and the file size is bigger than zero, means there is output
        print('82BE1.SFO file is produced with data!')
        pass
    else:
        success = False # Did not run successfully as SFO file is not produced
        Popen(r"C:\LANL\Examples\CavityTuning\CLR_TC.BAT") # Delete all files
   
    return success
#=============================================================================

def write_ell_file(eclipse_shape,current_ratio_value): # either dome or iris ratio
    ''' 
    This function opens, writes and saves different values of Right Dome Ratio 
    & Right Iris Ratio to B2BE.ell file for each iteration 
    
    OUTPUT:
    Save B2BE.ell file with different values of Right Dome Ration & 
    Right Iris Ratio
    '''
    with open('C:\LANL\Examples\CavityTuning\EllipticalCavity\82BE.ell','r',encoding="utf8") as f:
        file_read_str = f.read() # read the content of the file and put in string format
            
#-----------------------------------------------------------------------------
    if (eclipse_shape == 'RIGHT_DOME_A/B'):
        file_read_list = list(file_read_str)  # put file in list format
             
        for i in file_read_list[1200:1205]: #original - file_read_list[1200:1204]
            if i != '\n':
                not_replaced = True
                continue
            else:
                file_read_list[1200:1204] = list(current_ratio_value) # change old to new dome ratio
                file_read_new = ''.join(file_read_list) # join the list to form string again
                not_replaced = False
        if not_replaced == True:
            print('No space is found')
            file_read_list[1200:1205] = list(current_ratio_value) #original - file_read_list[1200:1204]
            print('replace the original list')
            file_read_new = ''.join(file_read_list)
            print('new file now\n')  

    if (eclipse_shape == 'RIGHT_IRIS_A/B'):
        file_read_list = list(file_read_str)  # put file in list format
        
        for i in file_read_list[1749:1753]: #original - file_read_list[1747:1751]
            if i != '\n':
                not_replaced = True
                continue
            else:
                file_read_list[1749:1752] = list(current_ratio_value) # change old to new dome ratio
                file_read_new = ''.join(file_read_list) # join the list to form string again
                not_replaced = False
        if not_replaced == True:
            print('No space is found')
            file_read_list[1749:1753] = list(current_ratio_value)
            print('replace the original list')
            file_read_new = ''.join(file_read_list)
            print('new file now')            
#-----------------------------------------------------------------------------
    with open('C:\LANL\Examples\CavityTuning\EllipticalCavity\82BE.ell','w',encoding="utf8") as f:
        f.write(file_read_new)

#=============================================================================
def extract_SFO_FileData():
    '''
    This function extracts & returns 4 types of data values (float value) for 
    each iteration 
    
    OUTPUT:
    1. Final resonant frequency 
    2. Quality factor, Q 
    3. Maximum electric field on the surface
    4. Maximum magnetic field on the surface 
    '''

    with open('C:\LANL\Examples\CavityTuning\EllipticalCavity\82BE1.SFO') as f:
        for line in f: # loop through every line in the file opened
            if line.find('Frequency                                 =') != -1: # If the line matches with the string specified
                line_freq = line.split() # Split the string and form a list 
                freq_data = float(line_freq[2]) # Extract the final resonant frequency value
                print('Resonant frequency:{}'.format(freq_data))
            if line.find('Q    =') != -1:
                line_Q = line.split()
                Q_data = float(line_Q[2]) # Extract Q factor
                print('Q factor:{}'.format(Q_data))
            if line.find('Maximum H') != -1:
                line_maxH = line.split()
                maxH_data = float(line_maxH[7]) # Extract maximum magnetic field
                print('Maximum H:{}'.format(maxH_data))
            if line.find('Maximum E') != -1:
                line_maxE = line.split()
                maxE_data = float(line_maxE[7]) # Extract maximum electric field
                print('Maximum E:{}'.format(maxE_data))
                print('#########################################################\n')
    
    return freq_data,Q_data,maxH_data,maxE_data

#=============================================================================
def move_files(folder_store_output_files):
    file_source = r'C:\LANL\Examples\CavityTuning\EllipticalCavity'
    final_dir = folder_store_output_files
    
    file_list = os.listdir(file_source)
    
    for f in file_list:
        if (f.endswith('LOG') or f.endswith('AM') or f.endswith('SEG')
        or f.endswith('SFO') or f.endswith('T35') or f.endswith('TBL')
        or f.endswith('TXT') or f.endswith('log') or f.endswith('INF')):
            shutil.move(f,final_dir)
            
#=============================================================================
def save_excel(list_dfs, xls_path):
    writer = pd.ExcelWriter(xls_path)
    dome_ratio = 0.73  # orignal = 0.49
    for df in list_dfs:
        dome_ratio = dome_ratio + 0.001
        df.to_excel(writer,'Dome_%s' % dome_ratio,index=False)
        
    writer.save()









