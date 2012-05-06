import os.path
import json

def get_wards(json_results):
	"""Display all wards from results"""
	
	wd = os.path.dirname(os.path.realpath(__file__))
	json_file = os.path.join(wd, json_results)
	
	f = open(json_file)
	data = json.load(f)
	
	return [result['ward'] for result in data]
	
if __name__ == '__main__':
	wards = get_wards('2012/local-election-results.json')
	
	print wards