# a channel contains a corpus and associated settings

from Tkinter import *
import tkFont
from tkSimpleDialog import askstring
from tkFileDialog   import asksaveasfilename
import corpus
import operator

class MasterChannel(Frame):
	def __init__(self, parent, textframe, channels):
		Frame.__init__(self, parent)
		self.channels = channels
		self.channel_num = len(channels)
		self.channel_name = 'master'
		self.mode = 'shift'
		self.num_options = 20
		self.settings = {'color': 'black'}
		self.parent = parent
		self.textframe = textframe
		self.corpus = corpus
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


	def make_keyboard(self, parent): 
		wordlist = self.get_combined_options()
		keyboard = Frame(parent, padx = 10)
		header = Frame(keyboard)
		self.title = Label(header, text = self.channel_name, fg = self.settings['color'])
		self.title.pack(side = LEFT)
		Button(header, text = 'X', command = self.onDel).pack(side = RIGHT)
		#self.wt_scale = Scale(header, from_=-100, to=100, orient=HORIZONTAL)
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
		#self.refresh_keyboard()
		self.master.refresh_keyboards()
		return 'break'
	
	def refresh_keyboard(self):
		self.keyboard.destroy()
		self.keyboard = self.make_keyboard(self)
		self.keyboard.pack(anchor = W)
		
	def get_combined_options(self):
		master_dict = {}
		for c in self.channels:
			if not c.channel_name == self.channel_name:
				channel_weight = c.wt_scale.get()
				if not channel_weight == 0:
					for word, score in c.current_options:
						if word in master_dict:
							master_dict[word] += score * channel_weight
						else:
							master_dict[word] = score * channel_weight
		master_list = list(reversed(sorted(master_dict.items(), key=operator.itemgetter(1))))
		
		self.current_options = master_list[0:100]
		
		suggestions = master_list[0:self.num_options]
		only_words = []
		print "\nmaster"
		for word, score in suggestions:
			print word, score
			only_words.append(word)
		return only_words
		
		
			

