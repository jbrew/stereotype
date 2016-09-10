from Tkinter import *
import os
from os.path import isfile, isdir, join
from channel import Channel

class LoadWindow(Frame):
	def __init__(self, parent=None, mainwindow=None):
		Frame.__init__(self, parent)
		self.mainwindow = mainwindow
		self.path = 'texts'
		self.path_list = []
		self.full_list = os.listdir(self.path)
		self.pane_width = 500
		self.selected = {}
		self.directory_pane = self.make_directory_pane()
		self.sel_pane = self.make_selection_pane()
		self.pack()
	
	def make_selection_pane(self):
		sel_pane = Frame(self, borderwidth=1, width = self.pane_width, relief=SOLID)
		Label(sel_pane, text = "selected paths").pack()
		sel_pane.pack(side = RIGHT)
		for path in self.selected:
			Label(sel_pane, text = path).pack()
		Button(sel_pane, text = "Load", command = self.addSelectedChannels).pack()
		return sel_pane
		
	def make_directory_pane(self):
		dir_pane = Frame(self, borderwidth=1, width = self.pane_width, relief=SOLID)
		self.file_list = self.make_file_list(dir_pane)
		self.dir_list = self.make_dir_list(dir_pane)
		
		dir_pane.pack(side = LEFT)
		return dir_pane
	
	def make_file_list(self, parent):
		f_window = Frame(parent, borderwidth=1, relief=SOLID)
		Label(f_window, text = "files in /%s" % self.path).pack()
				
		onlyfiles = [f for f in self.full_list if isfile(join(self.path, f))]
		
		for f in onlyfiles:
			full_path = self.path + '/' + f
			b = Button(f_window, text = f, bd = 1, relief = SUNKEN, command = lambda selpath = full_path: self.selectFile(selpath))
			b.pack(side = TOP, anchor = W)
		f_window.pack(pady = 5, padx = 10)
		return f_window
	
	def make_dir_list(self, parent):
		d_window = Frame(parent, borderwidth=2, relief=SOLID)
		onlydirs = [d for d in self.full_list if isdir(join(self.path, d))]
		
		Label(d_window, text = "directories in /%s" % self.path).pack()
		
		for d in onlydirs:
			full_path = self.path + '/' + d
			b = Button(d_window, text = d, command = lambda newpath = full_path: self.changePath(newpath))
			b.pack(side = TOP, anchor = W)
		Button(d_window, text = "back", command = self.upOneLevel).pack()
		d_window.pack(pady = 5, padx = 10)
		return d_window
	
	def selectFile(self, selpath):
		if not selpath in self.selected:
			self.selected[selpath] = 1
		else:
			del self.selected[selpath]
		self.refresh()
		return
		
	def upOneLevel(self):
		self.path = '/'.join(self.path.split('/')[:-1])
		self.refresh()
	
	def refresh(self):
		print "current path:", self.path
		self.full_list = os.listdir(self.path)
		self.directory_pane.destroy()
		self.directory_pane = self.make_directory_pane()
		self.sel_pane.destroy()
		self.sel_pane = self.make_selection_pane()
		
	def addSelectedChannels(self):
		for key in self.selected:
			self.path_list.append(key)
		self.mainwindow.channels = self.mainwindow.channels_from_paths(self.path_list, self.mainwindow.channels)
		self.mainwindow.refresh_keyboards()
		self.master.destroy()
		
	def changePath(self, newpath):
		self.path = newpath
		self.refresh()