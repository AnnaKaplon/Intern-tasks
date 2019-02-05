import sys
import pandas
import pycountry
from chardet.universaldetector import UniversalDetector

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

if __name__ == '__main__':
	args = sys.argv
	inputFile = args[1]