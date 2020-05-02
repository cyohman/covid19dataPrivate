import sys
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import date
from lmfit.models import LognormalModel
import numpy as np
import scipy as sp
from scipy.optimize import curve_fit

#2020.04.30, cey, Need to figure out the right curve to fit here
def func(x, a, b, c ):
    #return a * np.exp(-b * x) + c
    return a / (1+ np.exp(-b*(x-c)))
    #return a + b*np.log(x)

#2020.04.11, cey
#use filename provided by command- line and values in those files are assumed to be separated by a comma

c19_df =  pd.read_csv(sys.argv[1], sep=',')
print(c19_df.columns)

path = os.getcwd()
print ("The current working directory is %s" % path)

#2020.04.30, cey, Add the hour, minute, and second to the folder in 24 hour time
savePath = path+"/"+date.today().strftime("%m-%d-%Y")+"/";
os.mkdir(savePath);
print ("The save directory is %s" % savePath)

#2020.04.30, cey, The list of unique states & territories
uniqueStates = c19_df.state.unique()

for state in uniqueStates:
	state_df=c19_df[c19_df['state']==state]
	
	numDays = len(state_df['date'])
	xData = np.linspace(1, numDays, numDays, dtype=int) 
	#print(xData)

	y= state_df['cases']

	#2020.04.30, cey, Need to figure out what popt and pcov are
	popt, pcov = curve_fit(func, xData, y)	

	plt.plot(xData, y, 'ko', label="Original Case Data")	
	plt.plot(xData, func(xData, *popt), 'r-', label="Fitted Curve")

	print('Outputting '+state+' data')
	plt.savefig(savePath+state+'.png')
	
	#2020.04.26, chance.yohman@gmail.com, Fix the 20 plots warning
	plt.close()

