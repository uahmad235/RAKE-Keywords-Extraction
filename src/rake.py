from collections import defaultdict
from collections import Counter
import re 
import operator

class RAKE(object):
	"""" calculates and returns the keywords for 
		 the text passed as an arg """

	def __init__(self, text, phrases):
		""" initialize instance variables """
		self.text = text
		self.phrases = phrases
		self.cnt_degree = Counter()  # counts degree of tokens
		self.cnt_freq = Counter()    # counts freq of tokens
		self.cnt_Weight = Counter()	 # counts weights of tokens
		self.cnt_phrases_weight = Counter() # keeps track of phrase weights
		# nested dictionary having 0 as default value for inner dictionary
		self.com = defaultdict(lambda : defaultdict(int)) 

	def start(self):
		"""" orchestrates the whole process in this file"""
		self.create_cooccurance_matrix()
		self.split_phrases_into_tokens()
		self.update_cooccurance_matrix()
		self.calculate_frequency_and_degree()
		self.calculate_weights()
		self.calculate_final_scores()

		return self.cnt_phrases_weight.most_common(int(len(self.splitted)*0.30))

	@staticmethod
	def split_phrase(phrase): 
		""" split the phrase into space separated tokens """
		return re.split(r'[ ]',phrase)

	def create_cooccurance_matrix(self):
		""" creates cooccurance matrix for terms occuring in same phrase"""

		# calculating word co-occurance of words in same phrase
		for phrase in self.phrases:
			phrase_tokens = (RAKE.split_phrase(phrase)) # split phrase into space seperated words
			for i in range(len(phrase_tokens)-1):
				for j in range(i+1, len(phrase_tokens)):
					w1, w2 = phrase_tokens[i], phrase_tokens[j]
					self.com[w1][w2] += 1

	def split_phrases_into_tokens(self):
		""" splits phrases into individual tokens i.e.,
			convert phrases into list of tokens for matching occurance
			of those tokens in whole text corpus """

		self.splitted = [token.strip() 
							for phrase in self.phrases 
							for token in phrase.split(' ') 
							if token.strip()!=0]
	
	def update_cooccurance_matrix(self):
		""" updates cooccurance matrix by converting text """
		for x in self.splitted:
			if x != ' ' and x!= '–' and x.strip()!='?':
				# if any occurance matches, increment count
				if (re.search(re.compile(r'\b'+x+r'\b'), self.text.lower())): 
					self.com[x][x] += 1
				

	def calculate_frequency_and_degree(self):
		""" calculates frequency and degree of """

		for k in list(self.com):  # key of outer dict i.e., first word of phrase 
			for x in self.com[k]:    # all kvp's against first element
				if k == x:      # if same word 
					self.cnt_freq[k] = self.com[k][x]

				self.cnt_degree[k] += (self.com[k][x])
				if self.com[k][x] != self.com[x][k]:
					self.cnt_degree[k] += self.com[x][k]

	def calculate_weights(self):
		""" calculate weights of all candidate words """

		for word in self.cnt_degree:
				if self.cnt_freq[word] == 0: # avoid "/ by zero" Exception
					self.cnt_freq[word] = 0.1
				self.cnt_Weight[word] = self.cnt_degree[word] / self.cnt_freq[word]

	def calculate_final_scores(self):
		""" count final score for each phrase """
		for phrase in self.phrases:
			words = RAKE.split_phrase(phrase)
			for word in words:
				# add the individual weight of all words in phrase
				self.cnt_phrases_weight[phrase] += self.cnt_Weight[word]

