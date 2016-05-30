import os
import csv

def combine_csvs():
	'''
	when run in a directory of csvs
	takes all of the lines and writes them to one csv file
	called masterfile.csv
	'''
	with open("masterfile.csv", 'w') as f:
		for subfile in next(os.walk('.'))[2]:
			with open(subfile, 'r') as f2:
				for line in f2:
					f.append(line)

if __name__ == '__main__':
	combine_csvs()
