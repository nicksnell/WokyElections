# Generating results/charts from election results
# Nick Snell <n@nicksnell.com>

import os.path
import json

from ptable import Table
from pygooglechart import Chart, PieChart2D

def _get_results(json_results):
	wd = os.path.dirname(os.path.realpath(__file__))
	json_file = os.path.join(wd, json_results)

	f = open(json_file)
	data = json.load(f)

	return data

def get_results_for_party(json_results, party):
	"""Get the results for a party by ward"""

	data = _get_results(json_results)

	wards = {}

	for result in data:
		for candidate in result['candidates']:
			if candidate['party'] == party:
				wards[result['ward']] = candidate['votes']
				break

	return wards

def get_total_results(json_results):
	"""Generate totals for each party"""

	data = _get_results(json_results)

	total_results = {}

	for result in data:
		for candidate in result['candidates']:
			if not candidate['party'] in total_results:
				total_results[candidate['party']] = 0

			total_results[candidate['party']] += candidate['votes']

	return total_results

def get_total_votes(results):
	"""Get the total amount of votes placed"""
	return sum(results.values())

def generate_results_table(results):
	"""Generate a results table"""

	total_votes = get_total_votes(results)

	results_data = []
	ordered_results = sorted(results.iteritems(), key=lambda x: x[1])
	ordered_results.reverse()

	for party, votes in ordered_results:
		results_data.append([
			party,
			votes,
			'%.2f %%' % ((float(votes) / float(total_votes)) * 100.0),
		])

	t = Table(results_data)
	t.headers = ('Party', 'Votes', 'Percentage')
	t.col_separator = ' | '
	t.header_separator = '-'
	t.print_table()

class NewPieChart2D(PieChart2D):
	"""Subclass the Pie chart class as standard doesnt
	allow for marigns?!?"""

	def __init__(self, *args, **kwargs):
		self.margin = None
		super(NewPieChart2D, self).__init__(*args, **kwargs)

	def set_margin(self, margin):
		# Margin L/R/T/B
		self.margin = margin

	def get_url_bits(self, data_class=None):
		url_bits = Chart.get_url_bits(self, data_class=data_class)

		if self.pie_labels:
			url_bits.append('chl=%s' % '%7c'.join(self.pie_labels))

		if self.margin:
			url_bits.append('chma=%s' % self.margin)

		return url_bits

def generate_chart(results, save_to):
	"""Generate a chart based on the results - results being
	a dictionary of party/votes"""

	# Order our results (low-high)
	ordered_results = sorted(results.iteritems(), key=lambda x: x[1])

	chart = NewPieChart2D(500, 500, colours=('383c3d', '919da2'))
	chart.add_data([r[1] for r in ordered_results])
	chart.set_pie_labels([r[0] for r in ordered_results])
	chart.set_margin('95,98,5,5')

	wd = os.path.dirname(os.path.realpath(__file__))
	chart_file = os.path.join(wd, save_to)

	chart.download(chart_file)

if __name__ == '__main__':
	results = get_total_results('2012/local-election-results.json')
	generate_results_table(results)
	generate_chart(results, '2012/local-election-results.png')
