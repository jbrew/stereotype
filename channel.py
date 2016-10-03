# a channel contains a corpus and associated settings

from Tkinter import *
import tkFont
from tkSimpleDialog import askstring
from tkFileDialog   import asksaveasfilename
import corpus
import operator

class Channel(Frame):
	def __init__(self, parent, textframe, corpus, num=0):
		Frame.__init__(self, parent)
		self.channel_name = corpus.name
		self.channel_num = num
		self.mode = 'shift'
		self.num_options = 20
		self.settings = {'color': 'black'}
		self.parent = parent
		self.textframe = textframe
		self.corpora = [corpus]
		self.font = parent.font
		self.pack(side = LEFT)
		self.keyboard = Frame()
		self.refresh_keyboard()

	# first member of ith tuple is the label. second member is the keystroke to input i
	def optionmap(self):
		if self.mode == 'alpha':
			return [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), 
				('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('0', '0'),
				('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd'), ('e', 'e'), 
				('f', 'f'), ('g', 'g'), ('h', 'h'), ('i', 'i'), ('j', 'j')]
		elif self.mode == 'shift':
			return [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), 
				('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('0', '0'),
				('1*', '!'), ('2*', '@'), ('3*', '#'), ('4*', '$'), ('5*', '%'), 
				('6*', '^'), ('7*', '&'), ('8*', '*'), ('9*', '('), ('0*', ')')]
		
		
	def make_keyboard(self, parent, wordlist):
		keyboard = Frame(parent, padx = 10)
		header = Frame(keyboard)
		self.title = Label(header, text = self.channel_name, fg = self.settings['color'])
		self.title.pack(side = LEFT)
		Button(header, text = 'X', command = self.onDel).pack(side = RIGHT)
		self.wt_scale = Scale(header, from_=-100, to=100, orient=HORIZONTAL)
		#self.wt_scale.pack()
		header.pack()
		mainkeys = Frame(keyboard)
		for i in range(len(wordlist)):
			optkey = Frame(mainkeys)
			num = (i + 1) % 10
			keylabel = '%s.' % self.optionmap()[i][0]
			keystroke = self.optionmap()[i][1]
			Label(optkey, text = keylabel, width = 4, anchor = W, font = self.font).pack(side = LEFT)
			option = wordlist[i]
			label = option
			b = Button(optkey, text=label, font = self.font, width = 14, anchor = W, borderwidth = 0, 
			command= lambda word=option: self.onAddWord(word), pady = 0)
			b.pack(side = LEFT)
			self.textframe.bind(keystroke, lambda event, arg=option: self.onAddWord(arg))
			optkey.pack(side = TOP)
		mainkeys.pack()		
		return keyboard
	
	def getWeight(self):
		return self.wt_scale.get()
	
	def onDel(self):
		self.master.removeChannel(self.channel_num)
		self.destroy()
	
	def onAddWord(self, word):
		t = self.textframe
		t.insert(INSERT, " "+str(word))
		t.see(END)
		self.refresh_keyboard()
		#self.master.refresh_keyboards()
		return 'break'
	
	def refresh_keyboard(self):
		self.options = self.get_options()
		self.keyboard.destroy()
		self.keyboard = self.make_keyboard(self, self.options)
		self.keyboard.pack(anchor = W)
		
	# given two dictionaries, returns a dictionary with their values added
	def combine_dicts(self, a, b, op=operator.add):
		return dict(a.items() + b.items() + [(k, op(a[k], b[k])) for k in set(b) & set(a)])
	
	# given a list of dictionaries, returns a dictionary with their values added
	def combine_dlist(self, dlist):
		if len(dlist) == 0:
			return "Can't combine empty list of dictionaries!"
		elif len(dlist) == 1:
			return dlist[0]
		else:
			return self.combine_dlist(self.combine_dicts(dlist[0],dlist[1] + dlist[2:]))
			
	def get_options(self):
		previous_words = self.parent.get_previous()
		next_words = self.parent.get_next()
		
		
		for c in self.corpora:
			suggestions = c.suggest(previous_words, next_words)[0:self.num_options]
		#aggregate = self.combine_dlist
				
		only_words = []
		for word, score in suggestions:
			only_words.append(word)
		return only_words


