import sys
import pandas as pd
import matplotlib.pyplot as plt

#2020.04.11 cey
#use filename provided by command- line

c19_df =  pd.read_csv(sys.argv[1], sep=',')
print(c19_df.columns)

uniqueStates = c19_df.state.unique()
for state in uniqueStates:
	state_df=c19_df[c19_df['state']==state]
	#print(state_df)
	state_df.plot(kind='scatter',x='date',y='cases',color='red')
	plt.gcf().autofmt_xdate()
	ax = plt.axes()
	ax.xaxis.set_major_locator(plt.MaxNLocator(3))
	
	print('Outputting '+state+' data')
	plt.savefig(state+'.png')
	#plt.show()

#vt_df  = c19_df[c19_df['state']=='Vermont']
#print(vt_df)

#for row in covid19reader:
#   print(', '.join(row))
