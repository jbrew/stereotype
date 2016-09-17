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
		self.font = tkFont.Font(family="Helvetica", size=12)
		Button(self, text='Load',  command=self.onLoad).pack()
		self.text_frame = ScrolledText(self)
		self.textbox = self.text_frame.text
		self.paths = ['texts/bowie', 'texts/cosmos_sagan']
		#self.paths = []
		self.channels = self.channels_from_paths(self.paths)
		self.select_channel(0)
		self.textbox.bind('<BackSpace>', self.onDelWord)
		self.textbox.bind('<Return>', self.onReturn)
		self.textbox.bind('<Left>', self.onArrowLeft)
		self.textbox.bind('<Right>', self.onArrowRight)
		self.textbox.bind('<Tab>', self.onTab)
		self.textbox.bind('<Shift-Tab>', self.onShiftTab)
		#self.textbox.bind('c', self.printChannels)

	# selects channel n
	def select_channel(self, n):
		self.active_number = n
		self.refresh_keyboards()
		
	def removeChannel(self, channel_num):
		del self.channels[channel_num]
		if self.active_number == channel_num:
			self.select_channel(0)	

	def channels_from_paths(self, paths, channels = []):
		for path in paths:
			name = path.split('/')[1:]	
			if not self.name_in_channels(name, channels):
				source_text = file(path).read()
				corpus = Corpus(source_text, name)
				channels.append(Channel(self, self.textbox, corpus, len(channels)))
		return channels

	def printChannels(self, event):
		for channel_num in range(len(self.channels)):
			print channel_num, self.channels[channel_num].channel_name
		print "active:", self.active_number

	# returns true if one of the channels in a list of channels has the given name
	def name_in_channels(self, name, channel_list):
		found = False
		for channel in channel_list:
			if channel.channel_name == name:
				found = True
		return found

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

	def get_next(self):
		next = self.textbox.get(INSERT, 'insert lineend').split()
		if len(next)>=2:
			return next[0:2]
		else:
			return next
			
	def onGetNext(self):
		print self.get_next()


Editor().mainloop()