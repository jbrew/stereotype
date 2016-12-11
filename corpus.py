from __future__ import division
from ngram import Ngram
import operator
import string
import re
import math

class Corpus(object):
	def __init__(self, name, text):
		self.name = name
		self.text = text
		self.wordcount = 0
		self.max_reach = 2
		self.tree = {}
		self.baseline_weight = .001
		self.ccae_weight = .00001
		self.baseline = self.get_baseline()
		self.eat_text(text)
		#self.eat_ccae_filtered('ngram_data/w2_.txt',set(self.tree.keys()))
		#self.eat_ccae_filtered('ngram_data/w3_.txt', set(self.tree.keys()))
		#self.eat_ccae_filtered('ngram_data/w4_.txt', set(self.tree.keys()))
		self.memory = {}


	"""
	gives each word a minimal score simply based on its frequency of occurrence in the text
	"""
	def get_baseline(self):
		baseline = {}
		for word in self.text.lower().replace('\xe2\x80\x99',"'").split():
			self.tallyscore(word, self.baseline_weight, baseline)
		return baseline
	
	"""
	takes a natural language source text
	"""
	def eat_text(self, source_text):
		source_text = source_text.lower().replace('\xe2\x80\x99',"'") 	# last call gets rid of slanted apostrophe
		sentences = source_text.strip('\n') \
                        .translate(string.maketrans('', ''), string.punctuation.replace('\'', '')) \
                        .lower() \
                        .split('.\n' or '. ' or '?' or '!')
		for s in sentences:
			self.eat_token_string(s.split())		
		return
	
	"""
	s is a string of tokens
	reach is the number of tokens to look back and forward
	max_ngram_size is the largest chunks stored
	"""

	def eat_token_string(self, s, max_reach=2, max_ngram_size=2):
		for ngram_size in range(1, max_ngram_size+1):
			for i in range(len(s)):
				start = i
				end = i + ngram_size
				if start >= 0 and end < len(s)+1:
					before, current, after = s[:start],s[start:end],s[end:]
					
					if len(current) == 1:
						self.wordcount += 1
					
					ngram = " ".join(current)
					
					if ngram in self.tree:
						self.tree[ngram].count += 1
					else:
						self.tree[ngram] = Ngram(ngram, 1, max_reach)
					
					for reach in range(1,max_reach + 1):
					
						# update dictionary to reflect all words occurring after this ngram
						try:
							word = after[reach-1]
							#print 'after "%s" is "%s" with reach %s' % (ngram, word, reach)
							self.tree[ngram].add_after(word, reach, 1)
						except IndexError:
							pass
						
						"""
						# update dictionary to reflect all words occurring before this ngram
						try:
							word = before[-1*(reach)]
							self.tree[ngram].add_before(word, reach, 1)
						except IndexError:
							pass
						"""
					
			
	"""
	given a list of words preceding the insertion point and a list of words following it,
	returns a list of top suggestions
	"""
	def suggest(self, preceding, following, max_suggestions = 50):	
	
		suggestions = dict(self.baseline)
		
		for reach in range(1, self.max_reach+1):
			if reach == 1:
				ngram_list = [preceding[i:] for i in range(len(preceding)-1)]
			else:
				ngram_list = [preceding[i:reach*-1+1] for i in range(len(preceding)-1)]
				
			for ngram in ngram_list:
				ngram_size = len(ngram)
				ngram = " ".join(ngram)
				if ngram in self.tree:
					for word, count in self.tree[ngram].after[reach-1].iteritems():
						frequency = self.conditional_frequency(ngram, reach, word)
						score = frequency * 1/math.pow(2,reach) * math.pow(2,ngram_size)
						#print ngram, '...', word, score
						self.tallyscore(word, frequency, suggestions)
				else:
					pass
					#print '%s not in follower tree!' % ngram
					
		suggestion_list = list(reversed(sorted(suggestions.items(), key=operator.itemgetter(1))))
		
		# hash this state so next time it's encountered, no calculation needed
		context = (''.join(preceding), ''.join(following))
		self.memory[context] = suggestion_list
			
		return suggestion_list[0:max_suggestions]


	# returns overall frequency of word w in the corpus
	def overall_frequency(self, w):
		if w in self.tree:
			return self.tree[w].count / self.wordcount
		else:
			return 0

	# given a context, looks forward r words from that ngram and returns the frequency of word w
	def conditional_frequency(self, preceding, r, w):
		entry = self.tree[preceding]
		if w in entry.after[r-1]:
			return entry.after[r-1][w] / entry.count
		else:
			return 0
	
	# given a context, looks forward n words from that ngram and returns the significance score of word w	
	def sigscore(self, preceding, r, w):
		try:
			return self.conditional_frequency(preceding, r, w) / self.overall_frequency(w)
		except ZeroDivisionError:
			return 0
		
		


	""""
	ALTERNATE ENTRY METHODS
	"""
		
	"""
	takes an ngram frequency file formatted like so:
	
	word1 word2 word3 ...	 COUNT
	
	with the words separated by spaces and the count offset by a tab
	"""
	def eat_ngram_data(self, path):
		source_text = file(path).readlines()
		for line in source_text:
			sequence, count = line.split('\t')
			self.enter_sequence(sequence, int(count), self.tree)
		
	"""
	takes an ngram frequency file from the Corpus of Contemporary American English, formatted like so:
	
	count	word1	word2	word3 ...
	"""
	def eat_ccae(self, path):
		database = file(path).readlines()
		for line in database:
			splitline = line.split()
			count = float(splitline[0])
			sequence = " ".join(splitline[1:])
			score = count * self.ccae_weight
			self.enter_sequence(sequence, float(score), self.tree)
	
	# only process data that is in the wordset
	def eat_ccae_filtered(self, path, whitelist):
		database = file(path).readlines()
		for line in database:
			splitline = line.split()
			count = float(splitline[0])
			sequence_set = set(splitline[1:])
			
			if sequence_set < whitelist:
				sequence = " ".join(splitline[1:])
				score = count * self.ccae_weight
				self.enter_sequence(sequence, float(score), self.tree)

	# enters this ngram in the tree
	def enter_sequence(self, ngram, count, tree):
		components = ngram.split(' ')
		head = " ".join(components[:-1])
		tail = components[-1]
		
		if head in tree:
			tree[head].count += count
		else:
			tree[head] = Ngram(ngram, count, 1, 0)
			
		self.wordcount += count * len(components)
		
		branch = tree[head].after[0]
		if tail in branch:
			branch[tail] += count
		else:
			branch[tail] = count
	
	def tallyscore(self, ngram, score, tree):
		if ngram in tree:
			tree[ngram] += score
		else:
			tree[ngram] = score
			
