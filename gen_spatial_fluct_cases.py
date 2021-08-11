# coding: utf-8
import numpy as np
from pyFAST.input_output import TurbSimFile
import pyFAST.case_generation.case_gen as case_gen
from pyFAST.input_output import FASTInputFile

def gen_spatial_fluct_cases(lamda_range, umean, zhub):
    """Generate a set of OpenFAST cases to investigate effect of spatial
    velocity fluctuations at a specific frequency

    Inputs:
       lamda_range: Wavelength of oscillations in 'y' and 'z' direction
       umean: Mean inflow velocity
       zhub: Hub height of turbine

    Outputs:
       None: File written to UAero_lamda_{lamda_value}.bts
    """

            
        
    ref_dir   = 'template'  # Folder where the fast input files are located (will be copied)
    main_file = 'IEA-15-240-RWT.fst'  # Main file in ref_dir, used as a template
    work_dir = '.'     # Output folder (will be created)
    PARAMS = [ {'__name__': 'lamda_{:04.1f}'.format(l) } for l in lamda_range]
    fastfiles=case_gen.templateReplace(PARAMS, ref_dir, outputDir=work_dir, removeRefSubFiles=True, main_file=main_file, oneSimPerDir=True)
    
    for l in lamda_range:
        write_inflow_fluct(l, 8.0, 150.0)
        f = FASTInputFile('lamda_{:04.1f}/InflowFile_UAero.dat'.format(l))
        for i in f:
            if ( (type(i['value']) == str) and ('BTS_FILE' in i['value']) ):
                i['value'] = '"UAero_lamda_{:04.1f}.bts"'.format(l)
                break
        f.write()
    

def write_inflow_fluct(lamda, umean, zhub):
    """Write a TurbSim style bts file for investigating the effect of
    spatial velocity fluctuations at a specific frequency

    Inputs:
       lamda: Wavelength of oscillations in 'y' and 'z' direction
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
    u[0, 0, :, :] = umean + (0.1 * umean) * np.outer( np.sin(2.0 * np.pi / lamda * ts_file['y']), np.sin(2.0 * np.pi / lamda * (ts_file['z'] - zhub) ) )
    u[0, 1, :, :] = umean + (0.1 * umean) * np.outer( np.sin(2.0 * np.pi / lamda * ts_file['y']), np.sin(2.0 * np.pi / lamda * (ts_file['z'] - zhub) ) )
    ts_file['u'] = u
    ts_file.filename = 'lamda_{:04.1f}/UAero_lamda_{:04.1f}.bts'.format(lamda, lamda)
    ts_file.write()


if __name__=="__main__":

    lamda_range = np.linspace(3.0, 120.0, 30)
    gen_spatial_fluct_cases( lamda_range, 8.0, 150.0)
    
