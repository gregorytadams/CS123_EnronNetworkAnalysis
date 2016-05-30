import os, sys, csv
from shutil import copyfile

for f in os.listdir('output/'):
    '''
    takes the files listed in a csv
    and moves them into a new directory
    called consolidated_output
    '''
    print(f)
    with open('output/' + f) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            try:
                copyfile(row[0], 'consolidated_output/' + row[0].split('/')[-1])
            except Exception:
                print(f)
