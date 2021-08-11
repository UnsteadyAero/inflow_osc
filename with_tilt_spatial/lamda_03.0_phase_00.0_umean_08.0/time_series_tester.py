import matplotlib
matplotlib.use('Agg')
import pyFAST.input_output as io
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

of_data = io.fast_output_file.FASTOutputFile('IEA-15-240-RWT.outb').toDataFrame()
outputs = of_data.columns

for output in outputs:
    if "Root" in output:
        print(output)

