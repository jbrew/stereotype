from Tkinter import *
from tkSimpleDialog import askstring
from tkFileDialog   import asksaveasfilename
import re



from tkMessageBox import askokcancel

class Quitter(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        widget = Button(self, text='Quit', command=self.quit)
        widget.pack(expand=YES, fill=BOTH, side=LEFT)
    def quit(self):
        ans = askokcancel('Verify exit', "Really quit?")
        if ans: Frame.quit(self)

class VoiceBoard(Frame):
	def __init__(self, voice_list, parent=None):
		Frame.__init__(self, parent)
		self.pack()
		
		for voicename in voice_list:
			v = IntVar()
			b = Checkbutton(self, text=voicename, variable=v)
			b.pack()
			s = Scale(self, from_=0, to=100, resolution=1, orient=HORIZONTAL)
			s.pack()
			
class ScrolledText(Frame):
    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.makewidgets()
        self.settext(text, file)
        return self
    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
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


class SimpleEditor(ScrolledText):
    def __init__(self, parent=None, file=None):
    	self.options = []
    	
    	self.voice_list = ['batman','bowie','beyonce']
    	
        frm = Frame(parent)
        self.root = frm
        frm.pack(fill=X)
        Button(frm, text='Save',  command=self.onSave).pack(side=LEFT)
        Button(frm, text='Cut',   command=self.onCut).pack(side=LEFT)
        Button(frm, text='Paste', command=self.onPaste).pack(side=LEFT)
        Button(frm, text='Del word',  command=self.onDelWord).pack(side=LEFT)
        Button(frm, text='Get prev',  command=self.onGetPrev).pack(side=LEFT)
        Button(frm, text='Get next',  command=self.onGetNext).pack(side=LEFT)
        Quitter(frm).pack(side=LEFT)
        self.text_field = ScrolledText.__init__(self, parent, file=file)

    	wordlist = ['North','South','East','West']
        self.make_wordlist(parent, wordlist).pack()
        
        vb = VoiceBoard(self.voice_list)
        

        
        self.text.config(font=('courier', 10, 'normal'))
    
    def make_wordlist(self, parent, wordlist):
    	frm = Frame(parent)
    	
    	
    	for i in range(len(wordlist)):
    		option = wordlist[i]
    		num = i + 1
    		label = '%s. %s' % (num, option)
        	Button(frm, text=label,  command= lambda word=option: self.onAddWord(word)).pack(side=LEFT)
        	
        	def addWord(event):
        		self.onAddWord(option)
        	self.root.bind("<Return>", addWord)
        	
        return frm
    
    def set_options(self, options):
    	self.options = options
      
    def onSave(self):
        filename = asksaveasfilename()
        if filename:
            alltext = self.gettext()
            open(filename, 'w').write(alltext)
    def onCut(self):
        text = self.text.get(SEL_FIRST, SEL_LAST)
        self.text.delete(SEL_FIRST, SEL_LAST)
        self.clipboard_clear()
        self.clipboard_append(text)
    def onPaste(self):
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.text.insert(INSERT, text)
        except TclError:
            pass
    
    def onAddWord(self, word):
    	self.text.insert(INSERT, " "+word)
    
    def onDelWord(self):
        prev_wordbreak = self.text.search(' ', '%s-1c' % INSERT, stopindex='1.0', backwards=True)
    	next_wordbreak = self.text.search(' ', '%s-1c' % INSERT, stopindex='end')
    	if prev_wordbreak:
    	    start = prev_wordbreak
    	else:
    		start = '1.0'
    	if next_wordbreak:
    		end = next_wordbreak
    	else:
    		end = END
    	self.text.delete(start, end)
    
    
    def get_previous(self):
    	previous = self.text.get('insert linestart', INSERT).split()
    	if len(previous)>=2:
    		return previous[-2:]
    	else:
	    	return previous
    
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
    

	
    	
if __name__ == '__main__':
    try:
        SimpleEditor(file=sys.argv[1]).mainloop()
    except IndexError:
        SimpleEditor().mainloop()