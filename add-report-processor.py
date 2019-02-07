from chardet.universaldetector import UniversalDetector
import pandas as pd
import pycountry
from datetime import datetime
import math
import sys

def find_encoding(fileName):
	"""
	Returns detected encoding of given file.
	
	Arguments:
	fileName - name of file to find encoding
	"""
	
	detector = UniversalDetector()
	with open(fileName, 'rb') as file:
		for line in file.readlines():
			detector.feed(line)
			if detector.done: break
	detector.close()
	return detector.result['encoding']

def read_input_report(fileName, enc):
	df = pd.read_csv(fileName, encoding=enc, names=['date', 'state', 'impression', 'CTR'])
	
	for index, row in df.iterrows():
		date, state, impression = datetime.strptime(row['date'], '%m/%d/%Y'),\
		row['state'], int(row['impression'])
		try:
			CTR = float(row['CTR'])
		except ValueError:
			CTR = float(row['CTR'][:-1])
		try:
			countryCode = pycountry.subdivisions.lookup(state).country.alpha_3
		except LookupError:
			countryCode = 'XXX'
		add_to_memory(date, countryCode, impression, CTR)
	
def add_to_memory(date, countryCode, impression, CTR):
	if date not in memory:
		memory[date] = {}
	if countryCode not in memory[date]:
		memory[date][countryCode] = {}
		memory[date][countryCode]['impressions'] = impression
		memory[date][countryCode]['clicks'] = round(impression*CTR/100)
	else:
		memory[date][countryCode]['impressions'] += impression
		memory[date][countryCode]['clicks'] += round(impression*CTR/100)
		
def save_new_report():
	with open('outputReport.csv', 'w') as file:
		file.write
		for date in sorted(memory):
			for country in sorted(memory[date]):
				pass
				
			


if __name__ == '__main__':
	args = sys.argv
	global memory 
	inputFile = args[1]
	
	memory = {}
	try:
		read_input_report(inputFile, 'utf-8')
	except UnicodeDecodeError:
		read_input_report(inputFile, 'utf-16')
	save_new_report()
	