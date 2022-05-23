"""
5/23/22
June Lee
"""

import math
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt

def calcCasesByVariant():
    # access csv files, change file name as necessary
    casesData = pd.read_csv('CDC052322.csv', skiprows=(0,1))
    varData = pd.read_csv('CovidPropsJ.csv')

    # specify columns, convert to numpy
    dates = pd.DataFrame(casesData, columns=['Date'])
    avgCases = pd.DataFrame(casesData, columns=['7-Day Moving Avg'])
    dates = pd.DataFrame.to_numpy(dates, dtype=str)
    avgCases = pd.DataFrame.to_numpy(avgCases, dtype=int)
    
    percentDelta = pd.DataFrame(varData, columns=['perc_deltas'])
    percentOmicron = pd.DataFrame(varData, columns=['perc_omicrons'])
    percentDelta = pd.DataFrame.to_numpy(percentDelta, dtype=float)
    percentOmicron = pd.DataFrame.to_numpy(percentOmicron, dtype=float)
    
    # preallocate empty lists for biweekly dates and cases
    biweeklyDates = []
    biweeklyCases = []
    n = None

    #fill in biweekly dates/cases based on starting date (Jan 11 2021)
    for i in range(len(dates[:,0])):
        j = len(dates[:,0]) - 1 - i
        if dates[j,0] == 'Jan 11 2021':
            biweeklyDates.append(dates[j,0])
            biweeklyCases.append(avgCases[j,0])
            n = j
            break
    
    for i in range(34):
        n = n - 14
        biweeklyDates.append(dates[n,0])
        biweeklyCases.append(avgCases[n,0])
    

    numDelta = []
    numOmicron = []
    for i in range(len(biweeklyDates)):
        delta = percentDelta[i,0]*biweeklyCases[i]
        numDelta.append(delta)
        omicron = percentOmicron[i,0]*biweeklyCases[i]
        numOmicron.append(omicron)
        
    finalTable = [['Dates', '# of Delta', '# of Omicron', '# of Total Cases']]
    for i in range(len(biweeklyDates)):
        finalTable.append([biweeklyDates[i], numDelta[i], numOmicron[i], biweeklyCases[i]])
    
    return(biweeklyDates, biweeklyCases, numDelta, numOmicron)

    """
    plt.figure()
    fig, ax = plt.subplots()
    ax.plot(numDelta, label='# of Cases Delta')
    ax.plot(numOmicron, label='# of Cases Omicron')
    legend = ax.legend(loc='upper left')
    plt.title('Delta to Omicron Transition')
    plt.xlabel('Time (Biweekly)')
    plt.ylabel('# of Cases')       
    plt.savefig('DeltaToOmicron.png', bbox_inches='tight')
    plt.close('all')
    """
