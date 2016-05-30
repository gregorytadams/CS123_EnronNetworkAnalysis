import os, sys, csv
from shutil import copyfile

for f in os.listdir('output/'):
    with open(f) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            copyfile(row[0], 'consolidated_output/' + row[0].split('/')[-1])
            
            
