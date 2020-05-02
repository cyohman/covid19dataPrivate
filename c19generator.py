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
#def func(x, a, b, c ):
#    #return a * np.exp(-b * x) + c
#    #return a / (1+ np.exp(-b*(x-c)))
#    return 1 / (1+ np.exp(-x))
#    #return a + b*np.log(x)
def sigmoid(x, L ,x0, k, b):
    y = L / (1 + np.exp(-k*(x-x0)))+b
    return (y)


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
	print("Processing "+state+" data")
	state_df=c19_df[c19_df['state']==state]
	
	numDays = len(state_df['date'])
	xData = np.linspace(1, numDays, numDays, dtype=int) 
	#print(xData)

	y= state_df['cases']

	p0 = [max(y), np.median(xData),1,min(y)] # this is an mandatory initial guess
	print(p0)

	#2020.04.30, cey, Need to figure out what popt and pcov are
	#popt, pcov = curve_fit(func, xData, y)	
	popt, pcov = curve_fit(sigmoid, xData, y, p0,  maxfev=9999)
	print(popt)
	print(pcov)
	yData = sigmoid(xData, *popt)

	plt.plot(xData, y, 'ko', label="Original Case Data")	
	plt.plot(xData, yData, 'r-', label="Fitted Curve")

	print('Outputting '+state+' data')
	plt.savefig(savePath+state+'.png')
	
	#2020.04.26, chance.yohman@gmail.com, Fix the 20 plots warning
	plt.close()

