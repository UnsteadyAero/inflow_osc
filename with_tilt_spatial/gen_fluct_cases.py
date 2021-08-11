# coding: utf-8
import numpy as np
import pandas as pd
from pyFAST.input_output import TurbSimFile
import pyFAST.case_generation.case_gen as case_gen
from pyFAST.input_output import FASTInputFile

def gen_spatial_fluct_cases(lamda_range, phase, umean, zhub):
    """Generate a set of OpenFAST cases to investigate effect of spatial
    velocity fluctuations at a specific frequency

    Inputs:
       lamda_range: Wavelength of oscillations in 'y' and 'z' direction
       phase: Phase of oscillations w.r.t hub center
       umean: Mean inflow velocity
       zhub: Hub height of turbine

    Outputs:
       None: File written to UAero_lamda_{lamda_value}.bts
    """

    ref_dir   = 'template'  # Folder where the fast input files are located (will be copied)
    main_file = 'IEA-15-240-RWT.fst'  # Main file in ref_dir, used as a template
    work_dir = '.'     # Output folder (will be created)    
    PARAMS = [ {'__name__': 'lamda_{:04.1f}_phase_{:04.1f}_umean_{:04.1f}'.format(l, phase, umean) } for l in lamda_range]
    fastfiles=case_gen.templateReplace(PARAMS, ref_dir, outputDir=work_dir, removeRefSubFiles=True, main_file=main_file, oneSimPerDir=True)
    
    for l in lamda_range:
        write_inflow_fluct(l, phase, umean, 150.0)
        f = FASTInputFile('lamda_{:04.1f}_phase_{:04.1f}_umean_{:04.1f}/InflowFile_UAero.dat'.format(l, phase, umean))
        for i in f:
            if ( (type(i['value']) == str) and ('BTS_FILE' in i['value']) ):
                i['value'] = '"UAero_lamda_{:04.1f}_phase_{:04.1f}_umean_{:04.1f}.bts"'.format(l, phase, umean)
                break
        f.write()
    

def write_inflow_fluct(lamda, phase, umean, zhub):
    """Write a TurbSim style bts file for investigating the effect of
    spatial velocity fluctuations at a specific frequency

    Inputs:
       lamda: Wavelength of oscillations in 'y' and 'z' direction
       phase: Phase of oscillations w.r.t hub center
       umean: Mean inflow velocity
       zhub: Hub height of turbine

    Outputs:
       None: File written to UAero_lamda_{lamda_value}.bts
    """

    print("Working on fluctuation of wavelength {} ".format(lamda))    
    dy_dz = 0.1 * lamda
    ny_nz = int(np.rint(2.0 * zhub / dy_dz)) + 1

    ts_file = TurbSimFile()
    ts_file['info'] = 'Inflow file to study effect of unsteady inflow'
    ts_file['ID'] = 8
    ts_file['dt'] = 0.05
    ts_file['uHub'] = umean
    ts_file['zHub'] = zhub
    ts_file['y'] = np.linspace(-zhub, zhub, ny_nz)
    ts_file['z'] = np.linspace(-10.0, 2.0 * zhub - 10.0, ny_nz)
    ts_file['t'] = np.array([0,0.05])
    u = np.zeros((3, 2, ny_nz, ny_nz))
    u[0, 0, :, :] = umean * (1.0 + 0.1*np.outer( np.sin(2.0 * np.pi / lamda * ts_file['y'] + phase ), np.sin(2.0 * np.pi / lamda * (ts_file['z'] - zhub) + phase ) ))
    u[0, 1, :, :] = umean * (1.0 + 0.1*np.outer( np.sin(2.0 * np.pi / lamda * ts_file['y'] + phase ), np.sin(2.0 * np.pi / lamda * (ts_file['z'] - zhub) + phase ) ))
    ts_file['u'] = u
    ts_file.filename = 'lamda_{:04.1f}_phase_{:04.1f}_umean_{:04.1f}/UAero_lamda_{:04.1f}_phase_{:04.1f}_umean_{:04.1f}.bts'.format(lamda, phase, umean, lamda, phase, umean)
    ts_file.write()


