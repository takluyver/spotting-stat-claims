from __future__ import division, print_function

import numpy as np
import pandas as pd

class Extractor(object):
	"""
	Class to extract stats info from text
	"""
	def __init__(self, text_in):
		self.text = text_in

	def extract_stats_from_text(self):
		"""
		Function to extract num
		:return:
		"""
		pass

	def extract_numbers_from_text(self):
		"""

		:return:
		"""
		pass

if __name__ == '__main__':
	text_in = "The hon. Gentleman makes a reasonable point: 18 per cent. is " \
	          "still too high. However, that figure of 18 per cent. is significantly down on the percentage seven or eight years ago. The figures then were 23.7 per cent. in the Crown court, down to 13 per cent. in the latest figures, and 31 per cent. in the magistrates courts, down to 18 per cent., as I have just mentioned. We are absolutely committed to reducing those figures further, and good case management is of course part of that process."
	em = Extractor(text_in)