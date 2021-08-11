import matplotlib
matplotlib.use('Agg')
import pyFAST.input_output as io
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing
from multiprocessing import Pool
import pandas as pd

def plot_time_series(of_channels = ['TwrBsMyt_[kN-m]', 'RootFxb1_[kN]', 'RootMyb1_[kN-m]', 'RootFyb1_[kN]', 'RootMxb1_[kN-m]', 'RtAeroMxh_[N-m]', 'RtAeroFxh_[N]', 'OoPDefl1_[m]', 'LSShftMxa_[kN-m]', 'Wind1VelX_[m/s]', 'AB1N019Alpha_[deg]', 'AB1N035Alpha_[deg]', 'AB1N045Alpha_[deg]', 'AB1N019Fx_[N/m]', 'AB1N035Fx_[N/m]', 'AB1N045Fx_[N/m]', 'AB1N019Fy_[N/m]', 'AB1N035Fy_[N/m]', 'AB1N045Fy_[N/m]', 'AB1N019VUndx_[m/s]', 'AB1N035VUndx_[m/s]', 'AB1N045VUndx_[m/s]', 'AB1N019Cl_[-]', 'AB1N035Cl_[-]', 'AB1N045Cl_[-]']):

    vels = [08.0, 10.59, 13.0]
    lamdas = [03.0, 120.0]

    for vel in vels:
        end = '_umean_{:04.1f}/IEA-15-240-RWT.outb'.format(vel)
        responses = []
        for lamda in lamdas:
            start = 'lamda_{:04.1f}'.format(lamda)
            phases = ['00.0', '00.8', '01.6', '02.4']
            dataframes = []
            for phase in phases:
                df = io.fast_output_file.FASTOutputFile(start + '_phase_{}'.format(phase) + end).toDataFrame()
                dataframes.append(df)
            response = sum(dataframes)/len(dataframes)
            responses.append(response)
    
        steady_response = io.fast_output_file.FASTOutputFile('steady_{:04.1f}/IEA-15-240-RWT.outb'.format(vel)).toDataFrame()
        responses.append(steady_response)

        lamda_names = [r'$\lambda$ = {:04.1f}'.format(l) for l in lamdas]
        lamda_names.append('steady')
  
        with PdfPages('times_series_speed_{:04.1f}.pdf'.format(vel)) as pfpgs:
            for c in responses[0].columns[1:]:
                if c in of_channels:
                    fig = plt.figure()
                    for i in range(len(responses)):
                        response = responses[i]
                        tfilter = (response['Time_[s]'] > 75.0)
                        plt.plot(response['Time_[s]'][tfilter], response[c][tfilter], label = lamda_names[i])
                    plt.xlabel('Time (s)')
                    plt.ylabel(c)
                    plt.title(c + ' Time Series Response')
                    plt.legend()
                    plt.grid()
                    plt.tight_layout()
                    pfpgs.savefig()
                    plt.close(fig)


if __name__=="__main__":
    plot_time_series(['TwrBsMyt_[kN-m]', 'RootFxb1_[kN]', 'RootMyb1_[kN-m]', 'RootFyb1_[kN]', 'RootMxb1_[kN-m]', 'RtAeroMxh_[N-m]', 'RtAeroFxh_[N]', 'OoPDefl1_[m]', 'LSShftMxa_[kN-m]', 'Wind1VelX_[m/s]', 'AB1N019Alpha_[deg]', 'AB1N035Alpha_[deg]', 'AB1N045Alpha_[deg]', 'AB1N019Fx_[N/m]', 'AB1N035Fx_[N/m]', 'AB1N045Fx_[N/m]', 'AB1N019Fy_[N/m]', 'AB1N035Fy_[N/m]', 'AB1N045Fy_[N/m]', 'AB1N019VUndx_[m/s]', 'AB1N035VUndx_[m/s]', 'AB1N045VUndx_[m/s]', 'AB1N019Cl_[-]', 'AB1N035Cl_[-]', 'AB1N045Cl_[-]'])
