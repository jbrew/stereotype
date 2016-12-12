import unittest
import test_data
from corpus import Corpus
from analyzer import Analyzer

class AnalyzerTests(unittest.TestCase):
	
	def first_suggestion(self, analyzer, preceding):
		return analyzer.suggest(preceding, '')[0][0]

	def test_analyzer(self):
		c = Corpus('test', 'it was the best of times it was the worst of times')
		a = Analyzer(c)
		
		self.assertEqual(
			a.conditional_frequency('it',1,'was')
			,1)
		self.assertEqual(
			a.conditional_frequency('it was',1,'the')
			,1)
		self.assertEqual(
			a.conditional_frequency('it',1,'zeus')
			,0)
		self.assertEqual(
			a.conditional_frequency('it',2,'the')
			,1)
		self.assertEqual(
			a.conditional_frequency('was the',1,'best')
			,.5)
		self.assertEqual(
			a.conditional_frequency('was the',2,'of')
			,1)
		self.assertGreater(a.overall_frequency('it')
			,a.overall_frequency('worst'))
		self.assertEqual(a.overall_frequency('aphrodite'),0)
		
		self.assertGreater(a.sigscore('best of',1,'times'),a.overall_frequency('times'))
		
		self.first_suggestion(a, ['it', 'was'])
		self.assertEqual(self.first_suggestion(a, ['it', 'was']),'the')
		self.assertEqual(self.first_suggestion(a, ['it', 'zeus']),'the')
		self.assertEqual(self.first_suggestion(a, ['the', 'zeus']),'of')

    
if __name__ == '__main__':
  unittest.main()