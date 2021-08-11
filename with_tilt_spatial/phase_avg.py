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

def plot_stats_phase(of_channels = ['RtAeroMxh_[N-m]']):

    #Phase
    phase_range = ['00.0', '00.8', '01.6', '02.4']

    #Lamdas
    lamda_range = np.linspace(3.0, 120.0, 30)

    #Function of Phase (held velocity constant at 08.0 m/s)
    with PdfPages('phases.pdf') as pfpgs:
        phase_stats = []

        for phase in phase_range:
            end = '_phase_' + phase + '_umean_08.0'
            lamda_dirs = ['lamda_{:04.1f}'.format(l) + end for l in lamda_range]

            p = Pool(multiprocessing.cpu_count())
            of_stats = p.map(calc_stats, lamda_dirs)

            phase_stats.append(of_stats)

        #avg = sum(phase_stats)
        #print(avg)

        #phase_stats.append(avg)
        #phase_range.append('average')

        for o in of_channels:
            fig = plt.figure()
            average = []
            for i in range(len(phase_stats)):
                y = [c[o] for c in phase_stats[i]]
                average.append(y)
                plt.plot(lamda_range, y, label = phase_range[i])
            avg = [sum(x)/len(x) for x in zip(*average)]
            plt.plot(lamda_range, avg, label = 'average')
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
    plot_stats_phase(['RtAeroMxh_[N-m]'])
