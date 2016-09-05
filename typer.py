from Tkinter import *
import tkFont
from tkSimpleDialog import askstring
from tkFileDialog   import asksaveasfilename
from corpus import Corpus
from ngram import Ngram

class ScrolledText(Frame):
    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.makewidgets()
        self.settext(text, file)
        
    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN, takefocus = True, wrap = WORD)
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
		path = 'texts/howl'
		self.source_text = file(path).read()
		self.corpus = Corpus(self.source_text)
		self.options = self.get_options()
		#self.options = ['yes', 'no', 'marinara']
		self.keyboard = self.make_keyboard(self, self.options)
		self.keyboard.pack(anchor = W)
	
	def get_options(self):
		previous_words = self.get_previous()
		print "prev:",previous_words
		next_words = self.get_next()
		print "next:",next_words
		suggestions = self.corpus.suggest(previous_words, next_words, 9)
		only_words = []
		for word, score in suggestions:
			only_words.append(word)
		print only_words
		return only_words
	
	def make_keyboard(self, parent, wordlist):
		keyboard = Frame(parent)
		current_row = Frame(keyboard)
		for i in range(len(wordlist)):
			optkey = Frame(current_row)
			Label(optkey, text = str(i+1), width = 8, anchor = W, font = self.font).pack(side = LEFT)
			option = wordlist[i]
			num = i + 1
			label = option
			b = Button(optkey, text=label, font = self.font, width = 14, anchor = W, borderwidth = 0, 
			command= lambda word=option: self.onAddWord(word))
			b.pack(side = LEFT)
			self.text_frame.text.bind(str(num), lambda event, arg=option: self.onAddWord(arg))
			optkey.pack(side = TOP)
		current_row.pack()		
		return keyboard
	
	def refresh_keyboard(self):
		self.options = self.get_options()
		self.keyboard.destroy()
		self.keyboard = self.make_keyboard(self, self.options)
		self.keyboard.pack(anchor = W)
	
	def onAddWord(self, word):
		t = self.text_frame.text
		t.insert(INSERT, " "+str(word))
		self.refresh_keyboard()
		return 'break'
	
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
		self.refresh_keyboard()
	
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