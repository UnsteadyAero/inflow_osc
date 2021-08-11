import matplotlib
matplotlib.use('Agg')
import pyFAST.input_output as io
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

df = io.fast_output_file.FASTOutputFile('IEA-15-240-RWT.out').toDataFrame()

with PdfPages('openfast_output.pdf') as pfpgs:
    for c in df.columns[1:]:
        if ('AB1N' not in c):
            fig, ax = plt.subplots(1,1,figsize=(6.4,4.8))
            ax.plot(df['Time_[s]'],df[c])
            ax.set_xlabel('Time (s)')
            ax.set_ylabel(c.split('_')[0] + ' ' + c.split('_')[1])
            plt.tight_layout()
            pfpgs.savefig()
            plt.close(fig)