def gen_temporal_fluct_cases(freq_range, umean, zhub):
    """Generate a set of OpenFAST cases to investigate effect of temporal
    velocity fluctuations at a specific frequency

    Inputs:
       freq_range: Frequency range of temporal oscillations
       umean: Mean inflow velocity
       zhub: Hub height of turbine

    Outputs:
       None: Files written to UAero_freq_{lamda_value}
    """

    ref_dir   = 'template'  # Folder where the fast input files are located (will be copied)
    main_file = 'IEA-15-240-RWT.fst'  # Main file in ref_dir, used as a template
    work_dir = '.'     # Output folder (will be created)    
    PARAMS = [ {'__name__': 'freq_{:04.1f}_umean_{:04.1f}'.format(l, umean) } for l in freq_range]
    fastfiles=case_gen.templateReplace(PARAMS, ref_dir, outputDir=work_dir, removeRefSubFiles=True, main_file=main_file, oneSimPerDir=True)
    
    for l in freq_range:
        write_temporal_inflow_fluct(l, umean, 150.0)
        f = FASTInputFile('freq_{:04.1f}_umean_{:04.1f}/InflowFile_UAero.dat'.format(l, umean))
        for i in f:
            if ( (type(i['value']) == str) and ('BTS_FILE' in i['value']) ):
                i['value'] = '"UAero_freq_{:04.1f}_umean_{:04.1f}.bts"'.format(l, umean)
                break
        f.write()
    

def write_temporal_inflow_fluct(freq, umean, zhub):
    """Write a TurbSim style bts file for investigating the effect of
    temporal velocity fluctuations at a specific frequency

    Inputs:
       freq: Frequency of oscillations in time
       umean: Mean inflow velocity
       zhub: Hub height of turbine

    Outputs:
       None: File written to UAero_freq_{lamda_value}.bts
    """

    print("Working on fluctuation of frequency {} ".format(freq))    
    dy_dz = 10.0
    ny_nz = int(np.rint(2.0 * zhub / dy_dz)) + 1

    ts_file = TurbSimFile()
    ts_file['info'] = 'Inflow file to study effect of unsteady inflow'
    ts_file['ID'] = 8
    dt =  0.05 / freq
    ts_file['dt'] = dt
    ts_file['uHub'] = umean
    ts_file['zHub'] = zhub
    ts_file['y'] = np.linspace(-zhub, zhub, ny_nz)
    ts_file['z'] = np.linspace(-10.0, 2.0 * zhub - 10.0, ny_nz)
    time_ar =  np.arange(0, 1.0/freq+1e-6,  dt)
    ts_file['t'] = time_ar
    u = np.zeros((3, np.size(time_ar), ny_nz, ny_nz))
    for i, t in enumerate(time_ar):
        u[0, i, :, :] = umean * (1.0 + 0.1 * np.sin(2.0 * np.pi * freq * t) )
    ts_file['u'] = u
    ts_file.filename = 'freq_{:04.1f}_umean_{:04.1f}/UAero_freq_{:04.1f}_umean_{:04.1f}.bts'.format(freq, umean, freq, umean)
    ts_file.write()
    
if __name__=="__main__":

    # l_cases = pd.read_excel('Divya - OpenFAST Cases Parameter Combos.xlsx',sheet_name=1)
    # n_lamda = l_cases.iloc[:,0].isnull().argmax()
    # nPhase = l_cases.iloc[:,1].isnull().argmax()
    # phases = l_cases.iloc[:nPhase, 1]
    # lamdas = l_cases.iloc[:nLamda, 0]


    lamdas = np.linspace(3.0,120.0,30)
    phases = np.linspace(0, 0.75*np.pi, 4)
    windspeeds = np.array([8.0, 10.59, 13.0])

    for p in phases:
        for ws in windspeeds:
            gen_spatial_fluct_cases(lamdas, p, ws, 150.0)

    #for ws in windspeeds:
        #freqs = lamdas / (0.1 * ws)
        #gen_temporal_fluct_cases(freqs, ws, 150.0)
            
