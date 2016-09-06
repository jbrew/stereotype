from Tkinter import *
import tkFont
from tkSimpleDialog import askstring
from tkFileDialog   import asksaveasfilename
from corpus import Corpus
from ngram import Ngram
from channel import Channel

class ScrolledText(Frame):
    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.makewidgets()
        self.settext(text, file)
        
    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN, takefocus = True, wrap = WORD, height = 10)
        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        self.text = text
    def settext(self, text='', file=None):
        if file:
            text = open(file, 'r').read()
        self.text.delete('1.0', END)
        self.text.insert('1.0', text)
        self.text.mark_set(INSERT, '1.0')
        self.text.focus()
    def gettext(self):
        return self.text.get('1.0', END+'-1c')

class Editor(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack(expand=YES, fill=BOTH)
		self.font = tkFont.Font(family="Helvetica", size=12)
		self.text_frame = ScrolledText(self)
		self.text = self.text_frame.text
		self.text.bind('<BackSpace>', self.onDelWord)
		self.text.bind('<Return>', self.onReturn)
		self.text.bind('<Left>', self.onArrowLeft)
		self.text.bind('<Right>', self.onArrowRight)
		self.text.bind('<Tab>', self.onTabCycle)
		path = 'texts/howl'
		paths = ['texts/howl', 'texts/batman']
		self.channels = {}
		for path in paths:
			source_text = file(path).read()
			name = path.split('/')[-1]
			corpus = Corpus(source_text, name)
			self.channels[name] = Channel(self, self.text, corpus)
			self.active_channel = name
#		self.source_text = file(path).read()
#		self.corpus = Corpus(self.source_text, 'howl')
#		self.channels = [Channel(self, self.text, self.corpus)]

	def refresh_keyboards(self):
		for key in self.channels:
			channel = self.channels[key]
			channel.refresh_keyboard()
		self.channels[self.active_channel].refresh_keyboard()
	
	# goes to the next channel on tab press
	def onTabCycle(self, event):
		cur_index = self.channels.keys().index(self.active_channel)
		print cur_index
		next_index = (cur_index + 1) % len(self.channels.keys())
		print next_index
		self.active_channel = self.channels.keys()[next_index]
		print "active: ",self.active_channel
		self.channels[self.active_channel].refresh_keyboard()
		return 'break'
	
	def onReturn(self, event):
		self.refresh_keyboards()
		return 'break'
	
	def onArrowLeft(self, event):
		t = self.text_frame.text
		prev_wordbreak = t.search(' ', INSERT, stopindex='1.0', backwards=True)
		if prev_wordbreak:
			self.text.mark_set(INSERT, '%s+1c' % prev_wordbreak)
		else:
			self.text.mark_set(INSERT, '1.0')
		
	def onArrowRight(self, event):
		t = self.text_frame.text
		next_wordbreak = t.search(' ', '%s+1c' %INSERT, stopindex='end')
		if next_wordbreak:
			self.text.mark_set(INSERT, '%s-1c' % next_wordbreak)
		else:
			self.text.mark_set(INSERT, END)
	
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
		previous = self.text.get('insert linestart', INSERT).split()
		if len(previous)>=2:
			return previous[-2:]
		else:
			return ['[$]'] + previous		# sentence start marker
	
	def onGetPrev(self):
		print self.get_previous()

	def get_next(self):
		next = self.text.get(INSERT, 'insert lineend').split()
		if len(next)>=2:
			return next[0:2]
		else:
			return next
			
	def onGetNext(self):
		print self.get_next()
		
		
class LoadWindow(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
    


Editor().mainloop()