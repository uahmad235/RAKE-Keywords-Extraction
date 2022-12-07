import re
import os

class Preprocess(object):
	
	def __init__(self, text, stop_path):
		""" initialize local variables """
		self.text = text
		self.stop_path = stop_path

	@staticmethod
	def read_stopwords(path):
		""" returns the stop words read from file """
		with open(path) as file:
			next(file)					# ignore first line as 
			# file.readline()   		# it is a comment in a file

			stoplist = [line.strip()   # trim line if any escape sequences like '\n'
					for line in file]   # read file line by line
										#if not line.startswith('#')
		return stoplist

	@staticmethod
	def compile_pattern_for_phrases(stoplist):
		""" returns compiled pattern """
		string = '[,.:?]|'
		for stop in stoplist:
			string += r'\b' + stop + r'(?![\w-])' +r'|'
		pattern = re.compile(string,re.IGNORECASE)

		return pattern

	def text_to_phrases(self):
		""" returns phrases into stopwords-separated tokens """
		stoplist = Preprocess.read_stopwords(self.stop_path)
		pattern = Preprocess.compile_pattern_for_phrases(stoplist)

		phrases = [phrase.lower().strip()
				  for phrase in re.split(pattern, self.text) 
				  if phrase.strip()!='' ]

		return set(phrases), phrases