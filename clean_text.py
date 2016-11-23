import re


def clean_text(text):
	return re.sub('[0-9]|\[|\]','', text)
	
def clean_file(path):
	text = clean_text(file(path).read())
	outfile = open(path,'w')
	outfile.write(text)


clean_file('texts/numbers')
clean_file('texts/john')