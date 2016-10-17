from Tkinter import *
import tkFont
from tkSimpleDialog import askstring
from tkFileDialog   import asksaveasfilename
from corpus import Corpus
from ngram import Ngram
from channel import Channel
#from scrape_window import ScrapeWindow
from load_window import LoadWindow
from text_window import ScrolledText

class Editor(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack(expand=YES, fill=BOTH)
		self.font = tkFont.Font(family="Helvetica", size=14)
		Button(self, text='Load',  command=self.onLoad).pack()
		self.text_frame = ScrolledText(self)
		self.textbox = self.text_frame.text
		self.paths = ['texts/janis-joplin.txt','texts/jimi-hendrix.txt','texts/nirvana.txt','texts/the-doors.txt']
		self.channels = self.channels_from_paths(self.paths)
		#self.master_channel = MasterChannel(self.channels)
		#num_opt_dict = {'3': 3,'5': 5,'20':20}
		#self.num_options = 16
		#self.opt_box = self.make_num_opt_menu(self, num_opt_dict, 'Number of options')
		#self.opt_box.pack()
		self.select_channel(0)
		self.textbox.bind('<BackSpace>', self.onDelWord)
		self.textbox.bind('<Return>', self.onReturn)
		self.textbox.bind('<Left>', self.onArrowLeft)
		self.textbox.bind('<Right>', self.onArrowRight)
		self.textbox.bind('<Tab>', self.onTab)
		self.textbox.bind('<Shift-Tab>', self.onShiftTab)
		self.textbox.bind('D', self.onDebug)
		#self.textbox.bind('c', self.printChannels)

	# selects channel n
	def select_channel(self, n):
		self.active_number = n
		self.refresh_keyboards()
	
	# removes channel n
	def removeChannel(self, n):
		del self.channels[n]
		if self.active_number == n:
			self.select_channel(0)	

	# given a list of paths, and optionally a list of existing channels, adds new channels generated from those paths
	def channels_from_paths(self, paths, channels = []):
		for path in paths:
			name = path.split('/')[1:]
			if not self.name_in_channels(name, channels):
				source_text = file(path).read()
				corpus = Corpus(source_text, name)
				channels.append(Channel(self, self.textbox, corpus, len(channels)))
		return channels

	# returns true if one of the channels in a list of channels has the given name
	def name_in_channels(self, name, channel_list):
		found = False
		for channel in channel_list:
			if channel.channel_name == name:
				found = True
		return found

	def printChannels(self, event):
		for channel_num in range(len(self.channels)):
			print channel_num, self.channels[channel_num].channel_name
		print "active:", self.active_number

	def onScrape(self):
		self.sw = ScrapeWindow(Toplevel(self))

	def onLoad(self):
		self.load_window = LoadWindow(Toplevel(self), self)

	def refresh_keyboards(self):	
		for cnum in range(len(self.channels)):
			channel = self.channels[cnum]
		#	channel.bind('<Button-1>', lambda cnum = cnum: self.select_channel(cnum))
			if not cnum == self.active_number:
				channel.settings['color'] = 'black'
				channel.refresh_keyboard()
			active_channel = self.channels[self.active_number]
			active_channel.settings['color'] = 'blue'
			active_channel.refresh_keyboard()
		#for cnum in range(len(self.channels)):
		#	channel.keyboard.bind('<Button-1>', lambda cnum = cnum: self.select_channel(cnum))
	
	def get_master(self):
		keyboard = Frame(self, padx = 10)
		header = Frame(keyboard)
		Label(header, text = "master").pack()
		header.pack()
		mainkeys = Frame(keyboard)
		master_list = []
		for chnl in self.channels:
			channel_list = chnl.options
			for word in channel_list:
				break
		for i in range(len(wordlist)):
			optkey = Frame(mainkeys)
			num = (i + 1) % 10
			keylabel = '%s.' % Channel.optionmap()[i][0]
			keystroke = Channel.optionmap()[i][1]
			Label(optkey, text = keylabel, width = 4, anchor = W, font = self.font).pack(side = LEFT)
			option = wordlist[i]
			label = option
			b = Button(optkey, text=label, font = self.font, width = 14, anchor = W, borderwidth = 0, 
			command= lambda word=option: self.onAddWord(word), pady = 0)
			b.pack(side = LEFT)
			self.textframe.bind(keystroke, lambda event, arg=option: self.onAddWord(arg))
			optkey.pack(side = TOP)
		mainkeys.pack()
		
		
	# goes to the next channel on tab press
	def onTab(self, event):
		self.cycle(1)
		return 'break'
		
	def onShiftTab(self, event):
		self.cycle(-1)
		return 'break'
		
	def cycle(self, n):
		self.active_number = (self.active_number + n) % len(self.channels)
		self.select_channel(self.active_number)
		
	def onReturn(self, event):
		self.refresh_keyboards()
		return 'break'
	
	def onArrowLeft(self, event):
		t = self.text_frame.text
		prev_wordbreak = t.search(' ', INSERT, stopindex='1.0', backwards=True)
		if prev_wordbreak:
			self.textbox.mark_set(INSERT, '%s+1c' % prev_wordbreak)
		else:
			self.textbox.mark_set(INSERT, '1.0')
		self.refresh_keyboards()
		
	def onArrowRight(self, event):
		t = self.text_frame.text
		next_wordbreak = t.search(' ', '%s+1c' %INSERT, stopindex='end')
		if next_wordbreak:
			self.textbox.mark_set(INSERT, '%s-1c' % next_wordbreak) #TODO: fix this so that it grabs the right characters
		else:
			self.textbox.mark_set(INSERT, END)
		self.refresh_keyboards()
	
	def onDelWord(self, event):
		t = self.text_frame.text
		prev_wordbreak = t.search(' ', '%s-1c' % INSERT, stopindex='1.0', backwards=True)
		next_wordbreak = t.search(' ', '%s-1c' % INSERT, stopindex='end')
		if prev_wordbreak:
			start = prev_wordbreak
		else:
			start = '1.0'
		if next_wordbreak:
			end = next_wordbreak
		else:
			end = END
		t.delete('%s+1c' % start, end)
		self.refresh_keyboards()
	
	def get_previous(self):
		previous = self.textbox.get('insert linestart', INSERT).split()
		if len(previous)>=2:
			return previous[-2:]
		else:
			return ['[$]'] + previous		# sentence start marker
	
	def onGetPrev(self):
		print self.get_previous()
		
	def make_num_opt_menu(self, parent, dictionary, title):
		panel = Frame(parent)
		Label(panel, text = title).pack()
		ref_list = []
		var = 1
		for key in dictionary:
			b = Radiobutton(panel, text=key, variable=var, value=dictionary[key], command = self.setNumOptions)
			ref_list.append(b)
			b.pack(anchor=W)
		return panel

	def get_next(self):
		next = self.textbox.get(INSERT, 'insert lineend').split()
		if len(next)>=2:
			return next[0:2]
		else:
			return next
			
	def onGetNext(self):
		print self.get_next()
	
	def setNumOptions(self):
		for c in self.channels:
			c.num_options = self.opt_box.get()
	
	def onDebug(self, event):
		for ch in self.channels:
			for corpus in ch.corpora:
				print corpus.name
				print len(corpus.memory)
		return 'break'


Editor().mainloop()