from matplotlib import pyplot
from openpyxl import  load_workbook

wb = load_workbook('data_analysis_lab.xlsx')
sheet = wb['Data']

def getvalue(x):
    return x.value

years = list(map(getvalue, sheet['A'][1:]))
temp = list(map(getvalue, sheet['C'][1:]))
sun = list(map(getvalue, sheet['D'][1:]))

pyplot.plot(years,temp)
pyplot.plot(years,sun)

pyplot.show()