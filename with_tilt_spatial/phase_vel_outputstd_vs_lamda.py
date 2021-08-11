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

def plot_stats_phase(of_channels = ['TwrBsMyt_[kN-m]', 'RootFxb1_[kN]', 'RootMyb1_[kN-m]', 'RootFyb1_[kN]', 'RootMxb1_[kN-m]', 'RtAeroMxh_[N-m]', 'RtAeroFxh_[N]', 'OoPDefl1_[m]', 'LSShftMxa_[kN-m]', 'Wind1VelX_[m/s]', 'AB1N019Alpha_[deg]', 'AB1N035Alpha_[deg]', 'AB1N045Alpha_[deg]', 'AB1N019Fx_[N/m]', 'AB1N035Fx_[N/m]', 'AB1N045Fx_[N/m]', 'AB1N019Fy_[N/m]', 'AB1N035Fy_[N/m]', 'AB1N045Fy_[N/m]', 'AB1N019VUndx_[m/s]', 'AB1N035VUndx_[m/s]', 'AB1N045VUndx_[m/s]', 'AB1N019Cl_[-]', 'AB1N035Cl_[-]', 'AB1N045Cl_[-]']):

    #Phase
    phase_range = ['00.0', '00.8', '01.6', '02.4']

    #Lamdas
    lamda_range = np.linspace(3.0, 120.0, 30)

    #Function of Phase (held velocity constant at 08.0 m/s)
    with PdfPages('function_of_phase_output.pdf') as pfpgs:
        phase_stats = []
        for phase in phase_range:
            end = '_phase_' + phase + '_umean_08.0'
            lamda_dirs = ['lamda_{:04.1f}'.format(l) + end for l in lamda_range]

            p = Pool(multiprocessing.cpu_count())
            of_stats = p.map(calc_stats, lamda_dirs)
            phase_stats.append(of_stats)

        #baseline = calc_stats('steady')
        for o in of_channels:
            fig = plt.figure()
            for i in range(len(phase_stats)):
                y = [c[o] for c in phase_stats[i]]
                plt.plot(lamda_range, y, label = phase_range[i])
                #plt.axhline( baseline[o]['std'])
            plt.ylabel(o)
            plt.xlabel(r'$\lambda$ (m)')
            plt.title(o + ' SD vs ' + r'$\lambda$ (m)')
            plt.legend()
            plt.grid()
            plt.tight_layout()
            pfpgs.savefig()
            plt.close(fig)
            
        p.close()


def plot_stats_vel(of_channels = ['TwrBsMyt_[kN-m]', 'RootFxb1_[kN]', 'RootMyb1_[kN-m]', 'RootFyb1_[kN]', 'RootMxb1_[kN-m]', 'RtAeroMxh_[N-m]', 'RtAeroFxh_[N]', 'OoPDefl1_[m]', 'LSShftMxa_[kN-m]', 'Wind1VelX_[m/s]', 'AB1N019Alpha_[deg]', 'AB1N035Alpha_[deg]', 'AB1N045Alpha_[deg]', 'AB1N019Fx_[N/m]', 'AB1N035Fx_[N/m]', 'AB1N045Fx_[N/m]', 'AB1N019Fy_[N/m]', 'AB1N035Fy_[N/m]', 'AB1N045Fy_[N/m]', 'AB1N019VUndx_[m/s]', 'AB1N035VUndx_[m/s]', 'AB1N045VUndx_[m/s]', 'AB1N019Cl_[-]', 'AB1N035Cl_[-]', 'AB1N045Cl_[-]']):

    #Velocity
    vel_range = ['08.0', '10.6', '13.0']

    #Lamdas
    lamda_range = np.linspace(3.0, 120.0, 30)    

    #Function of Velocity (held phase constant at 00.0 rad)
    with PdfPages('function_of_vel_output.pdf') as pfpgs:
        vel_stats = []
        for vel in vel_range:
            end = '_phase_00.0_umean_' + vel
            lamda_dirs = ['lamda_{:04.1f}'.format(l) + end for l in lamda_range]

            p = Pool(multiprocessing.cpu_count())
            of_stats = p.map(calc_stats, lamda_dirs)
            vel_stats.append(of_stats)

        #baseline = calc_stats('steady')
        for o in of_channels:
            fig = plt.figure()
            for i in range(len(vel_stats)):
                y = [c[o] for c in vel_stats[i]]
                plt.plot(lamda_range, y, label = vel_range[i])
                #plt.axhline( baseline[o]['std'])
            plt.ylabel(o)
            plt.xlabel(r'$\lambda$ (m)')
            plt.title(o + ' SD vs ' + r'$\lambda$ (m)')
            plt.legend()
            plt.grid()
            plt.tight_layout()
            pfpgs.savefig()
            plt.close(fig)
            
        p.close()

if __name__=="__main__":
    plot_stats_phase(['TwrBsMyt_[kN-m]', 'RootFxb1_[kN]', 'RootMyb1_[kN-m]', 'RootFyb1_[kN]', 'RootMxb1_[kN-m]', 'RtAeroMxh_[N-m]', 'RtAeroFxh_[N]', 'OoPDefl1_[m]', 'LSShftMxa_[kN-m]', 'Wind1VelX_[m/s]', 'AB1N019Alpha_[deg]', 'AB1N035Alpha_[deg]', 'AB1N045Alpha_[deg]', 'AB1N019Fx_[N/m]', 'AB1N035Fx_[N/m]', 'AB1N045Fx_[N/m]', 'AB1N019Fy_[N/m]', 'AB1N035Fy_[N/m]', 'AB1N045Fy_[N/m]', 'AB1N019VUndx_[m/s]', 'AB1N035VUndx_[m/s]', 'AB1N045VUndx_[m/s]', 'AB1N019Cl_[-]', 'AB1N035Cl_[-]', 'AB1N045Cl_[-]'])
    plot_stats_vel(['TwrBsMyt_[kN-m]', 'RootFxb1_[kN]', 'RootMyb1_[kN-m]', 'RootFyb1_[kN]', 'RootMxb1_[kN-m]', 'RtAeroMxh_[N-m]', 'RtAeroFxh_[N]', 'OoPDefl1_[m]', 'LSShftMxa_[kN-m]', 'Wind1VelX_[m/s]', 'AB1N019Alpha_[deg]', 'AB1N035Alpha_[deg]', 'AB1N045Alpha_[deg]', 'AB1N019Fx_[N/m]', 'AB1N035Fx_[N/m]', 'AB1N045Fx_[N/m]', 'AB1N019Fy_[N/m]', 'AB1N035Fy_[N/m]', 'AB1N045Fy_[N/m]', 'AB1N019VUndx_[m/s]', 'AB1N035VUndx_[m/s]', 'AB1N045VUndx_[m/s]', 'AB1N019Cl_[-]', 'AB1N035Cl_[-]', 'AB1N045Cl_[-]'])
