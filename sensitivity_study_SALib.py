from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np
import modules 

#-----------------------------------------------------------------------------
# MAIN SCRIPT 
'''
PURPOSE ->  Find the correlation between dome ratio and iris ratio by looking 
            at the sensitivity indices 
        ->  Verify that dome ratio and iris ratio are the determinants for 
            the output results:
                1. Final Resonant Frequency 
                2. Peak Electric Field on cavity surface
                3. Peak Magnetic Field on cavity surface
                4. Quality Factor

METHOD FOR SENSITIVITY STUDY --> Sobol’ Sensitivity Analysis

APPROACH: 
1. Define input variables and their parameters range 
2. Generate sample values from the range  
3. Use each sample values to run the simulation
4. Collect the output for analysis later 

'''
#-----------------------------------------------------------------------------
# Self-defined variables and parameters range
problem = {
    'num_vars': 2,
    'names': ['dome ratio', 'iris ratio'],
    'bounds': [[0.5,1.2],
               [0.5,1.0]]
}
# generate the samples 
# Sobol’ sensitivity analysis --> Use Saltelli sampler
# Saltelli sampler generates N*(2D+2) , D=2 is the number of inputs 
# size of the matrix -> (1200 , 2)
param_values = saltelli.sample(problem, 200) #original = 200
input_dome_iris_ratio = np.around(param_values,decimals=2) # convert numbers in array to 2 decimal places 
# make zero arrays to store the output values after running the model 
# Then replace each element one by one 
out_freq = np.zeros([param_values.shape[0]])
out_Q = np.zeros([param_values.shape[0]])
out_Emax = np.zeros([param_values.shape[0]])
out_Hmax = np.zeros([param_values.shape[0]])


count_run = 0
count_run_success = 0 

for i, i_input in enumerate(input_dome_iris_ratio):  # loop through every input from parameter
    # write the 82BE.ell file with different dome & iris ratios for each iteration 
    modules.write_ell_file('RIGHT_DOME_A/B',str(float(i_input[0]))) # float is meant to convert the value to 2 decimal places 
    modules.write_ell_file('RIGHT_IRIS_A/B',str(float(i_input[1])))
    
    # execute the program 
    output = modules.launch_program(r'C:\LANL\ELLFISH.EXE',"C:\LANL\Examples\CavityTuning\EllipticalCavity\82BE.ell")
    count_run = count_run + 1 # check number of runs
    print('#RUN:{} , Output of program:{}\n'.format(count_run,output))
          
    if output == True:  # if run successfully
        count_run_success = count_run_success + 1 # count successful run
        freq,Q,maxH,maxE = modules.extract_SFO_FileData()
        # Store all the extract values in Y array
        out_freq[i] = freq
        out_Q[i] = Q
        out_Hmax[i] = maxH
        out_Emax[i] = maxE
    
    if output == False:  # if failed to run
        # Store zeros in Y array (keep the size consistent with input size)
        out_freq[i] = 0
        out_Q[i] = 0
        out_Hmax[i] = 0
        out_Emax[i] = 0
        
compute_freq = sobol.analyze(problem, out_freq)
compute_Q = sobol.analyze(problem, out_Q)
compute_Hmax = sobol.analyze(problem, out_Hmax)
compute_Emax = sobol.analyze(problem, out_Emax)

print('Total number of successful run:{}'.format(count_run_success))

