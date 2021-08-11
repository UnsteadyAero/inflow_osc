import numpy as np
import pyFAST.input_output as io
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

#Lamda Generation
lamda_range = np.linspace(3.0, 120.0, 30)
lamdas = lamda_range.tolist()

#DESIRED OUTPUTS: GenSpeed (4), OoPDefl1 (8), RootMyc (17), Spn2MLyb1 (22), YawBrFzp (29)
#Input: list of lists containing index and name: [[#, 'name'], ...]
desired_outputs = [[4, 'Generator Speed SD (rpm)'], [8, 'Blade 1 Out of Plane Tip Deflection SD (m)'], [17, 'Blade 1 Out of Plane Moment SD (kN-m)'], [22,'Blade 1 Local Flapwise Moment SD (kN-m)'], [29, 'Tower Top Axial Force SD (kN)']]

#Initialization and Data Extraction
for i in range(len(desired_outputs)):
    desired_outputs[i].append([])

for l in lamda_range:
    lamda_dir = "lamda_{:04.1f}".format(l) + "/IEA-15-240-RWT.outb"	#Name of output file for specific lamda
    data_stds = io.fast_output_file.FASTOutputFile(lamda_dir).toDataFrame().std()	#Standard deviations of outputs for specific lamda
    for i in range(len(desired_outputs)):
        data_index = desired_outputs[i][0]
        desired_outputs[i][2].append(data_stds[data_index])

#Plots
with PdfPages('divya_responsestds_vs_lamda.pdf') as pfpgs:
    for i in range(len(desired_outputs)):
        plt.plot(lamdas, desired_outputs[i][2])
        plt.title(desired_outputs[i][1] + ' vs. Wavelength')
        plt.xlabel('Wavelength Lamda (m)')
        plt.ylabel(desired_outputs[i][1])
        pfpgs.savefig()
        plt.close()
