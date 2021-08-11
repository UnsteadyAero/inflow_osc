import matplotlib
matplotlib.use('Agg')
import pyFAST.input_output as io
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

lamda_range = [116.0, 1e16]
lamda_dirs = ['lamda_116.0', 'steady']
#lamda_dirs = ['lamda_{:04.1f}/IEA-15-240-RWT.outb'.format(l) for l in lamda_range]

of_data = [ io.fast_output_file.FASTOutputFile('{}/IEA-15-240-RWT.outb'.format(l)).toDataFrame() for l in lamda_dirs]

name = lamda_dirs[0] + '_vs_' + lamda_dirs[1] + '_output.pdf'
with PdfPages(name) as pfpgs:
    for c in of_data[0].columns[1:]:
        if ('AB1N' not in c):
            fig, ax = plt.subplots(1,1,figsize=(6.4,4.8))
            for i, o in enumerate(of_data):
                tfilter = (o['Time_[s]'] > 150.0)
                ax.plot(o['Time_[s]'][tfilter], o[c][tfilter],
                        linewidth=0.3,
                        label=r'$\lambda = {}$'.format(lamda_range[i]))
                
            ax.set_xlabel('Time (s)')
            ax.set_ylabel(c.split('_')[0] + ' ' + c.split('_')[1])
            plt.legend(loc=0)
            plt.tight_layout()
            pfpgs.savefig()
            plt.close()
