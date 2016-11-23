from corpus2 import Corpus2

dtt = file('tests/texts/dontthinktwice').read()
c = Corpus2('dontthink',dtt)

print 'tree length', len(c.tree)
print c.suggest(['use'],[])

print c.tree['use'].after[0:]
print c.tree['use'].before[0:]
