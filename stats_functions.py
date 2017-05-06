from __future__ import division, print_function

import numpy as np
import pandas as pd
import re

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
		nums = [(m.start(0), m.end(0)) for m in re.finditer(
			r"[+-]?\d+(?:\.\d+)?", self.text)]
		starts = [n[0] for n in nums]
		print([list(self.text)[n[0]:n[1]] for n in nums])
		return starts

if __name__ == '__main__':
	text_in = "The hon. Gentleman makes a reasonable point: 18 per cent. is " \
	          "still too high. However, that figure of 18 per cent. is significantly down on the percentage seven or eight years ago. The figures then were 23.7 per cent. in the Crown court, down to 13 per cent. in the latest figures, and 31 per cent. in the magistrates courts, down to 18 per cent., as I have just mentioned. We are absolutely committed to reducing those figures further, and good case management is of course part of that process."
	em = Extractor(text_in)
	em.extract_numbers_from_text()