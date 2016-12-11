from Tkinter import *
import tkFont

from corpus import Corpus
from ngram import Ngram


class Editor(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.configure()
		
	def self.configure():
		### SETTINGS FOR THIS WINDOW ###
		fontfamily = "Helvetica"
		fontsize = 14
		
		### EXECUTE THESE SETTINGS ###
		self.font = tkFont.Font(family=fontfamily, fontsize)
	

Editor().mainloop()