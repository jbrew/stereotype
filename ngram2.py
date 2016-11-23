__author__ = 'jamiebrew'

# information about a unique string within a corpus
class Ngram2(object):

    def __init__(self, string, count=1, after_distance=0, before_distance=0):
        self.string = string
        self.count = count
        self.after = [{} for _ in range(after_distance)]
        self.before = [{} for _ in range(before_distance)]
        self.rhymes = {}

    def add(self, ngram, reach, count):
		if reach > 0:
			target_dict = self.after[abs(reach)-1]
		elif reach < 0:
			print 'adding "%s" after "%s" with reach %s' % (ngram, self.string, reach)
			target_dict = self.before[abs(reach)-1]
		
		if ngram in target_dict:
			target_dict[ngram] += count
		else:
			target_dict[ngram] = count
        
    def __str__(self):
        return self.string+"\ncount: "+str(self.count)+"\nfreq: "+str(self.frequency)+"\nsig: "+str(self.sig_score)+'\n'

    def __repr__(self):
        return self.string

    def __len__(self):
        return len(self.string)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
