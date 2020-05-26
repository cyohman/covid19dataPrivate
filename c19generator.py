import sys
import pandas as pd
import matplotlib
matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt
import os
from datetime import date
from datetime import datetime
import numpy as np
from scipy.optimize import curve_fit

#2020.04.30, cey, Need to figure out the right curve to fit here
def sigmoid(x, L ,x0, k, b):
#    print("L: ", L)
#    print("x0: ", x0)
#    print("k: ", k)
#    print("b: ", b)
    y = L / (1 + np.exp(-k*(x-x0)))+b
    return (y)


#2020.04.11, cey
#use filename provided by command- line and values in those files are assumed to be separated by a comma

workingPath = os.getcwd()
print ("The current working directory is %s" % workingPath)

#2020.04.30, cey, Add the hour, minute, and second to the folder in 24 hour time
rootSavePath = workingPath+"/"+datetime.now().strftime("%m-%d-%Y_%H%M%S")+"/";
os.mkdir(rootSavePath);

print ("The root save path is %s" % rootSavePath)

print("Processing US  data")
us_df = pd.read_csv('us.csv', sep=',')

numDays = len(us_df['date'])
xData = np.linspace(1, numDays, numDays, dtype=int) 

y= us_df['cases']

p0 = [max(y), np.median(xData),1,min(y)] # this is an mandatory initial guess

try:
	popt, pcov = curve_fit(sigmoid, xData, y, p0,  maxfev=99999)
	print (popt, pcov)
           
	if np.isfinite(pcov).all():
	   print ('valid')
	else:
	   print ('invalid')
              
	yData = sigmoid(xData, *popt)
	plt.plot(xData, yData, 'r-', label="Fitted Curve")
except TypeError as err:
   print(err)
except RuntimeError as err:
   print(err)
	
plt.yscale("log")

plt.plot(xData, y, 'ko', label="Original Case Data")	

plt.savefig(rootSavePath+'US.png')
	
#2020.04.26, chance.yohman@gmail.com, Fix the 20 plots warning
plt.close()

states_df =  pd.read_csv('us-states.csv', sep=',')

counties_df = pd.read_csv('us-counties.csv', sep=',')

#2020.04.30, cey, The list of unique states & territories
uniqueStates = states_df.state.unique()

for state in uniqueStates:
	
	stateRootSavePath = rootSavePath + state + "/"
	os.mkdir(stateRootSavePath);
	print ("The state root save path is %s" % stateRootSavePath)
	
	print("Processing "+state+" data")
	state_df=states_df[states_df['state']==state]
	
	numDays = len(state_df['date'])
	xData = np.linspace(1, numDays, numDays, dtype=int) 

	y= state_df['cases']

	p0 = [max(y), np.median(xData),1,min(y)] # this is an mandatory initial guess

	try:
	   popt, pcov = curve_fit(sigmoid, xData, y, p0,  maxfev=99999)
	   print (popt, pcov)
           
	   if np.isfinite(pcov).all():
	         print ('valid')
	   else:
    	         print ('invalid')
              
	   yData = sigmoid(xData, *popt)
	   plt.plot(xData, yData, 'r-', label="Fitted Curve")
	except TypeError as err:
	   print(err)
	except RuntimeError as err:
	   print(err)
	
	plt.yscale("log")

	plt.plot(xData, y, 'ko', label="Original Case Data")	

	plt.savefig(stateRootSavePath+state+'.png')
	
	#2020.04.26, chance.yohman@gmail.com, Fix the 20 plots warning
	plt.close()

	state_counties_df=counties_df[counties_df['state']==state]
	uniqueCounties = state_counties_df.county.unique()

	for county in uniqueCounties:

		if county != "Unknown":
        	   print("Processing "+state+" - "+county+" county data")
        	   county_df=state_counties_df[state_counties_df['county']==county]

        	   numDays = len(county_df['date'])
        	   xData = np.linspace(1, numDays, numDays, dtype=int)

        	   y= county_df['cases']

        	   p0 = [max(y), np.median(xData),1,min(y)] # this is an mandatory initial guess

        	   #2020.04.30, cey, Need to figure out what popt and pcov are
        	   try:
	              popt, pcov = curve_fit(sigmoid, xData, y, p0,  maxfev=99999)
	              print (popt, pcov)
	           
	              if np.isfinite(pcov).all():
    	                 print ('valid')
	              else:
    	                 print ('invalid')
	              
	              yData = sigmoid(xData, *popt)
        	      plt.plot(xData, yData, 'r-', label="Fitted Curve")
        	   except TypeError as err:
	      	      print(err)
	           except RuntimeError as err:
	              print(err)

        	   plt.yscale("log")

        	   plt.plot(xData, y, 'ko', label="Original Case Data")

        	   plt.savefig(stateRootSavePath+state+'_'+county+'_county.png')

        	   #2020.04.26, chance.yohman@gmail.com, Fix the 20 plots warning
        	   plt.close()
