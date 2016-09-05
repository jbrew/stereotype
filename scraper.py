from bs4 import BeautifulSoup
import urllib2
import re
import string

"""
rotten tomatoes scraper
"""

class MetacriticScraper(object):

	def __init__(self, start_url = 'not yet set'):
		self.start_url = start_url
		self.jury = 'critics'
		self.verdict = 'negative'
		self.jury_dict = {'critics': '/critic-reviews', 'users': '/user-reviews'}
		self.verdict_dict = {'positive': '?dist=positive', 'negative': '?dist=negative', 'medium': '?dist=neutral'}
	
	# test this
	def scrape_review_set(self, base_url, num_pages):
		scraped = ''
		for i in range(num_pages):
			url = '%s&page=%s' % (base_url, i)
			print url
			scraped += self.get_text_from_reviews_page(url)
		return scraped
	
	# test this
	def get_text_from_reviews_page(self, url):
			page = self.demand_page(url)
			soup = BeautifulSoup(page, "html.parser")
			if not re.search('critic-reviews', url) == None:
				reviews_list = soup.find(class_="reviews critic_reviews")
			elif not re.search('user-reviews', url) == None:
				reviews_list = soup.find(class_="reviews user_reviews")
			else:
				print "ERROR"
			scraped = ''
			if reviews_list:
				reviews = reviews_list.findAll(class_="review_body")
				for review in reviews:
					expanded = review.find(class_ = "blurb blurb_expanded")
					if expanded:
						scraped += (expanded.get_text()+ " ").encode('utf8')
					else:
						scraped += (review.get_text()+ " ").encode('utf8')
			return scraped
	
	# given a search term, returns a dictionary mapping title to search result
	# test this
	def get_search_results(self, search_term):
	
		search_term = '%20'.join(search_term.split())
		search_url = 'http://www.metacritic.com/search/all/%s/results' % search_term
		print search_url
		page = self.demand_page(search_url)
		soup = BeautifulSoup(page, "html.parser")
		results = soup.findAll(class_="product_title basic_stat")
		result_map = {}
		for result in results:
			link = result.find('a')
			suffix = link['href']
			name = link.get_text()
			type = suffix.split('/')[1]
			full_name = '%s (%s)' % (name, type)
			if full_name in result_map:
				fullest_name = '%s [%s]' % (full_name, suffix)
				result_map[fullest_name] = suffix
			else:
				result_map[full_name] = suffix
		return result_map
		
			
	def scrape_metacritic(self):

		search_term = raw_input('Enter search term:\n').split()
		search_term = '%20'.join(search_term)

		search_url = 'http://www.metacritic.com/search/all/%s/results' % search_term
		page = self.demand_page(search_url)
		soup = BeautifulSoup(page, "html.parser")
		results = soup.findAll(class_="result")
		print len(results)
	
		result_map = {}
	
		for result in results:
			link = result.find('a')
			suffix = link['href']
			name = link.get_text()
			type = suffix.split('/')[1]
			name_and_type = '%s (%s)' % (name, type)
			result_map[name_and_type] = suffix
		
		link_suffix = self.get_suffix(result_map, 'choose result:\n')
		
		movie_url = 'http://www.metacritic.com%s' % link_suffix
		print movie_url

		juries = {'critics': '/critic-reviews', 'users': '/user-reviews'}
		verdicts = {'positive': '?dist=positive', 'negative': '?dist=negative', 'medium': '?dist=neutral'}

		verdict_list = list(verdicts.keys())
		for i in range(len(verdict_list)):
			print "%s %s" % (i + 1,verdict_list[i])
		choice = raw_input('choose verdict:\n')
		verdict = verdict_list[int(choice) - 1]
		verdict_suffix = verdicts[verdict]
	
		jury_suffix = self.get_suffix(juries, 'choose jury:\n')
	
		reviews_url = movie_url + jury_suffix + verdict_suffix

		num_pages = 2
		urls = []
	
		destination = raw_input('Choose save name:\n')
		outfilename = "texts/%s.txt" % destination
		outfile = open(outfilename, 'w')
	
		for i in range(num_pages):
			url = '%s&page=%s' % (reviews_url, i)
			print url
			page = self.demand_page(url)
			soup = BeautifulSoup(page, "html.parser")
			foo = soup.findAll(class_="review_body")
			for x in foo:
				scraped_text = (x.get_text()+ " ").encode('utf8')
				outfile.write(scraped_text)

	def demand_page(self, url):
		hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
					   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
					   'Accept-Encoding': 'none',
					   'Accept-Language': 'pl-PL,pl;q=0.8',
					   'Connection': 'keep-alive'}

		req = urllib2.Request(url, headers=hdr)

		try:
			page = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print e.fp.read()
	
		return page

	# given a dictionary mapping names to url suffixes, asks user to choose a name, returns chosen suffix
	def get_suffix(self, map, prompt):
		menu = list(map.keys())
		for i in range(len(menu)):
			print "%s %s" % (i + 1,menu[i])
		choice = raw_input(prompt)
		name = menu[int(choice) - 1]
		suffix = map[name]
		return suffix

#s = MetacriticScraper()
#s.scrape_review_set('http://www.metacritic.com/movie/the-iron-giant/user-reviews?dist=positive', 2)

#s = Scraper()
#s.scrape_metacritic()