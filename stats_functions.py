from __future__ import division, print_function

import numpy as np
import pandas as pd
import re
import json
from nltk import tokenize

class Extractor(object):
	"""
	Class to extract stats info from text
	"""
	def __init__(self, text_in):
		self.text = text_in
		with open('word_numbers.json') as fp:
			self.word_list = json.load(fp)
		self.important = ['million', u"\xA3", 'per cent', 'thousand']

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
		#TODO instead of returning list of all, concatenate neighbouring indices
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

	def get_important(self):
		"""
		Function to check presence of important
		:return:
		"""
		for w in self.important:
			if w in self.text:
				return True

		return False

class Ranker(object):
	"""
	Class to extract and rank sentences in text based on presence of number
	"""
	def __init__(self, text_in):
		self.text = text_in

	def extract_sentences(self):
		"""
		Use NLTK to extract sent
		:return:
		"""
		sentences = tokenize.sent_tokenize(self.text)
		return sentences

	def get_sentence_ranking(self):
		"""
		Find all the sentences containing a number and return
		:return:
		"""
		sentences = self.extract_sentences()
		keep = []
		for s in sentences:
			ex= Extractor(s)
			vals = ex.extract_stats_from_text()

			if len(vals) > 0:
				imp = ex.get_important()
				keep.append([s, imp, vals])
		return sorted(keep, key=lambda x:x[1], reverse=True)

if __name__ == '__main__':
	text_in = "The hon. Gentleman makes a reasonable point: 18 per cent. is " \
	          "still too high. However, that figure of 18 per cent. is significantly down on the percentage seven or eight years ago. The figures then were 23.7 per cent. in the Crown court, down to 13 per cent. in the latest figures, and 31 per cent. in the magistrates courts, down to 18 per cent., as I have just mentioned. We are absolutely committed to reducing those figures further, and good case management is of course part of that process."
	em = Extractor(text_in)
	indices = em.extract_stats_from_text()
	print([''.join(list(em.text)[np.max([0, n[0] - 5]):
		np.min([len(em.text), n[1] + 5])]) for n
		       in indices])

	ra = Ranker(text_in)
	sentences = ra.get_sentence_ranking()
	print(sentences)