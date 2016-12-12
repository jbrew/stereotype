import unittest
import test_data
from analyzer import Analyzer
from corpus import Corpus


class CorpusTests(unittest.TestCase):
		
	def _test_ccae(self):
		empty_corpus = Corpus('JUST CCAE','')
		print empty_corpus.suggest(['an'],[])
	
	def test_corpus(self):
		c = Corpus('test','it was the best of times it was the worst of times')
		tree = c.tree
		
		self.assertEqual(tree['it'].count, 2)
		self.assertEqual(tree['was'].count, 2)
		self.assertEqual(tree['it was'].count, 2)
		self.assertEqual(tree['times it'].count, 1)

		self.assertEqual(tree['it'].after[0]['was'],2)
		self.assertEqual(tree['it'].after[1]['the'],2)
		self.assertEqual(tree['it was'].after[0]['the'],2)
		self.assertTrue('the' not in tree['it'].after[0])
		self.assertTrue('times' not in tree['it'].after[1])
		self.assertTrue('the' not in tree['the'].after[1])
		
		
		
		

		
	
	def _test_sigscore(self):
		c = Corpus('jack', 'jack the thing is the thing i want to tell you a thing jack this thing the main thing is the thing is that jack the ripper is here, that is what the thing is jack')
		self.assertGreater(c.sigscore('jack the',1,'ripper'), c.sigscore('jack the',1,'thing'))
		self.assertEqual(c.sigscore('jack the',1,'zeus'),0)
		
		

    
if __name__ == '__main__':
  unittest.main()