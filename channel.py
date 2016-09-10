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
		self.settings = {'color': 'black'}
		self.parent = parent
		self.textframe = textframe
		self.corpora = [corpus]
		self.font = parent.font
		self.pack(side = LEFT)
		self.keyboard = Frame()
		self.refresh_keyboard()

	
	def make_keyboard(self, parent, wordlist):
		keyboard = Frame(parent, padx = 10)
		header = Frame(keyboard)
		self.title = Label(header, text = self.channel_name, fg = self.settings['color'])
		self.title.pack()
		Button(header, text = 'X', command = self.onDel).pack(side = RIGHT)
		self.wt_scale = Scale(header, from_=-100, to=100, orient=HORIZONTAL)
		self.wt_scale.pack()
		header.pack()
		current_row = Frame(keyboard)
		for i in range(len(wordlist)):
			optkey = Frame(current_row)
			num = (i + 1) % 10
			Label(optkey, text = str(num), width = 8, anchor = W, font = self.font).pack(side = LEFT)
			option = wordlist[i]
			num = (i + 1) % 10
			label = option
			b = Button(optkey, text=label, font = self.font, width = 14, anchor = W, borderwidth = 0, 
			command= lambda word=option: self.parent.onAddWord(word))
			b.pack(side = LEFT)
			self.textframe.bind(str(num), lambda event, arg=option: self.onAddWord(arg))
			optkey.pack(side = TOP)
		current_row.pack()		
		return keyboard
	
	def getWeight(self):
		return self.wt_scale.get()
	
	def onDel(self):
		del self.master.channels[self.channel_name]
		self.master.cycle()
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
			suggestions = c.suggest(previous_words, next_words)[0:10]
		#aggregate = self.combine_dlist
				
		only_words = []
		for word, score in suggestions:
			only_words.append(word)
		return only_words


