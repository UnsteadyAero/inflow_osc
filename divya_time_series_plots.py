import matplotlib
matplotlib.use('Agg')
import pyFAST.input_output as io
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import os

#Finds lamda folders in current directory and creates list of them
currentdir = os.path.abspath(os.getcwd())
lamdas = []
for root, subdirs, files in os.walk(currentdir):
    for subdir in subdirs:
        if subdir.startswith("lamda"):
            lamdas.append(subdir)

#Iterates through lamda list and generates plots for each lamda
for lamda in lamdas:
    dir = currentdir + "/" + lamda
    os.chdir(dir)	#Changes directory to specific lamda folder (plot pdf will be generated in this folder)
    print(lamda)	#Checks what lamda the for loop is on

    #Runs analyze_case.py code and generates plots using simulaton results for specific lamda ('IEA-15-240-RWT.out')
    df = io.fast_output_file.FASTOutputFile('IEA-15-240-RWT.out').toDataFrame()
    name = 'openfast_output_' + lamda + '.pdf'	#Includes specific lamda in output pdf name
    with PdfPages(name) as pfpgs:
        for c in df.columns[1:]:
            if ('AB1N' not in c):
                fig, ax = plt.subplots(1,1,figsize=(6.4,4.8))
                ax.plot(df['Time_[s]'],df[c])
                ax.set_xlabel('Time (s)')
                ax.set_ylabel(c.split('_')[0] + ' ' + c.split('_')[1])
                plt.tight_layout()
                pfpgs.savefig()
                plt.close(fig)
