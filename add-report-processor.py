import pandas as pd
import pycountry
from datetime import datetime
import csv
import sys
import re

def read_input_report(fileName, enc):
	df = pd.read_csv(fileName, encoding=enc, names=['date', 'state', 'impression', 'CTR'])
	
	for index, row in df.iterrows():
		try:
			date, state, impression = datetime.strptime(row['date'], '%m/%d/%Y'),\
			row['state'], int(row['impression'])
		except Exception:
			print('Broken data in row {}. This data has been ignored'.format(index))
			continue
		try:
			CTR = float(row['CTR'])
		except Exception:
			if re.match('\d+(?:\.\d+)?%$', row['CTR']):
				CTR = float(row['CTR'][:-1])
			else:
				print('Broken data in row {}. This data has been ignored'.format(index))
				continue
				
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
	try:
		with open('outputReport.csv', 'w') as file:
			csvWriter = csv.writer(file, dialect='unix')

			csvWriter.writerow(['date', 'countryCode', 'impressions', 'clicks'])
			for date in sorted(memory):
				for country in sorted(memory[date]):
					impressions = memory[date][country]['impressions']
					clicks = memory[date][country]['clicks']
					csvWriter.writerow([date.strftime('%Y-%m-%d'), country, impressions, clicks])
	except IOException:
		print('Refusal to create a file. Report can not be generated.')
		exit()
				

if __name__ == '__main__':
	args = sys.argv
	global memory
	
	if len(args) < 2:
		print('No input file given. Report can not be generated.', file=sys.stderr)
		exit()
	if not inputFile.lower().endswith('.csv'):
		raise ValueError('Given file is not csv. Report can not be generated.')
	
	memory = {}
	try:
		read_input_report(inputFile, 'utf-8')
	except UnicodeDecodeError:
		try:
			read_input_report(inputFile, 'utf-16')
		except UnicodeDecodeError:
			print('Unexpected encoding of ' + inputFile + " Report can not be generated.")
			exit()
		except Exception as ex:
			print(ex)
			print('Unexpected error occurred.')
	
	save_new_report()
	