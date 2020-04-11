import sys
import pandas as pd

#2020.04.11 cey
#use filename provided by command- line

c19_df =  pd.read_csv(sys.argv[1], sep=',')
print(c19_df.columns)

vt_df  = c19_df[c19_df['state']=='Vermont']
print(vt_df)

#for row in covid19reader:
#   print(', '.join(row))
