from bs4 import BeautifulSoup
import urllib2
import re
import random

url = "http://bobdylan.com/songs/?may=filters&order=desc"
base = "http://www.lyricsfreak.com/"


def demand_page(url):
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
		print #e.fp.read()

	return page


page = demand_page(url)
	
soup = BeautifulSoup(page, "html.parser")

# finds all elements with the 'a' tag (i.e. all the links)
foo = soup.findAll(href=re.compile('/songs/'))

print len(foo)

outfilename = "texts/%s.txt" % 'dylan'
outfile = open(outfilename, 'w')

for link in foo[7:150]:
	#print link['href']
	url = link['href']
	print url
	try:
		page = demand_page(url)
	except:
		print "failed to get", url
	soup = BeautifulSoup(page, "html.parser")
	subfoo = soup.findAll(class_ = "article-content lyrics")
	print len(subfoo)
	#print subfoo[0].get_text()
	try:
		outfile.write("".join(subfoo[0].get_text().encode('utf8').split('Copyright')[0:-1])+ " ") # cuts off text after the word Copyright
	except:
		print "failed"