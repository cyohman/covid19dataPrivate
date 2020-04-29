import sys
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import date
from lmfit.models import LognormalModel
import numpy as np

#2020.04.11 cey
#use filename provided by command- line

c19_df =  pd.read_csv(sys.argv[1], sep=',')
print(c19_df.columns)

path = os.getcwd()
print ("The current working directory is %s" % path)
savePath = path+"/"+date.today().strftime("%m-%d-%Y")+"/";
os.mkdir(savePath);
print ("The save directory is %s" % savePath)

uniqueStates = c19_df.state.unique()
for state in uniqueStates:
	state_df=c19_df[c19_df['state']==state]
	#print(state_df)
	state_df.plot(kind='scatter',x='date',y='cases',color='red')
	plt.gcf().autofmt_xdate()
	ax = plt.axes()
	ax.xaxis.set_major_locator(plt.MaxNLocator(20))

        #data = covid_data[covid_data["Location"] == "Italy"]["Value"].values[::-1]
	#agegroups = agegroup_lookup["Italy"]
	#beds_per_100k = beds_lookup["Italy"]

	#outbreak_shift = 30
	# parameters to fit; form: {parameter: (initial guess, minimum value, max value)}
	#params_init_min_max = {"R_0_start": (3.0, 2.0, 5.0), "k": (2.5, 0.01, 5.0), 
        #               "x0": (90, 0, 120), "R_0_end": (0.9, 0.3, 3.5),
        #               "prob_I_to_C": (0.05, 0.01, 0.1), "prob_C_to_D": (0.5, 0.05, 0.8),
        #               "s": (0.003, 0.001, 0.01)}

	days = len(state_df['date'])
	print(days)    
	x_data = np.linspace(1, days, days, dtype=int)  # x_data i
	print(x_data)

	model = LognormalModel()
	params = model.guess(state_df['cases'], x=x_data)
	result = model.fit(state_df['cases'], params, x=x_data)   
	result.plot_fit()

	print('Outputting '+state+' data')
	plt.savefig(savePath+state+'.png')
	#2020.04.26, chance.yohman@gmail.com, Fix the 20 plots warning
	plt.close()

