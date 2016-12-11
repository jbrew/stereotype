import unittest
import test_data
from corpus import Corpus


class CorpusTests(unittest.TestCase):

	def first_suggestion(self, corpus, preceding):
		return corpus.suggest(preceding, '')[0][0]
		
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
		
		self.assertEqual(
			c.conditional_frequency('it',1,'was')
			,1)
		self.assertEqual(
			c.conditional_frequency('it was',1,'the')
			,1)
		self.assertEqual(
			c.conditional_frequency('it',1,'zeus')
			,0)
		self.assertEqual(
			c.conditional_frequency('it',2,'the')
			,1)
		self.assertEqual(
			c.conditional_frequency('was the',1,'best')
			,.5)
		self.assertEqual(
			c.conditional_frequency('was the',2,'of')
			,1)
		self.assertGreater(c.overall_frequency('it')
			,c.overall_frequency('worst'))
		self.assertEqual(c.overall_frequency('aphrodite'),0)
		
		self.assertGreater(c.sigscore('best of',1,'times'),c.overall_frequency('times'))
		
		self.first_suggestion(c, ['it', 'was'])
		
		self.assertEqual(self.first_suggestion(c, ['it', 'was']),'the')
		self.assertEqual(self.first_suggestion(c, ['it', 'zeus']),'the')
		self.assertEqual(self.first_suggestion(c, ['the', 'zeus']),'of')

		
	
	def _test_sigscore(self):
		c = Corpus('jack', 'jack the thing is the thing i want to tell you a thing jack this thing the main thing is the thing is that jack the ripper is here, that is what the thing is jack')
		self.assertGreater(c.sigscore('jack the',1,'ripper'), c.sigscore('jack the',1,'thing'))
		self.assertEqual(c.sigscore('jack the',1,'zeus'),0)
		
		

    
if __name__ == '__main__':
  unittest.main()