import matplotlib
matplotlib.use('Agg')
import pyFAST.input_output as io
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing
from multiprocessing import Pool

def calc_stats(case):
    return io.fast_output_file.FASTOutputFile('{}/IEA-15-240-RWT.outb'.format(case)).toDataFrame().describe()

def plot_stats(of_channels = ['TwrBsMyt_[Nm]','RootFxb1_[N]','RootMyb1_[Nm]','RootFyb1_[N]','RootMxb1_[Nm]','RtAeroFxh_[N]','RtAeroMxh_[Nm]','AB1N019Alpha_[deg]', 'AB1N035Alpha_[deg]', 'AB1N045Alpha_[deg]','AB1N019Fx_[N]', 'AB1N035Fx_[N]', 'AB1N045Fx_[N]', 'AB1N019Fy_[N]', 'AB1N035Fy_[N]', 'AB1N045Fy_[N]', 'OoPDefl1_[m]']):
    
    lamda_range = np.linspace(3.0, 120.0, 30)
    lamda_dirs = ['lamda_{:04.1f}'.format(l) for l in lamda_range]

    p = Pool(multiprocessing.cpu_count())
    of_stats = p.map(calc_stats, lamda_dirs)

    baseline = calc_stats('steady')
    
    with PdfPages('new_output_stds_vs_lamda.pdf') as pfpgs:
        for o in of_channels:
            fig = plt.figure()
            y = [ c[o]['std'] for c in of_stats ]
            plt.plot(lamda_range, y)
            plt.axhline( baseline[o]['std'], color = 'm')
            plt.ylabel(o)
            plt.xlabel(r'$\lambda$ (m)')
            plt.legend(['Turbulent Cases', 'Steady Case'])
            plt.grid()
            plt.tight_layout()
            pfpgs.savefig()
            plt.close(fig)
            
    p.close()
    


if __name__=="__main__":
    #plot_time_series()
    plot_stats(['RtAeroFxh_[N]','RtAeroMxh_[N-m]','AB1N019Alpha_[deg]', 'AB1N035Alpha_[deg]', 'AB1N045Alpha_[deg]','AB1N019Fx_[N/m]', 'AB1N035Fx_[N/m]', 'AB1N045Fx_[N/m]', 'AB1N019Fy_[N/m]', 'AB1N035Fy_[N/m]', 'AB1N045Fy_[N/m]', 'OoPDefl1_[m]'])
