import matplotlib
matplotlib.use('Agg')
import pyFAST.input_output as io
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing
from multiprocessing import Pool

def calc_stats(case):
    loads = io.fast_output_file.FASTOutputFile('{}/IEA-15-240-RWT.outb'.format(case)).toDataFrame()
    tfilter = (loads['Time_[s]'] > 75.0)
    return loads[tfilter].std()


def plot_stats_vel(of_channels = ['TwrBsMyt_[kN-m]', 'RootFxb1_[kN]', 'RootMyb1_[kN-m]', 'RootFyb1_[kN]', 'RootMxb1_[kN-m]', 'RtAeroMxh_[N-m]', 'RtAeroFxh_[N]', 'OoPDefl1_[m]', 'LSShftMxa_[kN-m]', 'Wind1VelX_[m/s]', 'AB1N019Alpha_[deg]', 'AB1N035Alpha_[deg]', 'AB1N045Alpha_[deg]', 'AB1N019Fx_[N/m]', 'AB1N035Fx_[N/m]', 'AB1N045Fx_[N/m]', 'AB1N019Fy_[N/m]', 'AB1N035Fy_[N/m]', 'AB1N045Fy_[N/m]', 'AB1N019VUndx_[m/s]', 'AB1N035VUndx_[m/s]', 'AB1N045VUndx_[m/s]', 'AB1N019Cl_[-]', 'AB1N035Cl_[-]', 'AB1N045Cl_[-]']):

    #Velocity
    vel_range = ['08.0', '10.6', '13.0']

    #freqs
    freqs =  1.0/np.logspace(-1, 2.18, 30)    

    #Function of Velocity (held phase constant at 00.0 rad)
    with PdfPages('function_of_vel_output.pdf') as pfpgs:
        vel_stats = []
        for vel in vel_range:
            end = '_phase_00.0_umean_' + vel
            freq_dirs = ['freq_{:06.3f}'.format(f) + end for f in freqs]

            p = Pool(multiprocessing.cpu_count())
            of_stats = p.map(calc_stats, freq_dirs)
            vel_stats.append(of_stats)

        #baseline = calc_stats('steady')
        for o in of_channels:
            fig = plt.figure()
            for i in range(len(vel_stats)):
                y = [c[o] for c in vel_stats[i]]
                plt.plot(freqs, y, label = vel_range[i])
                #plt.axhline( baseline[o]['std'])
            plt.ylabel(o)
            plt.xlabel('frequency [Hz]')
            plt.title(o + ' SD vs frequency')
            plt.legend()
            plt.grid()
            plt.tight_layout()
            pfpgs.savefig()
            plt.close(fig)
            
        p.close()

if __name__=="__main__":
    plot_stats_vel(['TwrBsMyt_[kN-m]', 'RootFxb1_[kN]', 'RootMyb1_[kN-m]', 'RootFyb1_[kN]', 'RootMxb1_[kN-m]', 'RtAeroMxh_[N-m]', 'RtAeroFxh_[N]', 'OoPDefl1_[m]', 'LSShftMxa_[kN-m]', 'Wind1VelX_[m/s]', 'AB1N019Alpha_[deg]', 'AB1N035Alpha_[deg]', 'AB1N045Alpha_[deg]', 'AB1N019Fx_[N/m]', 'AB1N035Fx_[N/m]', 'AB1N045Fx_[N/m]', 'AB1N019Fy_[N/m]', 'AB1N035Fy_[N/m]', 'AB1N045Fy_[N/m]', 'AB1N019VUndx_[m/s]', 'AB1N035VUndx_[m/s]', 'AB1N045VUndx_[m/s]', 'AB1N019Cl_[-]', 'AB1N035Cl_[-]', 'AB1N045Cl_[-]'])
