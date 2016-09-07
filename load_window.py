from Tkinter import *
import os
from os.path import isfile, isdir, join

class LoadWindow(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		texts = os.listdir('texts')
		path = 'texts'
		
		Label(self, text = "FILES").pack()
				
		onlyfiles = [f for f in texts if isfile(join('texts', f))]
		
		for t in onlyfiles:
			var = IntVar()
			c = Checkbutton(self, text = t, variable = var)
			c.pack(side = TOP, anchor = W)
			
		onlydirs = [d for d in texts if isdir(join('texts', d))]
		
		Label(self, text = "DIRECTORIES").pack()
		
		for d in onlydirs:
			b = Button(self, text = d, command = self.changePath)
			b.pack(side = TOP, anchor = W)
		
		
		self.pack()
	
	def changePath(self):
		return