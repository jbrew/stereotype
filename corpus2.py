from ngram2 import Ngram2
import operator
import string
import re

class Corpus2(object):
	def __init__(self, name, text):
		self.name = name
		self.min_count = 1
		self.wordcount = 0
		self.tree = {}
		self.eat_text(text)
		self.eat_ccae_filtered('ngram_data/w2_.txt', set(self.tree.keys()))
		#self.calculate_frequencies(self.tree)
		self.memory = {}
			
	
	"""
	takes a natural language source text
	"""
	def eat_text(self, source_text):
		source_text = source_text.lower()
		sentences = source_text.strip('\n') \
                        .translate(string.maketrans('', ''), string.punctuation.replace('\'', '')) \
                        .lower() \
                        .split('.\n' or '. ' or '?' or '!')
		for s in sentences:
			self.eat_token_string(s.split())		
		return
	
	# s is a string of tokens
	# reach is the number of tokens to look back and forward
	# max_ngram_size is the largest chunks stored
	def eat_token_string(self, s, max_back_reach=2, max_front_reach=0, max_ngram_size=2):
		for i in range(len(s)):
			before, current_word, after = s[:i],s[i],s[i+1:]
			#print '\n', before, current_word
			
			print current_word
			
			for ngram_size in range(1, max_ngram_size+1):
				for reach in range(1, max_back_reach+1):
					start = i+1 - reach - ngram_size
					end = i+1 - reach
					if start >= 0:
						print '\nreach', reach
						print 'ngram size', ngram_size
						print 'piece',s[start:end]
						print 'current word',current_word
						print 'start', start
						ngram = " ".join(s[start:end])
						if ngram not in self.tree:
							self.tree[ngram] = Ngram2(ngram, 1, max_back_reach, max_back_reach)
						
						self.tree[ngram].add(current_word, reach, 1)
			
	
	# enters this ngram in the tree
	def enter_sequence(self, ngram, count, tree):
		components = ngram.split(' ')
		head = " ".join(components[:-1])
		tail = components[-1]
		
		if head in tree:
			tree[head].count += count
		else:
			tree[head] = Ngram2(ngram, count, 1, 0)
			
		self.wordcount += count * len(components)
		
		branch = tree[head].after[0]
		if tail in branch:
			branch[tail] += count
		else:
			branch[tail] = count
	
	
	def tallyscore(self, ngram, count, tree):
		if ngram in tree:
			tree[ngram] += count
		else:
			tree[ngram] = count
	
			
	"""
	given a list of words preceding the insertion point and a list of words following it,
	returns a list of top suggestions
	"""
	def suggest(self, preceding, following):
		print 'preceding', preceding
		context = (''.join(preceding), ''.join(following))
		
		suggestions = {}
		
		# all subsets that end with the last one
		ngram_list = [preceding[i:] for i in range(len(preceding))]
		for ngram in ngram_list:
			ngram = " ".join(ngram)
			if ngram in self.tree:
				print ngram, '...is in tree'
				for word, count in self.tree[ngram].after[0].iteritems():
					print word, count
					self.tallyscore(word, count, suggestions)
			else:
				print '%s not in tree!' % ngram
		
		# all subsets that end with the second-last one
		ngram_list = [preceding[i:-1] for i in range(len(preceding)-1)]
		print 'ngram list for %s is %s' % (preceding, ngram_list)
		for ngram in ngram_list:
			ngram = " ".join(ngram)
			if ngram in self.tree:
				print ngram, '...is in tree'
				for word, count in self.tree[ngram].after[1].iteritems():
					print word, count
					self.tallyscore(word, count/5, suggestions)
			else:
				print '%s not in tree!' % ngram
		
		suggestion_list = list(reversed(sorted(suggestions.items(), key=operator.itemgetter(1))))
		
		print suggestion_list
		
		# hash entry
		self.memory[context] = suggestion_list
			
		return suggestion_list
	
	
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
			
	
	def calculate_frequencies(self, tree):
		for _, ngram in tree.iteritems():
			ngram.frequency = ngram.count / self.wordcount
	
		
	"""
	takes an ngram frequency file formatted like so:
	
	count	word1	word2	word3 ...
	"""
	def eat_ccae_data(self, path):
		print path
		database = file(path).readlines()
		for line in database:
			splitline = line.split()
			count = splitline[0]
			print 'count',count
			sequence = " ".join(splitline[1:])
			self.enter_sequence(sequence, int(count), self.tree)
	
	# only eat data that is in the wordset
	def eat_ccae_filtered(self, path, whitelist):
		database = file(path).readlines()
		for line in database:
			splitline = line.split()
			count = splitline[0]
			sequence_set = set(splitline[1:])
			if sequence_set < whitelist:
				sequence = " ".join(splitline[1:])
				#TODO: choose appropriate function for weighting this dictionary
				self.enter_sequence(sequence, int(count)/10000000, self.tree)
