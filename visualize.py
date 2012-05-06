"""Visualise tools"""

import os.path
import math
import Image
import ImageDraw

from voting import get_results_for_party

WARD_POINTS = { # X, Y
	'Bulmershe and Whitegates': (226, 440),
	'Charvil': (329, 338),
	'Emmbrook': (428, 569),
	'Evendons': (406, 634),
	'Finchampstead North Ward': (451, 727),
	'Finchampstead South Ward': (371, 776),
	'Hawkedon': (272, 550),
	'Hillside': (215, 532),
	'Hurst': (434, 463),
	'Loddon': (320, 466),
	'Maiden Erlegh': (257, 496),
	'Norreys': (488, 570),
	'Remenham, Wargrave and Ruscombe': (410, 227),
	'Shinfield South': (130, 650),
	'Twyford': (377, 328),
	'Wescott': (482, 619),
	'Winnersh': (350, 533),
	'Wokingham Without': (520, 705),
}

MAX_BUBBLE_SIZE = 110

def vote_visualization_for_party(results, party, color=(33, 86, 175), 
	outline=(28, 72, 145)):
	"""Draw a map with votes displayed in bubbles proportional to 
	the total votes recieved in other areas"""
	
	# Get the results for each ward
	results_by_ward = get_results_for_party(results, party)
	
	# Find our largest value
	max_value = max(results_by_ward.values())
	max_value_sq = math.sqrt(max_value)
	
	ward_symbols = {}
	
	# Get the symbol size for each ward
	for ward, votes in results_by_ward.items():
		ward_symbols[ward] = MAX_BUBBLE_SIZE * (math.sqrt(votes) / max_value_sq)
	
	# Read in our base image
	wd = os.path.dirname(os.path.realpath(__file__))
	base_img = os.path.join(wd, 'media/wokingham-wards.png')
	
	img = Image.open(base_img)
	draw_img = ImageDraw.Draw(img)
	
	# Now draw each symbol on the map (and locate to coord point)
	for ward, symbol_size in ward_symbols.items():
		# Get the coord point
		coords = WARD_POINTS[ward]
		
		# BB is north-west/south-east
		# Remap it to the size of the ellipse as point is for the center of ellipse
		bounding_box = (
			coords[0] - (((coords[0] + symbol_size) - coords[0]) / 2), 
			coords[1] - (((coords[1] + symbol_size) - coords[1]) / 2), 
			(coords[0] + symbol_size) - (((coords[0] + symbol_size) - coords[0]) / 2),
			(coords[1] + symbol_size) - (((coords[1] + symbol_size) - coords[1]) / 2),
		)
		
		draw_img.ellipse(bounding_box, fill=color, outline=outline)
	
	# Save our image
	img.save(os.path.join(
		wd,
		'2012/vote-vis-party-%s.png' % party.lower().replace(' ', '-')
	))

if __name__ == '__main__':
	vote_visualization_for_party(
		'2012/local-election-results.json',
		'Conservative',
		color=(33, 86, 175),
		outline=(28, 72, 145)
	)
	
	vote_visualization_for_party(
		'2012/local-election-results.json',
		'Labour',
		color=(226, 54, 54),
		outline=(194, 46, 46)
	)
	
	vote_visualization_for_party(
		'2012/local-election-results.json',
		'Liberal Democrat',
		color=(242, 231, 47),
		outline=(228, 217, 44)
	)
	