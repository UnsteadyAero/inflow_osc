import matplotlib
matplotlib.use('Agg')
import pyFAST.input_output as io
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing
from multiprocessing import Pool
import pandas as pd

def calc_stats(directory):
    response = io.fast_output_file.FASTOutputFile(directory).toDataFrame()
    tfilter = (response['Time_[s]'] > 75.0)
    return response[tfilter].std()

def plot_stats(of_channels = ['TwrBsMyt_[kN-m]', 'RootFxb1_[kN]', 'RootMyb1_[kN-m]', 'RootFyb1_[kN]', 'RootMxb1_[kN-m]', 'RtAeroMxh_[N-m]', 'RtAeroFxh_[N]', 'OoPDefl1_[m]', 'LSShftMxa_[kN-m]', 'Wind1VelX_[m/s]', 'AB1N019Alpha_[deg]', 'AB1N035Alpha_[deg]', 'AB1N045Alpha_[deg]', 'AB1N019Fx_[N/m]', 'AB1N035Fx_[N/m]', 'AB1N045Fx_[N/m]', 'AB1N019Fy_[N/m]', 'AB1N035Fy_[N/m]', 'AB1N045Fy_[N/m]', 'AB1N019VUndx_[m/s]', 'AB1N035VUndx_[m/s]', 'AB1N045VUndx_[m/s]', 'AB1N019Cl_[-]', 'AB1N035Cl_[-]', 'AB1N045Cl_[-]']):

    vels = [08.0, 10.59, 13.0]   
    freqs =  1.0/np.logspace(-1, 2.18, 30)

    vel_stats = []
    baselines = []

    for vel in vels:
        directories = []

        end = '_umean_{:04.1f}/IEA-15-240-RWT.outb'.format(vel)
        freq_dirs = ['freq_{:06.3f}'.format(f) + end for f in freqs]
        p = Pool(multiprocessing.cpu_count())
        of_stats = p.map(calc_stats, freq_dirs)
        vel_stats.append(of_stats)

        steady_response = io.fast_output_file.FASTOutputFile('steady_{:04.1f}/IEA-15-240-RWT.outb'.format(vel)).toDataFrame()
        tfilter = (steady_response['Time_[s]'] > 75.0)   
        baseline = steady_response[tfilter].std()
        baselines.append(baseline)
    
    with PdfPages('load_sd_response_vs_freq.pdf') as pfpgs:
        for o in of_channels:
            fig = plt.figure()
            colors = ['dodgerblue', 'forestgreen', 'darkorange']
            for i in range(len(vel_stats)):
                y = [c[o] for c in vel_stats[i]]
                plt.semilogx(freqs, y, color = colors[i], label = vels[i])
            for i in range(len(baselines)):
                plt.axhline(baselines[i][o], color = colors[i], linestyle = 'dashed')
            plt.axvline(x=0.1, color = 'black', linestyle = 'dotted')
            plt.ylabel(o)
            plt.xlabel('Frequency (Hz)')
            plt.title(o + ' SD vs frequency')
            plt.legend()
            plt.grid()
            plt.tight_layout()
            pfpgs.savefig()
            plt.close(fig)
        p.close()

if __name__=="__main__":
    plot_stats(['TwrBsMyt_[kN-m]', 'RootFxb1_[kN]', 'RootMyb1_[kN-m]', 'RootFyb1_[kN]', 'RootMxb1_[kN-m]', 'RtAeroMxh_[N-m]', 'RtAeroFxh_[N]', 'OoPDefl1_[m]', 'LSShftMxa_[kN-m]', 'Wind1VelX_[m/s]', 'AB1N019Alpha_[deg]', 'AB1N035Alpha_[deg]', 'AB1N045Alpha_[deg]', 'AB1N019Fx_[N/m]', 'AB1N035Fx_[N/m]', 'AB1N045Fx_[N/m]', 'AB1N019Fy_[N/m]', 'AB1N035Fy_[N/m]', 'AB1N045Fy_[N/m]', 'AB1N019VUndx_[m/s]', 'AB1N035VUndx_[m/s]', 'AB1N045VUndx_[m/s]', 'AB1N019Cl_[-]', 'AB1N035Cl_[-]', 'AB1N045Cl_[-]'])
