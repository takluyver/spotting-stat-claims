from __future__ import division, print_function

import numpy as np
import pandas as pd
import re
import json

class Extractor(object):
	"""
	Class to extract stats info from text
	"""
	def __init__(self, text_in):
		self.text = text_in
		with open('word_numbers.json') as fp:
			self.word_list = json.load(fp)

	def extract_stats_from_text(self):
		"""
		Function to extract stats-related info from text
		:return:
		"""
		nums = self._extract_numbers()
		nums.extend(self._extract_numberwords())
		nums = sorted(nums, key =lambda x:x[0])

		return nums

	def _extract_numberwords(self):
		"""
		Function to extract numerical related words
		:return:
		"""
		all_indices = []
		for k,v in self.word_list.items():
			for w in v:
				if w in self.text:
					word_find = re.finditer('\\b(%s)\\b' % w, self.text)
					word_inds = [(m.start(0), m.end(0)) for m in word_find]
					all_indices.extend(word_inds)

		return all_indices


	def _extract_numbers(self):
		"""
		Use regex to extract all digits in piece of text
		:return: initial index
		"""
		nums = [(m.start(0), m.end(0)) for m in re.finditer(
			r"[+-]?\d+(?:\.\d+)?", self.text)]

		return nums

if __name__ == '__main__':
	text_in = "The hon. Gentleman makes a reasonable point: 18 per cent. is " \
	          "still too high. However, that figure of 18 per cent. is significantly down on the percentage seven or eight years ago. The figures then were 23.7 per cent. in the Crown court, down to 13 per cent. in the latest figures, and 31 per cent. in the magistrates courts, down to 18 per cent., as I have just mentioned. We are absolutely committed to reducing those figures further, and good case management is of course part of that process."
	em = Extractor(text_in)
	indices = em.extract_stats_from_text()
	print([''.join(list(em.text)[np.max([0, n[0] - 5]):
		np.min([len(em.text), n[1] + 5])]) for n
		       in indices])