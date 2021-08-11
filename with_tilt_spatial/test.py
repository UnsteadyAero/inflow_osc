import matplotlib
matplotlib.use('Agg')
import pyFAST.input_output as io
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np

#steady = io.fast_output_file.FASTOutputFile('steady/IEA-15-240-RWT.outb').toDataFrame()
#time = steady['Time_[s]']
#print(time[0])

def steady_time_stds(time_range):
    steady = io.fast_output_file.FASTOutputFile('steady/IEA-15-240-RWT.outb').toDataFrame()
    stds = []
    times = []

    for time in time_range:
        #stats = steady[int(time):].std()
        #stds.append(stats)
        time = steady['Time_[s]'][int(time)]
        times.append(time)

    return times

time_range = np.linspace(0, 60000, 11).astype(int)
print(time_range)
