import csv
import sys

#2020.04.11 cey
#TODO: use filename provided by command- line
#FINISHED 2020.04.11 @ 1458 EDT

with open(sys.argv[1], newline='') as csvfile:
     covid19reader = csv.reader(csvfile, delimiter=',')
     for row in covid19reader:
         print(', '.join(row))
